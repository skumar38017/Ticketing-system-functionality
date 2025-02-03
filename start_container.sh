#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e
# ---------------------- Docker Cleanup ------------------------------
echo "Cleaning up Docker containers, images, and volumes..."

# Stop and remove all running containers, remove images, and prune unused resources
docker-compose --env-file .docker.env down 
docker stop $(docker ps -aq) || true  # Ignore errors if no containers are running
docker rm $(docker ps -aq) || true    # Ignore errors if no containers exist
docker rmi -f $(docker images -aq) || true  # Ignore errors if no images exist

# This step will clean up unused data but might cause issues with subsequent docker commands
docker system prune -a  # Clean up unused Docker data

# Ensure that the necessary Docker resources are available again
# Try to verify that the Docker daemon is still running before proceeding
if ! docker info > /dev/null 2>&1; then
  echo "Docker daemon isn't running. Exiting..."
  exit 1
fi

# ---------------------- Permissions ----------------------------------
echo "Setting necessary permissions..."

# Grant full access to files in the current directory (be cautious with this)
sudo chmod -R 755 ./*  # Prefer 755 instead of 777 for security reasons

# Ensure the user has Docker group permissions (requires re-login for effect)
if ! groups $USER | grep -q "\bdocker\b"; then
    echo "Adding $USER to the Docker group..."
    sudo usermod -aG docker $USER
else
    echo "$USER is already in the Docker group."
fi

# Set permissions for PostgreSQL data directory
if [ -d "/home/tagglab/Videos/Neon-Stdio-Holi-T25/postgres_data" ]; then
    sudo chmod -R 755 /home/tagglab/Videos/Neon-Stdio-Holi-T25/postgres_data
    sudo chmod -R u+rw /home/tagglab/Videos/Neon-Stdio-Holi-T25/postgres_data
else
    echo "PostgreSQL data directory not found!"
fi

# Set permissions for RabbitMQ data directory
if [ -d "/home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data" ]; then
    sudo chmod -R 755 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data
    sudo chmod +x /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data/plugins-entrypoint.sh
    sudo chown -R 1000:1000 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data
    sudo chmod 400  /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data/.erlang.cookie
    sudo chmod 777 /home/tagglab/Videos/Neon-Stdio-Holi-T25/redis_data/./*
    sudo chmod 777 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data/./*
else
    echo "RabbitMQ data directory not found!"
fi

# Set the Python path
export PYTHONPATH="$PYTHONPATH:/home/tagglab/Videos/Neon-Stdio-Holi-T25/app"

# ---------------------- Start Docker Compose -------------------------
echo "Starting Docker containers..."

# Use Docker Compose with the specified environment file
docker-compose --env-file .docker.env up -d --build


sudo chmod -R 755 /home/tagglab/Videos/Neon-Stdio-Holi-T25/postgres_data
sudo chown -R 1000:1000 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data
sudo chown -R 755 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data
sudo chmod 400  /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data/.erlang.cookie
sudo chmod 777 /home/tagglab/Videos/Neon-Stdio-Holi-T25/redis_data/./*
sudo chmod 777 /home/tagglab/Videos/Neon-Stdio-Holi-T25/rabbitmq_data/./*
export PYTHONPATH=/home/tagglab/Videos/Neon-Stdio-Holi-T25/app
export PYTHONPATH=/home/tagglab/Videos/Neon-Stdio-Holi-T25
docker restart $(docker ps -aq)   

# List all running containers
docker ps -a

echo "Containers have been started successfully."
