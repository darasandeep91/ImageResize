import asyncio
import random

import aiohttp

MAX_RETRIES_FOR_FAILED_REQUEST = 10
MAX_DOWNLOAD_TASKS = 2

async def download_images(queue_in: asyncio.Queue, queue_out: asyncio.Queue, time_out_for_stage: float):
    semaphores = asyncio.Semaphore(MAX_DOWNLOAD_TASKS)
    while True:
        async with semaphores:
            try:
                job = await asyncio.wait_for(queue_in.get(), time_out_for_stage)
            except asyncio.TimeoutError:
                print(f"Timeout reached {time_out_for_stage} secs, no messages received. Shutting down downloader.")
                break

            print(f"downloading image: {job.imageURL} related to job: {job.fileName}")
            fetch_image_job_obj = lambda: fetch_image_from_url(job.imageURL)
            downloaded_image_content = await retry_with_jitter(fetch_image_job_obj)
            job.downloadedImage = downloaded_image_content

            await queue_out.put(job)

async def fetch_image_from_url(url: str):
    timeout = aiohttp.ClientTimeout(total=2)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url) as response:
            print(response)
            if validate_response(response):
                return await response.read()
            return None


async def retry_with_jitter(coroutine_callable):
    result = None
    retry_counter = 0
    base_sleep = 1
    while retry_counter < MAX_RETRIES_FOR_FAILED_REQUEST:
        try:
            result = await coroutine_callable()
            if result is not None:
                return result

        except Exception as ex:
            if base_sleep > MAX_RETRIES_FOR_FAILED_REQUEST:
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
