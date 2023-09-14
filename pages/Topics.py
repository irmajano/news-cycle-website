import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.utils import add_logo, create_df, get_top_20, REQUEST_URL

st.set_page_config(layout="centered", page_title='Topics')

add_logo()

st.title("Top Topics")
st.subheader('Explore the top 20 topics of the past week')
st.write('''
Each topic is represented by a <a href="http://amueller.github.io/word_cloud/" target="_blank">**word cloud**</a> that displays the most representative words forming it.''', unsafe_allow_html=True)

st.markdown("""---""")

df = create_df()

#group df by topic, group by the sum of values in "count" column for each topic, add the "representative_words" and "representative_articles" columns, and sort by the sum of values in descending order, Keep the topic column as a column instead of an index
top_20 = get_top_20(df)

#for each row in the dataframe, create a wordcloud
for index, row in top_20.iterrows():
    text = ', '.join(row['representative_words'])
    # Create and generate a word cloud image:
    wordcloud = WordCloud().generate(text)
    st.markdown(f"### *Topic:* {row['topic']}".title())
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    fig = plt.gcf()
    st.pyplot(fig)
    with st.expander("**Expand to see the words in this topic**"):
        st.write(text)
