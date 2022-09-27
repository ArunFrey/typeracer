from bs4 import BeautifulSoup
import requests
import pandas as pd 
import logging


def get_raw_texts(full_text = True): 
    
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
    

    
    df.columns = [c.lower().replace(" ", "_") for c in df.columns.str.strip(".")]
    
    # change column types
    df = df.convert_dtypes()
    df['race'] = pd.to_numeric(df['race']).astype("int")
    df["date"] = pd.to_datetime(df["date"])
    df["wpm"] = pd.to_numeric(df["wpm"])
    df['acc'] = pd.to_numeric(df['acc.'].str.strip("%"))/100
    df['points'] = pd.to_numeric(df['points']).astype("int")
    



def format_data(df): 
    
    df.columns = [c.lower().replace(" ", "_") for c in df.columns.str.strip(".")]

    # change column types
    df = df.convert_dtypes()
    
    # format columns
    for c in df: 
        
        # add new column 
        if c == "top_score": 
                df["top_score_user"] = df[c].str.extract("\((.*)\)")
                df[c] = [l[0] for l in df[c].str.split(" —")]

        # convert percentage to number
        if c in ["acc"]: 
            df[c] = pd.to_numeric(df[c].str.replace("%", "", regex = True))/100
            continue

        # get rid of number formatting for other numeric variables
        if c in ['id', 'races', 'top_score', "race"]: 
            df[c] = df[c].str.replace("#|,|\.$", "", regex = True)
        
        # try and convert to numbers
        try: 
            df[c] = pd.to_numeric(df[c])
        except: 
            print(f"Column {c} cannot be converted to numeric")
        
    return df

df = get_raw_texts()

df2 = format_data(df)