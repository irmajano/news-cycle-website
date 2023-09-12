import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

MAX_TOPICS = 20
REQUEST_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-processed'

st.set_page_config(layout="wide")

st.title("NewsWatch")

# change page names in the sidebar to "About" and "Sources"


#st.title("NewsWatch Aggregator")

# display the title "NewsWatch Aggregator" using Righteous Regular font
#st.markdown("<h1 style='text-align: center; color: #000000; font-size: 50px; font-family: Righteous, sans-serif;'>NewsWatch Aggregator</h1>", unsafe_allow_html=True)

# Temporarily reading data from file
#df = pd.read_json("data.json", orient='table')

# Initialize number of topics
slider_val = 5

def process_request():
    r = requests.get(REQUEST_URL).json()
    df = pd.read_json(r)
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

def update_df(df, n_topics):
    # Select first n topics
    df = df.iloc[:n_topics, :]
    # Convert document counts to percentages
    df = df.apply(lambda x: x / x.sum(), axis=0).fillna(0)
    return df

def create_figure(df):
    x = df.columns.values.tolist()
    y = df.values.tolist()
    labels = df.index.values.tolist()
    fig = go.Figure()
    for y_, label in zip(y, labels):
        fig.add_trace(
            go.Scatter(x=x,
                       y=y_,
                       name=label,
                       mode='lines',
                       line=dict(width=0.5),
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
        title_text=f'Top {slider_val} topics between {x[0]} and {x[-1]}',
        title_x=0.3,
        title_font_size=20,
        hovermode='x unified'
    )
    fig.update_xaxes(tickangle=45) #rotate x-axis labels
    return fig

df = process_request()

with st.form("submit_form"):
    slider_val = st.slider('Select a number of topics', 1, MAX_TOPICS, 5)
    submitted = st.form_submit_button("Submit")
    if submitted:
        n_topics = slider_val
        df = update_df(df, n_topics)
        #labels = df.index.get_level_values('Name').tolist()
        fig = create_figure(df)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")

# add a sidebar with an About section that explains the app
#st.sidebar.markdown('## About')
st.sidebar.info('''
NewsWatch is a prototype of a news cycle aggregator. It uses a topic modeling algorithm to extract topics from news articles and then visualizes the results in a streamgraph. The app is built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/).
''')

# Place the logo at the bottom in the sidebar
st.sidebar.image('newswatch-high-resolution-color-logo.png', width=300)
