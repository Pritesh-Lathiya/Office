import streamlit as st
import pandas as pd
import os

# Set Streamlit app settings
st.set_page_config(page_title="Office Listings", layout="centered")
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

# Load Excel file from GitHub (ensure it's raw link!)
excel_url = "https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.xlsx"
df = pd.read_excel(excel_url, sheet_name="Data-Rent", engine="openpyxl")

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

# Local photo folder
image_folder = "Photos"

# Display Listings
for idx, row in filtered_df.iterrows():
    sr_no = row['Sr. No.']
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        #st.markdown(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        # Look for all images starting with <Sr. No.>_ in Photos folder
        try:
            image_files = sorted([
                os.path.join(image_folder, f)
                for f in os.listdir(image_folder)
                if f.startswith(f"{sr_no}_") and f.lower().endswith((".png", ".jpg", ".jpeg"))
            ])
        except Exception as e:
            st.error(f"Error accessing image folder: {e}")
            image_files = []

        if image_files:
            for i in range(0, len(image_files), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(image_files):
                        with cols[j]:
                            st.image(image_files[i + j], use_container_width=True)
        else:
            st.warning("🚫 No photos found for this property.")
