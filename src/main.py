import asyncio
import settings
import services.sius.message_parser
import util

from aiologger import Logger

async def tcp_client():
    await logger.info("Connecting to shooting range")
    reader, writer = await asyncio.streams.open_connection(
        settings.SIUSDATA_HOST, settings.SIUSDATA_PORT)
    
    while(True):
        data = await reader.readline()

        SiusMessageParser = services.sius.message_parser.SiusMessageParser()
        await SiusMessageParser.message_parser(data.decode(encoding="iso-8859-1"))
        
        #Publish = services.messaging.publisher.Publisher(settings.RABBITMQ_URI, settings.RANGE_TYPE)
        #await Publish.publish_range_events(message)

async def main():
    await logger.info("Checking if environment variable 'SHOOTING_RANGE_ID' is valid")
    if util.check_shooting_range_id(settings.SHOOTING_RANGE_ID) == True:
        await logger.info(f"SHOOTING_RANGE_ID is valid - Value: \"{settings.SHOOTING_RANGE_ID}\"")
        await logger.info("Creating Streaming task")

        task_sius = asyncio.create_task(
            tcp_client()
        )

        await logger.info("Executing Streaming task")
        await task_sius
    else:
        await logger.debug(f"SHOOTING_RANGE_ID is NOT valid - Value: \"{settings.SHOOTING_RANGE_ID}\"")
logger = Logger.with_default_handlers(name='RangeConnect')
asyncio.run(main())
