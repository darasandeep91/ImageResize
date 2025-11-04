import asyncio

from Job import Job
from consumer import consumer
from producer import submit_job
from ResizeEnum import Resize
from enum import Enum
import random


async def orchestrator():
    queue = asyncio.Queue()
    jobs = create_mock_jobs(10)

    producer_task = submit_job(jobs, queue)
    consumer_task = asyncio.create_task(consumer(queue))
    await asyncio.gather(producer_task, consumer_task)


def create_mock_jobs(num_jobs):
    jobs = []
    possible_resizes = list(Resize)
    base_url = "https://place.dog/300/200"
    base_file_name = "Dog"

    for i in range(1, num_jobs + 1):
        file_name = f"{base_file_name}{i}.jpeg"
        resize_choice = random.choice(possible_resizes)
        job = Job(
            imageURL=base_url,
            fileName=file_name,
            resize=resize_choice
        )
        jobs.append(job)

    return jobs


if __name__ == "__main__":
    asyncio.run(orchestrator())
