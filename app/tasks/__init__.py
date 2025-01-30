#  app/tasks/__init__.py

from app.tasks.otp_task import send_otp_task
from app.tasks.test_task import test_send_otp_task

__all__ = ["send_otp_task", "test_send_otp_task"]