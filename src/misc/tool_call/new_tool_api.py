from openai import OpenAI
import json
import requests

# Initialize the OpenAI client for llama.cpp's server
client = OpenAI(base_url="http://localhost:9100/v1", api_key="EMPTY")

# Define the tool (function) for getting weather
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a specified location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name (e.g., Shanghai)"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

# Mock function to simulate getting weather data (replace with real API if needed)
def get_weather(location):
    # For demonstration, return mock data
    # In practice, replace with an API call, e.g., to OpenWeatherMap
    return {"temperature": 25, "condition": "Sunny", "location": location}

# Main function to handle the chat interaction
def chat_with_qwen3():
    # Initial user message
    messages = [
        {"role": "user", "content": "What's the weather in Shanghai?"}
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
                if tool_call.function.name == "get_weather":
                    # Parse the arguments
                    args = json.loads(tool_call.function.arguments)
                    location = args.get("location")

                    # Execute the function
                    weather_data = get_weather(location)
                    print(f"Tool call executed: get_weather({location}) -> {weather_data}")

                    # Append the tool response to messages
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(weather_data),
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