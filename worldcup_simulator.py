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