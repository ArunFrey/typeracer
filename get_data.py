from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
import numpy as np

def get_raw_races(username, last_races = 99999999): 
    """Downloads a user's typeracer data from typeracerdata.com
    

    Args:
        username (str): Username used for typeracer.
        last_races (int, optional): Number of last races to retrieve. Defaults to 99999999

    Returns:
        pd.DataFrame: A dataframe containing a user's race data. 
    """

    # get parsed data
    r = requests.get(f"http://www.typeracerdata.com/profile?username={username}&last={last_races}")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    
    # extract data from tables
    tables = soup.find_all('table')
    table = tables[2]
    columns = [header.text for header in table.find_all("th")]
    
    race_data = list()
    for row in table.find_all("tr"): 
        content = list()
        for column in row.find_all("td"): 
            if len(column) > 0:
                content.append(column.text)
        if len(content) > 0:
            race_data.append(content)

    df = pd.DataFrame(race_data, columns = columns)
    
    return df


def get_raw_texts(full_text = True): 
    """Downloads all texts available on typeracer.com
    
    Args:
        full_text (bool): Denotes whether or not to download full_text, or first 63 characters. Defaults to True.

    Returns:
        pd.DataFrame: A dataframe containing all text data. 
    """

    
    if full_text: 
        text_content = "texts=full"
    else: 
        text_content = ""
        
    r = requests.get(f"http://www.typeracerdata.com/texts?{text_content}&sort=id")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table")
    
    columns = [column.text for column in table.find_all("th")]
    
    text_data = list()
    for row in table.find_all("tr"): 
        content = list()
        for column in row.find_all("td"): 
            if len(column) > 0:
                content.append(column.text)
        if len(content) > 0:
            text_data.append(content)
        
    df = pd.DataFrame(text_data, columns=columns)
    
    return df


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
            df['race_rank'] = df[c].str.extract("\((\d) of \d\)").astype('int')
            continue
        
        # convert percentage to number
        if c in ["acc"]: 
            df[c] = pd.to_numeric(df[c].str.replace("%", "", regex = True))/100
            continue

        # get rid of number formatting for other numeric variables
        if c in ['id', 'races', 'top_score', "race"]: 
            df[c] = df[c].str.replace("#|,|\.$", "", regex = True)
        
        if c in ['date', 'active_since']: 
            df[c] = pd.to_datetime(df[c])
        
        else:
            # convert other columns to numbers
            try: 
                df[c] = pd.to_numeric(df[c])
            except: 
                print(f"Column {c} cannot be converted to numeric")
        
    return df