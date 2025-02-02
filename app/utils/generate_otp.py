# app/utils/generate_otp.py
import random
import logging

logger = logging.getLogger(__name__)

def generate_otp(length: int = 6) -> str:
    """
    Generate a random OTP of the specified length.
    """
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    logger.info(f"Generated OTP: {otp}")
    return otp