#  Neon-Stdio-Holi-T25/Dockerfile

# Use a Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CELERY_RESULT_BACKEND=rpc://
ENV CELERY_BROKER_URL=amqp://guest:guest@rabbitmq:5672//

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt \
    # Remove pip cache to save space
    && rm -rf ~/.cache/pip

# Copy the application code into the container
COPY . /app/

# Expose necessary ports (default for your app is 8001)
EXPOSE 8001

# Clean up any unnecessary temporary files
RUN find / -name '*.pyc' -delete \
    && find / -name '__pycache__' -delete

# Default command for the container (Celery worker)
CMD ["celery", "-A", "app.workers.celery_app", "worker", "--loglevel=info"]