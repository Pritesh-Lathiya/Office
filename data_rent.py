import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# ---- SETTINGS ----
CSV_URL = "https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.csv"

# ---- FUNCTIONS ----
def get_drive_image_url(file_id_or_link):
    """Convert Google Drive file ID or URL to direct image download link"""
    if "drive.google.com" in file_id_or_link:
        if "id=" in file_id_or_link:
            file_id = file_id_or_link.split("id=")[1]
        elif "/d/" in file_id_or_link:
            file_id = file_id_or_link.split("/d/")[1].split("/")[0]
        else:
            return None
    else:
        file_id = file_id_or_link.strip()
    return f"https://drive.google.com/uc?export=download&id={file_id}"

def load_image_from_drive(file_id):
    url = get_drive_image_url(file_id)
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# ---- LOAD DATA ----
df = pd.read_csv(CSV_URL, encoding="utf-8-sig")
df["PHOTOS"] = df["PHOTOS"].apply(lambda x: [i.strip() for i in str(x).split(",") if i.strip()])

# ---- UI LAYOUT ----
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
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

# ---- DISPLAY LISTINGS ----
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        photo_ids = row["PHOTOS"]
        cols = st.columns(2)

        for i, photo_id in enumerate(photo_ids):
            with cols[i % 2]:
                try:
                    img = load_image_from_drive(photo_id)
                    st.image(img, use_container_width=True)
                except Exception as e:
                    st.error(f"Image load failed: {photo_id}")
