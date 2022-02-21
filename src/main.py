import asyncio
import settings
import time

async def tcp_client():
    reader, writer = await asyncio.streams.open_connection(
        settings.SIUSDATA_HOST, settings.SIUSDATA_PORT)
    
    while(True):
        data = await reader.readline()
        print(f'Received: {data.decode(encoding="iso-8859-1")}')
        print(f"Received at {time.strftime('%X')}")

async def count_numbers():
    number = 0
    while(True):
        print(f'Number is: {number}')
        number = number + 1
        await asyncio.sleep(5)

async def main():
    task_sius = asyncio.create_task(
        tcp_client())
    #task_count_number = asyncio.create_task(count_numbers())

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task_sius
    #await task_count_number

asyncio.run(main())
#loop.run_forever(tcp_client())