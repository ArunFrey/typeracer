from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd 
import argparse

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


def main():
    
    """Main function to be executed directly from terminal
    """

    parser = argparse.ArgumentParser(
        description='Getting text data from typeracer.')
    
    # TODO: add parser and text functions

if __name__ == "__main__":
    main()