#worldcup_simulator.py
#Ali Ji-Afram
#404130573

import csv
import random as r
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

        self.goals1, self.goals2, self.winner = self.team1.simulate_match(self.team2, self.is_knockout)
        return self.goals1, self.goals2, self.winner


class Group:
    """class to represent a group containing 4 teams in the World Cup"""

    def __init__(self, name, teams):
        """Initialize a Group object with a name and a list of Team objects"""

        self.name = name
        self.teams = teams

        for team in self.teams:
            team.group = name

    def play_all_matches(self):
        """Simulate all matches in the group and update team statistics"""

        for i in range(len(self.teams)):
            for j in range(i + 1, len(self.teams)):
                match = Match(self.teams[i], self.teams[j], is_knockout=False)
                match.play()

    def get_ranking(self):
        """Return the teams in the group sorted by points, goal difference, goals for, and randomly if necessary"""

        shuffled_teams = self.teams[:]
        r.shuffle(shuffled_teams)

        return sorted(shuffled_teams, key=lambda team: (team.points, team.goal_difference(), team.goals_for), reverse=True)

    def advance_teams(self):
        """Return the top 2 teams in the group that advance to the knockout stage"""
        
        ranking = self.get_ranking()
        return ranking[0], ranking[1]


class KnockoutStage:
    """class to represent the knockout stage of the World Cup"""

    def __init__(self, round_name, matches):
        """Initialize a KnockoutStage object with a round name and list of Match objects"""

        self.round_name = round_name
        self.matches = matches

    def play_round(self):
        """Simulate a round of matches in the knockout stage and update team statistics"""

        for match in self.matches:
            match.play()

    def get_winners(self):
        """Return the winners team of the knockout stage in the order they were played"""

        winners = []

        for match in self.matches:
            if match.winner is not None:
                winners.append(match.winner)

        return winners

    def display_results(self, display=True):
        """Display the results of the knockout stage matches"""

        if display:

            print(f"===== {self.round_name} =====")

            for match in self.matches:

                print(
                    f"{match.team1.name} "
                    f"{match.goals1}-{match.goals2} "
                    f"{match.team2.name} | "
                    f"Winner: {match.winner.name}"
                )


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

    def load_teams_from_csv(self, filename, display=True):
        """Load teams from a CSV file and create Team objects"""

        self.teams = []

        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:

                    name = row["name"]
                    attack = int(row["attack"])
                    defense = int(row["defense"])
                    rank = int(row["rank"])

                    if type(name) is str and 0 <= attack <= 100 and 0 <= defense <= 100 and 1 <= rank <= 32:
                        team = Team(name, attack, defense, rank)
                        self.teams.append(team)
                    else:
                        if display:
                            print(f"Invalid data type or value for team: {row}")
                        return False

                if len(self.teams) != 32:
                    if display:
                        print("Invalid count of teams: Expected 32 teams in the CSV file")
                    return False

            return True

        except FileNotFoundError:
            if display:
                print("CSV file not found: Please check the file path and name")
            return False

    def seed_and_draw_groups(self):
        """Group draw based on seeding like fifa rankings"""

        self.groups = []

        seed1 = []
        seed2 = []
        seed3 = []
        seed4 = []

        # Divide teams into seeds based on rank
        for team in self.teams:

            if 1 <= team.rank <= 8:
                seed1.append(team)

            elif 9 <= team.rank <= 16:
                seed2.append(team)

            elif 17 <= team.rank <= 24:
                seed3.append(team)

            elif 25 <= team.rank <= 32:
                seed4.append(team)

        # Shuffle each seed to randomize the draw
        r.shuffle(seed1)
        r.shuffle(seed2)
        r.shuffle(seed3)
        r.shuffle(seed4)

        # Create groups and assign teams from each seed
        group_names = ["A", "B", "C", "D", "E", "F", "G", "H"]

        #Create 8 groups, each with one team from each seed
        for i in range(8):
            group_teams = [seed1[i], seed2[i], seed3[i], seed4[i]]
            group = Group(group_names[i], group_teams)
            self.groups.append(group)

        return True

    def run_group_stage(self, display=True):
        """Run the group stage of the World Cup and determine the teams that advance to the knockout stage"""

        for group in self.groups:

            group.play_all_matches()
            ranking = group.get_ranking()

            if display:

                print(f"===== Group {group.name} =====")

                rank = 1
                for team in ranking:
                    print(
                        f"{rank}. {team.name} - Points: {team.points}, "
                        f"Goal Difference: {team.goal_difference()}, "
                        f"Goals For: {team.goals_for}"
                    )
                    rank += 1

        return True

    def setup_knockout_bracket(self):
        """Set up the knockout stage bracket based on the teams that advanced from the group stage"""

        A1, A2 = self.groups[0].advance_teams()
        B1, B2 = self.groups[1].advance_teams()
        C1, C2 = self.groups[2].advance_teams()
        D1, D2 = self.groups[3].advance_teams()
        E1, E2 = self.groups[4].advance_teams()
        F1, F2 = self.groups[5].advance_teams()
        G1, G2 = self.groups[6].advance_teams()
        H1, H2 = self.groups[7].advance_teams()

        Matches = [
            Match(A1, B2, is_knockout=True),
            Match(C1, D2, is_knockout=True),
            Match(E1, F2, is_knockout=True),
            Match(G1, H2, is_knockout=True),
            Match(B1, A2, is_knockout=True),
            Match(D1, C2, is_knockout=True),
            Match(F1, E2, is_knockout=True),
            Match(H1, G2, is_knockout=True)
        ]

        self.round_of_16 = KnockoutStage("Round of 16", Matches)

        return True

    def run_knockout_stage(self):
        """Run the knockout stage of the World Cup and determine the champion"""

        #run the round of 16
        self.round_of_16.play_round()
        self.round_of_16.display_results()

        winners = self.round_of_16.get_winners()

        matches = [
            Match(winners[0], winners[1], is_knockout = True),
            Match(winners[2], winners[3], is_knockout = True),
            Match(winners[4], winners[5], is_knockout = True),
            Match(winners[6], winners[7], is_knockout = True)
        ]

        self.quarterfinals = KnockoutStage("Quarter Finals", matches)

        #run the quarterfinals
        self.quarterfinals.play_round()
        self.quarterfinals.display_results()

        winners = self.quarterfinals.get_winners()

        matches = [
            Match(winners[0], winners[1], is_knockout = True),
            Match(winners[2], winners[3], is_knockout = True)
        ]

        self.semifinals = KnockoutStage("Semi Finals", matches)

        #run the semifinals
        self.semifinals.play_round()
        self.semifinals.display_results()

        winners = self.semifinals.get_winners()

        matches = [
            Match(winners[0], winners[1], is_knockout = True)
        ]

        self.final = KnockoutStage("Final", matches)

        #run the final
        self.final.play_round()
        self.final.display_results()

        winners = self.final.get_winners()

        self.champion = winners[0]

        return True

    def run_full_simulation(self):
        """Run the full World Cup simulation, including group stage and knockout stage and determine the champion"""

        for team in self.teams:
            team.reset_stats()

        self.seed_and_draw_groups()
        self.run_group_stage()
        self.setup_knockout_bracket()
        self.run_knockout_stage()

        return self.champion

    def most_likely_champion(self, num_simulations=1000, display=True):
        """Run multiple simulations of the World Cup and determine the most likely champion"""

        if num_simulations <= 0 or type(num_simulations) is not int:
            if display:
                print("Number of simulations is invalid: Please provide a positive integer")
            return False

        champion_counts = {}

        for team in self.teams:
            champion_counts[team.name] = 0

        for _ in range(num_simulations):
            champion = self.run_full_simulation()
            champion_counts[champion.name] += 1

        champion_percentages = {}

        for team_name, count in champion_counts.items():
            champion_percentages[team_name] = (count / num_simulations) * 100

        return champion_percentages

    def display_bracket(self, display=True):
        """Display the knockout stage bracket and results"""

        if self.round_of_16 is None:
            if display:
                print("No simulation has been run yet: Please run a full simulation first")
            return False

        if display:
            
            print("===== Knockout Bracket =====")

            self.round_of_16.display_results()
            self.quarterfinals.display_results()
            self.semifinals.display_results()
            self.final.display_results()

            print(f"Champion: {self.champion.name}")

        return True