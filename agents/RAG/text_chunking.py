from langchain_text_splitters import RecursiveCharacterTextSplitter
import agents.load_env_variables as s
from pathlib import Path
from loguru import logger


def semantic_text_chunking() -> list:
    """
    This function takes a PDF file name as input, reads the content of the PDF, and splits it into smaller chunks using the RecursiveCharacterTextSplitter from the langchain_text_splitters library.

    Parameters:
        None
    Returns:
        List: A list of text chunks extracted from the PDF.
    """
    try:
        # Load the PDF data
        with open(
            Path(s.data_folder) / "pdf_text" / f"{s.file_name}.txt", "rb"
        ) as file:
            pdf_text = file.read().decode("utf-8")

        # Create an instance of the RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            is_separator_regex=False,
        )

        # Split the text into chunks
        chunks = text_splitter.split_text(pdf_text)
        return chunks
    except Exception as e:
        logger.error(f"Error in semantic_text_chunking: {e}")
        return []
