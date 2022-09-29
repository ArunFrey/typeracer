from get_races import get_raw_races
from get_texts import get_raw_texts
from helpers import format_data
from os.path import exists


import logging
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go
pio.templates.default = "plotly_white"

from string import punctuation

count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))


def plot_wpm_over_time(username, rolling_avg = 50):
    """Generates a plotly plot of words/minute over time

    Args:
        username (str): Username used for race data
        rolling_avg (int, optional): Number of races aggregated in rolling average. Defaults to 50.

    Returns:
        obj: plotly figure
    """
    try: 
        df = pd.read_csv(f"data/races_{username}.csv")
    except:
        logging.warning(f"User data for {username} not yet available. Downloading now...")
        df = get_raw_races(username)
        df = format_data(df)
    
    fig = px.scatter(
        df,
        x="race",
        y="wpm",
        color = 'acc',
        opacity=0.5,
        trendline="rolling",
        trendline_options=dict(window=rolling_avg),
        labels={
            "race": "Race",
            "wpm": "Words/Minute",
            "acc": "Accuracy",
        })
    
    fig.write_image(f"plots/{username}_wpm-time.pdf", width=600, height=350)
    
    return fig


def plot_hist(username, min_races = 100):
    
    # get user data
    try: 
        df = pd.read_csv(f"data/races_{username}.csv")
    except:
        logging.warning(f"User data for {username} not yet available. Downloading now...")
        df = get_raw_races(username)
        df = format_data(df)

    # get text data
    try: 
        texts = pd.read_csv(f"data/texts.csv")
        texts_abbrev = pd.read_csv(f"data/texts_abbrev.csv")
    except:
        logging.error(f"Text data not yet available. Needs to be downloaded first")
    
    # select races with at least min_races
    texts = texts[texts['races'] >= min_races]
    
    fig = px.histogram(texts, 
                       x = 'average',
                       opacity=0.8,
                       labels={
                        "average": "Average performance across races",
                        })

    fig.add_vline(x = np.mean(df['wpm']), 
                  line_dash = "dash",
                  annotation_text = int(np.mean(df['wpm'])))

    fig.add_vline(x = np.mean(df['wpm'][0:10]), 
                  line_dash = "dot",
                  annotation_text = int(np.mean(df['wpm'][0:10])))

    fig.add_vline(x = np.max(df['wpm']), 
                  line_dash = "longdash",
                  annotation_text = int(np.max(df['wpm'])))
    
    fig.write_image(f"plots/{username}_hist.pdf", width=300, height=350)
    
    return fig


def main(): 
    