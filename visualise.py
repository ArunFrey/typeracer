from string import punctuation
from get_data import get_raw_races, get_raw_texts, format_data

import pandas as pd
import plotly.io as pio
import plotly.express as px
import plotly.graph_objs as go

pio.templates.default = "plotly_white"

count = lambda l1, l2: len(list(filter(lambda c: c in l2, l1)))

# download race data
df = get_raw_races("abnf")
df = format_data(df)

# download text data
texts = get_raw_texts()
texts_abbrev = get_raw_texts(full_text=False)
texts = format_data(texts)
texts_abbrev = format_data(texts_abbrev)

# merge race and text data
df = pd.merge(df, texts_abbrev[["id", "text"]], on="text", how="left")
df = df.rename(columns={"text": "text_abbrev"})
df = pd.merge(df, texts, on="id", how="left")

# Generate new variables
df = df.assign(
    # last 100 races
    last_100=df["race"] >= max(df["race"] - 100),
    # won
    won=df["race_rank"] == 1,
    # relative performance
    rel_performance=df["wpm"] - df["average"],
    # punctuation count
    punctuation=[count(word, punctuation) for word in df["text"]],
)

# progression of wpm over time
fig = px.scatter(
    df,
    x="race",
    y="wpm",
    opacity=0.5,
    trendline="rolling",
    trendline_options=dict(window=50),
    labels={
        "race": "Race",
        "wpm": "Words/Minute",
    },
)

fig2 = px.bar(
    df,
    x="race",
    y="rel_performance",
    color=df["rel_performance"] >= 0,
    labels={
        "rel_performance": "Relative performance",
        "race": "Race",
    },
)
fig2.update_layout(bargap=0)
fig2.add_hline(y=0, line_width=1, line_dash="dash", line_color="black")
fig2.update_layout(showlegend=False)