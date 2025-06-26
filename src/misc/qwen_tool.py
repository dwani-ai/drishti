import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import json
import re

# 1. Load model and tokenizer
model_name = "Qwen/Qwen3-8B"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
    device_map="auto",
    trust_remote_code=True
)

# 2. Define your function/tool (OpenAI-compatible format)
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

# 3. Prepare chat messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is the current time in New York?"}
]

# 4. Format input for the model
prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

# 5. Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

# 6. Generate output
with torch.no_grad():
    output_ids = model.generate(
        **inputs,
        max_new_tokens=256,
        do_sample=False,
        temperature=0.7
    )
output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

print("=== Raw Model Output ===")
print(output_text)

# 7. (Optional) Extract function call from output using regex
# Qwen3 typically outputs a JSON block for function calls
function_call_match = re.search(r"\{[\s\S]*?\}", output_text)
if function_call_match:
    try:
        function_call = json.loads(function_call_match.group(0))
        print("\n=== Function Call Detected ===")
        print(json.dumps(function_call, indent=2))
    except Exception as e:
        print("\nCould not parse function call JSON:", e)
else:
    print("\nNo function call detected in output.")

# 8. (Optional) Implement your own function execution here
# For example:
# if function_call.get("name") == "get_time":
#     tz = function_call["arguments"]["timezone"]
#     # Call your own get_time(tz) function, etc.
