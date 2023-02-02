import json
import aio_pika

class Publisher:

    def __init__(self, amqp_connection_uri: str) -> None:
        self.amqp_connection_uri = amqp_connection_uri

    async def publish_range_events(self, message: dict) -> None:
        connection = await aio_pika.connect(self.amqp_connection_uri)
        queue_name = "shooting_range_events"
        routing_key = queue_name
        async with connection:
            # Creating a channel
            channel = await connection.channel()

            # Declaring queue
            await channel.declare_queue(
                queue_name,
                durable=True
            )

            message_body = json.dumps(message).encode()

            message = aio_pika.Message(
                message_body,
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            )

            # Sending the message
            await channel.default_exchange.publish(
                message,
                routing_key=routing_key
            )
            #print(f"{message}")