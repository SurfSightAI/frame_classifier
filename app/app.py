from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time
import os


def main(img_location, storage_client):
    # Create frame generator
    frames = utils.get_frames()
    
    
    # Iterate over frames, drop previous data form session, save new data
    if st.button("New Frame"):
        utils.new_frame(frames, img_location)
        
    cols = st.columns(5)
    # Classify frame as choppy conditions  
    with cols[0]:
        if st.button("Choppy"):
            bucket = constants.LABELED_FRAME_DATA_BUCKET
            frame_name = st.session_state["frame_name"]
            frame_data = st.session_state["frame_data"]
            frame_path = os.path.join(constants.CHOPPY_PREFIX, frame_name)
            utils.save_frame(bucket, frame_path, frame_data, storage_client)
            utils.new_frame(frames, img_location)
    
    # Classify frame as semi-choppy conditions  
    with cols[1]:
        if st.button("Semi-Chop"):
            bucket = constants.LABELED_FRAME_DATA_BUCKET
            frame_name = st.session_state["frame_name"]
            frame_data = st.session_state["frame_data"]
            frame_path = os.path.join(constants.SEMI_CHOP_PREFIX, frame_name)
            utils.save_frame(bucket, frame_path, frame_data, storage_client)
            utils.new_frame(frames, img_location)
    
    # Classify frame as glassy conditions  
    with cols[2]:
        if st.button("Glassy"):
            bucket = constants.LABELED_FRAME_DATA_BUCKET
            frame_name = st.session_state["frame_name"]
            frame_data = st.session_state["frame_data"]
            frame_path = os.path.join(constants.GLASSY_PREFIX, frame_name)
            utils.save_frame(bucket, frame_path, frame_data, storage_client)
            utils.new_frame(frames, img_location)
    
    # Classify frame as inactive for gating  
    with cols[3]:
        if st.button("Active"):
            bucket = constants.LABELED_FRAME_DATA_BUCKET
            frame_name = st.session_state["frame_name"]
            frame_data = st.session_state["frame_data"]
            frame_path = os.path.join(constants.ACTIVE_PREFIX, frame_name)
            utils.save_frame(bucket, frame_path, frame_data, storage_client)
            utils.new_frame(frames, img_location)
    
    # Classify frame as inactive for gating  
    with cols[4]:
        if st.button("Inactive"):
            bucket = constants.LABELED_FRAME_DATA_BUCKET
            frame_name = st.session_state["frame_name"]
            frame_data = st.session_state["frame_data"]
            frame_path = os.path.join(constants.INACTIVE_PREFIX, frame_name)
            utils.save_frame(bucket, frame_path, frame_data, storage_client)
            utils.new_frame(frames, img_location)
            
        
        
if __name__ == "__main__":
    storage_client = storage.Client()
    img_location = st.empty()
    main(img_location, storage_client)
