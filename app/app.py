import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image

def main():
    storage_client = storage.Client()
    img_blobs = list(storage_client.list_blobs(constants.FRAME_DATA_BUCKET))
    img_bytes = img_blobs[0].download_as_string()
    img = Image.open(img_bytes)
    st.image(img)


if __name__ == "__main__":
    main() 

