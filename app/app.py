from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time

def main(client, img_location):
    frames = utils.get_frames(storage_client)
    if st.button("New Frame"):
        img_location.image(next(frames))

if __name__ == "__main__":
    storage_client = storage.Client()
    img_location = st.empty()
    main(storage_client, img_location)
