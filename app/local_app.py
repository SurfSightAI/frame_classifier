from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time

def give_nums():
    for i in range(100):
        yield i

def next_frame (nums: Generator):
    st.write(next(nums))

def main(nums):
    st.button("New Num", on_click=next_num(nums))



if __name__ == "__main__":
    storage_client = storage.Client()
    main() 

