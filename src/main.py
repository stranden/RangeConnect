import asyncio
import settings

async def tcp_client():
    reader, writer = await asyncio.streams.open_connection(
        settings.SIUSDATA_HOST, settings.SIUSDATA_PORT)
    
    while(True):
        data = await reader.readline()
        await message_parser(data.decode(encoding="iso-8859-1"))

async def message_parser(data):
    eventType = data.split(";")[0]
    if eventType == "_SHOT":
        print(f"Recieved SHOT")
        print(f"{data}")
    elif eventType == "_GRPH":
        print(f"Recieved GROUP")
        print(f"{data}")
    elif eventType == "_NAME":
        print(f"Recieved NAME")
        print(f"{data}")
    elif eventType == "_PRCH":
        print(f"Recieved PRACTICE")
        print(f"{data}")
    elif eventType == "_SNAT":
        print(f"Recieved NATION")
        print(f"{data}")
    elif eventType == "_TEAM":
        print(f"Recieved TEAM")
        print(f"{data}")

async def main():
    task_sius = asyncio.create_task(
        tcp_client()
    )
    
    await task_sius

asyncio.run(main())
