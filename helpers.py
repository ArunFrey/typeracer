import string
import re

import pandas as pd
import numpy as np

from sklearn.svm import SVR
from curses.ascii import isupper


def format_data(df):
    """Formats raw data received from typeracer.com

    Args:
        df (object): Dataframe object with typeracer data.

    Returns:
        pd.DataFrame: Cleaned dataframe.
    """

    df.columns = [c.lower().replace(" ", "_") for c in df.columns.str.strip(".")]

    # change column types
    df = df.convert_dtypes()

    # format columns
    for c in df:

        # add new column for top scorer
        if c == "top_score":
            df["top_score_user"] = df[c].str.extract("\((.*)\)")
            df[c] = [l[0] for l in df[c].str.split(" —")]

        # add new column for race rank
        if c == "outcome":
            df["race_rank"] = df[c].str.extract("\((\d+) of \d+\)").astype("int")
            continue

        # convert percentage to number
        if c in ["acc"]:
            df[c] = df[c].str.replace("%|—", "", regex=True)
            df[c] = pd.to_numeric(df[c]) / 100
            continue

        # get rid of number formatting for other numeric variables
        if c in ["id", "races", "top_score", "race", "points"]:
            df[c] = df[c].str.replace("#|—|,|\.$", "", regex=True)

        if c in ["date", "active_since"]:
            df[c] = pd.to_datetime(df[c])

        else:
            # convert other columns to numbers
            try:
                df[c] = pd.to_numeric(df[c])
            except:
                print(f"Column {c} cannot be converted to numeric")

    # drop early race data, where no accuracy or point metrics existed
    df.dropna(inplace=True)

    return df


def combine_text_and_races(df, texts, texts_abbrev):
    """Merges user and text data

    Args:
        df (pd.DataFrame): User data
        texts (pd.DataFrame): Text data
        texts_abbrev (pd.DataFrame): Text data (abbreviated)

    Returns:
        pd.DataFrame: Merged dataframe
    """

    # merge data
    df = pd.merge(df, texts_abbrev[["id", "text"]], on="text", how="left")
    df = df.rename(columns={"text": "text_abbrev"})
    df = pd.merge(df, texts, on="id", how="left")

    p = re.compile("[" + re.escape(string.punctuation) + "]")

    # add punctuation, letter, and capitalization count
    df["punct"] = df["text"].str.count(p)
    df["letters"] = df["text"].str.count("\w")
    df["punct_rate"] = df["punct"] / df["length"]
    df["cap"] = df["text"].str.count("[A-Z]")
    df["cap_rate"] = df["cap"] / df["length"]

    # control for progression, and save residual
    X = np.array(df["race"]).reshape((-1, 1))
    y = np.array(df["wpm"])

    svr_rbf = SVR(kernel="rbf")

    reg = svr_rbf.fit(X, y)
    df["pred"] = reg.predict(X)
    df["res"] = y - df["pred"]

    return df
