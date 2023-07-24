import requests

def fetch_odds(api_key, sport = 'soccer_england_league1', regions = 'uk', markets = 'h2h', odds_format = 'decimal', dates_format = 'iso'):
    params = {
        'api_key': api_key,
        'regions': regions,
        'markets': markets,
        'oddsFormat': odds_format,
        'dateFormat': dates_format,
    }

    try:
        response = requests.get(f'https://api.the-odds-api.com/v4/sports/{sport}/odds', params = params)
        response.raise_for_status()
        json_data = response.json()
        print('Remaining requests', response.headers['x-requests-remaining'])
        print('Used requests', response.headers['x-requests-used'])
        return json_data
    except requests.exceptions.RequestException as error:
        print(f'Failed to get odds: {error}')
        return None
    

    