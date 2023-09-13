import streamlit as st
import requests
from pages.Sources import NUM_SOURCES

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
        unsafe_allow_html=True
    )

add_logo()

# Explain the app
st.title("About")
st.markdown('''
### Explore the Latest News Trends of the Week!
Welcome to our news aggregation app, your go-to source for staying informed about the most significant news topics of the past week. We've designed this app with simplicity and convenience in mind, so you can effortlessly discover what's been making headlines recently.
### Stay Updated
In today's fast-paced world, it can be challenging to keep up with the ever-changing news landscape. Our app helps you stay updated by curating and presenting the top news topics that have dominated the past week. No more sifting through endless articles – we bring the highlights directly to you.
### User-Friendly Interface
Navigating our app is a breeze. The intuitive user interface allows you to quickly browse through the week's top news topics. Each topic is presented with a concise summary, making it easy to decide which stories pique your interest.
### Save Time
With our app, you won't need to spend hours searching for news updates. We do the heavy lifting for you by collecting and summarizing the top news stories.
### Deep-Dives
Once you find a news topic that captivates you, dive in and explore more about it.
Start exploring the latest news topics from the past week today.
''')

# provide a link to the Sources page that opens in the same tab using target="_self"
st.write("For more information about the sources, please visit the [Sources](/Sources) page.", target="_self")
