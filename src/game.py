from random import random

class Game:

    def __init__(self, home_team, away_team):
        self.home_team = home_team
        self.away_team = away_team

    def determine_winner(self):
        home_team_win_chance = self.home_team.ovr / (self.home_team.ovr + self.away_team.ovr)
        rand_num = random()
        if rand_num < home_team_win_chance:
            self.adjust_records(self.home_team, self.away_team)
        else:
            self.adjust_records(self.away_team, self.home_team)

    def adjust_records(self, winner, loser):
        winner.wins += 1
        winner.pts += 2
        loser.losses += 1