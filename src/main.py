import asyncio
import settings
import services.sius.message_parser

async def tcp_client():
    reader, writer = await asyncio.streams.open_connection(
        settings.SIUSDATA_HOST, settings.SIUSDATA_PORT)
    
    while(True):
        data = await reader.readline()

        SiusMessageParser = services.sius.message_parser.SiusMessageParser()
        #Publish = services.messaging.publisher.Publisher(settings.RABBITMQ_URI, settings.RANGE_TYPE)

        await SiusMessageParser.message_parser(data.decode(encoding="iso-8859-1"))
        #await Publish.publish_range_events(message)

async def main():
    task_sius = asyncio.create_task(
        tcp_client()
    )
    
    await task_sius

asyncio.run(main())
