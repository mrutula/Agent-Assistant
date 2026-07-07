from loguru import logger
from text_chunking import semantic_text_chunking
from embeddings import embedding_and_vector_store
from retrieval import get_grounded_llm_response
from load_data import load_pdf_data
from pathlib import Path
import agents.load_env_variables as s


def get_rag_tool(user_input: str) -> str:
    """
    Retrieve information from internal documentation using RAG

    Parameters:
        user_input (str): The user's query or input.

    Returns:
        str: The retrieved information or response based on the user's input.
    """
    try:
        # Phase 1 : Ingestion
        # Documents → Chunking → Embedding → Vector DB Storage

        load_pdf_data()
        logger.info("PDF data loaded successfully.")

        # chunking the text
        chunks = semantic_text_chunking()
        if not chunks:
            logger.error("Text chunking failed.")

        logger.info("Text chunking completed successfully.")
        # write the chunks to a file for debugging
        with open(
            Path(s.data_folder) / "chunks" / "chunks.txt", "w", encoding="utf-8"
        ) as f:
            for i, chunk in enumerate(chunks, 1):
                f.write(f"Chunk {i}:\n{chunk}\n\n")

        # Create embeddings and store in vector database
        embedding_and_vector_store(chunks)

        # Retrieval (Finding Relevant Knowledge) and LLM Response Generation
        llm_response = get_grounded_llm_response(user_input, chunks)
        return llm_response

    except Exception as e:
        logger.error(f"Error in while extracting data using RAG: {e}")
        return "Error occurred while extracting data using RAG. Please check the logs for more details."
