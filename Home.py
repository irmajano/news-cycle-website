import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
from utils.utils import add_logo, fetch_data, create_df, get_top_20
from random import shuffle

st.set_page_config(layout="wide", page_title='NewsWatch')

MAX_TOPICS = 20

submitted = False # Initialize Submit button state
slider_val = 5 # Initialize number of topics

with st.sidebar:
    with st.form(key='my_form'):
        st.info(':information_source: **Update the graph:** choose how many topics to display')
        #add info in bold

        slider_val = st.slider('Select number of topics to visualize', 1, MAX_TOPICS, 5)
        submitted = st.form_submit_button(label='Submit')

st.title("NewsWatch")
st.subheader("Visualize last week's trending topics in world news")
st.markdown("""
**NewsWatch** is a news aggregator that collects news from the past week and boils them down to <a href="/Topics" target="_self">20 topics</a> for you to visualize and consult.""", unsafe_allow_html=True)

add_logo()

@st.cache_data
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

df = create_df()
processed_df = process_request(df)
PROCESSED_DF = processed_df
num_documents = df['count'].sum()
# get the number of topics in PROCESSED_DF by grouping by the "topic" column and counting the number of groups
NUM_TOPICS = len(df.groupby('topic'))
FIRST_DAY = None
LAST_DAY = None

# Fetch data from the API
data = fetch_data()
num_sources = data.get("feed_count", 0)

@st.cache_data
def update_df(n_topics):
    # Select first n topics
    new_df = PROCESSED_DF.iloc[:n_topics, :]
    # Convert document counts to percentages
    new_df = new_df.apply(lambda x: x / x.sum() * 100, axis=0).fillna(0)
    #if today's date is found as a column in new_df, drop it
    if str(date.today()) in new_df.columns:
        new_df = new_df.drop(columns=[str(date.today())])
    #format values in new_df to 2 decimal places
    new_df = new_df.round(2)
    return new_df

st.markdown("""---""")

@st.cache_data
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
                       name=label.title(),
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
        title_text=f'Evolution of Top {slider_val} News Topics Last Week',
        title_x=0.3,
        title_font_size=20,
        hovermode='x unified',
        xaxis_title="Date",
        yaxis_title="Articles per topic"
    )
    fig.update_xaxes(tickangle=45) #rotate x-axis labels
    return fig

if submitted:
    n_topics = slider_val
    df = update_df(n_topics)
    fig = create_figure(df)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")
else:
    df = update_df(slider_val)
    fig = create_figure(df)
    st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")

st.markdown("""---""")

st.markdown(f"**NewsWatch** is currently based on:")
col1, col2, col3, col4, col5 = st.columns(5)
col2.metric("RSS Feeds", f"{'{:,}'.format(num_sources)}", help='Number of RSS feeds scraped')
col4.metric("News Articles", f"{'{:,}'.format(num_documents)}", help='Number of news articles analyzed')
