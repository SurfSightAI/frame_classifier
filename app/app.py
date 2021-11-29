from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time

def main():
    storage_client = storage.Client()
    frames = utils.get_frames(storage_client)
    st.image(next(frames))

if __name__ == "__main__":
    main()
