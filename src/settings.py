import os

# SIUS Data
SIUSDATA_HOST = os.getenv("SIUSDATA_HOST", default="localhost")
SIUSDATA_PORT = os.getenv("SIUSDATA_PORT", default=4000)

# RabbitMQ
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", default="guest")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", default="guest")