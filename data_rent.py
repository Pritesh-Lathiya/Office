import streamlit as st
import pandas as pd
import os
from PIL import Image

# Set page config
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

# Sample image list from Photos folder
photo_dir = "Photos"
photo_files = [os.path.join(photo_dir, f) for f in os.listdir(photo_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
photos = (photo_files * 8)[:16]  # repeat to ensure 16 images

# Create mock DataFrame for 15 offices
data = {
    "PROPERTY ADDRESS": ["EMPIRE STATE BUILDING"] * 15,
    "AREA": ["RING ROAD"] * 15,
    "SQ FT": [250] * 15,
    "RENT": [35000] * 15,
    "PHOTOS": [photos] * 15,
    "MESSAGE": [
        """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
    ] * 15
}

df = pd.DataFrame(data)

# --- Sidebar Filter ---
min_sqft = df['SQ FT'].min()
max_sqft = df['SQ FT'].max()

if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# --- Display Listings (Vertical, Lazy-load Images) ---
for idx, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        photos = row["PHOTOS"]
        for i in range(0, len(photos), 4):
            row1 = st.columns(2)
            with row1[0]:
                st.image(photos[i], use_container_width=True)
            with row1[1]:
                st.image(photos[i+1], use_container_width=True)
            row2 = st.columns(2)
            with row2[0]:
                st.image(photos[i+2], use_container_width=True)
            with row2[1]:
                st.image(photos[i+3], use_container_width=True)
