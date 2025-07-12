import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Set Streamlit app settings
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

# Load Excel file from GitHub (ensure it's raw link!)
excel_url = "https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.xlsx"
df = pd.read_excel(excel_url, sheet_name="Data-Rent", engine="openpyxl")

# Ensure 'PHOTOS' column is string and split by comma
df["PHOTOS"] = df["PHOTOS"].astype(str).apply(lambda x: [f"https://drive.google.com/uc?export=view&id={id.strip()}" for id in x.split(",")])

# Sidebar SQ FT Filter
min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())

if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# Display Listings
for idx, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.markdown(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        photo_urls = row["PHOTOS"]
        for i in range(0, len(photo_urls), 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(photo_urls):
                    with cols[j]:
                        try:
                            st.image(photo_urls[i + j], use_container_width=True)
                        except:
                            st.warning(f"Image load failed: {photo_urls[i + j]}")


import streamlit as st

st.subheader("🔍 Google Drive Image Test")

# Correct Google Drive image ID
image_id = "1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W"
test_url = f"https://drive.google.com/uc?export=download&id={image_id}"

# Show the URL for debugging
st.markdown(f"**Image URL:** [{test_url}]({test_url})")

# Display image
st.image(test_url, caption="Image from Google Drive", use_container_width=True)
