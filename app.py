import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from random import shuffle

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

st.set_page_config(layout="wide", page_title='NewsWatch')

MAX_TOPICS = 20
REQUEST_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-processed'

submitted = False # Initialize Submit button state
slider_val = 5 # Initialize number of topics

with st.sidebar:
    with st.form(key='my_form'):
        slider_val = st.slider('Select number of top news topics to visualize', 1, MAX_TOPICS, 5)
        submitted = st.form_submit_button(label='Submit')

st.title("NewsWatch")
st.subheader("Visualize last week's trending topics in world news")
st.markdown(f"""
**NewsWatch** is a news aggregator that collects news from last week from a wide range of RSS feeds and displays them in a single place.\n
The app uses a topic modeling algorithm to extract topics from news articles and then visualizes the results in a streamgraph.
""")

add_logo()

@st.cache
def process_request(df):
    df['date'] = pd.to_datetime(df['date']).dt.date #add column with only date, without time
    new_df = pd.DataFrame()
    for topic in df.groupby('topic'):
        for day in topic[1].groupby('date'):
            # Sum the values in "count" column for each day
            new_df.loc[topic[0], str(day[0])] = day[1]['count'].sum()
    #Sort new_df by the sum of values in each row
    new_df['sum'] = new_df.sum(axis=1)
    new_df = new_df.sort_values(by=['sum'], ascending=False).drop(columns=['sum'])
    new_df.sort_index(inplace = True, axis=1)
    return new_df

r = requests.get(REQUEST_URL).json()
df = pd.read_json(r)
#drop rows with empty topic column
df = df[df['topic'].str.len() > 1]
#drop rows with nan values in topic column
df = df.dropna(subset=['topic'])

#group df by topic and remove rows with only one date
df = df.groupby('topic').filter(lambda x: len(x) > 1)
#remove rows with less than 10 in count column
df = df[df['count'] > 10]

#group df by topic, group by the sum of values in "count" column for each topic, add the "representative_words" and "representative_articles" columns, and sort by the sum of values in descending order, Keep the topic column as a column instead of an index
top_20 = df.groupby('topic').agg({'count': 'sum', 'representative_words': 'first', 'representative_articles': 'first'}).sort_values(by=['count'], ascending=False).reset_index()
TOP_20_TOPICS = top_20.head(MAX_TOPICS)

PROCESSED_DF = process_request(df)
NUM_DOCUMENTS = df['count'].sum()
# get the number of topics in PROCESSED_DF by grouping by the "topic" column and counting the number of groups
NUM_TOPICS = len(df.groupby('topic'))
FIRST_DAY = None
LAST_DAY = None
from pages.Sources import NUM_SOURCES


st.markdown(f"**NewsWatch** is currently based on:")
col1, col2, col3 = st.columns(3)
col1.metric("RSS Feeds", f"{'{:,}'.format(NUM_SOURCES)}", help='Number of RSS feeds scraped')
col2.metric("News Articles", f"{'{:,}'.format(NUM_DOCUMENTS)}", help='Number of news articles analyzed')
col3.metric("Topics Extracted", f"{'{:,}'.format(NUM_TOPICS)}", help='Number of topics automatically extracted from the news articles')

@st.cache
def update_df(n_topics):
    # Select first n topics
    new_df = PROCESSED_DF.iloc[:n_topics, :]
    # Convert document counts to percentages
    new_df = new_df.apply(lambda x: x / x.sum(), axis=0).fillna(0)
    new_df = new_df.drop(columns=[str(date.today())])
    return new_df

@st.cache
def create_figure(df):
    x = df.columns.values.tolist()
    y = df.values.tolist()
    labels = df.index.values.tolist()
    FIRST_DAY = x[0]
    LAST_DAY = x[-1]
    fig = go.Figure()
    num_colors = len(y)
    colors = [f'hsl({i * 360 // num_colors}, 100%, 50%)' for i in range(num_colors)]
    shuffle(colors)
    for y_, label, color in zip(y, labels, colors):
        fig.add_trace(
            go.Scatter(x=x,
                       y=y_,
                       name=label,
                       mode='lines',
                       line=dict(width=0.5, color=color),
                       line_shape='spline',
                       stackgroup='one',
                       groupnorm='percent',
                       hoveron='fills+points',
                       showlegend=True)
            )
    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(type='linear', range=[1, 100], ticksuffix='%'),
        title_text=f'Last week in topics',
        title_x=0.3,
        title_font_size=20,
        hovermode='x unified',
        xaxis_title="Date",
        yaxis_title="Articles per topic"
    )
    fig.update_xaxes(tickangle=45) #rotate x-axis labels
    return fig

# Create a function to update the information panel based on the hovered legend label
def update_info_panel(fig):
    while True:
        event = st.pydeck_chart(fig)
        if event:
            label = event["label"]
            # Here, you can fetch and display additional information related to the hovered legend label
            additional_info = f"Additional Info for {label}"  # Replace with your logic to fetch information
            info_panel.text(additional_info)

update_info_panel(fig)  # Start listening for hover events

if submitted:
    n_topics = slider_val
    df = update_df(n_topics)
    fig = create_figure(df)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")
else:
    df = update_df(slider_val)
    fig = create_figure(df)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")
