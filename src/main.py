import asyncio
from asyncore import loop
import signal
import settings
import services.megalink.message_parser
import services.sius.message_parser
from util import *
import websockets

async def sius_client_reader(reader):
    if settings.RANGE_TYPE == "sius":
        
        SiusMessageParser = services.sius.message_parser.SiusMessageParser()

        while(True):
            data = await reader.readline()
            await SiusMessageParser.message_parser(data.decode(encoding="iso-8859-1"))

async def sius_client_writer(writer):
    if settings.RANGE_TYPE == "sius":
        
        while(True):
            await asyncio.sleep (240)
            writer.write("keepalive".encode())
            logging.info("Sending keepalive")
            await writer.drain()

async def mlrange_websocket():
    if settings.RANGE_TYPE == "megalink":

        MegalinkMessageParser = services.megalink.message_parser.MegalinkMessageParser()

        async with websockets.connect(settings.MLRANGE_URI) as websocket:
            async for data in websocket:
                await MegalinkMessageParser.message_parser(data)
            
async def main():
    if check_shooting_range_id(settings.SHOOTING_RANGE_ID) == True:
        logging.info(f"SHOOTING_RANGE_ID is valid - value: \"{settings.SHOOTING_RANGE_ID}\"")

        logging.info(f"RANGE_TYPE is: \"{str(settings.RANGE_TYPE).upper()}\"")

        if settings.RANGE_TYPE == "sius":
            logging.info("Connecting to SIUS shooting range")

            connection = await asyncio.streams.open_connection(
                settings.SIUSDATA_HOST,
                settings.SIUSDATA_PORT
            )
            
            reader, writer = connection

            logging.info("Creating stream reader task")
            task_stream_reader = asyncio.create_task(
                sius_client_reader(reader)
            )

            logging.info("Creating stream writer task")
            task_stream_writer = asyncio.create_task(
                sius_client_writer(writer)
            )

            logging.info("Executing stream reader task")
            await task_stream_reader

            logging.info("Executing stream writer task")
            await task_stream_writer
        
        elif settings.RANGE_TYPE == "megalink":
            logging.info("Connecting to MEGALINK shooting range")
            
            
            logging.info("Creating websocket task")
            task_mlrange_websocket = asyncio.create_task(
                mlrange_websocket()
            )
            
            logging.info("Executing websocket task")
            await task_mlrange_websocket

        else:
            logging.error(f"RANGE_TYPE is NOT supported - value: \"{settings.RANGE_TYPE}\"")

    else:
        logging.error(f"SHOOTING_RANGE_ID is NOT valid - value: \"{settings.SHOOTING_RANGE_ID}\"")

asyncio.run(main())
