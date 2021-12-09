import datetime
from io import BytesIO
from typing import List, Optional, Tuple

import constants
import streamlit as st
from google.cloud import storage
from PIL import Image
from PIL.Image import Image as PIL_Image
import streamlit.components.v1 as components


classification_map = {"Surf Quality": "surf_quality_data", "Gating": "gating_data"}


def get_frame(
    classification: str,
    spot_prefix: str,
    start_date: datetime.date,
    end_date: datetime.date,
    time_range: Tuple[int, int],
    img_location: st.empty,
    error_location: st.empty,
    
) -> None:
    """
    Display first frame maching day, month and time filters.
    Frame path and skipped frames managed in streamlit session_state (ephemeral browser session). 
    """
    storage_client = storage.Client()
    skipped_frames = st.session_state.get("skipped_frames")
    error_location.empty()
    
    if st.session_state.get("undo") == True:
        st.session_state["undo"] = False
        frame_name = st.session_state.get("cur_frame_name")
        frame_name = "/".join(frame_name.split("/")[2:])
        
        bucket = storage_client.bucket(constants.FRAME_DATA_BUCKET)
        blob = bucket.blob(frame_name)
        
        data = blob.download_as_string()
        img = Image.open(BytesIO(data))
        img_location.image(img, caption=blob.name, width=1000)
        _cache_frame(blob.name)
        return
        
    labeled_img_blobs_names = _get_labeled_blob_names(storage_client, classification)
    
    # All GCP storage blobs that end in .png and are from the selected spot
    img_blobs = [
        blob
        for blob in storage_client.list_blobs(
            constants.FRAME_DATA_BUCKET, prefix=spot_prefix
        )
        if blob.name.endswith(".png")
    ]

    # Return first frame macthing filters
    for blob in img_blobs:
        str_name = blob.name.split("/")[-1]
        frame_date = parse_to_date(str_name)

        if str_name in labeled_img_blobs_names:
            continue

        if skipped_frames and f"{classification}/{blob.name}" in skipped_frames:
            continue

        if not start_date <= frame_date <= end_date:
            continue

        if not time_range[0] <= int(str_name.split("_")[3]) <= time_range[1]:
            continue

        data = blob.download_as_string()
        img = Image.open(BytesIO(data))
        img_location.image(img, caption=blob.name, width=1000)
        _cache_frame(blob.name)

        return blob.name, img
    
    # If no frames can be found, clear page and show error message
    img_location.empty()
    error_location.error("No Matching Frames")
    

def get_spot_names() -> List[str]:
    storage_client = storage.Client()
    img_blobs = list(storage_client.list_blobs(constants.FRAME_DATA_BUCKET))
    return list(
        set(
            [
                blob.name.split("/")[0]
                for blob in img_blobs
                if blob.name.endswith(".png")
            ]
        )
    )


def _cache_frame(name: str) -> None:
    """Cache new frame"""
    st.session_state["cur_frame_name"] = name


def undo_previous_classification(image_location: st.empty, storage_client: storage.Client)-> None:
    prev_frame_path = st.session_state.get("prev_frame_name")
    
    if prev_frame_path:       
        
        bucket = storage_client.bucket(constants.LABELED_FRAME_DATA_BUCKET)
        blob = bucket.blob(prev_frame_path)
        blob.delete()
        
        st.session_state["cur_frame_name"] = prev_frame_path
        st.session_state["undo"] = True
        del st.session_state["prev_frame_name"]


def skip_frame(classification: str) -> None:
    frame_name = st.session_state.get("cur_frame_name")
    if not frame_name:
        return

    skipped_frames = st.session_state.get("skipped_frames")
    if skipped_frames:
        skipped_frames.append(f"{classification}/{frame_name}")
        st.session_state["skipped_frames"] = skipped_frames
    else:
        st.session_state["skipped_frames"] = [f"{classification}/{frame_name}"]


def save_frame(
    frame_path: str, storage_client: storage.Client
) -> None:
    """Cache frame info to enable undo button. Save frame to GCP storage"""
    st.session_state["prev_frame_name"] = frame_path
    
    _copy_blob(storage_client, frame_path)


def parse_to_date(frame_name) -> datetime.date:
    split_name = frame_name.split("_")
    return datetime.date(int(split_name[0]), int(split_name[1]), int(split_name[2]))


def _copy_blob(
    storage_client: storage.Client,
    destination_blob_name: str,
)-> None:
    """Copy source frame to desired location"""
    source_bucket = storage_client.bucket(constants.FRAME_DATA_BUCKET)
    source_blob_name = st.session_state["cur_frame_name"]
    
    source_blob = source_bucket.blob(source_blob_name)
    
    destination_bucket = storage_client.bucket(constants.LABELED_FRAME_DATA_BUCKET)
    
    source_bucket.copy_blob(
        source_blob, destination_bucket, destination_blob_name
    )


def _get_labeled_blob_names(storage_client: storage.client, classification: str) -> List[str]:
    """Define labeled frames based on gating bucket or surf_quality bucket"""
    if classification == "gating":
        return [
            blob.name.split("/")[-1]
            for index, blob in enumerate(
                list(
                    storage_client.list_blobs(
                        constants.LABELED_FRAME_DATA_BUCKET,
                        prefix=classification_map.get("Gating"),
                    )
                )
            )
            if blob.name.split("/")[-1].endswith(".png")
        ]
    if classification == "quality":
        return [
            blob.name.split("/")[-1]
            for index, blob in enumerate(
                list(
                    storage_client.list_blobs(
                        constants.LABELED_FRAME_DATA_BUCKET,
                        prefix=classification_map.get("Surf_Quality"),
                    )
                )
            )
            if blob.name.split("/")[-1].endswith(".png")
        ]
