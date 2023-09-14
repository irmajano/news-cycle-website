import streamlit as st
from utils.utils import add_logo, fetch_data

st.title("Sources")
add_logo()

# Fetch data from the API
data = fetch_data()
NUM_SOURCES = data.get("feed_count", 0)

if data:
    sources_list = data.get("sources", [])

    st.subheader(f"NewsWatch aggregates news from a wide-range of [RSS feeds](https://en.wikipedia.org/wiki/RSS) that are provided by the most prominent news outlets.")
    st.write(f"NewsWatch is currently based on {NUM_SOURCES} RSS feeds.")

    # Search bar
    search_query = st.text_input("Search sources:")

    # Filter and display the list of sources based on the search query
    filtered_sources = [source for source in sources_list if search_query.lower() in source.lower()]

    if filtered_sources:
        st.write("List of Sources:")
        for source in filtered_sources:
            st.write(source)
    else:
        st.write("No matching sources found.")
