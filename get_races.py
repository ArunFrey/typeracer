from bs4 import BeautifulSoup
import requests
import argparse
import pandas as pd
from helpers import format_data


def get_raw_races(username, last_races=99999999):

    """Downloads a user's typeracer data from typeracerdata.com


    Args:
        username (str): Username used for typeracer.
        last_races (int, optional): Number of last races to retrieve. Defaults to 99999999

    Returns:
        pd.DataFrame: A dataframe containing a user's race data.
    """
    url = f"http://www.typeracerdata.com/profile?username={username}&last={last_races}"
    # get parsed data
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    # extract data from tables
    tables = soup.find_all("table")
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

    df = pd.DataFrame(race_data, columns=columns)

    return df


def main():

    """Main function to be executed directly from terminal"""

    parser = argparse.ArgumentParser(description="Getting racer data from typeracer.")
    parser.add_argument(
        "-u",
        "--user_name",
        type=str,
        required=True,
        help="Enter the username of the user whose data you want to download.",
    )
    parser.add_argument(
        "-lr",
        "--last_races",
        type=int,
        required=False,
        help="Enter the last number of races you wish to download. Defaults to all.",
    )
    args = parser.parse_args()

    # get data
    if args.last_races is not None:
        df = get_raw_races(args.user_name, args.last_races)
    else:
        df = get_raw_races(args.user_name)

    # format data
    df = format_data(df)
    # store data
    df.to_csv(f"data/races_{args.user_name}.csv", index=False)


if __name__ == "__main__":
    main()
