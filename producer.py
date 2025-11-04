import asyncio
import random
from typing import List

import aiohttp

import Job

MAX_RETRIES = 10


async def submit_job(input_job_lst: List[Job], queue: asyncio.Queue):
    for job in input_job_lst:
        imageURL = job.imageURL
        print(f"downloading image: {imageURL} related to job: {job.fileName}")
        fetch_image_obj = lambda: fetch_image(imageURL)
        downloaded_image_content = await retry_with_jitter(fetch_image_obj)
        print(f"downloaded image size {len(downloaded_image_content)}")
        job.downloadedImage = downloaded_image_content
        queue.put_nowait(job)


async def fetch_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)
            if validate_response(response):
                return await response.read()
            return None


async def retry_with_jitter(coroutine_callable):
    result = None
    retry_counter = 0
    base_sleep = 1
    while retry_counter < MAX_RETRIES:
        try:
            result = await coroutine_callable()
            if result is not None:
                return result

        except Exception as ex:
            if base_sleep > MAX_RETRIES:
                print(f"retries exhausted")
                return None
            sleep_time = (base_sleep * (2 ** retry_counter)) + random.uniform(0, 1)
            print(f"received exception: {ex} sleeping for {sleep_time} seconds")
            await asyncio.sleep(sleep_time)
            retry_counter += 1
    return result


def validate_response(response: aiohttp.ClientResponse) -> bool:
    rules = {
        "status_check": lambda r: r.status == 200,
        "content_type_check": lambda r: r.content_type.startswith("image/"),
        "content_length_check": lambda r: r.content_length > 50000,
    }

    failed_rules = []
    for rule in rules.values():
        if not rule(response):
            failed_rules.append(rule)

    if failed_rules:
        raise Exception(f"failed rules: {failed_rules}")
    return True
