from typing import Generator, Tuple, List
from google.cloud import storage
import constants
from PIL import Image
from PIL.Image import Image as PIL_Image
from typing import Optional
from io import BytesIO
import types
import streamlit as st
import os
import re

classification_map = {
    "Surf Quality": "surf_quality_data",
    "Gating": "gating_data"}


@st.cache(hash_funcs={types.GeneratorType: id})
def get_frames(
    spot_prefix: str, day_date_range: Tuple[int, int], month_date_range: Tuple[int, int], time_range: Tuple[int, int] 
    )-> Generator:
    """
    Return a genorator of all frames in bucket. Filter based on day, month and time.
    """
    storage_client = storage.Client()

    img_blobs = list(storage_client.list_blobs(constants.FRAME_DATA_BUCKET, prefix=spot_prefix))
    for blob in img_blobs:
        str_name = blob.name.split("/")[-1]

        if not str_name.endswith(".png"):
            continue
        
        if not month_date_range[0] <= int(str_name.split("_")[1]) <= month_date_range[1]:
            continue            
        
        if not day_date_range[0] <= int(str_name.split("_")[2]) <= day_date_range[1]:    
            continue
        
        if not time_range[0] <= int(str_name.split("_")[3]) <= time_range[1]:
            continue
        
        data = blob.download_as_string()
        yield blob.name, Image.open(BytesIO(data))
    

def get_spot_names()->List[str]:
    storage_client = storage.Client()
    img_blobs = list(storage_client.list_blobs(constants.FRAME_DATA_BUCKET))
    return list(set([blob.name.split("/")[0] for blob in img_blobs if blob.name.endswith(".png")]))
    


def new_frame(
    frames: Generator, 
    img_location: st.empty, 
    classification_type_prefix: str, 
    storage_client: storage.Client,
    )-> Tuple[str, PIL_Image]:
    """
    Iterates over frames genorator and returns the frame and name. They are saved in session.
    """
    
    labeled_img_blobs_names = [
        blob.name.split("/")[-1] 
        for index, blob in enumerate(list(storage_client.list_blobs(constants.LABELED_FRAME_DATA_BUCKET, prefix=classification_map.get(classification_type_prefix)))) 
        if blob.name.split("/")[-1].endswith(".png") 
        ]

    
    while True:
        try:
            name, frame = next(frames)
            if name.split("/")[-1] in labeled_img_blobs_names:
                continue
            else:
                break
        except StopIteration:
            st.write("No Frames")
            st.stop()
            break
        
    img_location.image(frame, caption=name, width=1000)
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



