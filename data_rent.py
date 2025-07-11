import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Helper to convert Google Drive ID/link to direct download URL
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

# --- Base office data ---
base_office = {
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

# --- Duplicate the same office 3 times ---
offices = [base_office, base_office, base_office]

st.set_page_config(page_title="Office Listings", layout="wide")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

# Columns for 3 office cards
cols = st.columns(3)

for i, col in enumerate(cols):
    office = offices[i]
    with col:
        st.subheader(f"📍 {office['PROPERTY ADDRESS']} - {office['AREA']}")
        st.write(f"**Rent:** ₹{office['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{office['MESSAGE']}</div>", unsafe_allow_html=True)

        # 2x2 image grid
        photos = office["PHOTOS"]
        row1 = st.columns(2)
        row1[0].image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[0])).content)), use_container_width=True)
        row1[1].image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[1])).content)), use_container_width=True)

        row2 = st.columns(2)
        row2[0].image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[2])).content)), use_container_width=True)
        row2[1].image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[3])).content)), use_container_width=True)
