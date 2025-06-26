from openai import OpenAI
import json
from datetime import datetime
import pytz

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

# Function to get the current time for a given timezone using pytz
def get_current_time(timezone):
    try:
        tz = pytz.timezone(timezone)
        current_time = datetime.now(tz)
        formatted_time = current_time.strftime("%I:%M:%S %p %Z, %A, %B %d, %Y")
        return {"timezone": timezone, "current_time": formatted_time}
    except pytz.exceptions.UnknownTimeZoneError:
        return {"error": f"Invalid timezone: {timezone}"}
    except Exception as e:
        return {"error": f"Failed to fetch time for {timezone}: {str(e)}"}

# Main function to handle the chat interaction
def chat_with_qwen3():
    messages = [
        {"role": "user", "content": "What's the current time in Berlin?"}
    ]

    try:
        response = client.chat.completions.create(
            model="Qwen3-32B",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.6,
            max_tokens=32768
        )

        response_message = response.choices[0].message

        if response_message.tool_calls:
            for tool_call in response_message.tool_calls:
                if tool_call.function.name == "get_current_time":
                    args = json.loads(tool_call.function.arguments)
                    timezone = args.get("timezone", "Europe/Berlin")
                    time_data = get_current_time(timezone)
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(time_data),
                        "tool_call_id": tool_call.id
                    })
                    final_response = client.chat.completions.create(
                        model="Qwen3-32B",
                        messages=messages,
                        temperature=0.6,
                        max_tokens=32768
                    )
                    print(final_response.choices[0].message.content)
                else:
                    print(f"Unknown tool called: {tool_call.function.name}")
        else:
            print(response_message.content)

    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Run the chat
if __name__ == "__main__":
    chat_with_qwen3()