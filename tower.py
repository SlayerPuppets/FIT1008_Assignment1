from __future__ import annotations

from random_gen import RandomGen
from team import MonsterTeam
from battle import Battle

from elements import Element

from data_structures.referential_array import ArrayR

class BattleTower:

    MIN_LIVES = 2
    MAX_LIVES = 10

    def __init__(self, battle: Battle|None=None) -> None:
        self.player_team_lives = None
        self.battle = battle or Battle(verbosity=0)
        self.player_team = None
        self.enemy_teams = ArrayR[MonsterTeam](0)
        self.enemy_lives = ArrayR[int](0)
        self.enemy_index = 0

    def set_my_team(self, team: MonsterTeam) -> None:
        # Generate the team lives here too.
        self.player_team = team
        # Generate player team lives between MIN_LIVES and MAX_LIVES
        self.player_team_lives = RandomGen.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_teams(self, n: int) -> None:
        self.enemy_teams = ArrayR[MonsterTeam](n)  # Initialize an ArrayR to store enemy teams
        for i in range(n):
            enemy_team = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
            enemy_team.retrieve_from_team()  # Assuming this method doesn't require arguments
            self.enemy_teams[i] = enemy_team  # Assign the enemy team to the ArrayR

    def battles_remaining(self) -> bool:
        return self.player_team_lives > 0 and any(enemy_team_lives > 0 for (_, enemy_team_lives) in self.enemy_teams)

    def next_battle(self) -> tuple[Battle.Result, MonsterTeam, MonsterTeam, int, int]:
        if not self.battles_remaining():
            raise ValueError("No battles remaining in the Battle Tower.")

        enemy_team, enemy_team_lives = self.enemy_teams[0]  # Get the next enemy team
        result = self.battle.battle(self.player_team, enemy_team)

        if result == Battle.Result.TEAM1:
            self.player_team_lives -= 1
        elif result == Battle.Result.TEAM2:
            enemy_team_lives -= 1
        elif result == Battle.Result.DRAW:
            self.player_team_lives -= 1
            enemy_team_lives -= 1

        self.enemy_teams[0] = (enemy_team, enemy_team_lives)  # Update the enemy team in the array

        return result, self.player_team, enemy_team, self.player_team_lives, enemy_team_lives


def out_of_meta(self) -> ArrayR[Element]:
    if self.enemy_teams is None:
        raise ValueError("Enemy teams have not been generated yet.")

        # Collect elements from all enemy teams and filter out duplicates
    enemy_elements = set()
    for (enemy_team, _) in self.enemy_teams:
        enemy_elements.update(enemy_team.get_all_elements())

    # Find elements not present in the player team's elements
    missing_elements = [element for element in Element if
                        element not in self.player_team.get_all_elements() and element in enemy_elements]

    # Return the missing elements in the order of Elements enum
    return ArrayR[Element](missing_elements)


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
