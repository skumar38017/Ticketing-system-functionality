# app/workers/celery_app.py
import socket
from celery import Celery
from app.config import config
from celery.signals import worker_ready
from celery.result import AsyncResult
import logging
from app.tasks.otp_task import send_otp_task

# Get the hostname of the machine to create a unique worker name
hostname = socket.gethostname()
unique_worker_name = f"worker_{hostname}"

# Initialize the Celery application
celery_app = Celery(
    "ticket_management_system",
    broker=config.rabbitmq_url,
    backend=config.rabbitmq_result_backend,
)

# Update Celery's configuration for detailed output
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="utc",  # Use UTC for timestamps
    enable_utc=True,  # Enable UTC for timestamps
    broker_connection_retry_on_startup=True,
    worker_hostname=unique_worker_name,  # Use the unique worker name
    task_queues={
        "otp_queue": {
            "exchange": "otp_exchange",
            "routing_key": "otp_task",
        },
        "payment_queue": {
            "exchange": "payment_exchange",
            "routing_key": "payment_task",
        },
        "email_queue": {
            "exchange": "email_exchange",
            "routing_key": "email_task",
        },
        "qr_queue": {
            "exchange": "qr_exchange",
            "routing_key": "qr_task",
        },
    },
    task_default_queue="default",
    task_default_exchange="default",
    task_default_routing_key="default",
    task_routes={
        "app.tasks.otp_task.send_otp_task": {"queue": "otp_queue"},
        "app.tasks.payment_task.*": {"queue": "payment_queue"},
        "app.tasks.qr_task.*": {"queue": "qr_queue"},
        "app.tasks.email_task.*": {"queue": "email_queue"},
    },
    worker_log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    worker_task_log_format="%(asctime)s - %(task_name)s - %(levelname)s - %(message)s",
)

# Set the logging level to DEBUG to capture detailed logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("celery")

# Autodiscover tasks in the project
celery_app.autodiscover_tasks(["app.tasks"], force=True)

@worker_ready.connect
def on_worker_ready(sender, **kwargs):
    """
    Signal handler for when a worker is ready.
    """
    logger.info(f"Worker {sender.hostname} is ready.")

# Example function to trigger a task and fetch the task_id automatically
def trigger_task_and_get_id(phone_no, name, otp):
    """
    Trigger the task to send OTP and return the task ID.
    
    :param phone_no: Phone number to send OTP
    :param name: Name of the user
    :param otp: Generated OTP
    :return: AsyncResult object
    """
    # Trigger the task (example task)
    task_result = celery_app.send_task('app.tasks.otp_task.send_otp_task', args=[phone_no, name, otp])

    # Automatically get the task_id
    task_id = task_result.id
    logger.info(f"Triggered task with ID: {task_id}")
    
    # Now we can create an AsyncResult using the task_id
    result = AsyncResult(task_id)
    
    # Wait for the result (you can adjust timeout and other parameters)
    if result.ready():
        logger.info(f"Task {task_id} result: {result.result}")
    else:
        logger.info(f"Task {task_id} is still in progress...")

    # Return the result or task_id
    return result
