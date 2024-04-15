from random import random, randint, choices
from numpy import random as np

class Game:

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team
        self.h_num_1st_prd_gls = 0
        self.h_num_2nd_prd_gls = 0
        self.h_num_3rd_prd_gls = 0
        self.a_num_1st_prd_gls = 0
        self.a_num_2nd_prd_gls = 0
        self.a_num_3rd_prd_gls = 0
        self.num_home_goals = 0
        self.num_away_goals = 0
        self.ot = False

    def determine_winner(self):
        self.home_team.curr_game += 1
        self.away_team.curr_game += 1
        chances_per_game = 7
        home_team_goal_chance = self.home_team.ovr / (self.home_team.ovr + self.away_team.ovr)
        away_team_goal_chance = self.away_team.ovr / (self.away_team.ovr + self.home_team.ovr)
        self.num_home_goals = np.binomial(chances_per_game, home_team_goal_chance)
        self.num_away_goals = np.binomial(chances_per_game, away_team_goal_chance)

        # decides goals per period for home team
        temp_home_goals = self.num_home_goals
        period = 1
        chosen_num = 0
        while(temp_home_goals > 0):
            if period == 1:
                chosen_num = randint(0, temp_home_goals)
                self.h_num_1st_prd_gls += chosen_num
            elif period == 2:
                chosen_num = randint(0, temp_home_goals)
                self.h_num_2nd_prd_gls += chosen_num
            else:
                chosen_num = randint(0, temp_home_goals)
                self.h_num_3rd_prd_gls += chosen_num

            temp_home_goals -= chosen_num
            
            if period % 3 == 0:
                period = 1
            else:
                period += 1

        # decides goals per period for away team
        temp_away_goals = self.num_away_goals
        chosen_num = 0
        period = 1
        while(temp_away_goals > 0):
            if period == 1:
                chosen_num = randint(0, temp_away_goals)
                self.a_num_1st_prd_gls += chosen_num
            elif period == 2:
                chosen_num = randint(0, temp_away_goals)
                self.a_num_2nd_prd_gls += chosen_num
            else:
                chosen_num = randint(0, temp_away_goals)
                self.a_num_3rd_prd_gls += chosen_num

            temp_away_goals -= chosen_num
            
            if period % 3 == 0:
                period = 1
            else:
                period += 1

        # check for ot
        if self.num_home_goals == self.num_away_goals:
            self.ot = True
            rand_num = random()
            home_ot_goal = 0
            away_ot_goal = 0
            home_shootout_goals = 0
            away_shootout_goals = 0
            if rand_num < home_team_goal_chance:
                home_ot_goal =  1
            rand_num = random()
            if rand_num < away_team_goal_chance:
                away_ot_goal = 1

            # shootout
            if home_ot_goal == away_ot_goal:
                # makes no sense to score 2 goals in ot so set to 0
                if home_ot_goal == 1:
                    home_ot_goal = 0
                    away_ot_goal = 0
                home_shootout_goals = np.binomial(3, home_team_goal_chance)
                away_shootout_goals = np.binomial(3, away_team_goal_chance)
                while(home_shootout_goals == away_shootout_goals):
                    rand_num = random()
                    if rand_num < home_team_goal_chance:
                        home_shootout_goals += 1
                    rand_num = random()
                    if rand_num < away_team_goal_chance:
                        away_shootout_goals += 1
            
            if home_ot_goal > away_ot_goal or home_shootout_goals > away_shootout_goals:
                self.num_home_goals += 1
            else:
                self.num_away_goals += 1

        # determine winner
        if self.num_home_goals > self.num_away_goals:
            self.adjust_records(self.home_team, self.away_team)
            self.print_results()
        else:
            self.adjust_records(self.away_team, self.home_team)
            self.print_results()

        # rand_num = random()
        # self.home_team.curr_game += 1
        # self.away_team.curr_game += 1
        # if rand_num < home_team_win_chance:
        #     self.adjust_records(self.home_team, self.away_team)
        #     self.print_results(self.home_team)
        # # else:
        #     self.adjust_records(self.away_team, self.home_team)
        #     self.print_results(self.away_team)

    def adjust_records(self, winner, loser):
        winner.wins += 1
        winner.pts += 2
        loser.losses += 1
        if self.ot:
            loser.pts += 1
            loser.otlosses += 1

    def print_results(self):
        # pos_goals_winner = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # winner_weights = [.2, .2, .15, .1, .1, .1, .05, .05, .05]
        # winner_score = choices(pos_goals_winner, winner_weights)[0]
        # loser_score = randint(0, winner_score-1)
        print(f'\n{self.home_team.name}: {self.num_home_goals} - {self.num_away_goals} :{self.away_team.name}')

