from ..messaging import publisher
import aiohttp
import json
import logging
import settings

class MegalinkMessageParser:

    async def message_parser(self,message):
        if message:
            message_data = json.loads(message)
            scoreEventType = message_data['params']['type']
            Publish = publisher.Publisher(settings.RABBITMQ_URI)
            if scoreEventType == "SHOT":
                result = await self.shot_event(message)
                await Publish.publish_range_events(result)
            else:
                logging.warning(f"Could not process event type - message: {str(message).rstrip()}")
        else:
            logging.error("Message in 'message_parser' is empty - aborting!")
            raise Exception(f"ABORTING! Message in 'message_parser' is empty - connection to shooting range is lost!")

    async def shot_event(self,message):
        eventData = json.loads(message)

        eventDict = dict()
        eventDict['shootingRangeID'] = str(settings.SHOOTING_RANGE_ID)
        eventDict['scoreEventType'] = str("SHOT")
        eventDict['firingPointID'] = int(eventData['params']['lane'])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.MLRANGE_HTTP_URI}/get?method=fp&params=[\"{eventDict['firingPointID']}\"]&id=1") as response:
                responseData = await response.json()

        if response.status == 200:

            # Remove this log entry after testing phase
            logging.info("Send a response to TV server")

            numberOfShots = len(responseData['result'][0]['shots'])
            shot = responseData['result'][0]['shots'][numberOfShots-1]

            # Remove this log entry after testing phase
            logging.info(f"Logging TV response: {responseData}")
            logging.info(f"Logging parsed TV response: {shot}")

            eventDict['shotValue'] = responseData['result'][0]['shots'][numberOfShots-1]['v']
            eventDict['shotValueDecimal'] = responseData['result'][0]['shots'][numberOfShots-1]['vd']
            eventDict['shotID'] = int(responseData['result'][0]['shots'][numberOfShots-1]['nr'])
            eventDict['xCoord'] = float(responseData['result'][0]['shots'][numberOfShots-1]['x'])
            eventDict['yCoord'] = float(responseData['result'][0]['shots'][numberOfShots-1]['y'])


        logging.info(f"Processed SHOT (SHOT) event: {eventDict}")
        return eventDict        


    