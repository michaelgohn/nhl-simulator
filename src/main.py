from team import Team
from nhl_structure import team_names
from random import randint, random
from game import Game

curr_game = 0
teams = []

def check_if_same_teams(team1, team2):
    if team1 == team2:
        return True
    else:
        return False
    
def find_matching_spot(team1, team2):
    for index in range(len(team1.schedule)):
        if team1.schedule[index] == None and team2.schedule[index] == None:
            return index
    
    return None

def simulate_games():
    global curr_game
    while True:
        try:
            num_games = int(input('Enter the number of games you want to simulate: '))
            break
        except ValueError:
            print('Error: Not an integer')

    for team in teams:
        if curr_game != team.curr_game:
            continue
        for i in range(num_games):
            team.schedule[curr_game].determine_winner()
            curr_game += 1


# create teams
for team_name in team_names:
    teams.append(Team(team_name, randint(60, 100)))

# create schedules
for curr_team in teams:
    num_created_games = sum(1 for elem in curr_team.schedule if elem is not None)
    if num_created_games < 82:
        for i in range(82 - num_created_games):
            # initialize random numbers
            rand_num = random()
            rand_team = randint(0, 31)
            opp_team = teams[rand_team]

            # if opp_team has no matching spots or is same as curr_team pick new team
            while find_matching_spot(curr_team, opp_team) == None or check_if_same_teams(curr_team, opp_team):
                rand_team = randint(0, 31)
                opp_team = teams[rand_team]

            # create game and save to schedule
            index = find_matching_spot(curr_team, opp_team)
            if rand_num < .5:
                game = Game(curr_team, opp_team)
                curr_team.schedule[index] = game
                opp_team.schedule[index] = game
            else:
                game = Game(opp_team, curr_team)
                curr_team.schedule[index] = game
                opp_team.schedule[index] = game

# for team in teams:
#     team.print_to_file_schedule()
                
simulate_games()