import os

class Team:
    def __init__(self, name, ovr):
        self.name = name
        self.curr_game = 0
        self.wins = 0
        self.losses = 0
        self.otlosses = 0
        self.rw = 0
        self.row = 0 # reg + ot wins (excluding shootout)
        self.pts = 0
        self.diff = 0 # goal differential (counts regulation, overtime, and 1 goal for a shootout win)
        self.gf = 0 # goals for
        self.ga = 0 # goals against
        self.schedule = [None] * 82
        self.ovr = ovr

    def print_to_file_schedule(self):
        try:
            print('Writing to file...')
            directory = 'text-files'
            abs_path = os.path.abspath(directory) 
            print(f"Absolute path: {abs_path}")
            count = 1
            for game in self.schedule:
                with open(f'{directory}/{self.name}.txt', 'a+') as file:
                    file.write(f'{count}. {game.home_team.name} vs. {game.away_team.name}\n')
                count += 1
        except AttributeError:
            print('Error: schedule does not contain iterable elements or element values are None.')