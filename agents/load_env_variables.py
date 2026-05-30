from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


with open("data/react_agent.txt", "r") as f:
    react_prompt = f.read()