from visualizer import plot_wins, plot_wpm_over_time, plot_hist, plot_facetted_residuals
from get_races import get_raw_races
from get_texts import get_raw_texts
from helpers import format_data

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Typeracer analysis",
    page_icon="img/icon-racer.ico",
    layout="centered",
    initial_sidebar_state="auto",
)

st.title("Visualizing typeracer data")

st.markdown(
    """
         This app allows you to visualise typeracer data of any player, and monitor your progress in typing speed!
         Once you input a username, it will download the user's race history 
         from https://typeracerdata.com, or load the data from disk if it already exists. 

        The app allows you to monitor your progress over time, 
        analyse what components of a text you are struggling with, 
        and compare your performance to that of other players.
        
        The app was created by me, [Arun Frey](https://arunfrey.github.io). You can view the source code [here](https://github.com/arunfrey/typeracer).
        
         """
)


username = st.text_input(
    "Type in a user name to generate user analytics",
    value="abnf",
    placeholder="Add user name here",
)


if username is not None:
    try:
        user = pd.read_csv(f"data/races_{username}.csv")
    except:
        st.spinner("User data not available. Downloading now...")
        try:
            user = get_raw_races(username)
            user = format_data(user)
            user.to_csv(f"data/races_{username}.csv")
        except:
            st.write(f"User {username} does not exist.")

    try:
        texts = pd.read_csv("data/texts.csv")
        texts_abbrev = pd.read_csv("data/texts_abbrev.csv")
    except:
        st.spinner("Text data not available. Downloading now...")
        texts = get_raw_texts()
        texts = format_data(texts)
        texts_abbrev = get_raw_texts(full_text=False)
        texts_abbrev = format_data(texts_abbrev)

tab1, tab2, tab3 = st.tabs(["WPM Improvement", "Text analysis", "Relative performance"])


with tab1:
    st.header("Improvement in WPM over time")
    st.markdown(
        f"""
            This plot visualises the words-per-minute (WPM) across all of **{username}**'s typeracer races. 
            Each point indicates the wpm at one particular race, while the black trendline 
            visualises your progress using a 10-race rolling average. 
            The color of each point denotes the accuracy of a particular race. 

            An increase in WPM across races suggests that your typing speed is improving (yay!). 
            """
    )
    fig1a = plot_wpm_over_time(user)
    st.plotly_chart(fig1a, use_container_width=True)
    st.header("Chance of winning a race")
    st.markdown(
        f"""
            Below you'll see the probability of winning a race over time.
            One line ("% of total") shows how your chance of winning a race has changed over time, over all races. 
            The other line ("% of last 50") visualises the percentage of your last 50 races that you've won. 
            """
    )
    fig1b = plot_wins(user)
    st.plotly_chart(fig1b, use_container_width=True)

with tab2:
    st.header("Analysing residual performance")
    st.markdown(
        f"""
               These plots help you understand what text features you are struggling with the most.
               To do this, I plot the residuals from a simple SVR kernel model that only takes races as an input
               against various text features, including a text's **Punctuation rate** (the share of punctuations in a given text), 
               **Capitalization rate** (the share of letters in a given text that are capitalized), 
               **Difficulty rating** (the overall difficulty rating given to the text by typeracer.com), and **Length** (a text's length).
               The color of each point denotes the accuracy of a particular race. 
               
               A negative correlation between residual scores and Punctuation rate, for example, suggests that you tend 
               to perform worse as the share of punctuations in a text increases.
               """
    )
    fig2 = plot_facetted_residuals(user, texts, texts_abbrev)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Comparing your performance to average race times")
    st.markdown(
        f"""
               The histogram visualises the average race speed across all typeracer texts, to benchmark your performance to other race times.
               
               Each line displayes your average performance, your performance on the last 50 races, and your best race time.
               """
    )

    fig3 = plot_hist(user, texts)
    st.plotly_chart(fig3, use_container_width=True)
