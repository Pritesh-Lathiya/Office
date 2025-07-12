import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# --- Helper Function ---
def get_drive_image_url(file_id):
    file_id = file_id.strip()
    return f"https://drive.google.com/uc?export=download&id={file_id}"

# --- Load Data ---
CSV_URL = "https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.csv"
df = pd.read_csv(CSV_URL, encoding="cp1252")

# --- Parse Photos Column ---
df["PHOTOS"] = df["PHOTOS"].apply(lambda x: [get_drive_image_url(i) for i in str(x).split(",")])

# --- UI ---
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

# --- Filter ---
min_sqft = df["SQ FT"].min()
max_sqft = df["SQ FT"].max()
if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

filtered_df = df[(df["SQ FT"] >= sqft_range[0]) & (df["SQ FT"] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# --- Listings ---
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.markdown(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)
        
        photos = row["PHOTOS"]
        cols = st.columns(2)
        for i, photo_url in enumerate(photos):
            try:
                image = Image.open(BytesIO(requests.get(photo_url).content))
                cols[i % 2].image(image, use_container_width=True)
            except:
                cols[i % 2].error(f"Image load failed:\n{photo_url}")
