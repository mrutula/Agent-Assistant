from tools import get_calculator, get_daily_astrology
from openai import OpenAI
import load_env_variables as s
import json
from utils import is_valid_match
from loguru import logger

answer = ''
failure_reason = ''   # tracker for failure
tools = {
    "get_calculator": get_calculator,
    "get_daily_astrology": get_daily_astrology
}
# define openai client 
client = OpenAI(api_key=s.openai_api_key)

user_input = input("Please enter your query: ")

input_list = [
    {"role": "user",  "content": user_input}
]
# keep track of the tool calls 
tool_calls = []

max_iterations = 5
i = 0

while i <= max_iterations:
    i+=1
    logger.info(f"Iteration number: {i}")
    # make an initial request to the LLM 
    response = client.responses.create(
        model='gpt-4.1-mini',
        instructions=s.react_prompt,
        input=input_list
    )
    try:
        output_dict = json.loads(response.output_text)
    except json.JSONDecodeError as e:
        failure_reason = f"Invalid JSON generated : {e}"
        logger.error(f"Invalid JSON syntax: {e}")
        input_list.append({
            "role": "user",
            "content": json.dumps({
                "type": "error",
                "status": "invalid json"
                "message":"Your last output was invalid JSON. Regenerate ONLY valid JSON"
            })
        })
        continue

    logger.info(f"Thought: {output_dict.get('thought', '')}")
    # if its a tool call
    if "action" in output_dict:
        func_name = output_dict.get("action", {}).get("name", '')
        func_arg = output_dict.get("action", {}).get("input", [])
        func_reason = output_dict.get("action", {}).get("reason", '')

        input_list.append({
            "role": "assistant",
            "content": json.dumps({
                "type": "action",
                "tool": func_name,
                "input": func_arg,
                "reason": func_reason
            })
        })

        logger.info(f"Action: Use the function: {func_name}.Reason: {func_reason}, using these arguments {func_arg}")

        # if tool exists in our list 
        if func_name in tools:
            # check if arguments are of type dictionary
            if not isinstance(func_arg, dict):
                failure_reason = f"Arguments provided in format {type(func_arg).__name__} for function {func_name}"
                logger.error("Function arguments aren't stored in a dictionary")
                input_list.append({
                "role": "user",
                "content": json.dumps({
                    "type": "observation",
                    "tool": func_name,
                    "output": 'Provide function arguments in a dictionary'
                })
                })
                continue
            tool_function = tools.get(func_name)
            # check if all the required arguments for the fuction are provided 
            if not is_valid_match(tool_function, func_arg):
                failure_reason = f"LLM didnt provide the correct number of arguments needed for {func_name}"
                input_list.append({
                    "role": "user",
                    "content": json.dumps({
                        "type": "observation",
                        "tool": func_name,
                        "output": "Provide the correct number of arguments for the function"
                    })
                })
                continue

            observation = tool_function(**func_arg) 
            input_list.append({
                "role": "user",
                "content": json.dumps({
                    "type": "observation",
                    "tool": func_name,
                    "output": observation
                })
            })
            logger.info(f"observation: {observation}")
        else:
            failure_reason = "Invalid function name provided by LLM"
            logger.error("Invalid function name")
            input_list.append({
                    "role": "user",
                    "content": json.dumps({
                        'type': 'error',
                        'status': 'invalid function name',
                        'message':f"Invalid function name. Please choose a tool from the provided list. If no tool can be chosen and you don't know the answer please reply 'Dont know the answer' " 
                        })
            })

    elif "answer" in output_dict:
        input_list.append({
            "role": "assistant",
            "content": json.dumps({
                "type": "success",
                "status": "answer",
                "output": response.output_text
                })
        })
        answer =  output_dict.get("answer")  
        logger.info(f"Answer to the question is : {answer}")
        break

if not answer:
    if i >= max_iterations and not failure_reason:
        failure_reason = f"Agent exceeded the maximum allowance of iterations: {max_iterations} before it could arrive at an answer"
    logger.error(f"Execution failed. Reason: {failure_reason}")






