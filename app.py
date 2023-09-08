import streamlit as st
import requests
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

st.markdown('# News Cycle Aggregator')

#url = 'https://url-to-api.com'
#df = requests.get(url).json()

# Temporarily reading data from file
df = pd.read_json("data.json", orient='table')

# Initialize number of topics
n_topics = 0



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
                       stackgroup='one',
                       groupnorm='percent')
            )
    fig.update_layout(showlegend=True,
                      xaxis_type='category',
                      yaxis=dict(type='linear', range=[1, 100],
                                 ticksuffix='%'))
    return fig

with st.form("submit_form"):
    slider_val = st.slider('Select a number of topics', 1, len(df), 10)

    submitted = st.form_submit_button("Submit")
    if submitted:
        n_topics = slider_val
        df = update_df(df, n_topics)
        # Get x, y and labels
        x = df.columns.values.tolist()
        y = df.values.tolist()
        labels = df.index.get_level_values('Name').tolist()
        fig = create_figure(x, y, labels)
        st.plotly_chart(fig, use_container_width=True)
