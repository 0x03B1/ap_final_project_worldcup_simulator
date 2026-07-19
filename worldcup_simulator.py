#worldcup_simulator.py
#Ali Ji-Afram
#404130573

import csv
import random as r
import math as m
import numpy as np

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

    def simulate_match(self, opponent, is_knockout=False):
        """Simulate a match between this team and an opponent team.

        Args:
            opponent (Team): The opposing team.
            is_knockout (bool): Whether the match is in knockout stage.

        Returns:
            tuple: (goals_self, goals_opponent, winner)
                winner is None in group stage if the match ends in a draw.
        """
        
        # -------------------------
        # 1) Regular 90 minutes
        # -------------------------
        lambda_self = (self.attack / 100) * 1.5 + (1 - opponent.defense / 100) * 0.8
        lambda_opponent = (opponent.attack / 100) * 1.5 + (1 - self.defense / 100) * 0.8

        goals_self = int(np.random.poisson(lam=lambda_self))
        goals_opponent = int(np.random.poisson(lam=lambda_opponent))

        # -------------------------
        # 2) Group stage
        # -------------------------
        if not is_knockout:
            self.goals_for += goals_self
            self.goals_against += goals_opponent
            opponent.goals_for += goals_opponent
            opponent.goals_against += goals_self

            if goals_self > goals_opponent:
                self.points += 3
                winner = self
            elif goals_opponent > goals_self:
                opponent.points += 3
                winner = opponent
            else:
                self.points += 1
                opponent.points += 1
                winner = None

            return goals_self, goals_opponent, winner

        # -------------------------
        # 3) Knockout stage
        # -------------------------
        if goals_self == goals_opponent:
            extra_lambda_self = lambda_self * 0.33
            extra_lambda_opponent = lambda_opponent * 0.33

            extra_goals_self = int(np.random.poisson(lam=extra_lambda_self))
            extra_goals_opponent = int(np.random.poisson(lam=extra_lambda_opponent))

            goals_self += extra_goals_self
            goals_opponent += extra_goals_opponent

        # Update stats with only regular + extra time goals
        self.goals_for += goals_self
        self.goals_against += goals_opponent
        opponent.goals_for += goals_opponent
        opponent.goals_against += goals_self

        # If still tied after extra time, go to penalties
        if goals_self == goals_opponent:
            def penalty_success_prob(team, other_team):
                p = 0.75 + (team.attack - other_team.defense) / 250
                return max(0.6, min(0.9, p))

            p_self = penalty_success_prob(self, opponent)
            p_opponent = penalty_success_prob(opponent, self)

            # 5 initial penalties each
            self_penalties = 0
            opponent_penalties = 0

            for i in range(5):
                if r.random() < p_self:
                    self_penalties += 1
                if r.random() < p_opponent:
                    opponent_penalties += 1

            # Sudden death if needed
            while self_penalties == opponent_penalties:
                if r.random() < p_self:
                    self_penalties += 1
                if r.random() < p_opponent:
                    opponent_penalties += 1

            winner = self if self_penalties > opponent_penalties else opponent
            return goals_self, goals_opponent, winner

        winner = self if goals_self > goals_opponent else opponent
        return goals_self, goals_opponent, winner


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


class Group:
    """class to represent a group containing 4 teams in the World Cup"""

    def __init__(self, name, teams):
        """Initialize a Group object with a name and a list of Team objects"""

        self.name = name
        self.teams = teams

    def play_all_matches(self):
        """Simulate all matches in the group and update team statistics"""

        pass

    def get_ranking(self):
        """Return the teams in the group sorted by points, goal difference, goals for, and randomly if necessary"""

        pass

    def advance_teams(self):
        """Return the top 2 teams in the group that advance to the knockout stage"""
        
        pass


class KnockoutStage:
    """class to represent the knockout stage of the World Cup"""

    def __init__(self, round_name, matches):
        """Initialize a KnockoutStage object with a list of Team objects"""

        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """Simulate a round of matches in the knockout stage and update team statistics"""

        pass

    def get_winners(self):
        """Return the winners team of the knockout stage in the order they were played"""

        pass

    def display_results(self):
        """Display the results of the knockout stage matches"""

        pass


class WorldCupSimulator:
    """class to represent the World Cup tournament"""

    def __init__(self):
        """Initialize a WorldCupSimulator object, the main class that will run the simulation"""
        
        self.teams = []
        self.groups = []
        self.round_of_16 = None
        self.quarterfinals = None
        self.semifinals = None
        self.final = None
        self.champion = None

    def load_teams_from_csv(self, filename):
        """Load teams from a CSV file and create Team objects"""

        pass

    def seed_and_draw_groups(self):
        """Group draw based on seeding like fifa rankings"""

        pass

    def run_group_stage(self):
        """Run the group stage of the World Cup and determine the teams that advance to the knockout stage"""

        pass

    def setup_knockout_bracket(self):
        """Set up the knockout stage bracket based on the teams that advanced from the group stage"""

        pass

    def run_knockout_stage(self):
        """Run the knockout stage of the World Cup and determine the champion"""

        pass

    def run_full_simulation(self):
        """Run the full World Cup simulation, including group stage and knockout stage and determine the champion"""

        pass

    def most_likely_champion(self, num_simulations=1000):
        """Run multiple simulations of the World Cup and determine the most likely champion"""

        pass

    def display_bracket(self):
        """Display the knockout stage bracket and results"""

        pass