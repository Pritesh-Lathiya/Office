import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Convert Google Drive link or ID to direct image URL
def get_drive_image_url(file_id_or_link):
    if "drive.google.com" in file_id_or_link:
        if "id=" in file_id_or_link:
            file_id = file_id_or_link.split("id=")[1]
        elif "/d/" in file_id_or_link:
            file_id = file_id_or_link.split("/d/")[1].split("/")[0]
        else:
            return None
    else:
        file_id = file_id_or_link
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# Common office data
office_data = {
    "PROPERTY ADDRESS": "EMPIRE STATE BUILDING",
    "AREA": "RING ROAD",
    "SQ FT": 250,
    "RENT": 35000,
    "PHOTOS": [
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV"
    ],
    "MESSAGE": """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
}

# Streamlit Page Settings
st.set_page_config(page_title="Office Listings", layout="wide")
st.title("🏢 Office Listings")

# Sidebar filter (for visual purpose)
st.sidebar.header("🔍 Filter by Square Feet")
st.sidebar.info("Only one office listed with 250 sq ft.")

# 3 Columns: Each for 1 Office
col1, col2, col3 = st.columns(3)

for col in [col1, col2, col3]:
    with col.expander(f"📍 {office_data['PROPERTY ADDRESS']} - {office_data['AREA']} ({office_data['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{office_data['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{office_data['MESSAGE']}</div>", unsafe_allow_html=True)

        photos = office_data["PHOTOS"]

        row1 = st.columns(2)
        with row1[0]:
            st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[0])).content)), use_container_width=True)
        with row1[1]:
            st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[1])).content)), use_container_width=True)

        row2 = st.columns(2)
        with row2[0]:
            st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[2])).content)), use_container_width=True)
        with row2[1]:
            st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[3])).content)), use_container_width=True)
