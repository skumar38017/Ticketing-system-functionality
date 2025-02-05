#  This file is part of the RabbitMQ server
# app/RabbitMQ/plugins-entrypoint.sh

#!/bin/bash
# Enable RabbitMQ plugins
rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_web_stomp rabbitmq_federation

# Apply configuration (this will load users, permissions, etc., from definitions.json)
rabbitmqctl stop_app
rabbitmqctl reset
rabbitmqctl start_app

# Start RabbitMQ server
exec rabbitmq-server "$@"
