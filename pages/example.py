import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# add a sidebar with an About section that explains the app
st.sidebar.info('''
NewsWatch is a prototype of a news cycle aggregator. It uses a topic modeling algorithm to extract topics from news articles and then visualizes the results in a streamgraph. The app is built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).
''')
# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch_logo.png', use_column_width=True)

# Create some sample text
text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

# Create and generate a word cloud image:
wordcloud = WordCloud().generate(text)

# Display the generated image:
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()
fig = plt.gcf()
st.pyplot(fig)
