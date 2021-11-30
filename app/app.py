from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time
import os
import datetime


def main(img_location, storage_client):
    
    spot_names = utils.get_spot_names()
    st.sidebar.image(str(constants.LOGO_PATH), use_column_width=True)
    classification_type = st.sidebar.selectbox("Please select a classification type.", ["Gating", "Surf Quality"]) 
    selected_spot = st.sidebar.selectbox("Please select a spot.", spot_names)
    
    startdate = st.sidebar.date_input('Start Date', (datetime.date.today() - datetime.timedelta(days=1)))
    enddate = st.sidebar.date_input('End Date', datetime.date.today())
    day_date_range = (startdate.day, enddate.day)
    month_date_range = (startdate.month, enddate.month)
    
    starttime = st.sidebar.time_input('Start Time', datetime.time(6))
    endtime = st.sidebar.time_input('End Time', datetime.time(18))
    time_range = (starttime.hour, endtime.hour)
    
    
    # Create frame generator
    frames = utils.get_frames(spot_prefix=selected_spot, day_date_range=day_date_range, month_date_range=month_date_range, time_range=time_range)

    
    if classification_type == "Surf Quality":
        
        # Iterate over frames, drop previous data form session, save new data
        if st.button("New Frame"):
            utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
            
        cols = st.columns(3)
        # Classify frame as choppy conditions  
        with cols[0]:
            if st.button("Choppy"):
                bucket = constants.LABELED_FRAME_DATA_BUCKET
                frame_name = st.session_state["frame_name"]
                frame_data = st.session_state["frame_data"]
                frame_path = os.path.join(constants.CHOPPY_PREFIX, frame_name)
                utils.save_frame(bucket, frame_path, frame_data, storage_client)
                utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
        
        # Classify frame as semi-choppy conditions  
        with cols[1]:
            if st.button("Semi-Chop"):
                bucket = constants.LABELED_FRAME_DATA_BUCKET
                frame_name = st.session_state["frame_name"]
                frame_data = st.session_state["frame_data"]
                frame_path = os.path.join(constants.SEMI_CHOP_PREFIX, frame_name)
                utils.save_frame(bucket, frame_path, frame_data, storage_client)
                utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
        
        # Classify frame as glassy conditions  
        with cols[2]:
            if st.button("Glassy"):
                bucket = constants.LABELED_FRAME_DATA_BUCKET
                frame_name = st.session_state["frame_name"]
                frame_data = st.session_state["frame_data"]
                frame_path = os.path.join(constants.GLASSY_PREFIX, frame_name)
                utils.save_frame(bucket, frame_path, frame_data, storage_client)
                utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
    
    
    if classification_type == "Gating":
        
        # Iterate over frames, drop previous data form session, save new data
        if st.button("New Frame"):
            utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
        
        cols = st.columns(2)
        # Classify frame as inactive for gating  
        with cols[0]:
            if st.button("Visible"):
                bucket = constants.LABELED_FRAME_DATA_BUCKET
                frame_name = st.session_state["frame_name"]
                frame_data = st.session_state["frame_data"]
                frame_path = os.path.join(constants.ACTIVE_PREFIX, frame_name)
                utils.save_frame(bucket, frame_path, frame_data, storage_client)
                utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
        
        # Classify frame as inactive for gating  
        with cols[1]:
            if st.button("Not Visible"):
                bucket = constants.LABELED_FRAME_DATA_BUCKET
                frame_name = st.session_state["frame_name"]
                frame_data = st.session_state["frame_data"]
                frame_path = os.path.join(constants.INACTIVE_PREFIX, frame_name)
                utils.save_frame(bucket, frame_path, frame_data, storage_client)
                utils.new_frame(frames, img_location, classification_type_prefix=classification_type, storage_client=storage_client)
                
                
            
        
        
if __name__ == "__main__":
    st.set_page_config(layout="wide")

    storage_client = storage.Client()
    img_location = st.empty()
    main(img_location, storage_client)
