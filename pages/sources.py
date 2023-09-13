import streamlit as st
import requests

st.set_page_config(page_title='ℹ️ Sources', layout='centered')
st.title("Sources")
# add a sidebar with an About section that explains the app
st.sidebar.info('''
NewsWatch is a prototype of a news cycle aggregator. It uses a topic modeling algorithm to extract topics from news articles and then visualizes the results in a streamgraph. The app is built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).
''')
# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch_logo.png', use_column_width=True)


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
