from openai import OpenAI
import load_env_variables as s
import json


# step 1: Define a list of tools agent can call
tools = [
    {
        "type": "function",
        "name": "get_calculator",
        "description": "Function that performs basic arithmetic operations such as addition, subtraction, multiplication, and division." ,
        "parameters":{
            "type": "object",
            "properties": {
                "num1": {
                    "type": "integer",
                    "description": "The first number for the calculation."
                },
                "num2": {
                    "type": "integer",
                    "description": "The second number for the calculation."
                },
                "operation": {
                    "type": "string",
                    "description": "The arithmetic operation to perform. Supported operations are 'add', 'subtract', 'multiply', and 'divide'."
                }
            },
            "required": ["num1", "num2", "operation"],

        }

    }
]

# define the function that the agent can call
def get_calculator(num1: int, num2: int, operation: str) -> str:
    """
    A calculator tool that can perform basic arithmetic operations.

    Parameters:
    - num1: The first number for the calculation.
    - num2: The second number for the calculation.
    - operation: The arithmetic operation to perform. Supported operations are 'add', 'subtract', 'multiply', and 'divide'.

    Returns:
    - A string describing the result of the calculation or an error message if the operation is unsupported or if there is a division by zero.
    """
    if operation == "add":
        return f"The result of adding {num1} and {num2} is {num1 + num2}."
    elif operation == "subtract":
        return f"The result of subtracting {num2} from {num1} is {num1 - num2}."
    elif operation == "multiply":
        return f"The result of multiplying {num1} and {num2} is {num1 * num2}."
    elif operation == "divide":
        if num2 != 0:
            return f"The result of dividing {num1} by {num2} is {num1 / num2}."
        else:
            return "Error: Division by zero is not allowed."
    else:
        return "Error: Unsupported operation. Please use 'add', 'subtract', 'multiply', or 'divide'."

# Create a running input list we will add to over time
input_list = [
    {"role": "user",  "content": "What is 5 multiplied by 3?"}
    ]

client = OpenAI(api_key=s.openai_api_key)

# Make a request to the model with the tools it could call
response = client.responses.create(
        model="gpt-4.1-mini",
        tools=tools,
        input=input_list
)

# Receive a tool call from the model. 
# Save function call outputs for subsequent requests
input_list += response.output

# execute code on application side with input from the tool call 
for item in response.output:
    if item.type == 'function_call':
        if item.name == 'get_calculator':
            # load the arguments for the function call
            arguments = json.loads(item.arguments)
            # call the function and get the result
            result = get_calculator(arguments.get('num1'), arguments.get('num2'), arguments.get('operation'))

            #provide function call result back to the model
            input_list.append({
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": result
            })

print(f"Final Output: {input_list}")

# Make a second request to the model with tool output
final_response = client.responses.create(
        model="gpt-4.1-mini",
        instructions="Based on the function call output, provide the final answer to the user's question.",
        tools=tools,
        input=input_list
)

# 5. The model should be able to give a response!
print(f"Final Response: {final_response.output_text}")

