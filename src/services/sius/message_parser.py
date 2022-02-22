class SiusMessageParser:
    
    def __init__(self):
        pass
        
    async def message_parser(self,data):
        eventType = data.split(";")[0]
        if eventType == "_GRPH":
            print(f"Recieved GROUP")
        elif eventType == "_NAME":
            print(f"Recieved NAME")
            await self.name_event(data)
        elif eventType == "_PRCH":
            print(f"Recieved PRACTICE")
        elif eventType == "_SHOT":
            print(f"Recieved SHOT")
            await self.shot_event(data)
        elif eventType == "_SNAT":
            print(f"Recieved NATION")
            await self.nation_event(data)
        elif eventType == "_TEAM":
            print(f"Recieved TEAM")
            await self.team_event(data)


    async def group_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 15:
            print(f"GROUP Parser")

    async def name_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 6:
            lane = eventData[1]
            fireingpoint = eventData[2]
            shooterID = eventData[3]
            shooterName = eventData[5]
            print(f"NAME is {shooterName} with ID {shooterID} and standing on lane {lane} or fireingpoint {fireingpoint}")
    
    async def practice_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 26:
            lane = eventData[1]
            fireingpoint = eventData[2]
            shooterID = eventData[3]
            shooterName = eventData[5]
            print(f"NAME is {shooterName} with ID {shooterID} and standing on lane {lane} or fireingpoint {fireingpoint}")

    async def shot_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 24:
            shotValue = eventData[10]
            shotDecimalDigitValue = eventData[11][-1]
            shotDecimalValue = str(shotValue) + "," + str(shotDecimalDigitValue)
            print(f"SHOT is a: {shotValue} - more exactly a: {shotDecimalValue}")

    async def nation_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 6:
            lane = eventData[1]
            fireingpoint = eventData[2]
            shooterID = eventData[3]
            shooterNation = eventData[5]
            print(f"NATION is {shooterNation} on shooter with ID {shooterID} and standing on lane {lane} or fireingpoint {fireingpoint}")

    async def team_event(self,data):
        eventData = data.split(";")
        if len(eventData) == 6:
            lane = eventData[1]
            fireingpoint = eventData[2]
            shooterID = eventData[3]
            shooterTeam = eventData[5]
            print(f"TEAM is {shooterTeam} on shooter with ID {shooterID} and standing on lane {lane} or fireingpoint {fireingpoint}")
    