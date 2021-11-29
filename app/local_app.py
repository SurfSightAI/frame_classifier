from typing import Generator
import streamlit as st
from google.cloud import storage
import constants
import utils
from PIL import Image
import time
import types 

@st.cache(hash_funcs={types.GeneratorType: id})
def give_nums():
    for i in range(100):
        yield i

nums = [1,2,3]

def next_num(num):
    st.write(num)

def main(nums, location):
    if st.button("New Num"):
        var = next(nums)
        location.write(var)
        print(var)
        
        
        
    




if __name__ == "__main__":
    nums = give_nums() # Returns gen
    if st.button("New Num"):
        var = next(nums)
        st.write(var)
        print(var)

    
    
