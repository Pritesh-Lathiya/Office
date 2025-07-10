import streamlit as st
import pandas as pd

# ✅ Load data from raw GitHub CSV
csv_url = "https://raw.githubusercontent.com/Pritesh-Lathiya/Office/main/Data-Rent.csv"
df = pd.read_csv(csv_url)

# 🏢 Page title
st.title("🏢 Office Rental Finder")

# 🔍 Sidebar filter
st.sidebar.header("Filter by Square Feet")
min_sqft = int(df['SQ FT'].min())
max_sqft = int(df['SQ FT'].max())

sqft_range = st.sidebar.slider(
    "Select Range",
    min_value=min_sqft,
    max_value=max_sqft,
    value=(min_sqft, max_sqft)
)

# 🔎 Filter data by SQ FT
filtered_df = df[(df['SQ FT'] >= sqft_range[0]) & (df['SQ FT'] <= sqft_range[1])]

# 📌 Display match count
st.success(f"{len(filtered_df)} office(s) match your filter.")

# 📝 Show office details
for index, row in filtered_df.iterrows():
    with st.expander(f"📍 {row['PROPERTY ADDRESS']} - {row['AREA']} ({row['SQ FT']} sq ft)"):
        st.write(f"**Rent:** ₹{row['RENT']}")

        # Display rich message
        if pd.notna(row['MESSAGE']):
            st.markdown(f"<div style='white-space: pre-wrap;'>{row['MESSAGE']}</div>", unsafe_allow_html=True)

        # Display photo link
        if pd.notna(row['PHOTOS']) and row['PHOTOS'].startswith("http"):
            st.markdown(f"[📷 View Photos]({row['PHOTOS']})", unsafe_allow_html=True)
