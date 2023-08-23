from __future__ import annotations
from enum import auto
from typing import Optional

from base_enum import BaseEnum
from team import MonsterTeam


class Battle:

    class Action(BaseEnum):
        ATTACK = auto()
        SWAP = auto()
        SPECIAL = auto()

    class Result(BaseEnum):
        TEAM1 = auto()
        TEAM2 = auto()
        DRAW = auto()

    def __init__(self, verbosity=0) -> None:
        self.verbosity = verbosity

    def process_turn(self) -> Optional[Battle.Result]:
        """
        Process a single turn of the battle. Should:
        * process actions chosen by each team
        * level and evolve monsters
        * remove fainted monsters and retrieve new ones.
        * return the battle result if completed.
        """
        # Determine the actions for each team
        action_team1 = self.team1.choose_action()
        action_team2 = self.team2.choose_action()

        # Process actions for team 1
        if action_team1 == Battle.Action.SWAP:
            self.out1 = self.team1.retrieve_from_team()
            if self.out1 is None:
                return Battle.Result.TEAM2
        elif action_team1 == Battle.Action.SPECIAL:
            self.out1.special(self.team1)
            self.out1 = self.team1.retrieve_from_team()
            if self.out1 is None:
                return Battle.Result.TEAM2

        # Process actions for team 2
        if action_team2 == Battle.Action.SWAP:
            self.out2 = self.team2.retrieve_from_team()
            if self.out2 is None:
                return Battle.Result.TEAM1
        elif action_team2 == Battle.Action.SPECIAL:
            self.out2.special(self.team2)
            self.out2 = self.team2.retrieve_from_team()
            if self.out2 is None:
                return Battle.Result.TEAM1

        # Determine attack order based on speed
        if self.out1.get_speed() > self.out2.get_speed():
            attacker, defender = self.out1, self.out2
        elif self.out1.get_speed() < self.out2.get_speed():
            attacker, defender = self.out2, self.out1
        else:
            attacker, defender = self.out1, self.out2

        # Perform attacks
        damage_attacker = attacker.calculate_damage(defender)
        defender.take_damage(damage_attacker)

        # Check for fainted monsters and retrieve new ones
        if defender.get_hp() <= 0:
            if attacker == self.out1:
                self.out2 = self.team2.retrieve_from_team()
            else:
                self.out1 = self.team1.retrieve_from_team()

        # Check for battle result
        if self.team1.is_empty():
            return Battle.Result.TEAM2
        elif self.team2.is_empty():
            return Battle.Result.TEAM1

        # Check for level up and evolution
        if self.out1.get_hp() > 0:
            self.out1.level_up()
            if self.out1.get_evolution() and self.out1.get_level() != self.out1.get_original_level():
                self.out1.evolve()
        if self.out2.get_hp() > 0:
            self.out2.level_up()
            if self.out2.get_evolution() and self.out2.get_level() != self.out2.get_original_level():
                self.out2.evolve()

        return None  # Battle is not yet finished

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        # Add any pregame logic here.
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        # Add any postgame logic here.
        return result

if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
