import asyncio


async def monitor_queue_for_fullness(queue: asyncio.Queue):
    while queue.full():
        print("queue full sleeping for 5 seconds")
        await asyncio.sleep(5)