from get_races import get_raw_races
from get_texts import get_raw_texts
from helpers import format_data

from plotly.subplots import make_subplots

import logging
import argparse
import numpy as np
import pandas as pd
import plotly.io as pio
import plotly.express as px

pio.templates.default = "plotly_white"


def plot_wpm_over_time(username, rolling_avg=50):
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
        logging.warning(
            f"User data for {username} not yet available. Downloading now..."
        )
        df = get_raw_races(username)
        df = format_data(df)

    fig = px.scatter(
        df,
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

    fig.write_image(f"plots/{username}_wpm-time.png", width=1200, height=600, scale = 1)

    return fig


def plot_hist(username, min_races=100):
    """Plots a histogram of average text speed, and adds vlines for user performance (avg, last 10m, max)

    Args:
        username (str): Username of user for which plot should be created
        min_races (int, optional): Cutoff for including only races with at least x amount of races. Defaults to 100.

    Returns:
        Plotly plot
    """

    # get user data
    try:
        df = pd.read_csv(f"data/races_{username}.csv")
    except:
        logging.warning(
            f"User data for {username} not yet available. Downloading now..."
        )
        df = get_raw_races(username)
        df = format_data(df)

    # get text data
    try:
        texts = pd.read_csv(f"data/texts.csv")
        texts_abbrev = pd.read_csv(f"data/texts_abbrev.csv")
    except:
        logging.error(f"Text data not yet available. Needs to be downloaded first")

    # select races with at least min_races
    texts = texts[texts["races"] >= min_races]

    fig = px.histogram(
        texts,
        x="average",
        opacity=0.8,
        labels={
            "average": "Average performance across races",
        },
    )

    fig.add_vline(
        x=np.mean(df["wpm"]),
        line_dash="dash",
        annotation_text=f"Avg: {int(np.mean(df['wpm']))}",
    )

    fig.add_vline(
        x=np.mean(df["wpm"][0:20]),
        line_dash="dot",
        annotation_text=f"Last 10: {int(np.mean(df['wpm'][0:10]))}",
    )

    fig.add_vline(
        x=np.max(df["wpm"]),
        line_dash="longdash",
        annotation_text=f"Max: {int(np.max(df['wpm']))}",
    )

    fig.write_image(f"plots/{username}_hist.png", width=1000, height=700, scale = 1)

    return fig


def main():

    parser = argparse.ArgumentParser(description="Plotting data for typeracer user.")
    parser.add_argument(
        "-u",
        "--user_name",
        type=str,
        required=True,
        help="Enter the username of the user whose data you want to plot.",
    )
    args = parser.parse_args()

    fig = make_subplots(rows=1, cols=2)

    figures = [plot_wpm_over_time(args.user_name), plot_hist(args.user_name)]

    fig = make_subplots(rows=len(figures), cols=1)

    for i, figure in enumerate(figures):
        for trace in range(len(figure["data"])):
            fig.append_trace(figure["data"][trace], row=i + 1, col=1)

    return fig.show()


if __name__ == "__main__":
    main()
