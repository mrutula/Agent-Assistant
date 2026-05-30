import inspect
from loguru import logger

def is_valid_match(func_name: callable, data_dict: dict) -> bool:
    """
    Checks if all the required parameters of the function are present in the data dictionary.

    Parameters:
    - func_name: The function to check against.
    - data_dict: A dictionary containing the parameters to check.
    Returns:
    - True if all required parameters are present, False otherwise.
    """
    try:
        logger.info("Checking if all required arguments are provided")
        # Extracts the signature from the function automatically
        params = inspect.signature(func_name).parameters

        # Required keys for function
        required_keys = {name for name, p in params.items() if p.default is inspect.Parameter.empty}

        # all keys 
        all_keys = params.keys()

        # provided keys
        provided_keys = set(data_dict.keys())

        # validation
        # missing required keys?
        missing = required_keys - provided_keys

        # any additional keys?
        extra = provided_keys - all_keys
        
        if extra:
            logger.error("Additional arguments provided") 
            return False
        
        if missing:
            logger.error("Missing required arguments")
            return False

        logger.info("Valid: All required arguments provided")
        return True
    except Exception as e:
        logger.error(f"Error checking the validity of the arguments: {e}")
        return False