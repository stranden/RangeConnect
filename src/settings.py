import os

# SIUS Data
SIUSDATA_HOST = os.getenv("SIUSDATA_HOST", default="localhost")
SIUSDATA_PORT = os.getenv("SIUSDATA_PORT", default=4000)

# RabbitMQ
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER", default="guest")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS", default="guest")

# Shooting Range ID
# EBA2ED57-BF56-47DE-91F8-DEA032843FE3 is our test range
SHOOTING_RANGE_ID = os.getenv("SHOOTING_RANGE_ID", default="EBA2ED57-BF56-47DE-91F8-DEA032843FE3")