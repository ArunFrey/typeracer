# Typeracer: Analyse and plot user & text data

This app allows you to visualise textracer data of any player, and monitor your progress in typing speed! Once you input a username, it will download the user's race history from https://typeracerdata.com, or load the data from disk if it already exists.

The app allows you to monitor your progress over time, analyse what components of a text you are struggling with, and compare your performance to that of other players.

You can launch the app here: 

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://arunfrey-typeracer-app-siw3aw.streamlitapp.com/)


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


## Plot data

To generate user plots, run: 
```
python3 -m visualizer -u abnf
```
This will generate a **scatter plot** of the words-per-minute for user abnf across all races, as well as a histogram comparing the user's performance to the average speed across all texts. 



