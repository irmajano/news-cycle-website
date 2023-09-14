import streamlit as st
from utils.utils import add_logo, fetch_data

st.set_page_config(layout="centered", page_title='Sources')

st.title("Sources")
add_logo()

# Fetch data from the API
data = fetch_data()
num_sources = data.get("feed_count", 0)

st.subheader(f"NewsWatch is currently based on {num_sources} RSS feeds")

if data:
    sources_list = data.get("sources", [])

    st.write(f"""**NewsWatch** aggregates news from a wide range of <a href="https://en.wikipedia.org/wiki/RSS" target="_self">RSS feeds</a> provided by the most prominent news outlets.""", unsafe_allow_html=True)
    st.write('Consult all the sources scraped using the form below.')
    st.markdown("""---""")

    # Search bar
    search_query = st.text_input("Search sources:")

    # Filter and display the list of sources based on the search query
    filtered_sources = [source for source in sources_list if search_query.lower() in source.lower()]

    if filtered_sources:
        st.write("**List of Sources:**")
        for source in filtered_sources:
            st.write(source)
    else:
        st.write("No matching sources found.")
