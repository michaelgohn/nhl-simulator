from team import Team
from nhl_structure import team_names
from random import randint, random
from game import Game
import os

curr_game = 0
teams = []
pacific = []
central = []
atlantic = []
metro = []
west = []
east = []
west_wc = []
east_wc = []
playoff_teams = []
west_playoff_teams = []
east_playoff_teams = []
division_list = [pacific, central, atlantic, metro]

def print_to_file_rankings():
    global teams
    try:
        print('Writing to file...')
        directory = 'text-files'
        abs_path = os.path.abspath(directory) 
        print(f"Absolute path: {abs_path}")
        rank = 1
        with open(f'{directory}/rankings.txt', 'a+') as file:
            file.write(f'{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            teams = sort_team_list(teams)
            for team in teams:
                file.write(f'\n{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
    except AttributeError:
        print('Error: schedule does not contain iterable elements or element values are None.')

def any_teams_tied(team_list, attribute):
    seen_values = set()
    for team in team_list:
        value = getattr(team, attribute)
        if value in seen_values:
            return True
        seen_values.add(value)
    return False

def sort_team_list(team_list):
    reordered = True
    team_list.sort(key=lambda team: team.pts, reverse=True)
    if any_teams_tied(team_list=team_list, attribute='pts'):
        while(reordered):
            reordered = False
            for i in range(len(team_list) - 1):
                team_a = team_list[i]
                team_b = team_list[i + 1]
                updated_list = apply_tiebreaker_checks(team_list, team_a, team_b)
                if updated_list != team_list:
                    team_list = updated_list
                    reordered = True
                    break
    return team_list


def apply_tiebreaker_checks(team_list, team_a, team_b):
    temp_team_list = list(team_list)
    if team_a.pts > team_b.pts:
        return temp_team_list
    elif team_a.pts < team_b.pts:
        index_a = temp_team_list.index(team_a)
        index_b = temp_team_list.index(team_b)
        temp_team_list[index_a] = team_b
        temp_team_list[index_b] = team_a
        return temp_team_list
    else:
        if team_a.rw > team_b.rw:
            return temp_team_list
        elif team_a.rw < team_b.rw:
            index_a = temp_team_list.index(team_a)
            index_b = temp_team_list.index(team_b)
            temp_team_list[index_a] = team_b
            temp_team_list[index_b] = team_a
            return temp_team_list
        else:
            if team_a.row > team_b.row:
                return temp_team_list
            elif team_a.row < team_b.row:
                index_a = temp_team_list.index(team_a)
                index_b = temp_team_list.index(team_b)
                temp_team_list[index_a] = team_b
                temp_team_list[index_b] = team_a
                return temp_team_list
            else:
                if team_a.wins > team_b.wins:
                    return temp_team_list
                elif team_a.wins < team_b.wins:
                    index_a = temp_team_list.index(team_a)
                    index_b = temp_team_list.index(team_b)
                    temp_team_list[index_a] = team_b
                    temp_team_list[index_b] = team_a
                    return temp_team_list
                else:
                    if team_a.diff > team_b.diff:
                        return temp_team_list
                    elif team_a.diff < team_b.diff:
                        index_a = temp_team_list.index(team_a)
                        index_b = temp_team_list.index(team_b)
                        temp_team_list[index_a] = team_b
                        temp_team_list[index_b] = team_a
                        return temp_team_list
                    else:
                        if team_a.gf > team_b.gf:
                            return temp_team_list
                        elif team_a.gf < team_b.gf:
                            index_a = temp_team_list.index(team_a)
                            index_b = temp_team_list.index(team_b)
                            temp_team_list[index_a] = team_b
                            temp_team_list[index_b] = team_a
                            return temp_team_list
                        else:
                            if team_a.ga < team_b.ga:
                                return temp_team_list
                            elif team_a.ga > team_b.ga:
                                index_a = temp_team_list.index(team_a)
                                index_b = temp_team_list.index(team_b)
                                temp_team_list[index_a] = team_b
                                temp_team_list[index_b] = team_a
                                return temp_team_list
                            else:
                                for i in range(5):
                                    print('*********************************')
                                print('HOW ARE THEY STILL TIED!?!?!')
                                for i in range(5):
                                    print('*********************************')


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
            if num_games < 1 or num_games > (82 - curr_game):
                raise ValueError()
            break
        except ValueError:
            print('Error: Must be integer between 1 and number of remaining games (inclusive)')

    for i in range(num_games):
        for team in teams:
            if curr_game != team.curr_game:
                continue
            team.schedule[curr_game].determine_winner()
        curr_game += 1

def determine_playoff_structure(higher_div, lower_div, conf_wc_list):
    playoff_list = higher_div[:4]
    playoff_list.extend(lower_div[:4])
    playoff_list.extend(conf_wc_list)
    return playoff_list

def print_standings(option):
    global central
    global pacific
    global atlantic
    global metro
    global west
    global east
    global teams
    rank = 1
    match option:
        case 1:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            central = sort_team_list(central)
            for team in central:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 2:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            pacific = sort_team_list(pacific)
            for team in pacific:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 3:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            atlantic = sort_team_list(atlantic)
            for team in atlantic:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 4:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            metro = sort_team_list(metro)
            for team in metro:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 5:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            west = sort_team_list(west)
            for team in west:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 6:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            east = sort_team_list(east)
            for team in east:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 7:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            teams = sort_team_list(teams)
            for team in teams:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 8:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            for team in west_playoff_teams:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1
        case 9:
            print(f'\n{"Team" : <20}{"Points" : ^20}{"Wins" : ^20}{"Losses" : ^20}{"OT Losses" : ^20}{"RW" : ^20}{"ROW" : ^20}{"DIFF" : ^20}{"GF" : ^20}{"GA" : ^20}{"Overall" : >10}')
            for team in east_playoff_teams:
                print(f'{rank}. {team.name : <20}{team.pts : ^20}{team.wins : ^20}{team.losses : ^20}{team.otlosses : ^20}{team.rw : ^20}{team.row : ^20}{team.diff : ^20}{team.gf : ^20}{team.ga : ^20}{team.ovr : >10}')
                rank += 1


# create teams
for team_name in team_names:
    teams.append(Team(team_name, randint(60, 100)))
    pacific = teams[:8]
    central = teams[8:16]
    atlantic = teams[16:24]
    metro = teams[24:]
    west = teams[:16]
    east = teams[16:]

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

while(curr_game < 82):
    simulate_games()

pacific = sort_team_list(pacific)
central = sort_team_list(central)
atlantic = sort_team_list(atlantic)
metro = sort_team_list(metro)

# determine wc teams
west_wc = pacific[3:]
west_wc.extend(central[3:])
east_wc = atlantic[3:]
east_wc.extend(metro[3:])
west_wc = sort_team_list(west_wc)
east_wc = sort_team_list(east_wc)

# if pacific[0].pts > central[0].pts:
#     west_playoff_teams = determine_playoff_structure(higher_div=pacific, lower_div=central, conf_wc_list=west_wc)
# elif pacific[0].pts < central[0].pts:
#     west_playoff_teams = determine_playoff_structure(higher_div=central, lower_div=pacific, conf_wc_list=west_wc)
# else:
#     if pacific[0].rw > central[0].rw:
#         west_playoff_teams = determine_playoff_structure(higher_div=pacific, lower_div=central, conf_wc_list=west_wc)
#     elif pacific[0].rw < central[0].rw:
#         west_playoff_teams = determine_playoff_structure(higher_div=central, lower_div=pacific, conf_wc_list=west_wc)
#     else:
#         if pacific[0].row > central[0].row:
#             west_playoff_teams = determine_playoff_structure(higher_div=pacific, lower_div=central, conf_wc_list=west_wc)
#         elif pacific[0].row < central[0].row:
#             west_playoff_teams = determine_playoff_structure(higher_div=central, lower_div=pacific, conf_wc_list=west_wc)
#         else:
#             if pacific[0].wins > central[0].wins:
#                 west_playoff_teams = determine_playoff_structure(higher_div=pacific, lower_div=central, conf_wc_list=west_wc)
#             elif pacific[0].wins < central[0].wins:
#                 west_playoff_teams = determine_playoff_structure(higher_div=central, lower_div=pacific, conf_wc_list=west_wc)
#             else:

# determine playoff teams
div_leaders = [pacific[0], central[0]]
updtd_div_leaders = apply_tiebreaker_checks(team_list=div_leaders, team_a=pacific[0], team_b=central[0])
if div_leaders == updtd_div_leaders:
    west_playoff_teams = pacific[:3]
    west_playoff_teams.extend(central[:3])
    west_playoff_teams.extend(west_wc[:2])
else:
    west_playoff_teams = central[:3]
    west_playoff_teams.extend(pacific[:3])
    west_playoff_teams.extend(west_wc[:2])

div_leaders = [atlantic[0], metro[0]]
updtd_div_leaders = apply_tiebreaker_checks(team_list=div_leaders, team_a=atlantic[0], team_b=metro[0])
if div_leaders == updtd_div_leaders:
    east_playoff_teams = atlantic[:3]
    east_playoff_teams.extend(metro[:3])
    east_playoff_teams.extend(east_wc[:2])
else:
    east_playoff_teams = metro[:3]
    east_playoff_teams.extend(atlantic[:3])
    east_playoff_teams.extend(east_wc[:2])

option = 0
while(option != 10):
    option = int(input('Option: '))
    if(option != 10):
        print_standings(option=option)

# print_to_file_rankings()