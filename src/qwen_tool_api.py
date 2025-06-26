from openai import OpenAI
import json
from datetime import datetime
import pytz  # pip install pytz

# 1. OpenAI client for llama.cpp server
client = OpenAI(base_url="http://localhost:91000/v1", api_key="sk-local")

# 2. Define your function/tool
functions = [
    {
        "name": "get_time",
        "description": "Get the current time in a given timezone.",
        "parameters": {
            "type": "object",
            "properties": {
                "timezone": {
                    "type": "string",
                    "description": "Timezone, e.g., America/New_York"
                }
            },
            "required": ["timezone"]
        }
    }
]

# 3. Prepare messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the current time in New York?"}
]

# 4. Call the chat completion endpoint with function calling
response = client.chat.completions.create(
    model="Qwen3-8B-GGUF",
    messages=messages,
    functions=functions,
    function_call="auto"
)

# 5. Parse function call from response
message = response.choices[0].message
if hasattr(message, "function_call") and message.function_call:
    func = message.function_call
    func_name = func.name
    args = json.loads(func.arguments)
    print(f"Function call requested: {func_name} with args {args}")

    # 6. Calculate current time in requested timezone
    if func_name == "get_time":
        tz = args.get("timezone", "UTC")
        try:
            utc_time = datetime.now(pytz.UTC)
            local_time = utc_time.astimezone(pytz.timezone(tz))
            print(f"Current time in {tz}: {local_time}")
        except Exception as e:
            print(f"Error: {e}")
else:
    print("No function call detected. Model response:")
    print(message.content)
