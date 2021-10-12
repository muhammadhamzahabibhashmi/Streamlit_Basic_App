from typing import KeysView
import streamlit as st
import numpy as np
import cv2

uploaded_file = st.file_uploader("Upload a Dataset", type=["png", "jpg"])
if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    im = cv2.imdecode(file_bytes, 1)
    st.image(im, channels="BGR")

dicttt = {
    "Pressery Pho":10,
    "Etai's Croissant Turkey":2,
    "Purely Elizabeth Oatmeal":1
         }

len_diccct = len(dicttt)

col1 , col2 = st.beta_columns(2)
values = dicttt.values()
kKeys = dicttt.keys()

values_list = list(values)
keys_list = list(kKeys)

for i in range(len_diccct):
    col1.warning(f"{keys_list[i]}")
    col2.success(f"{values_list[i]}")

