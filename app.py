import os
import base64
from rembg import remove
from PIL import Image
import streamlit as st

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


def remove_background(input_path, output_path):
    input_image = Image.open(input_path)
    output_image = remove(input_image)
    output_image.save(output_path)


def get_binary_file_downloader_html(file_path):
    """
    Generates a link allowing the user to download the content in `file_path`
    """
    with open(file_path, 'rb') as file:
        data = file.read()
    encoded_data = base64.b64encode(data).decode()
    href = f'<a href="data:file/png;base64,{encoded_data}" download="{file_path}">Download {file_path}</a>'
    return href


st.title('Remove Background')

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "webp"])

if uploaded_file is not None:
    image_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(image_path, caption="Original Image", use_column_width=True)

    if st.button('Remove Background'):
        rembg_img_name = uploaded_file.name.split('.')[0] + "_rembg.png"
        remove_background(image_path, os.path.join(UPLOAD_FOLDER, rembg_img_name))
        st.image(os.path.join(UPLOAD_FOLDER, rembg_img_name), caption="Image with Background Removed",
                 use_column_width=True)

        # Add a "Download" button
        st.markdown(get_binary_file_downloader_html(os.path.join(UPLOAD_FOLDER, rembg_img_name)),
                    unsafe_allow_html=True)
