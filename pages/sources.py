import streamlit as st
import requests

def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.postimg.cc/QNH0Rdz4/2.png);
                background-size: 250px;
                width: 900;
                height: 900px;
                background-repeat: no-repeat;
                background-position: center;
                background-position-x: 60%;
                background-position-y: 50px;
                padding-top: 250px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Define the API endpoint URL
API_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-sources'
API_KEY = 'c5f4ff6906b0c8ef5a34c027fddc2c59'

def fetch_data():
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from the API.")
        return None

st.title("Sources")
# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch_logo.png', use_column_width=True)
add_logo()

# Fetch data from the API
data = fetch_data()
NUM_SOURCES = data.get("feed_count", 0)

if data:
    sources_list = data.get("sources", [])
    #num_sources = data.get("feed_count", 0)

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
