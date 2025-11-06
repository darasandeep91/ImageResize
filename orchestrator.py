import asyncio

from consumer import consume_images_for_processing
from downloader import download_images
from urlProducer import producer_urls


async def orchestrator():
    total_number_of_images_to_process = 10
    time_out_for_stage = 15
    queue_in = asyncio.Queue(maxsize=5)
    queue_out = asyncio.Queue(maxsize=5)


    url_producer_task = producer_urls(total_number_of_images_to_process, queue_in)
    producer_task = download_images(queue_in, queue_out, time_out_for_stage)
    consumer_task = consume_images_for_processing(queue_out, time_out_for_stage)
    await asyncio.gather(url_producer_task, producer_task, consumer_task)

    # res = await asyncio.create_task(producer_urls(total_number_of_images_to_process, queue_in))
    # print(res)


if __name__ == "__main__":
    asyncio.run(orchestrator())
