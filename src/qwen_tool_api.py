from openai import OpenAI

client = OpenAI(base_url="http://localhost:91000/v1", api_key="sk-local")

# Define your function/tool
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

# Prepare messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the current time in New York?"}
]

# Call the chat completion endpoint with function calling
response = client.chat.completions.create(
    model="Qwen3-8B-GGUF",  # Use the model name (or alias) as shown in your server logs
    messages=messages,
    functions=functions,
    function_call="auto"
)

print(response)
