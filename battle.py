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
        action1 = self.team1.choose_action(self.out1, self.out2)
        action2 = self.team2.choose_action(self.out2, self.out1)

        # Process SWAP/SPECIAL actions first
        if action1 == Battle.Action.SWAP:
            self.team1.add_to_team(self.out1)
            self.out1 = self.team1.retrieve_from_team()
        elif action1 == Battle.Action.SPECIAL:
            self.team1.add_to_team(self.out1)
            self.team1.special()
            self.out1 = self.team1.retrieve_from_team()

        if action2 == Battle.Action.SWAP:
            self.team2.add_to_team(self.out2)
            self.out2 = self.team2.retrieve_from_team()
        elif action2 == Battle.Action.SPECIAL:
            self.team2.add_to_team(self.out2)
            self.team2.special()
            self.out2 = self.team2.retrieve_from_team()

        # Process ATTACK actions
        if action1 == Battle.Action.ATTACK and action2 != Battle.Action.ATTACK:
            self.out1.attack(self.out2)

        elif action2 == Battle.Action.ATTACK and action1 != Battle.Action.ATTACK:
            self.out2.attack(self.out1)

        elif action1 == Battle.Action.ATTACK and action2 == Battle.Action.ATTACK:
            if self.out1.get_speed() == self.out2.get_speed():
                self.out1.attack(self.out2)
                self.out2.attack(self.out1)
            elif self.out1.get_speed() > self.out2.get_speed():
                self.out1.attack(self.out2)
                if self.out2.alive():
                    self.out2.attack(self.out1)
            else:
                self.out2.attack(self.out1)
                if self.out1.alive():
                    self.out1.attack(self.out2)

        # if action1 == Battle.Action.ATTACK or action2 == Battle.Action.ATTACK:
        #     if self.out1.get_speed() == self.out2.get_speed():
        #         self.out1.attack(self.out2)
        #         self.out2.attack(self.out1)
        #     elif self.out1.get_speed() > self.out2.get_speed():
        #         self.out1.attack(self.out2)
        #         if self.out2.alive():
        #             self.out2.attack(self.out1)
        #     else:
        #         self.out2.attack(self.out1)
        #         if self.out1.alive():
        #             self.out1.attack(self.out2)

        if not self.out2.alive() and self.out1.alive():
            self.out1.level_up()
            if self.out1.ready_to_evolve():
                self.out1 = self.out1.evolve()
            self.out2 = self.team2.retrieve_from_team()
            if self.out2 is None:
                return Battle.Result.TEAM2

        if not self.out1.alive() and self.out2.alive():
            self.out2.level_up()
            if self.out2.ready_to_evolve():
                self.out2 = self.out2.evolve()
            self.out1 = self.team1.retrieve_from_team()
            if self.out1 is None:
                return Battle.Result.TEAM1

        # Subtract 1 from HP if both survive
        if self.out1.alive() and self.out2.alive():
            self.out1.set_hp(self.out1.get_hp() - 1)
            self.out2.set_hp(self.out2.get_hp() - 1)

    def battle(self, team1: MonsterTeam, team2: MonsterTeam) -> Battle.Result:
        if self.verbosity > 0:
            print(f"Team 1: {team1} vs. Team 2: {team2}")
        self.turn_number = 0
        self.team1 = team1
        self.team2 = team2
        self.out1 = team1.retrieve_from_team()
        self.out2 = team2.retrieve_from_team()
        result = None
        while result is None:
            result = self.process_turn()
        return result


if __name__ == "__main__":
    t1 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    t2 = MonsterTeam(MonsterTeam.TeamMode.BACK, MonsterTeam.SelectionMode.RANDOM)
    b = Battle(verbosity=3)
    print(b.battle(t1, t2))
