from bs4 import BeautifulSoup
import requests
import pandas as pd
import argparse
from os.path import exists
from helpers import format_data


def get_raw_texts(full_text=True):
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

    url = f"http://www.typeracerdata.com/texts?{text_content}&sort=id"
    r = requests.get(url)
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

    """Main function to be executed directly from terminal"""

    parser = argparse.ArgumentParser(description="Getting text data from typeracer.")
    parser.add_argument(
        "--feature",
        action=argparse.BooleanOptionalAction,
        help="Specify whether to return full or abbreviated texts. Defaults to full.",
        required=False,
    )
    args = parser.parse_args()

    # get data
    if args.feature is not None:
        filepath = "data/texts_abbrev.csv"
    else:
        filepath = "data/texts.csv"

    if exists(filepath):
        choice = input(f"{filepath} already exists. Download anyways? [Y/N]")

        if choice.lower() not in ["yes", "ye", "y"]:
            return print("Data not downloaded")

    if args.feature is not None:
        df = get_raw_texts(args.feature)
    else:
        df = get_raw_texts()

    # format data
    df = format_data(df)
    # save data
    df.to_csv(filepath, index=False)


if __name__ == "__main__":
    main()
