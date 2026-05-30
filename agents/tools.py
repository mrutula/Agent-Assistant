

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
    if operation in ("add" , '+') :
        return f"The result of adding {num1} and {num2} is {num1 + num2}."
    elif operation in ("subtract", '-'):
        return f"The result of subtracting {num2} from {num1} is {num1 - num2}."
    elif operation in ("multiply", '*'):
        return f"The result of multiplying {num1} and {num2} is {num1 * num2}."
    elif operation in ("divide", "/"):
        if num2 != 0:
            return f"The result of dividing {num1} by {num2} is {num1 / num2}."
        else:
            return "Error: Division by zero is not allowed."
    else:
        return "Error: Unsupported operation. Please use 'add', 'subtract', 'multiply', or 'divide'."

def get_daily_astrology(astrology_sign: str) -> str:
    """
    A daily astrology tool that provides a horoscope based on the user's astrology sign.

    Parameters:
    - astrology_sign: The user's astrology sign (e.g., "aries", "taurus", "gemini", etc.).
    Returns:
    - A string containing the horoscope for the given astrology sign or an error message if the sign is invalid.
    """

    astrology_dictionary ={
        "aries": "Today is a great day for new beginnings. Take initiative and embrace change.",
        "taurus": "Focus on your finances today. It's a good time to budget and plan for the future.",
        "gemini": "Communication is key today. Reach out to friends and family for support.",
        "cancer": "Take care of your emotional well-being today. Spend time doing things you love.",
        "leo": "Your confidence is high today. Use it to pursue your goals and take risks.",
        "virgo": "Pay attention to the details today. It's a good time to organize and plan.",
        "libra": "Focus on your relationships today. Spend quality time with loved ones.",
        "scorpio": "Embrace your passion today. It's a great time to work on creative projects.",
        "sagittarius": "Adventure awaits you today. Step out of your comfort zone and explore new opportunities.",
        "capricorn": "Hard work pays off today. Stay focused and determined to achieve your goals.",
        "aquarius": "Innovation is in the air today. Embrace new ideas and think outside the box.",
        "pisces": "Trust your intuition today. It's a good time to reflect and connect with your inner self."
    }

    return f"For {astrology_sign}, {astrology_dictionary.get(astrology_sign.lower(), 'Invalid astrology sign. Please provide a valid sign.')}"