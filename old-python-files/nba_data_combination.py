import json
import pandas as pd


data_frames = []

for year in range(2017,2020):
    
    data = None
    with open("nba_team_2019.json", "r") as f:  
        data = json.load(f)

    new_data = {}

    mini_data_frames = []

    for team, values in data.items():
        print(team)
        
        mini_data = values.copy()
        num_games = len(values['win_percentage'])

        opp_win_percentage_5  = []
        opp_win_percentage = []
        opp_avg_margin_5 = []
        opp_avg_margin = []

        for i in range(num_games):

            opponent = values['opponent'][i]
            opp_values = data[opponent]

            opp_win_percentage_5.append(opp_values['win_percentage_5'][i])
            opp_win_percentage.append(opp_values['win_percentage'][i])
            opp_avg_margin_5.append(opp_values['avg_margin_5'][i])
            opp_avg_margin.append(opp_values['avg_margin'][i])

        mini_data['opp_win_percentage_5'] = opp_win_percentage_5
        mini_data['opp_win_percentage'] = opp_win_percentage
        mini_data['opp_avg_margin_5'] = opp_avg_margin_5
        mini_data['opp_avg_margin'] = opp_avg_margin

        mini_data.pop('opponent')

        mini_data_frames.append(pd.DataFrame.from_dict(mini_data))
    
    
    data_frames.append(pd.concat(mini_data_frames))


training_data_2017_2018 = pd.concat(data_frames[:2])
test_data_2019 = data_frames[2]

with open('training_data.csv', 'w') as train:
    training_data_2017_2018.to_csv(train)

with open('testing_data.csv','w') as test:
    test_data_2019.to_csv(test)


