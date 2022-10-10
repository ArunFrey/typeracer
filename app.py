from visualizer import plot_wpm_over_time, plot_hist, plot_facetted_residuals
from get_races import get_raw_races
from helpers import format_data

import streamlit as st 
import pandas as pd 


username = st.text_input('Input user name:',placeholder="Add user name here")

if username is not None: 
    try: 
        user = pd.read_csv(f'data/races_{username}.csv')
    except: 
        st.spinner("User data not available. Downloading now...")
        try: 
            user = get_raw_races(username)
            user = format_data(user)
        except: 
            st.write(f"User {username} does not exist.")
        
texts = pd.read_csv('data/texts.csv')
texts_abbrev = pd.read_csv('data/texts_abbrev.csv')

fig1 = plot_wpm_over_time(user)
fig2 = plot_facetted_residuals(user, texts, texts_abbrev)
fig3 = plot_hist(user, texts)

st.plotly_chart(fig1, use_container_width=True)
st.plotly_chart(fig2, use_container_width=True)
st.plotly_chart(fig3, use_container_width=True)

