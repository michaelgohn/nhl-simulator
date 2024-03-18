from random import random, randint, choices

class Game:

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

    def determine_winner(self):
        home_team_win_chance = self.home_team.ovr / (self.home_team.ovr + self.away_team.ovr)
        rand_num = random()
        self.home_team.curr_game += 1
        self.away_team.curr_game += 1
        if rand_num < home_team_win_chance:
            self.adjust_records(self.home_team, self.away_team)
            self.print_results(self.home_team)
        else:
            self.adjust_records(self.away_team, self.home_team)
            self.print_results(self.away_team)

    def adjust_records(self, winner, loser):
        winner.wins += 1
        winner.pts += 2
        loser.losses += 1

    def print_results(self, winner):
        pos_goals_winner = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        winner_weights = [.2, .2, .15, .1, .1, .1, .05, .05, .05]
        winner_score = choices(pos_goals_winner, winner_weights)[0]
        loser_score = randint(0, winner_score-1)

        if winner == self.home_team:
            print(f'\n{self.home_team.name}: {winner_score} - {loser_score} :{self.away_team.name}')
        else:
            print(f'\n{self.home_team.name}: {loser_score} - {winner_score} :{self.away_team.name}')


