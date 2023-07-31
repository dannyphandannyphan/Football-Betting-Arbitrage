import pandas as pd
import requests
import time
import datetime

from data_fetch import fetch_odds
from find_arbitrage import find_arbitrage_opportunities
from data_process import create_excel_file, create_pandas_dataframe
from send_emails import send_daily_email

if __name__ == "__main__":

    file_path = 'C:\\Users\\Danny\\Desktop\\ArbitrageBot\\Football-Betting-Arbitrage\\ArbitrageBot\\API_KEY.txt'
    with open(file_path) as f:
        api_key = f.read()

    json_data = fetch_odds(api_key, sport='soccer_england_league1', regions='uk', markets='h2h', odds_format='decimal', dates_format='iso')

    match_tables = create_pandas_dataframe(json_data)

    arbitrage_tables = {}

    for name, match in match_tables.items():
        arbitrage_tables[name] = find_arbitrage_opportunities(match)

    non_empty_arbitrage_tables = {}

    for name, match in arbitrage_tables.items():
        if not arbitrage_tables[name].empty:
            non_empty_arbitrage_tables[name] = match
 
    current_date = datetime.datetime.now().strftime("%d_%m_%Y")
    file_path = create_excel_file(non_empty_arbitrage_tables, f"arbitrage_opportunities_{current_date}.xlsx")    
    send_daily_email(non_empty_arbitrage_tables, file_path)



