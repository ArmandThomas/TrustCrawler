import time

import streamlit as st

from functions import execute_scrapy_spider, brands, sidebar

st.set_page_config(page_title="TrustpilotExtract - Home", page_icon="✨", layout="wide")

st.title("Extract reviews")

with st.sidebar:
    sidebar()

is_scraped = False
brand_scraped = []

list_brands = brands()

selected_brands = st.multiselect(
    label="Select brands",
    options=list_brands
)

if st.button(label='Get reviews') and selected_brands != []:

    is_scraped = False
    brand_scraped = []

    for brand in selected_brands:
        with st.status(f"Scraping {brand}", expanded=True) as status:
            st.write(f"Init scraping {brand}...")
            time.sleep(1)
            time_init = time.time()
            st.write(f"Getting reviews from {brand}, please wait...")
            extract = execute_scrapy_spider(brand)
        if extract != 0:
            status.update(label=f"Scraping {brand} failed", state="error", expanded=False)
        else:
            status.update(label=f"Scraping {brand} done", state="complete", expanded=False)
            brand_scraped.append(brand)

    is_scraped = True

    selected_brands = []

if is_scraped:
    for brand in brand_scraped:
        with open(f'TrustpilotReviews/TrustpilotReviews/exports/{brand.replace(".", "")}.csv', 'rb') as f:
            st.download_button(
                label=f"Download {brand} reviews",
                data=f,
                file_name=f"{brand.replace('.', '')}.csv",
                mime="text/csv",
                key=f"{brand.replace('.', '')}"
            )



