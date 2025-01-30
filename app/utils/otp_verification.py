import json
from app.utils.redis_data_storage import RedisDataStorage
from app.config import config

async def verify_otp(redis_key: str, otp: str) -> dict:
    """
    Verify the OTP stored in Redis.
    """
    redis_storage = RedisDataStorage()

    # Retrieve stored user data
    print('redis_key in verify_otp', redis_key)
    user_data_json = redis_storage.get_data_from_redis(redis_key)
    print('user_data_json in verify_otp', user_data_json)
    if not user_data_json:
        return None  # OTP expired or does not exist

    # Convert to dictionary
    user_data = json.loads(user_data_json)

    # Validate OTP
    if user_data.get("otp") != otp:
        return None  # Invalid OTP

    # Remove OTP before saving user
    user_data.pop("otp", None)

    # Delete Redis key after successful verification
    redis_storage.delete_data_from_redis(redis_key)

    return user_data
