#worldcup_simulator.py
#Ali Ji-Afram
#404130573

import csv
import random
import math

class Team:
    """class to represent a team in the World Cup"""

    def __init__(self, name, attack, defense, rank):
        """Initialize a Team object with name, attack, defense, and rank attributes"""

        self.name = name
        self.attack = attack
        self.defense = defense
        self.rank = rank

        self.goals_for = 0
        self.goals_against = 0
        self.points = 0
        self.group = None

    def goal_difference(self):
        """Calculate the goal difference for the team"""

        return self.goals_for - self.goals_against

    def reset_stats(self):
        """Reset the team's statistics for a new tournament"""

        self.goals_for = 0
        self.goals_against = 0
        self.points = 0

    def simulate_match(self, opponent, is_knockout):
        """Simulate a match between this team and an opponent team"""

        pass

class Match:
    """class to represent a match between two teams"""

    def __init__(self, team1, team2, is_knockout):
        """Initialize a Match object with two Team objects"""

        self.team1 = team1
        self.team2 = team2
        self.is_knockout = is_knockout

        self.goals1 = 0
        self.goals2 = 0
        self.winner = None

    def play(self):
        """Simulate the match and determine the winner"""

        pass