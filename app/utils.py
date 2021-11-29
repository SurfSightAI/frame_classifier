from typing import Generator
from google.cloud import storage
import constants
from PIL import Image
from typing import Optional
from io import BytesIO

def get_frames(client: storage.Client, prefix: Optional[str]=None)-> Generator:
    """
    Args:
        client (storage.Client): Google cloud storage client.
        prefix (Optional[str], optional): An optional file path. Used to only get frames from specific spot.

    Yields:
        Generator: All frames in bucket and prefix
    """
    img_blobs = list(client.list_blobs(constants.FRAME_DATA_BUCKET, prefix=prefix))
    for index, blob in enumerate(img_blobs):
        if index == 0: 
            continue
        data = blob.download_as_string()
        yield Image.open(BytesIO(data))
    
def next_frame(frames: Generator):
    return next(frames)
