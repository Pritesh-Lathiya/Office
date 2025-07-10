import streamlit as st
import pandas as pd

# 🧾 Hardcoded data with updated image
data = {
    "PROPERTY ADDRESS": ["EMPIRE STATE BUILDING"],
    "AREA": ["RING ROAD"],
    "SQ FT": [250],
    "RENT": [35000],
    "PHOTOS": ["https://drive.google.com/uc?export=view&id=1LbD0FybifnYtqe4PPhuMfhC7bEex3K-W"],  # 🔁 New PNG image
    "MESSAGE": [
        """🧾 Fully Furnished Office for Rent – Empire State Building
📍 Location: M-12, Empire State Building, Near Udhna Darwaja

✔️ Office Features:
✅ 1 Big Boss Cabin
✅ 1 Staff Cabin"""
    ]
}

# Load into DataFrame
df = pd.DataFrame(data)

# 🏢 App Title
st.title("🏢 Office Rental Finder")

# 📏 Square Feet Filter
st.sidebar.header("Filter by Square Feet")
min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())

if min_sqft == max_sqft:
    st.sidebar.info(f"Only one office listed with {min_sqft} sq ft.")
    sqft_range = (min_sqft, max_sqft)
else:
    sqft_range = st.sidebar.slider(
        "Select Range (sq ft)",
        min_value=min_sqft,
        max_value=max_sqft,
        value=(min_sqft, max_sqft)
    )

# 🔍 Filter records
filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]
st.success(f"{len(filtered_df)} office(s) match your filter.")

# 📦 Display results
for _, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")

        if pd.notna(row['MESSAGE']):
            st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        if pd.notna(row['PHOTOS']) and row['PHOTOS'].startswith("http"):
            st.image(row['PHOTOS'], caption="📷 Office Photo", use_column_width=True)
