import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.utils import add_logo

# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch_logo.png', use_column_width=True)
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
