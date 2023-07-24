import pandas as pd

def extract_info(match):
    """
    Extracts match and bookmaker information from a given dictionary representing a single match.
    """
    match_data = []
    for bookmaker in match['bookmakers']: # We iterate over bookmakers and markets because they are nested in the json
        for market in bookmaker['markets']:
            outcomes = {outcome['name']: outcome['price'] for outcome in market['outcomes']}
            match_data.append({
                'Team 1': match['home_team'],
                'Team 2': match['away_team'],
                'Date': match['commence_time'],
                'Bookmaker': bookmaker['title'],
                'Team 1 win odds': outcomes.get(match['home_team'], None),
                'Team 2 win odds': outcomes.get(match['away_team'], None),
                'Draw odds': outcomes.get('Draw', None),
            })
    return match_data

def create_pandas_dataframe(json_data):
    """
    Turns our json list into a dictionary that pandas can display
    """
    match_tables = {}

    for match in json_data:
        match_name = f"{match['home_team']} vs {match['away_team']}" # set name

        match_data = extract_info(match)
    
        if match_name not in match_tables:
            match_tables[match_name] = pd.DataFrame(match_data)
        else:
            match_tables[match_name] = pd.concat([match_tables[match_name], pd.DataFrame(match_data)])

    return match_tables

def create_excel_file(data_dict, excel_filename):
    """
    Creates an Excel file with the tabs as each match, and the match data as each key
    """

    writer = pd.ExcelWriter(excel_filename, engine='xlsxwriter')

    for match_name, match_df in data_dict.items():
        
        sheet_name = match_name[:31]

        # Combine the bookmakers' names with the DataFrame
        match_df.insert(0, 'Bookmaker', match_df.index)

        # Write the DataFrame to the Excel sheet
        match_df.to_excel(writer, sheet_name=sheet_name, index=False)

    writer.close()