# app/utils/generate_otp.py
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_otp(length: int = 6) -> str:
    logger.info('Generating OTP')
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    logger.info(f'Generated OTP: {otp}')
    print(f'Generated OTP: {otp}')
    return otp