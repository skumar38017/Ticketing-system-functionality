#!/bin/bash
set -e

# Start RabbitMQ in the background
rabbitmq-server -detached

# Wait for RabbitMQ to be ready
echo "Waiting for RabbitMQ to be ready..."
while ! rabbitmqctl status; do
  sleep 5
done

# Enable necessary plugins
echo "Enabling RabbitMQ plugins..."
rabbitmq-plugins enable rabbitmq_management rabbitmq_federation rabbitmq_federation_management rabbitmq_shovel rabbitmq_shovel_management
rabbitmq-plugins enable --offline rabbitmq_web_stomp

# Load pre-defined configurations (e.g., exchanges, queues)
if [ -f /etc/rabbitmq/definitions.json ]; then
  echo "Loading RabbitMQ definitions..."
  rabbitmqctl import_definitions /etc/rabbitmq/definitions.json
fi

# Stop the RabbitMQ server started earlier
rabbitmqctl stop

# Start RabbitMQ in the foreground
exec rabbitmq-server
