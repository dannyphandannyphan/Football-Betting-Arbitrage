import pandas as pd

def find_arbitrage_opportunities(match, match_name):
    """
    Finds arbitrage opportunities for a given match

    Input: 
        match: a pandas dataframe
        match_name: name of the match

    This should be one of the matches from match_tables.
    """

    df = match
    
    df['Team 1 win prob'] = 1 / df['Team 1 win odds']
    df['Team 2 win prob'] = 1 / df['Team 2 win odds']
    df['Draw prob'] = 1 / df['Draw odds']

    team_1_win_list = list(df['Team 1 win odds'])
    team_2_win_list = list(df['Team 2 win odds'])
    draw_list = list(df['Draw odds'])

    team_1_win_list = list(df['Team 1 win odds'])
    team_2_win_list = list(df['Team 2 win odds'])
    draw_list = list(df['Draw odds'])

    # Formatting: team_1_win_dict = {'Bookmaker A Bookmaker B Bookmaker C'} : {A's Team1 win odds: B's Team2 win odds: C's draw odds}

    team_1_win_dict = {df['Bookmaker'].iloc[i] : team_1_win_list[i] for i in range(len(team_1_win_list))}
    team_2_win_dict = {df['Bookmaker'].iloc[i] : team_2_win_list[i] for i in range(len(team_2_win_list))}
    draw_dict = {df['Bookmaker'].iloc[i] : draw_list[i] for i in range(len(draw_list))}

    unique_triplets = {}

    for key1, val1 in team_1_win_dict.items():
        for key2, val2 in team_2_win_dict.items():
            for key3, val3 in draw_dict.items():

                if key1 != key2 and key1 != key3 and key2 != key3:
                    string = key1 + " " + key2 + " " + key3
                    unique_triplets[string] = [val1, val2, val3]
            
    arbitrage_opportunities = {}

    for key, val in unique_triplets.items():
        team1win, team2win, draw = val
        if 1/ team1win + 1 / team2win + 1 / draw < 1:
            arbitrage_opportunities[key] = val

    arbitrage_df = pd.DataFrame.from_dict(arbitrage_opportunities).T

    if len(arbitrage_df):
        arbitrage_df['Profit (%)'] = (1 - (1 / arbitrage_df[0] + 1 / arbitrage_df[1] + 1 / arbitrage_df[2])) * 100

        arbitrage_df.rename(columns={0: "Team 1 win odds", 1: "Team 2 win odds", 2 : "Draw odds"}, inplace = True)

        arbitrage_df.sort_values(by = 'Profit (%)', ascending = False, inplace = True)

        return arbitrage_df
    else:
        return arbitrage_df

def find_arbitrage_profit(investment, match, team1name, team2name):
    """
    Inputs: 
        investment : Total bet amount in £
        match : A pandas dataframe for a single match
        team1name : The name of team 1
        team2name : The name of team 2
    """

    x = (100 - match['Profit (%)'].iloc[0]) / 100 # If our edge is 1% then our arbitrage % is 99%
    
    profit = (investment / x) - investment

    individual_arbitrage_1 = 1 / match['Team 1 win odds'].iloc[0]
    individual_bet_1 = (investment * individual_arbitrage_1) / x 

    individual_arbitrage_2 = 1 / match['Team 2 win odds'].iloc[0]
    individual_bet_2 = (investment * individual_arbitrage_2) / x 

    individual_arbitrage_3 = 1 / match['Draw odds'].iloc[0]
    individual_bet_3 = (investment * individual_arbitrage_3) / x 

    message = f"""If your investment is £{investment}, you would make £{profit}. 
               You must bet £{individual_bet_1} on {team1name}, £{individual_bet_2} 
               on {team2name}, and £{individual_bet_3} on Draw"""
    
    return message





