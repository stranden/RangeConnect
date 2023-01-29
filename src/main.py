import asyncio
from asyncore import loop
import settings
import services.sius.message_parser
from util import *

async def tcp_client_reader(reader):
    if settings.RANGE_TYPE == "sius":
        
        SiusMessageParser = services.sius.message_parser.SiusMessageParser()

        while(True):
            data = await reader.readline()
            await SiusMessageParser.message_parser(data.decode(encoding="iso-8859-1"))

async def tcp_client_writer(writer):
    if settings.RANGE_TYPE == "sius":
        
        while(True):
            await asyncio.sleep (240)
            writer.write("keepalive".encode())
            logging.info("Sending keepalive")
            await writer.drain()
            
async def main():
    if check_shooting_range_id(settings.SHOOTING_RANGE_ID) == True:
        logging.info(f"SHOOTING_RANGE_ID is valid - value: \"{settings.SHOOTING_RANGE_ID}\"")

        logging.info(f"RANGE_TYPE is: \"{str(settings.RANGE_TYPE).upper()}\"")
        if settings.RANGE_TYPE == "sius":
            logging.info("Connecting to shooting range")

            connection = await asyncio.streams.open_connection(
                settings.SIUSDATA_HOST,
                settings.SIUSDATA_PORT
            )
            
            reader, writer = connection

            logging.info("Creating stream reader task")
            task_stream_reader = asyncio.create_task(
                tcp_client_reader(reader)
            )

            logging.info("Creating stream writer task")
            task_stream_writer = asyncio.create_task(
                tcp_client_writer(writer)
            )

            logging.info("Executing stream reader task")
            await task_stream_reader

            logging.info("Executing stream writer task")
            await task_stream_writer

        else:
            logging.error(f"RANGE_TYPE is NOT supported - value: \"{settings.RANGE_TYPE}\"")

    else:
        logging.error(f"SHOOTING_RANGE_ID is NOT valid - value: \"{settings.SHOOTING_RANGE_ID}\"")

asyncio.run(main())
