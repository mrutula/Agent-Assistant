
import agents.load_env_variables as s
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from loguru import logger

def embedding_and_vector_store(chunks: list) -> None:
    """
    Function to generate embeddings for a list of text chunks and store them in a vector database.

    parameters:
        chunks (list): A list of text chunks to be embedded.
    returns:
        None
    """
    # Re run the embeddings if chunk size has been changed/or if the index has not been created yet.
    # 1. Initialize the Embedding Model
    # This uses the standard 'text-embedding-3-small' model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=s.openai_api_key)
    # 2. Create the Vector Database (FAISS)
    # This step automatically generates embeddings and builds the index
    vector_db = FAISS.from_texts(chunks, embeddings)

    # 7. Optional: Save the index to use it later without re-embedding
    vector_db.save_local(Path(s.data_folder)/ "vector" / "my_faiss_index")

    logger.info("Embeddings generated and stored in FAISS vector database successfully.")

    # To load it back later:
    # new_db = FAISS.load_local("my_faiss_index", embeddings, allow_dangerous_deserialization=True)


