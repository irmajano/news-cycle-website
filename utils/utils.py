import requests
import streamlit as st
# Fetch

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

def fetch_data():
    headers = {"api-key": API_KEY}
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        st.error("Failed to fetch data from the API.")
        return None

# Define the API endpoint URL
API_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-sources'
API_KEY = 'c5f4ff6906b0c8ef5a34c027fddc2c59'
