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

    import streamlit as st
    import requests
    from PIL import Image  # Optional: If you want to use PIL for more complex image handling

    def display_image_from_google_drive(file_id):
        url = f"https://drive.google.com/uc?export=view&id={file_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            # Method 1: Display using bytes (no need for PIL)
            st.image(response.content, caption=f"Image from Google Drive (ID: {file_id})")

            # Method 2: (Requires PIL)
            # image = Image.open(io.BytesIO(response.content))
            # st.image(image, caption=f"Image from Google Drive (ID: {file_id})")

        except requests.exceptions.RequestException as e:
            st.error(f"Error fetching image: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")


    # Example usage:
    file_id_1 = "1FlbaLnpIbqk7mmrvknULUw9UxtF8msJF"  # Replace with your actual file ID
    file_id_2 = "1FlbaLnpIbqk7mmrvknULUw9UxtF8msJF" # Replace with another file id
    display_image_from_google_drive(file_id_1)
    display_image_from_google_drive(file_id_2)


    # st.image(["image_url_1", "image_url_2"], caption=["Caption 1", "Caption 2"])
