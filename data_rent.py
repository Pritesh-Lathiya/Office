import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# Title
st.title("🏢 Office Listings")

# Load Excel from GitHub
github_excel_url = "https://github.com/Pritesh-Lathiya/Office/raw/main/Data-Rent.xlsx"
sheet_name = "Data-Rent"

# Read Excel file into DataFrame
response = requests.get(github_excel_url)
df = pd.read_excel(BytesIO(response.content), sheet_name=sheet_name)

# Show number of offices
st.success(f"{len(df)} office(s) match your filter.")

# Show each office listing
for idx, row in df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.markdown(f"**Rent:** ₹{row['RENT']}")
        st.markdown(row['MESSAGE'])

        # Parse Google Drive IDs (comma-separated)
        drive_ids = str(row['PHOTOS']).split(",")

        # Loop through each ID
        for file_id in drive_ids:
            file_id = file_id.strip()
            if file_id:
                img_url = f"https://drive.google.com/uc?export=view&id={file_id}"
                try:
                    st.image(img_url, caption=file_id, use_container_width=True)
                except Exception as e:
                    st.error(f"Image load failed for ID: {file_id}")
