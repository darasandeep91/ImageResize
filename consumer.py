import asyncio
import os.path

from PIL import Image

from Job import Job
import io


async def consumer(queue: asyncio.Queue):
    while True:
        print("......................waiting for job......................")
        if not queue.empty():
            job = await queue.get()
            print(f"......................processing job {job.fileName}......................")
            await asyncio.to_thread(process_image, job)
        else:
            print("no job found sleeping for 2 seconds")
            await asyncio.sleep(1)


def process_image(job: Job):
    img_buffer = io.BytesIO(job.downloadedImage)
    img_object = Image.open(img_buffer)
    convert_img = img_object.convert("RGB")
    resized_img = convert_img.resize(job.resize.value)
    current_dir = os.getcwd()
    filename = os.path.join(current_dir, "ResizedImages", job.fileName)
    print(f"saving image to {filename}")
    resized_img.save(filename, "JPEG")
