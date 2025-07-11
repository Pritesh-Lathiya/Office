import streamlit as st
import pandas as pd
from PIL import Image
import requests
from io import BytesIO

# Helper function to convert Google Drive share link to direct view URL
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

# Hardcoded office data
data = {
    "PROPERTY ADDRESS": ["EMPIRE STATE BUILDING"],
    "AREA": ["RING ROAD"],
    "SQ FT": [250],
    "RENT": [35000],
    "PHOTOS": ["1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W"],  # Just the file ID or full link
    "MESSAGE": [
        """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
    ]
}

# Load DataFrame
df = pd.DataFrame(data)

# Streamlit UI
st.title("🏢 Office Listings")
st.sidebar.header("🔍 Filter by Square Feet")

min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())

# Slider only when range exists
if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider("Select Range (sq ft)", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

# Filtered results
filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# Show office listings
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")
        st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        # Show image
        photo_url = get_drive_image_url(row['PHOTOS'])
        try:
            response = requests.get(photo_url)
            if response.status_code == 200:
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="📷 Office Photo", use_container_width=True)
            else:
                st.warning("⚠️ Could not load image.")
        except:
            st.warning("⚠️ Invalid image link or Google Drive permissions.")
