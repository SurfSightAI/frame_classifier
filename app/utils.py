from typing import Generator, Tuple
from google.cloud import storage
import constants
from PIL import Image
from PIL.Image import Image as PIL_Image
from typing import Optional
from io import BytesIO
import types
import streamlit as st

@st.cache(hash_funcs={types.GeneratorType: id})
def get_frames(prefix: Optional[str]=None)-> Generator:
    storage_client = storage.Client()
    """
    Args:
        prefix (Optional[str], optional): An optional file path. Used to only get frames from specific spot.

    Yields:
        Generator: All frames in bucket, respecting prefix
    """
    img_blobs = list(storage_client.list_blobs(constants.FRAME_DATA_BUCKET, prefix=prefix))
    for index, blob in enumerate(img_blobs):
        if index == 0: 
            continue
        data = blob.download_as_string()
        yield blob.name, Image.open(BytesIO(data))
    


def new_frame(frames: Generator, img_location: st.empty)-> Tuple[str, PIL_Image]:
    """
    Return new frame and name.
    Args:
        frames (Generator)
        img_location (st.empty)

    Returns:
        Tuple[str, Image]
    """
    name, frame = next(frames)
    img_location.image(frame)
    try:
        del st.session_state["frame_name"]
        del st.session_state["frame_data"]
    except KeyError:
        pass
    st.session_state["frame_name"] = name
    st.session_state["frame_data"] = frame.tobytes()

    return name, frame

def save_frame(bucket: str, frame_path: str, img_data: bytes, storage_client: storage.Client)-> None:
        bucket = storage_client.bucket(bucket)
        blob = bucket.blob(frame_path)
        blob.upload_from_string(img_data, content_type='image/png')
