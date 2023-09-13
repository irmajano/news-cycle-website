import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

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

st.title("Top Topics of the Week")
st.markdown('''
Explore the top 20 topics of the week.\n
Each topic is a wordcloud that shows the most representative words in it.
''')

from Home import TOP_20_TOPICS

#for each row in the dataframe, create a wordcloud
for index, row in TOP_20_TOPICS.iterrows():
    text = ', '.join(row['representative_words'])
    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)
    st.markdown(f"### {row['topic']}".title())





    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    #plt.show()
    fig = plt.gcf()
    #display the figure in size
    st.pyplot(fig)
