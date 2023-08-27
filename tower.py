from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR
from data_structures.bset import BSet

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        """The method is simple assignment of variables, which makes it complexity O(1) best/worst cases"""
        self.battle = battle or Battle(verbosity=0)
        self.teams = None  # Will be initialized in generate_teams
        self.team_lives = None
        self.team_count = 0
        self.player_team = None
        self.player_lives = 0

    def set_my_team(self, team: MonsterTeam) -> None:
        """
        Set the player's monster team and randomly assign the player's lives within the allowed range.
        :complexity: O(1), as assigning a team and generating a random number are constant time operations.
        """
        # Generate the team lives here too.
        self.player_team = team
        self.player_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_teams(self, n: int) -> None:
        """
        Generate 'n' number of enemy teams with monsters chosen at random.
        :complexity: O(n), where 'n' is the number of teams generated. Each team generation is O(1).
        """
        self.teams = ArrayR[MonsterTeam](n)
        self.team_lives = ArrayR[int](n)
        self.team_count = n
        for i in range(n):
            enemy_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            enemy_team_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.teams[i] = enemy_team
            self.team_lives[i] = enemy_team_lives

    def battles_remaining(self) -> bool:
        """
        Check if there are any battles remaining based on player and enemy teams' lives.
        :complexity: O(n), where 'n' is the number of enemy teams. The loop iterates over all enemy teams.
        """
        if self.player_lives <= 0:
            return False
        for i in range(self.team_count):
            if self.team_lives[i] > 0:
                return True
        return False

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        """
        Conducts the next battle between the player and the next available enemy team.
        :complexity: O(n), where 'n' is the number of enemy teams.
        The loop iterates until an enemy with lives greater than 0 is found.
        """
        if not self.battles_remaining():
            raise ValueError("No battles remaining.")

        for i in range(self.team_count):
            team = self.teams[i]
            lives = self.team_lives[i]
            if lives > 0 and not len(team) == 0:  # Add check for empty team here
                result = self.battle.battle(self.player_team, team)
                if result == Battle.Result.TEAM2:  # Player is team1 and enemy is team2
                    self.team_lives[i] -= 1
                elif result == Battle.Result.TEAM1:
                    self.player_lives -= 1
                else:  # result == Battle.Result.DRAW:
                    self.player_lives -= 1
                    self.team_lives[i] -= 1
                return result, self.player_team, team, self.player_lives, self.team_lives[i]

    def out_of_meta(self) -> ArrayR[Element]:
        """
        Compute the elements that are out of meta by comparing the elements of monsters from all battled teams and the upcoming enemy team.
        :complexity: O(n*m), where 'n' is the number of teams and 'm' is the average number of monsters in each team.
                     The outer loop iterates over all enemy teams, and the inner loop iterates over monsters of each team.
        """
        # Create a set to store elements of the upcoming enemy team
        upcoming_enemy_elements = BSet()
        for monster in self.teams[self.team_count].get_monsters():
            upcoming_enemy_elements.add(monster.element.value)

        # Create a set to store elements of the player team
        player_team_elements = BSet()
        for monster in self.player_team.get_monsters():
            player_team_elements.add(monster.element.value)

        # Create a set to store elements that have been present in the battles so far, including the player's team
        battled_elements = player_team_elements

        # Iterate over past enemy teams
        for i in range(self.team_count):
            enemy_elements = BSet()
            for monster in self.teams[i].get_monsters():
                enemy_elements.add(monster.element.value)
            battled_elements = battled_elements.union(enemy_elements)

        # Compute the elements that are out of meta
        out_of_meta_elements = battled_elements.difference(upcoming_enemy_elements).difference(player_team_elements)

        # Convert the set to a sorted array based on the order of element definition in Elements.py
        # Using the __str__ method of BSet to get the elements and converting them to integers
        out_of_meta_array = ArrayR(len(out_of_meta_elements))
        out_of_meta_str_elements = str(out_of_meta_elements)[1:-1].split(', ')

        for i, elem in enumerate(out_of_meta_str_elements):
            out_of_meta_array[i] = Element(int(elem))

        return out_of_meta_array

    def sort_by_lives(self):
        # 1054 ONLY
        raise NotImplementedError

def tournament_balanced(tournament_array: ArrayR[str]):
    # 1054 ONLY
    raise NotImplementedError

if __name__ == "__main__":

    RandomGen.set_seed(129371)

    bt = BattleTower(Battle(verbosity=3))
    bt.set_my_team(MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM))
    bt.generate_teams(3)

    for result, my_team, tower_team, player_lives, tower_lives in bt:
        print(result, my_team, tower_team, player_lives, tower_lives)