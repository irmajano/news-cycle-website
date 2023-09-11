import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

MAX_TOPICS = 20
REQUEST_URL = 'https://news-cycle-aggregator-fudwhg6x5q-ew.a.run.app/get-processed'

st.set_page_config(layout="wide")

st.markdown('# News Cycle Aggregator')

# Temporarily reading data from file
#df = pd.read_json("data.json", orient='table')

# Initialize number of topics
slider_val = 5

def process_request(r):
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

def create_figure(x, y, labels):
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
                       hoveron='fills',
                       showlegend=True)
            )
    fig.update_layout(
        showlegend=True,
        xaxis_type='category',
        yaxis=dict(type='linear', range=[1, 100],
                    ticksuffix='%'),
        title=f'Top {slider_val} topics between {x[0]} and {x[-1]}'
        )
    fig.update_xaxes(tickangle=45)
    return fig

r = requests.get(REQUEST_URL).json()
df = process_request(r)

with st.form("submit_form"):
    slider_val = st.slider('Select a number of topics', 1, MAX_TOPICS, 5)

    submitted = st.form_submit_button("Submit")
    if submitted:
        n_topics = slider_val
        df = update_df(df, n_topics)
        # Get x, y and labels
        x = df.columns.values.tolist()
        y = df.values.tolist()
        labels = df.index.values.tolist()
        #labels = df.index.get_level_values('Name').tolist()
        fig = create_figure(x, y, labels)
        st.plotly_chart(fig, use_container_width=True, theme="streamlit", sharing="streamlit")
