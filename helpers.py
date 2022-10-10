from curses.ascii import isupper
import string
import pandas as pd
import numpy as np 

from sklearn.linear_model import LinearRegression
from plotly.subplots import make_subplots


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
            df["race_rank"] = df[c].str.extract("\((\d) of \d\)").astype("int")
            continue

        # convert percentage to number
        if c in ["acc"]:
            df[c] = pd.to_numeric(df[c].str.replace("%", "", regex=True)) / 100
            continue

        # get rid of number formatting for other numeric variables
        if c in ["id", "races", "top_score", "race"]:
            df[c] = df[c].str.replace("#|,|\.$", "", regex=True)

        if c in ["date", "active_since"]:
            df[c] = pd.to_datetime(df[c])

        else:
            # convert other columns to numbers
            try:
                df[c] = pd.to_numeric(df[c])
            except:
                print(f"Column {c} cannot be converted to numeric")

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
    
    count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))
    
    # add punctuation, letter, and capitalization count
    df['letters'] =  [count(words, string.ascii_letters) for words in df['text']]
    df['punct'] = [count(words, string.punctuation) for words in df['text']]
    df['punct_rate'] = df['punct']/df['length']
    df['cap'] = [sum(1 for c in words if c.isupper()) for words in df['text']]
    df['cap_rate'] = df['cap']/df['length']

    # control for linear progression, and save residual
    X = np.array(df['race']).reshape((-1, 1))
    y = np.array(df['wpm'])
    reg = LinearRegression().fit(X, y)
    df['pred'] = reg.predict(X)
    df['res'] = (y - df['pred'])
    
    return df
