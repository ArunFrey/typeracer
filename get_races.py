from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 

def get_raw_data(username, last_races = 99999999): 
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


def format_data(df): 
    """Formats the raw data received from typeracerdata.com

    Args:
        df (pd.DataFrame): Dataframe of raw typeracer data.

    Returns:
        pd.DataFrame: A dataframe where are variables are formatted. 
    """
    
    df.columns = [c.lower() for c in df.columns.str.strip(".")]
    
    # change column types
    df = df.convert_dtypes()
    df['race'] = pd.to_numeric(df['race']).astype("int")
    df["date"] = pd.to_datetime(df["date"])
    df["wpm"] = pd.to_numeric(df["wpm"])
    df['acc'] = pd.to_numeric(df['acc.'].str.strip("%"))/100
    df['points'] = pd.to_numeric(df['points']).astype("int")
    
    return df
