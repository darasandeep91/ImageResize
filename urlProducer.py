import asyncio
import time
from random import choice

from Job import Job
from ResizeEnum import Resize


async def producer_urls(number_of_images: int, queue: asyncio.Queue):
    mock_job_gen_obj = create_mock_jobs(number_of_images)
    for _ in range(number_of_images + 1):
        await queue.put(next(mock_job_gen_obj))
    print("Finished producing images")


def create_mock_jobs(number_of_images: int):
    for _ in range(number_of_images + 1):
        possible_resizes = list(Resize)
        base_url = "https://place.dog/300/200"
        base_file_name = "Dog"
        file_name = f"{base_file_name}{time.time()}.jpeg"
        resize_choice = choice(possible_resizes)
        job = Job(
            imageURL=base_url,
            fileName=file_name,
            resize=resize_choice
        )
        yield job
