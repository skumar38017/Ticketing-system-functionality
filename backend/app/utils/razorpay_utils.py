#  app/utils/razorpay_utils.py

import razorpay
import logging
from app.config import config
from razorpay.errors import BadRequestError, GatewayError, ServerError
from app.database.models import User

# Configure logging
logger = logging.getLogger(__name__)

class RazorpayError(Exception):
    """Custom exception for Razorpay-related errors."""
    def __init__(self, message, error_data=None):
        super().__init__(message)
        self.error_data = error_data

class RazorpayClient:
    """Handles Razorpay API interactions."""

    try:
        # Initialize Razorpay client
        client = razorpay.Client(auth=(config.razorpay_key["key"], config.razorpay_key["secret"]))
        logger.info("✅ Razorpay client initialized successfully.")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Razorpay client: {e}")
        raise RazorpayError("Failed to initialize Razorpay client") from e

    @staticmethod
    def is_connected():
        """
        Checks if the Razorpay client is connected by making a test API call.
        
        :return: True if connected, False otherwise.
        """
        try:
            response = RazorpayClient.client.payment.all({"count": 1})  # Fetch 1 payment as a test
            if response and isinstance(response, dict):
                logger.info("✅ Razorpay API is reachable.")
                return True
        except BadRequestError as e:
            logger.error(f"❌ Razorpay BadRequestError: {e}")
        except GatewayError as e:
            logger.error(f"❌ Razorpay GatewayError: {e}")
        except ServerError as e:
            logger.error(f"❌ Razorpay ServerError: {e}")
        except Exception as e:
            logger.exception(f"❌ Unexpected error while checking Razorpay connection: {e}")

        return False

    @staticmethod
    def create_order(data):
        """
        Creates a Razorpay order.
        
        :param data: Dictionary containing order details
        :return: Razorpay order response or None if an error occurs
        :raises: RazorpayError in case of API failure
        """
        try:
            order = RazorpayClient.client.order.create(data)
            logger.info(f"✅ Order created successfully: {order}")
            return order
        except BadRequestError as e:
            logger.error(f"❌ Bad Request Error: {e}")
            raise RazorpayError("Invalid request sent to Razorpay", e)
        except ServerError as e:
            logger.error(f"❌ Razorpay Server Error: {e}")
            raise RazorpayError("Razorpay server encountered an error", e)
        except GatewayError as e:
            logger.error(f"❌ Gateway Error: {e}")
            raise RazorpayError("Payment gateway error", e)
        except Exception as e:
            logger.exception(f"❌ Unexpected error while creating Razorpay order: {e}")
            raise RazorpayError("Unexpected error occurred while creating order", e)


# app/utils/razorpay_utils.py

class RazorpayClient:
    """Handles Razorpay API interactions."""

    @staticmethod
    def create_order(data, user_uuid: str,  payment_method=None):
        """
        Creates a Razorpay order.
        
        :param data: Dictionary containing order details
        :param payment_method: Payment method specified by the user (optional)
        :return: Razorpay order response or None if an error occurs
        :raises: RazorpayError in case of API failure
        """
        try:
            # If a specific payment method is provided, modify the order data accordingly
            if payment_method:
                data['method'] = payment_method  # Add the payment method if it's specified

            # Creating the Razorpay order
            order = RazorpayClient.client.order.create(data)
            data['notes'] = {'user_uuid': user_uuid}  # Include the user_uuid in the notes field
            logger.info(f"✅ Order created successfully: {order}")
            return order
        except razorpay.errors.BadRequestError as e:
            logger.error(f"❌ Bad Request Error: {e}")
            raise RazorpayError("Invalid request sent to Razorpay", e)
        except razorpay.errors.ServerError as e:
            logger.error(f"❌ Razorpay Server Error: {e}")
            raise RazorpayError("Razorpay server encountered an error", e)
        except razorpay.errors.GatewayError as e:
            logger.error(f"❌ Gateway Error: {e}")
            raise RazorpayError("Payment gateway error", e)
        except Exception as e:
            logger.exception(f"❌ Unexpected error while creating Razorpay order: {e}")
            raise RazorpayError("Unexpected error occurred while creating order", e)
