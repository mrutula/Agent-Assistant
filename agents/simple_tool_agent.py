from openai import OpenAI
import load_env_variables as s
import json
from tools import get_calculator, get_daily_astrology


# step 1: Define a list of tools agent can call
tools = [
    {
        "type": "function",
        "name": "get_calculator",
        "description": "Function that performs basic arithmetic operations such as addition, subtraction, multiplication, and division.",
        "parameters": {
            "type": "object",
            "properties": {
                "num1": {
                    "type": "integer",
                    "description": "The first number for the calculation.",
                },
                "num2": {
                    "type": "integer",
                    "description": "The second number for the calculation.",
                },
                "operation": {
                    "type": "string",
                    "description": "The arithmetic operation to perform. Supported operations are 'add', 'subtract', 'multiply', and 'divide'.",
                },
            },
            "required": ["num1", "num2", "operation"],
        },
    },
    {
        "type": "function",
        "name": "get_daily_astrology",
        "description": "Function that provides a daily horoscope based on the user's astrology sign.",
        "parameters": {
            "type": "object",
            "properties": {
                "astrology_sign": {
                    "type": "string",
                    "description": "The user's astrology sign (e.g., 'aries', 'taurus', 'gemini', etc.).",
                }
            },
            "required": ["astrology_sign"],
        },
    },
]


user_input = input("Ask a question to the agent: ")
# Create a running input list we will add to over time
input_list = [{"role": "user", "content": user_input}]

client = OpenAI(api_key=s.openai_api_key)

# Make a request to the model with the tools it could call
response = client.responses.create(model="gpt-4.1-mini", tools=tools, input=input_list)

# Receive a tool call from the model.
# Save function call outputs for subsequent requests
input_list += response.output

# execute code on application side with input from the tool call
for item in response.output:
    if item.type == "function_call":
        if item.name == "get_calculator":
            # load the arguments for the function call
            arguments = json.loads(item.arguments)
            # call the function and get the result
            result = get_calculator(
                arguments.get("num1"), arguments.get("num2"), arguments.get("operation")
            )

            # provide function call result back to the model
            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result,
                }
            )
        elif item.name == "get_daily_astrology":
            # load the arguments for the function call
            astrology_sign = json.loads(item.arguments).get("astrology_sign")
            result = get_daily_astrology(astrology_sign)

            input_list.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": result,
                }
            )

print(f"Final Output: {input_list}")

# Make a second request to the model with tool output
final_response = client.responses.create(
    model="gpt-4.1-mini",
    instructions="Based on the function call output, provide the final answer to the user's question.",
    tools=tools,
    input=input_list,
)

# 5. The model should be able to give a response!
print(f"Final Response: {final_response.output_text}")
