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
                shotDict, athleteDict = await self.shot_event(message)
                if not len(athleteDict) == 0:
                    await Publish.publish_range_events(athleteDict)
                await Publish.publish_range_events(shotDict)
                
            else:
                logging.warning(f"Could not process event type - message: {str(message).rstrip()}")
        else:
            logging.error("Message in 'message_parser' is empty - aborting!")
            raise Exception(f"ABORTING! Message in 'message_parser' is empty - connection to shooting range is lost!")

    async def shot_event(self,message):
        eventData = json.loads(message)

        eventDict = dict()
        eventDict['shootingRangeID'] = str(settings.SHOOTING_RANGE_ID)
        eventDict['shootingRangeType'] = str(settings.RANGE_TYPE).upper()
        eventDict['scoreEventType'] = str("SHOT")
        eventDict['firingPointID'] = str(eventData['params']['lane'])

        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.MLRANGE_HTTP_URI}/get?method=fp&params=[\"{eventDict['firingPointID']}\"]&id=1") as response:
                responseData = await response.json()

        if response.status == 200:

            # Remove this log entry after testing phase
            logging.info("Send a response to TV server")

            # Count ShotArray from TV Server in order to subtract the numeric value 1 in order to get correct shot
            numberOfShots = len(responseData['result'][0]['shots'])

            # Remove this log entry after testing phase
            logging.info(f"Logging TV response: {responseData}")
            
            eventDict['startNumber'] = responseData['result'][0]['startNr']

            if responseData['result'][0]['seriesType'] == "sight":
                eventDict['series_type'] = str("SIGHTERS")
            elif responseData['result'][0]['seriesType'] == "match":
                eventDict['series_type'] = str("MATCH")
            elif responseData['result'][0]['seriesType'] == "shootoff":
                eventDict['series_type'] = str("SHOOTOFF")

            eventDict['shotValue'] = responseData['result'][0]['shots'][numberOfShots-1]['v']
            eventDict['shotValueDecimal'] = responseData['result'][0]['shots'][numberOfShots-1]['vd']
            eventDict['shotID'] = int(responseData['result'][0]['shots'][numberOfShots-1]['nr'])
            eventDict['xCoord'] = float(responseData['result'][0]['shots'][numberOfShots-1]['x'])
            eventDict['yCoord'] = float(responseData['result'][0]['shots'][numberOfShots-1]['y'])

            # Create Dict for shooter information
            shooterDict = dict()
            if not len(str(responseData['result'][0]['name']).strip()) == 0:
                shooterDict['shootingRangeID'] = str(settings.SHOOTING_RANGE_ID)
                shooterDict['shootingRangeType'] = str(settings.RANGE_TYPE).upper()
                shooterDict['scoreEventType'] = str("ATHLETE")
                shooterDict['firingPointID'] = str(eventData['params']['lane'])
                shooterDict['startNumber'] = responseData['result'][0]['startNr']
                shooterDict['name'] = responseData['result'][0]['name']
                shooterDict['team'] = responseData['result'][0]['club']
                shooterDict['group'] = responseData['result'][0]['class']
                logging.info(f"Processed ATHLETE (ATHLETE) event: {shooterDict}")

        logging.info(f"Processed SHOT (SHOT) event: {eventDict}")
        return eventDict, shooterDict
