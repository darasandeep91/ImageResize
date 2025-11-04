from dataclasses import dataclass

from ResizeEnum import Resize


@dataclass
class Job:
    imageURL: str
    fileName: str
    resize: Resize
    downloadedImage: bytes = None
