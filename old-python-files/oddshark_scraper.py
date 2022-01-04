from bs4 import BeautifulSoup
import requests
import pprint
from datetime import datetime

import json


columns = ['Win %','avg margin of victory','home or away']

all_data = {}

for year in range(2020,2022):
    print('\n'*2)
    print(year)
    for j in range(30):
        print(j)
        URL = 'https://www.oddsshark.com/stats/gamelog/basketball/nba/207'+str(22+j)+'/'+str(year)
        page = requests.get(URL)

        soup = BeautifulSoup(page.content,'html.parser')

        #pprint.pprint(soup)
        title_text = soup.find(id = 'page-title').text.split()
        team = title_text[0]

        if team == 'Los':
            if title_text[2][0]=='C':
                team = 'LAC'
            else: team = 'LAL'

        print(team)

        results = soup.find(id='content')
        
        if results is None:
            continue
        games = results.find_all('tr')



        total_data = {'wins':[],'losses':[], 'won by':[],'home or away':[],'spread':[],'won against spread':[],'opponent':[]}
        for game in games:
            data = game.find_all('td')
            new_data = ['Date','Opponent','Game','Result','Score','ATS','Spread']
            storage = {}
            if data:
                for i in range(len(new_data)):
                    storage[new_data[i]] = data[i].text
                if storage['Game'] == 'REG':

                    if str(storage['ATS'])== 'W':
                        ATS = 1
                    else: ATS = 0
                    total_data['won against spread'].append(ATS)

                    game_opp = storage['Opponent'].split()
                    if '@' in game_opp[0]:
                        home = 0
                    else: home = 1
                    total_data['home or away'].append(home)
                    
                    opponent = game_opp[1]
                    if opponent == 'LA':
                        opponent =  opponent+game_opp[2][0]
                    total_data['opponent'].append(opponent)

                    won_by = eval(storage['Score'])
                    total_data['won by'].append(won_by)

                    result = storage['Result']
                    try:
                        num_wins = total_data['wins'][-1]
                        num_loss = total_data['losses'][-1]
                    except:
                        num_wins = 0
                        num_loss = 0

                    if result == 'W':
                        total_data['wins'].append(num_wins+1)
                        total_data['losses'].append(num_loss)
                    else:
                        total_data['wins'].append(num_wins)
                        total_data['losses'].append(num_loss+1)

                    total_data['spread'].append(eval(storage['Spread']))


        formatted_data = {}    
        win_percentage = []
        win_percentage_5 = []
        avg_margin = []
        avg_margin_5 = []
        num_games = len(total_data['wins'])
        for i in range(num_games):
            wins = total_data['wins'][i]
            losses = total_data['losses'][i]

            win_percentage.append(float(wins)/(wins+losses))

            if i<5:
                wins_5 = 0
                losses_5 = 0
                avg_margin_5games = 0
            else:
                wins_5 = total_data['wins'][i-5]
                loss_5 = total_data['losses'][i-5]
                avg_margin_5games = avg_margin[i-5]
            
            last_5_games_wins =  wins-wins_5
            last_5_games_losses = losses-losses_5
            last_5_games_win_percent =float(last_5_games_wins)/(last_5_games_wins+last_5_games_losses)
            win_percentage_5.append(last_5_games_win_percent)

            margin = sum(total_data['won by'][:i+1])/float(i+1)
            avg_margin.append(margin)

            avg_margin_5.append(margin-avg_margin_5games)


        formatted_data['win_percentage_5'] = win_percentage_5
        formatted_data['win_percentage'] = win_percentage
        formatted_data['avg_margin_5'] = avg_margin_5
        formatted_data['avg_margin'] = avg_margin
        formatted_data['home_or_away'] = total_data['home or away']
        formatted_data['spread'] = total_data['spread']
        formatted_data['beat_spread'] = total_data['won against spread']
        formatted_data['opponent'] = total_data['opponent']
        all_data[team] = formatted_data


    with open("nba_team_"+str(year)+".json", "w") as outfile:  
        json.dump(all_data, outfile,indent=4) 