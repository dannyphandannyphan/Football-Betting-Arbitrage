import pandas as pd
import itertools

def find_arbitrage_opportunities(match):
    """
    Finds arbitrage opportunities for a given match. NOT OPTIMISED

    Input: 
        match: a pandas dataframe consisting of the columns: 
            {'Team 1', 'Team 2', 'Date', 'Bookmaker', 'Team 1 win odds', Team 2 win odds', Draw odds'}
    """
    df = match

    team_1_name = df['Team 1'].iloc[0]
    team_2_name = df['Team 2'].iloc[0]

    df['Team 1 win probability'] = 1 / df['Team 1 win odds']
    df['Team 2 win probability'] = 1 / df['Team 2 win odds']
    df['Draw probability'] = 1 / df['Draw odds']

    team_1_win_list = list(df['Team 1 win odds']) # Make a list of the odds for team 1, team 2, and team 3 winning
    team_2_win_list = list(df['Team 2 win odds'])
    draw_list = list(df['Draw odds'])

    # Formatting: team_1_win_dict = {'Bookmaker A'} : {Bookmaker A's odds for team 1 winning}

    team_1_win_dict = {df['Bookmaker'].iloc[i] : team_1_win_list[i] for i in range(len(team_1_win_list))}
    team_2_win_dict = {df['Bookmaker'].iloc[i] : team_2_win_list[i] for i in range(len(team_2_win_list))}
    draw_dict = {df['Bookmaker'].iloc[i] : draw_list[i] for i in range(len(draw_list))}

    unique_triplets = {}
    
    # This is bruteforced and needs optimising, this can be probably be done using something like 3sum:
    
    for book1, win_odds in team_1_win_dict.items():
        for book2, lose_odds in team_2_win_dict.items():
            for book3, draw_odds in draw_dict.items():
                if book1 != book2 and book1 != book3 and book2 != book3: # All bookmakers are different
                    unique_books = book1 + "/" + book2 + "/" + book3 # 
                    unique_triplets[unique_books] = [win_odds, lose_odds, draw_odds]
    
    arbitrage_opportunities = {}
    
    for key, val in unique_triplets.items():
        team1win, team2win, draw = val
        if 1 / team1win + 1 / team2win + 1 / draw < 1:
            arbitrage_opportunities[key] = val

    arbitrage_df = pd.DataFrame.from_dict(arbitrage_opportunities).T

    arbitrage_df['Team 1 Name'] = team_1_name 
    arbitrage_df['Team 2 Name'] = team_2_name

    arbitrage_df = format_tables(arbitrage_df)

    return arbitrage_df

def format_tables(arbitrage_df):
    """
    Simply adds some columns that are necessary
    """
    if len(arbitrage_df):
        

        bet = 1000 # Sample bet amount

        # Adding needed columns to the dataframe

        arbitrage_df['Arb (%)'] = (1 / arbitrage_df[0] + 1 / arbitrage_df[1] + 1 / arbitrage_df[2]) * 100
        arbitrage_df['Profit (%)'] = ((1 - (1 / arbitrage_df[0] + 1 / arbitrage_df[1] + 1 / arbitrage_df[2])) * 100)
        arbitrage_df['ProfitIfBet1000'] = (bet / (arbitrage_df['Arb (%)'] / 100)) - bet

        arbitrage_df.rename(columns={0: "Team 1 win odds", 1: "Team 2 win odds", 2 : "Draw odds"}, inplace = True) 
        arbitrage_df.sort_values(by = 'Profit (%)', ascending = False, inplace = True) # Sorts profits

        arbitrage_df['Bookmakers'] = arbitrage_df.index # Weird issue, otherwise the bookmakers, i.e.: Coral/Betfair/BoyleSports are in the df.index
        arbitrage_df.reset_index(drop=True, inplace=True)

        arb_percent = (100 - arbitrage_df['Profit (%)'].iloc[0]) / 100 # If our edge is 1% then our arbitrage % is 99%
        indiv_arb_1 = 1 / arbitrage_df['Team 1 win odds'].iloc[0]
        indiv_bet_1 = (bet * indiv_arb_1) / arb_percent

        indiv_arb_2 = 1 / arbitrage_df['Team 2 win odds'].iloc[0]
        indiv_bet_2 = (bet * indiv_arb_2) / arb_percent

        indiv_arb_3 = 1 / arbitrage_df['Draw odds'].iloc[0]
        indiv_bet_3 = (bet * indiv_arb_3) / arb_percent

        arbitrage_df["BetSplit1000"] = f"{indiv_bet_1:.3f} \ {indiv_bet_2:.3f} \ {indiv_bet_3:.3f}"

    return arbitrage_df
