from helpers import combine_text_and_races

from plotly.subplots import make_subplots

import numpy as np
import plotly.express as px


def plot_wpm_over_time(user, rolling_avg=10):

    fig = px.scatter(
        user,
        x="race",
        y="wpm",
        color="acc",
        opacity=0.7,
        trendline="rolling",
        trendline_options=dict(window=rolling_avg),
        labels={
            "race": "Race",
            "wpm": "Words/Minute",
            "acc": "Accuracy",
        },
    )
    
    fig.update_traces(
        marker_line_width=0, 
        )
    fig.update_traces(
        line_width=1, 
        line_color = 'black', 
        )

    return fig


def plot_wins(user): 
    
    user['win'] = user['race_rank'] == 1
    user['cum_win'] = user.sort_values('race')['win'].cumsum()
    user['cum_50_win'] = user.sort_values('race')['win'].rolling(50).sum()
    user['% of total'] = user['cum_win'] / user['race']
    user['% of last 50'] = user['cum_50_win'] / 50
    
    user = user[['race', '% of total', '% of last 50']].melt(id_vars='race')
    
    fig = px.line(
        user, 
        x = 'race', 
        y = 'value',
        color = 'variable',
        labels={
            "race": "Race",
            "value": "Share of races won",
            "variable": ""
        },
        color_discrete_sequence = ["#7201a8", "#fb9f3a"]
        )
    
    fig.update_traces(
        line_width=3, 
        )
    
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
    ))
    
    return fig


    
def plot_hist(user, texts, min_races=100):

    # select races with at least min_races
    texts = texts[texts["races"] >= min_races]

    fig = px.histogram(
        texts,
        x="average",
        histnorm='probability',
        color_discrete_sequence=["#d33682"],
        labels={
            "average": "Mean performance across all texts",
        },
    )

    fig.add_vline(
        x=np.mean(user["wpm"]),
        line_dash="dash",
        line_color="white",
        annotation_text="Avg.", 
        annotation_position="top left",
    )

    fig.add_vline(
        x=np.mean(user["wpm"][0:51]),
        line_dash="dot",
        line_color="white",
        annotation_text="Last 50", 
        annotation_position="top right",
    )

    fig.add_vline(
        x=np.max(user["wpm"]),
        line_dash="longdash",
        line_color="white",
        annotation_text="Top", 
        annotation_position="top right",
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
                           opacity = 0.4,
                           trendline='lowess', 
                           labels = {"acc": "Accuracy"},
                           trendline_color_override='#DC143C')["data"]        
        # auto selecting a position of the grid
        if col_pos == n_cols: row_pos += 1
        col_pos = col_pos + 1 if (col_pos < n_cols) else 1
        # adding trace to the grid
        fig.add_trace(trace[0], row=row_pos, col=col_pos)
        fig.add_trace(trace[1], row=row_pos, col=col_pos)

    fig.update_traces(marker_line_width=1, marker_size=7)
    fig.update_traces(line_width=3, line_color = 'black')

    return fig