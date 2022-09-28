import pandas as pd 


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

