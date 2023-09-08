import streamlit as st
import requests

import numpy as np
import pandas as pd

st.markdown('# News Cycle Aggregator')
## This is a sub header

#url = 'https://blabla'
#df = requests.get(url).json()

df = pd.DataFrame({
    'first column': list(range(1, 11)),
    'second column': np.arange(10, 101, 10)
})

# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider
line_count = st.slider('Select a line count', 1, 10, 3)

# and used to select the displayed lines
head_df = df.head(line_count)

head_df
