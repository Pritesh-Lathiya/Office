import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO

# 🧾 Embedded office rental data
data = [
    {
        "PROPERTY ADDRESS": "EMPIRE STATE BUILDING - RING ROAD",
        "AREA": "RING ROAD",
        "SQ FT": 250,
        "RENT": 35000,
        "MESSAGE": "📋 Fully Furnished Office for Rent – Empire State Building\n📍 Location: M-12, Empire State Building, Near Udhna Darwaja\n✅ Office Features:\n🟩 1 Big Boss Cabin\n🟩 1 Staff Cabin",
        "PHOTOS": "https://drive.google.com/file/d/1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W/view?usp=sharing"
    }
]

# 📊 Create DataFrame
df = pd.DataFrame(data)

# 🏢 Title
st.title("🏢 Office Rental Finder")

# 📏 Sidebar filters
st.sidebar.header("Filter by Square Feet")
min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())
sqft_range = st.sidebar.slider("Select Range", min_value=min_sqft, max_value=max_sqft, value=(min_sqft, max_sqft))

# 🔎 Filter
filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]

# 📌 Show result count
st.success(f"{len(filtered_df)} office(s) match your filter.")

# 🏢 Display offices
for index, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")
        
        if pd.notna(row['MESSAGE']):
            st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        # 🖼️ Show image from Google Drive
        if pd.notna(row['PHOTOS']) and "drive.google.com/file/d/" in row['PHOTOS']:
            try:
                file_id = row['PHOTOS'].split("/d/")[1].split("/")[0]
                direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
                response = requests.get(direct_url)
                if response.status_code == 200:
                    img = Image.open(BytesIO(response.content))
                    st.image(img, caption="📷 Office Photo", use_container_width=True)
                else:
                    st.warning("⚠️ Could not load photo.")
            except Exception as e:
                st.error(f"❌ Error loading image: {e}")
