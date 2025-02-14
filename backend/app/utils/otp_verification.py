#  app/utils/otp_verification.py

import json
from app.config import config
from app.utils.redis_data_storage import RedisDataStorage

async def verify_otp(redis_key: str, otp: str) -> dict:
    """
    Verify the OTP stored in Redis.
    """
    redis_storage = RedisDataStorage()

    # Retrieve stored user data
    user_data_json = redis_storage.get_data_from_redis(redis_key)
    
    if not user_data_json:
        return None

    # Convert to dictionary
    user_data = json.loads(user_data_json)

    # Validate OTP
    if user_data.get("otp") != otp:
        return None  # Invalid OTP

    # Remove OTP before saving user
    user_data.pop("otp", None)

    return user_data