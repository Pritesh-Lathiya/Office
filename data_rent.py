import streamlit as st
import pandas as pd
from io import StringIO
import requests

# URL to your GitHub raw CSV (replace with your actual GitHub raw link)
CSV_URL = 'https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.csv'

# Load data from GitHub CSV
@st.cache_data
def load_data():
    response = requests.get(CSV_URL)
    response.encoding = 'utf-8-sig'
    return pd.read_csv(StringIO(response.text))

df = load_data()

# Helper function: convert Drive file ID to direct image view link
def get_drive_image_url(file_id):
    return f"https://drive.google.com/uc?export=view&id={file_id.strip()}"

# Page title
st.markdown("## 🏢 Office Listings")

# Optional filter
sqft_filter = st.sidebar.selectbox("Filter by Square Feet", sorted(df['SQ FT'].unique()))
filtered_df = df[df['SQ FT'] == sqft_filter]

st.success(f"{len(filtered_df)} office(s) match your filter.")

# Show listings
for idx, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.markdown(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"{row['MESSAGE']}")
        
        # Show all photos (Google Drive IDs separated by commas)
        photo_ids = str(row['PHOTOS']).split(',')
        for file_id in photo_ids:
            image_url = get_drive_image_url(file_id)
            st.image(image_url, use_column_width=True)
