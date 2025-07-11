import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# --- Helper: Convert Google Drive ID or URL to direct image URL ---
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

# --- Image IDs manually written (repeating the same 2 IDs) ---
data = {
    "PROPERTY ADDRESS": ["EMPIRE STATE BUILDING"],
    "AREA": ["RING ROAD"],
    "SQ FT": [250],
    "RENT": [35000],
    "PHOTOS": [[
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 1st row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 2nd row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 3rd row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 4th row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 5th row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 6th row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV",  # 7th row
        "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W", "1yVNJwjT4Vz58h6WuB5fCZbQc9TOlHQjV"   # 8th row
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

# --- Streamlit Layout ---
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())

if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# --- Display Listing ---
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        photos = row['PHOTOS']
        # 8 manually written rows (2 images each), no loops
        col1, col2 = st.columns(2)
        img1_url = get_drive_image_url(photos[0])
        img2_url = get_drive_image_url(photos[1])
        col1.image(Image.open(BytesIO(requests.get(img1_url).content)), use_container_width=True)
        col2.image(Image.open(BytesIO(requests.get(img2_url).content)), use_container_width=True)

        col3, col4 = st.columns(2)
        col3.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[2])).content)), use_container_width=True)
        col4.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[3])).content)), use_container_width=True)

        col5, col6 = st.columns(2)
        col5.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[4])).content)), use_container_width=True)
        col6.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[5])).content)), use_container_width=True)

        col7, col8 = st.columns(2)
        col7.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[6])).content)), use_container_width=True)
        col8.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[7])).content)), use_container_width=True)

        col9, col10 = st.columns(2)
        col9.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[8])).content)), use_container_width=True)
        col10.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[9])).content)), use_container_width=True)

        col11, col12 = st.columns(2)
        col11.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[10])).content)), use_container_width=True)
        col12.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[11])).content)), use_container_width=True)

        col13, col14 = st.columns(2)
        col13.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[12])).content)), use_container_width=True)
        col14.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[13])).content)), use_container_width=True)

        col15, col16 = st.columns(2)
        col15.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[14])).content)), use_container_width=True)
        col16.image(Image.open(BytesIO(requests.get(get_drive_image_url(photos[15])).content)), use_container_width=True)
