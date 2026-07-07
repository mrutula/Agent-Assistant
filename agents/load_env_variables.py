from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
data_folder = os.getenv("DATA_FOLDER")
file_name = os.getenv("FILE_NAME")

os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")


with open("data/react_agent.txt", "r") as f:
    react_prompt = f.read()
