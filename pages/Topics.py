import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils.utils import add_logo, create_df, get_top_20, REQUEST_URL

# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch_logo.png', use_column_width=True)
add_logo()

st.title("Top Topics of the Week")
st.markdown('''
Explore the top 20 topics of the week.\n
Each topic is a wordcloud that shows the most representative words in it.
''')

df = create_df()

#group df by topic, group by the sum of values in "count" column for each topic, add the "representative_words" and "representative_articles" columns, and sort by the sum of values in descending order, Keep the topic column as a column instead of an index
top_20 = get_top_20(df)

#for each row in the dataframe, create a wordcloud
for index, row in top_20.iterrows():
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
