import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Convert Google Drive file ID to direct image URL
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

# Original office data with repeated images
office_data = {
    "PROPERTY ADDRESS": "EMPIRE STATE BUILDING",
    "AREA": "RING ROAD",
    "SQ FT": 250,
    "RENT": 35000,
    "PHOTOS": [
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV"
    ],
    "MESSAGE": """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
}

# Create a list of 15 copies
office_list = [office_data.copy() for _ in range(15)]

# Streamlit UI
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")
st.sidebar.info("Only one office listed with 250 sq ft.")

st.success(f"{len(office_list)} office(s) match your filter.")

# Display all 15 office listings with lazy image loading
for index, office in enumerate(office_list):
    with st.expander(f"📍 {office['PROPERTY ADDRESS']} - {office['AREA']} ({office['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{office['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{office['MESSAGE']}</div>", unsafe_allow_html=True)

        if st.toggle(f"Show Photos for Office {index + 1}", key=f"toggle_{index}"):
            photos = office["PHOTOS"]

            for i in [0, 4, 8, 12]:
                row1 = st.columns(2)
                with row1[0]:
                    st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[i])).content)), use_container_width=True)
                with row1[1]:
                    st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[i+1])).content)), use_container_width=True)

                row2 = st.columns(2)
                with row2[0]:
                    st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[i+2])).content)), use_container_width=True)
                with row2[1]:
                    st.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[i+3])).content)), use_container_width=True)
