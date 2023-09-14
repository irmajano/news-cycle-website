import streamlit as st
from utils.utils import add_logo

st.set_page_config(layout="wide", page_title='About')

add_logo()

# Explain the app
st.title("About")

st.write('''For information about the sources, please visit the <a href="/Sources" target="_self">Sources</a> page.''', unsafe_allow_html=True)

st.write('''### Explore the Latest News Trends of the Week!
Welcome to our **news aggregation app**, your go-to source for staying informed about the most significant news topics of the past week. We've designed this app with simplicity and convenience in mind, so you can effortlessly discover what's been making headlines recently.''')
st.write('''### Stay Updated
In today's fast-paced world, it can be challenging to keep up with the ever-changing news landscape. Our app helps you stay updated by **curating and presenting** the <a href="/Topics" target="_self">top news topics</a> that have dominated the **past week**. No more sifting through endless articles — we bring the highlights directly to you.''', unsafe_allow_html=True)
st.write('### NewsWatch Workflow')
st.image('NewsWatch_Setup.png')
st.write('''### User-Friendly Interface
Navigating our app is a breeze. The intuitive user interface allows you to quickly browse through the week's **top news topics**. Each topic is presented with a concise summary, making it easy to decide which stories pique your interest.''', unsafe_allow_html=True)
st.write('''### Save Time
With our app, you won't need to spend hours searching for news updates. We do the heavy lifting for you by **collecting and summarizing** the top news stories.''')
st.write('''### Deep-Dives
Once you find a news topic that captivates you, dive in and explore more about it.
Start exploring the latest news topics from the past week today.''')
