import datetime
from io import BytesIO
from typing import List, Tuple

import constants
import streamlit as st
from google.cloud import storage
from PIL import Image
from PIL.Image import Image as PIL_Image

classification_map = {"Surf Quality": "surf_quality_data", "Gating": "gating_data"}


def get_frame(
    classification: str,
    spot_prefix: str,
    start_date: datetime.date,
    end_date: datetime.date,
    time_range: Tuple[int, int],
    img_location: st.empty,
) -> Tuple[str, PIL_Image]:
    """
    Return a genorator of all frames in bucket. Filter based on day, month and time.
    """
    storage_client = storage.Client()
    skipped_frames = st.session_state.get("skipped_frames")

    if classification == "gating":
        labeled_img_blobs_names = [
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
        labeled_img_blobs_names = [
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

    img_blobs = [
        blob
        for blob in storage_client.list_blobs(
            constants.FRAME_DATA_BUCKET, prefix=spot_prefix
        )
        if blob.name.endswith(".png")
    ]

    for blob in img_blobs:
        str_name = blob.name.split("/")[-1]
        spot_name = blob.name.split("/")[0]
        frame_date = parse_to_date(str_name)

        if str_name in labeled_img_blobs_names:
            continue

        if skipped_frames and f"{classification}_{str_name}" in skipped_frames:
            continue

        if not str_name.endswith(".png") or spot_name != spot_prefix:
            continue

        if not start_date <= frame_date <= end_date:
            continue

        if not time_range[0] <= int(str_name.split("_")[3]) <= time_range[1]:
            continue

        data = blob.download_as_string()
        img = Image.open(BytesIO(data))
        img_location.image(img, caption=blob.name, width=1000)
        _cache_frame(img, blob.name)

        return blob.name, img
    st.write("NO frames")


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


def _cache_frame(frame: PIL_Image, name: str) -> None:
    """
    Cache frame info in session
    """
    try:
        del st.session_state["frame_name"]
        del st.session_state["frame_data"]
    except KeyError:
        pass
    st.session_state["frame_name"] = name
    st.session_state["frame_data"] = frame.tobytes()

    return name, frame


def skip_frame(classification) -> None:
    frame_name = st.session_state.get("frame_name")
    if not frame_name:
        return

    skipped_frames = st.session_state.get("skipped_frames")
    if skipped_frames:
        skipped_frames.append(f"{classification}_{frame_name}")
        st.session_state["skipped_frames"] = skipped_frames
    else:
        st.session_state["skipped_frames"] = [f"{classification}_{frame_name}"]


def save_frame(
    bucket: str, frame_path: str, img_data: bytes, storage_client: storage.Client
) -> None:
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(frame_path)
    blob.upload_from_string(img_data, content_type="image/png")


def parse_to_date(frame_name) -> datetime:
    split_name = frame_name.split("_")
    year = int(split_name[0])
    month = int(split_name[1])
    day = int(split_name[2])
    return datetime.date(year, month, day)
