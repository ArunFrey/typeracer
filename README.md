# Typeracer app: App that lets you plot, analyse, and monitor your progress on typeracer.com

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://arunfrey-typeracer-app-siw3aw.streamlitapp.com/)

This app allows you to visualise textracer data of any player, and monitor your progress in typing speed! Once you input a username, it will download the user's race history from https://typeracerdata.com, or load the data from disk if it already exists.

The app allows you to monitor your progress over time, analyse what components of a text you are struggling with, and compare your performance to that of other players.

You can launch the app by clicking [here](https://arunfrey-typeracer-app-siw3aw.streamlitapp.com/).

Alternatively, you can follow the steps below to install the repo, download user or text data, and run the app locally.

![](img/example.gif)

## Installation: 

```
pip install -r requirements.txt
```

## Download data: 

### Download user data: 
To download user data, run: 
```
python3 -m get_races -u abnf
```

You can also download only a specific number of last races. E.g. to download the last 100 races, run: 
```
python3 -m get_races -u abnf -lr 100
```

### Download text data: 
To download text data, run: 
```
python3 -m get_texts 
```

Instead of downloading the full texts, you can also download the abbreviated texts by running: 
```
python3 -m get_texts --no-feature 
```

### Run this app locally

To run this app locally, run:

```
pip install --upgrade streamlit
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/main/streamlit_app.py
```
