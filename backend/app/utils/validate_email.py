#  app/utils/validate_email.py

import re

def validate_email(email: str) -> str:
    """
    Validates the given email address using a regular expression.
    
    Args:
        email (str): The input email address.
        
    Returns:
        str: The normalized email address, or raises ValueError if invalid.
        
    Raises:
        ValueError: If the email address is not valid.
    """
    # Define the regular expression for a valid email
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    if re.match(email_regex, email):
        return email.strip()  # Normalize the email by stripping extra spaces
    else:
        raise ValueError(f"Invalid email address: {email}")
