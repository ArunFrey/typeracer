from helpers import combine_text_and_races

from plotly.subplots import make_subplots

import numpy as np
import plotly.io as pio
import plotly.express as px

pio.templates.default = "plotly_white"


def plot_wpm_over_time(user, rolling_avg=50):

    fig = px.scatter(
        user,
        x="race",
        y="wpm",
        color="acc",
        opacity=0.5,
        trendline="rolling",
        trendline_options=dict(window=rolling_avg),
        labels={
            "race": "Race",
            "wpm": "Words/Minute",
            "acc": "Accuracy",
        },
    )

    return fig


def plot_hist(user, texts, min_races=100):

    # select races with at least min_races
    texts = texts[texts["races"] >= min_races]

    fig = px.histogram(
        texts,
        x="average",
        histnorm='probability',
        color_discrete_sequence=["rgb(255, 127, 14)"],
        labels={
            "average": "Average performance across races",
        },
    )

    fig.add_vline(
        x=np.mean(user["wpm"]),
        line_dash="dash",
    )

    fig.add_vline(
        x=np.mean(user["wpm"][0:20]),
        line_dash="dot",
    )

    fig.add_vline(
        x=np.max(user["wpm"]),
        line_dash="longdash",
    )

    return fig


def plot_facetted_residuals(user,
                           texts,
                           texts_abbrev, 
                           y = 'res', 
                           vars = ['punct_rate', 'cap_rate', 'difficulty_rating', 'length'], 
                           vars_labels = ['Punctuation rate', 'Capitalization rate', 'Difficulty', 'Length'], 
                           n_cols = 2):

    # format data
    df = combine_text_and_races(user, texts, texts_abbrev)    
        
    # plot data    
    n_rows = -(-len(vars) // n_cols) 
    
    row_pos, col_pos = 1, 0
    
    fig = make_subplots(rows=n_rows, 
                        cols=n_cols,
                        subplot_titles=vars_labels)

    for v in vars:
        # trace extracted from the fig
        trace = px.scatter(df, 
                           x=v, 
                           y=y, 
                           color = 'acc',
                           opacity = 0.5,
                           trendline='lowess', 
                           labels = {"acc": "Accuracy"},
                           trendline_color_override='#DC143C')["data"]
        
        # auto selecting a position of the grid
        if col_pos == n_cols: row_pos += 1
        col_pos = col_pos + 1 if (col_pos < n_cols) else 1
        # adding trace to the grid
        fig.add_trace(trace[0], row=row_pos, col=col_pos)
        fig.add_trace(trace[1], row=row_pos, col=col_pos)
        
    return fig