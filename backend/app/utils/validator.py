#  app/utils/validator.py

import re

def validate_phone(phone_no: str) -> str:
    """
    Normalize the phone number to the format +{country_code}{phone_no}.
    - Supports various input formats like `7463061637`, `917463061637`, or `+91-74630 61636`.
    - Extracts or defaults the country code to `91` if not provided.
    - Removes spaces, dashes, and formats the phone number properly.

    Args:
        phone_no (str): The input phone number.

    Returns:
        str: The normalized phone number in the format +{country_code}{phone_no}.
    """
    # Remove all non-digit characters except "+"
    cleaned_phone = re.sub(r"[^\d+]", "", phone_no)

    # Handle phone numbers with "+" (international format)
    if cleaned_phone.startswith("+"):
        # Extract country code and local phone number
        cleaned_phone = cleaned_phone[1:]  # Remove "+"
        # Country code may vary, let's extract it correctly
        country_code_length = 2  # Assume country code is 2 digits (e.g., 91 for India)
        
        # Extract the country code and local number
        country_code = cleaned_phone[:country_code_length]
        local_number = cleaned_phone[country_code_length:]
    elif len(cleaned_phone) > 10:  # Likely includes a country code but no "+"
        country_code = cleaned_phone[:2]  # Assume first 2 digits are the country code
        local_number = cleaned_phone[2:]
    else:  # Assume no country code, default to "91" (India)
        country_code = "91"
        local_number = cleaned_phone

    # Ensure the local number is exactly 10 digits
    if len(local_number) != 10:
        raise ValueError("Local phone number must be exactly 10 digits.")

    # Return phone number in the required format: +{country_code}{local_number}
    return f"+{country_code}{local_number}"
