import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tempfile
import os

def dodgeV2(x, y):
    return cv2.divide(x, 255 - y, scale=256)

def pencilsketch(inp_img):
    img_gray = cv2.cvtColor(inp_img, cv2.COLOR_BGR2GRAY)
    img_invert = cv2.bitwise_not(img_gray)
    img_smoothing = cv2.GaussianBlur(img_invert, (21, 21), sigmaX=0, sigmaY=0)
    final_img = dodgeV2(img_gray, img_smoothing)
    return final_img

# Page Title and Description
st.title('PencilSketcher App')
st.write('This webapp is use to convert your photos to realistic pencil sketches')

# Sidebar Options
st.sidebar.title('Options')
brightness = st.sidebar.slider('Brightness', -100, 100, 0, 10)
contrast = st.sidebar.slider('Contrast', -100, 100, 0, 10)

# Image Upload
file_image = st.sidebar.file_uploader('Upload Your Photo', type=['jpeg', 'jpg', 'png'])

if file_image is not None:
    # Load and Process the Image
    input_img = Image.open(file_image)
    img_array = np.array(input_img)
    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    img_array = cv2.convertScaleAbs(img_array, alpha=contrast/10, beta=brightness)
    final_sketch = pencilsketch(img_array)

    # Display Input and Output
    col1, col2 = st.columns(2)
    with col1:
        st.header('Input Photo')
        st.image(input_img, use_column_width=True)

    with col2:
        st.header('Output Pencil Sketch')
        st.image(final_sketch, caption='Pencil Sketch', use_column_width=True)

    # Save the Sketch as a Temporary File
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_filename = temp_file.name
        cv2.imwrite(temp_filename, final_sketch)

    # Download the Pencil Sketch
    st.download_button("Download Pencil Sketch", temp_filename, file_name='pencil_sketch.jpg')

# Styling the App
hide_footer_style = """
    <style>
    .reportview-container .main footer {visibility: hidden;}
    """
st.markdown(hide_footer_style, unsafe_allow_html=True)
st.sidebar.markdown("---")
st.sidebar.markdown("<p style='text-align: center; color: #888;'>Powered by Streamlit</p>", unsafe_allow_html=True)
