from openai import OpenAI
import json
import requests
from datetime import datetime

# Initialize the OpenAI client for llama.cpp's server
client = OpenAI(base_url="http://localhost:9100/v1", api_key="EMPTY")

# Define the tool (function) for getting the current time
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current local time for a specified timezone",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {
                        "type": "string",
                        "description": "The IANA timezone name (e.g., Europe/Berlin)"
                    }
                },
                "required": ["timezone"]
            }
        }
    }
]

# Function to get the current time for a given timezone using worldtimeapi.org
def get_current_time(timezone):
    try:
        # Query the worldtimeapi.org for the current time
        response = requests.get(f"http://worldtimeapi.org/api/timezone/{timezone}")
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        
        # Parse the datetime and format it
        current_time = datetime.fromisoformat(data["datetime"].replace("Z", "+00:00"))
        formatted_time = current_time.strftime("%I:%M:%S %p %Z, %A, %B %d, %Y")
        return {"timezone": timezone, "current_time": formatted_time}
    except requests.RequestException as e:
        return {"error": f"Failed to fetch time for {timezone}: {str(e)}"}
    except KeyError:
        return {"error": f"Invalid response from time API for {timezone}"}

# Main function to handle the chat interaction
def chat_with_qwen3():
    # Initial user message
    messages = [
        {"role": "user", "content": "What's the current time in Berlin?"}
    ]

    try:
        # First API call to get the model's response
        response = client.chat.completions.create(
            model="Qwen3-32B",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.6,
            max_tokens=32768
        )

        # Extract the response message
        response_message = response.choices[0].message
        print("Model response:", response_message)

        # Check if the model returned a tool call
        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    # Parse the arguments
                    args = json.loads(tool_call.function.arguments)
                    timezone = args.get("timezone", "Europe/Berlin")  # Default to Berlin

                    # Execute the function
                    time_data = get_current_time(timezone)
                    print(f"Tool call executed: get_current_time({timezone}) -> {time_data}")

                    # Append the tool response to messages
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(time_data),
                        "tool_call_id": tool_call.id
                    })

                    # Make a second API call to get the final response
                    final_response = client.chat.completions.create(
                        model="Qwen3-32B",
                        messages=messages,
                        temperature=0.6,
                        max_tokens=32768
                    )

                    # Print the final response
                    final_message = final_response.choices[0].message.content
                    print("Final response:", final_message)
                else:
                    print(f"Unknown tool called: {tool_call.function.name}")
        else:
            # No tool call, print the direct response
            print("Direct response:", response_message.content)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Run the chat
if __name__ == "__main__":
    print("Starting chat with Qwen3-32B...")
    chat_with_qwen3()