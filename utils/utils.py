import requests
import streamlit as st
import requests
import pandas as pd

REQUEST_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-processed'
# Define the API endpoint URL
API_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-sources'
API_KEY = 'c5f4ff6906b0c8ef5a34c027fddc2c59'


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


def create_df():
    r = requests.get(REQUEST_URL).json()

    df = pd.read_json(r)
    #drop rows with empty topic column
    df = df[df['topic'].str.len() > 1]
    #drop rows with nan values in topic column
    df = df.dropna(subset=['topic'])

    #group df by topic and remove rows with only one date
    df = df.groupby('topic').filter(lambda x: len(x) > 1)
    #remove rows with less than 10 in count column
    return df[df['count'] > 10]

def get_top_20(df):
    return df.groupby('topic').agg({
        'count': 'sum',
        'representative_words': 'first',
        'representative_articles': 'first'
    }).sort_values(by=['count'], ascending=False).reset_index()
