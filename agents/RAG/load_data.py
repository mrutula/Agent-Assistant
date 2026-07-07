# importing required classes
from pypdf import PdfReader
from pathlib import Path
import agents.load_env_variables as s
from loguru import logger


def load_pdf_data() -> None:
    """
    Function to load PDF data from a file and return it as a string.

    parameters:
        None
    returns:
        None
    """
    try:
        pdf_path = Path(s.data_folder) / "pdf_files" / f"{s.file_name}.pdf"
        pdf_text_path = Path(s.data_folder) / "pdf_text" / f"{s.file_name}.txt"

        # create a pdf reader object
        reader = PdfReader(pdf_path)

        # initialize an empty string to store the text
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        with open(pdf_text_path, "w") as f:
            f.write(text)
    except Exception as e:
        logger.error(f"Error in load_pdf_data: {e}")
