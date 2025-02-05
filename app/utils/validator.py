#  app/utils/validator.py

# Validator for phone number
import re

def validate_phone(phone_no: str) -> str:
    """
    Normalize the phone number to the format {country_code} <phone_no>.
    - Supports various input formats like `7463061637`, `917463061637`, or `+91-74630 61636`.
    - Extracts or defaults the country code to `91`.
    - Removes spaces, dashes, and formats the phone number properly.

    Args:
        phone_no (str): The input phone number.

    Returns:
        str: The normalized phone number in the format {country_code} <phone_no>.
    """
    # Remove all non-digit characters except "+"
    cleaned_phone = re.sub(r"[^\d+]", "", phone_no)

    # Handle phone numbers with "+" (international format)
    if cleaned_phone.startswith("+"):
        # Extract country code and local phone number
        cleaned_phone = cleaned_phone[1:]  # Remove "+"
        country_code = cleaned_phone[:2]  # Assume 2-digit country code
        local_number = cleaned_phone[2:]
    elif len(cleaned_phone) > 10:  # Likely includes a country code but no "+"
        country_code = cleaned_phone[:2]  # Assume first 2 digits are the country code
        local_number = cleaned_phone[2:]
    else:  # Assume no country code, default to "91" (India)
        country_code = "91"
        local_number = cleaned_phone

    # Ensure the local number is exactly 10 digits
    if len(local_number) != 10:
        raise ValueError("Local phone number must be exactly 10 digits.")

    return f"+{country_code}-{local_number}"