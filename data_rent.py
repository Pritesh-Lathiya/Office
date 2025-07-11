import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Helper: Convert Drive ID to direct image URL
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

# Repeating 2 images, 16 total
data = {
    "PROPERTY ADDRESS": ["EMPIRE STATE BUILDING"],
    "AREA": ["RING ROAD"],
    "SQ FT": [250],
    "RENT": [35000],
    "PHOTOS": [[
        "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8", "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8",
        "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8", "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8",
        "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8", "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8",
        "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8", "1gELoXJO1Akj3heW0QRJHWLshRPfA7tl8"
    ]],
    "MESSAGE": [
        """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
    ]
}

df = pd.DataFrame(data)

# --- UI ---
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office For Sale")
st.sidebar.header("🔍 Filter by Square Feet")

min_sqft = df['SQ FT'].min()
max_sqft = df['SQ FT'].max()

if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# --- Display Listings ---
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        #       st.write(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        photos = row["PHOTOS"]

        # Display 2x2 grids (4 images per group) — NO LOOP
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
