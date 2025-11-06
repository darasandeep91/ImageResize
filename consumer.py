import asyncio
import io
import os.path

from PIL import Image

from Job import Job


async def consume_images_for_processing(queue: asyncio.Queue, time_out_for_stage: float):
    while True:
        try:
            job = await asyncio.wait_for(queue.get(), timeout=time_out_for_stage)
        except asyncio.TimeoutError:
            print(f"Timeout reached {time_out_for_stage} secs, no messages received. Shutting down consumer.")
            break

        print(f"Processing job {job.fileName}")
        await asyncio.to_thread(process_image, job)
        queue.task_done()


def process_image(job: Job):
    img_buffer = io.BytesIO(job.downloadedImage)
    img_object = Image.open(img_buffer)
    convert_img = img_object.convert("RGB")
    resized_img = convert_img.resize(job.resize.value)
    current_dir = os.getcwd()
    filename = os.path.join(current_dir, "ResizedImages", job.fileName)
    print(f"saving image to {filename}")
    resized_img.save(filename, "JPEG")
