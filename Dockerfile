# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CELERY_RESULT_BACKEND=rpc://
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . /app/

# Expose necessary ports (if required for your application)
EXPOSE 8001

# Default command (can be overridden by docker-compose)
# Command for Celery worker
CMD ["celery", "-A", "app.workers.celery_app", "worker", "--loglevel=info"]