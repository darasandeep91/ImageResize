import asyncio

import aiohttp

import Job
from typing import List


async def submit_job(input_job_lst: List[Job], queue: asyncio.Queue):
    for job in input_job_lst:
        imageURL = job.imageURL
        print(f"downloading image: {imageURL}")
        downloaded_image_content = await fetch_image(imageURL)
        print(f"downloaded image size {len(downloaded_image_content)}")
        job.downloadedImage = downloaded_image_content
        queue.put_nowait(job)


async def fetch_image(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(response)
            if response.status != 200 or not response.content_type.startswith("image/"):
                print(f"not a valid image: {url}")
            return await response.read()
