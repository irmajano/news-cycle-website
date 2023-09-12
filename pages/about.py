import streamlit as st
import requests
from pages.sources import NUM_SOURCES

st.set_page_config(page_title='About', layout='centered')


# Explain the app
#st.title("About")
st.write("NewsWatch is a news aggregator that collects news from a wide-range of RSS feeds and displays them in a single place.")
st.write(f"NewsWatch is currently based on {NUM_SOURCES} RSS feeds from the most prominent news outlets.")
st.write("NewsWatch is a prototype built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).")
