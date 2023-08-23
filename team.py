from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR

if TYPE_CHECKING:
    from battle import Battle


class MonsterTeam:
    class TeamMode(BaseEnum):

        FRONT = auto()
        BACK = auto()
        OPTIMISE = auto()

    class SelectionMode(BaseEnum):

        RANDOM = auto()
        MANUAL = auto()
        PROVIDED = auto()

    class SortMode(BaseEnum):

        HP = auto()
        ATTACK = auto()
        DEFENSE = auto()
        SPEED = auto()
        LEVEL = auto()

    TEAM_LIMIT = 6

    def __init__(self, team_mode: TeamMode, selection_mode, **kwargs) -> None:
        # Add any preinit logic here.
        self.team_count = 0
        self.team_mode = team_mode
        if team_mode == MonsterTeam.TeamMode.OPTIMISE:
            self.sort_key = kwargs.get('sort_key', None)
        self.team_data = ArrayR(self.TEAM_LIMIT)

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def _get_sort_value(self, monster: MonsterBase) -> int:
        if self.sort_key == self.SortMode.HP:
            return monster.get_hp()
        elif self.sort_key == self.SortMode.ATTACK:
            return monster.get_attack()
        elif self.sort_key == self.SortMode.SPEED:
            return monster.get_speed()
        elif self.sort_key == self.SortMode.DEFENSE:
            return monster.get_defense()
        elif self.sort_key == self.SortMode.LEVEL:
            return monster.get_level()
        else:
            raise ValueError(f"Unsupported sort_key: {self.sort_key}")

    def add_to_team(self, monster: MonsterBase):
        if self.team_count >= self.TEAM_LIMIT:
            raise ValueError("Team is already full!")

        new_team = ArrayR(self.TEAM_LIMIT)
        if self.team_mode == self.TeamMode.FRONT:
            new_team[0] = monster
            for i in range(self.team_count):  # Use team_count here
                new_team[i + 1] = self.team_data[i]
        elif self.team_mode == self.TeamMode.BACK:
            for i in range(self.team_count):  # Use team_count here
                new_team[i] = self.team_data[i]
            new_team[self.team_count] = monster
        elif self.team_mode == self.TeamMode.OPTIMISE:
            inserted = False
            for i in range(self.team_count):  # Use team_count here
                if not inserted and self.team_data[i] is not None and self._get_sort_value(
                        monster) > self._get_sort_value(self.team_data[i]):
                    new_team[i] = monster
                    inserted = True
                new_team[i + int(inserted)] = self.team_data[i]
            if not inserted:
                new_team[self.team_count] = monster

        self.team_data = new_team
        self.team_count += 1
        # new_team = ArrayR(self.TEAM_LIMIT)
        #
        # if self.team_mode == self.TeamMode.FRONT:
        #     new_team[0] = monster
        #     for i in range(len(self.team_data)):
        #         new_team[i + 1] = self.team_data[i]
        # elif self.team_mode == self.TeamMode.BACK:
        #     for i in range(len(self.team_data)):
        #         new_team[i] = self.team_data[i]
        #     new_team[len(self.team_data)] = monster
        # elif self.team_mode == self.TeamMode.OPTIMISE:
        #     inserted = False
        #
        #     for i in range(len(self.team_data)):
        #         if monster.get_hp() >= self.team_data[i].get_hp():
        #             new_team[i] = monster
        #             for j in range(i, len(self.team_data)):
        #                 new_team[j + 1] = self.team_data[j]
        #             inserted = True
        #             break
        #         new_team[i] = self.team_data[i]
        #     if not inserted:
        #         new_team[len(self.team_data)] = monster
        #
        # self.team_data = new_team

    def retrieve_from_team(self) -> MonsterBase:
        if self.team_count == 0:
            raise ValueError("Team is empty")
        monster = self.team_data[0]
        for i in range(1, self.team_count):
            self.team_data[i - 1] = self.team_data[i]

        self.team_data[self.team_count - 1] = None

        # Decrease the count of monsters
        self.team_count -= 1
        return monster

    def special(self) -> None:
        if self.team_mode == self.TeamMode.FRONT:
            # We'll only perform swaps for half of the team, as we're swapping in pairs.
            swaps = min(3, self.team_count // 2)
            for i in range(swaps):
                self.team_data[i], self.team_data[self.team_count - i - 1] = self.team_data[self.team_count - i - 1], \
                    self.team_data[i]
        if self.team_mode == MonsterTeam.TeamMode.BACK:
            mid_point = self.team_count // 2
            new_team = ArrayR(self.TEAM_LIMIT)
            # First, place the reversed second half of the original team into the new_team
            for idx in range(mid_point, self.team_count):
                new_team[idx - mid_point] = self.team_data[self.team_count - 1 - (idx - mid_point)]
            # Then, append the first half of the original team into the new_team
            for idx in range(mid_point):
                new_team[self.team_count - mid_point + idx] = self.team_data[idx]

            self.team_data = new_team
        elif self.team_mode == self.TeamMode.OPTIMISE:
            reversed_team_data = ArrayR(self.team_count)  # Use team_count to ensure the correct size.
            for i in range(self.team_count):  # Loop up to team_count to avoid None values.
                reversed_team_data[i] = self.team_data[self.team_count - i - 1]
            self.team_data = reversed_team_data


    def regenerate_team(self) -> None:
        """
        Regenerates the team by recreating each monster instance and resetting their attributes.

        :complexity: O(n), where n is the size of the team.
        """
        new_team = ArrayR(self.TEAM_LIMIT)
        for i in self.team_data:
            new_monster = type(self.team_data[i])(self.team_data[i].simple_mode,
                                                  level=1)  # Recreate the monster instance
            new_team[i] = new_monster  # Add the monster to the new team
        self.team_data = new_team

    def select_randomly(self):
        team_size = RandomGen.randint(1, self.TEAM_LIMIT)
        monsters = get_all_monsters()
        n_spawnable = 0
        for x in range(len(monsters)):
            if monsters[x].can_be_spawned():
                n_spawnable += 1

        for _ in range(team_size):
            spawner_index = RandomGen.randint(0, n_spawnable - 1)
            cur_index = -1
            for x in range(len(monsters)):
                if monsters[x].can_be_spawned():
                    cur_index += 1
                    if cur_index == spawner_index:
                        # Spawn this monster
                        self.add_to_team(monsters[x])
                        break
            else:
                raise ValueError("Spawning logic failed.")

    def select_manually(self):
        """
        Prompt the user for input on selecting the team.
        Any invalid input should have the code prompt the user again.

        First input: Team size. Single integer
        For _ in range(team size):
            Next input: Prompt selection of a Monster class.
                * Should take a single input, asking for an integer.
                    This integer corresponds to an index (1-indexed) of the helpers method
                    get_all_monsters()
                * If invalid of monster is not spawnable, should ask again.

        Add these monsters to the team in the same order input was provided. Example interaction:

        How many monsters are there? 2
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 38
        MONSTERS Are:
        1: Flamikin [✔️]
        2: Infernoth [❌]
        3: Infernox [❌]
        4: Aquariuma [✔️]
        5: Marititan [❌]
        6: Leviatitan [❌]
        7: Vineon [✔️]
        8: Treetower [❌]
        9: Treemendous [❌]
        10: Rockodile [✔️]
        11: Stonemountain [❌]
        12: Gustwing [✔️]
        13: Stormeagle [❌]
        14: Frostbite [✔️]
        15: Blizzarus [❌]
        16: Thundrake [✔️]
        17: Thunderdrake [❌]
        18: Shadowcat [✔️]
        19: Nightpanther [❌]
        20: Mystifly [✔️]
        21: Telekite [❌]
        22: Metalhorn [✔️]
        23: Ironclad [❌]
        24: Normake [❌]
        25: Strikeon [✔️]
        26: Venomcoil [✔️]
        27: Pythondra [✔️]
        28: Constriclaw [✔️]
        29: Shockserpent [✔️]
        30: Driftsnake [✔️]
        31: Aquanake [✔️]
        32: Flameserpent [✔️]
        33: Leafadder [✔️]
        34: Iceviper [✔️]
        35: Rockpython [✔️]
        36: Soundcobra [✔️]
        37: Psychosnake [✔️]
        38: Groundviper [✔️]
        39: Faeboa [✔️]
        40: Bugrattler [✔️]
        41: Darkadder [✔️]
        Which monster are you spawning? 2
        This monster cannot be spawned.
        Which monster are you spawning? 1
        """

        """"    Time Complexity Analysis:

        Prompting for team size: O(1)
        Looping through the team size and monster selection process: O(n)
        Within this loop, getting available monster classes and printing them: O(k), where k is the number of available monsters
        Each selection process and checks: O(1)
        Looping through the selected monsters and adding them to the team: O(n)
        Overall worst-case time complexity: O(n * k), where n is the team size and k is the number of available monsters.
        Overall best-case time complexity: O(n * k), same as worst-case.
        """
        # while True:
        #     try:
        #         team_size = int(input("How many monsters are there? "))
        #         if 1 <= team_size <= self.TEAM_LIMIT:
        #             break
        #         else:
        #             print(f"Team size should be between 1 and {self.TEAM_LIMIT}.")
        #     except ValueError:
        #         print("Invalid input. Please enter a valid integer.")
        #
        # print("MONSTERS Are:")
        # monsters = get_all_monsters()
        # for i, monster_cls in enumerate(monsters, start=1):
        #     print(f"{i}: {monster_cls.get_name()} [{'✔️' if monster_cls.can_be_spawned() else '❌'}]")
        #
        # # For each monster in the team
        # for _ in range(team_size):
        #     while True:
        #         try:
        #             selection = int(input("Which monster are you spawning? "))
        #             if 1 <= selection <= len(monsters) and monsters[selection - 1].can_be_spawned():
        #                 self.add_to_team(monsters[selection - 1])
        #                 break
        #             else:
        #                 print("Invalid selection. Please choose a valid monster.")
        #         except ValueError:
        #             print("Invalid input. Please enter a valid integer.")

        # try:
        #     # Prompt user for team size
        #     team_size = int(input("How many monsters are there? "))
        #     if team_size <= 0:
        #         print("Team size must be a positive integer.")
        #         return
        #
        #     # Get the available monster classes
        #     monsters = get_all_monsters()
        #
        #     # Initialize an empty array to store selected monsters
        #     selected_monsters = ArrayR(self.TEAM_LIMIT)
        #     sel_index = 0
        #
        #     # Prompt user for each monster in the team
        #     for _ in range(team_size):
        #         print("MONSTERS Available:")
        #         for index, monster_class in enumerate(monsters, 1):
        #             spawnable_status = "✔️" if monster_class.can_be_spawned() else "❌"
        #             print(f"{index}: {monster_class.get_name()} [{spawnable_status}]")
        #
        #         while True:
        #             try:
        #                 selected_index = int(input("Which monster are you spawning? "))
        #                 if 1 <= selected_index <= len(monsters):
        #                     selected_monster_class = monsters[selected_index - 1]
        #                     if selected_monster_class.can_be_spawned():
        #                         selected_monsters[sel_index] = selected_monster_class
        #                         sel_index += 1
        #                         break
        #                     else:
        #                         print("This monster cannot be spawned. Please select another.")
        #                 else:
        #                     print("Invalid monster index. Please try again.")
        #             except ValueError:
        #                 print("Invalid input. Please enter a valid monster index.")
        #
        #     # Add the selected monsters to the team in the same order
        #     for monster in selected_monsters:
        #         self.add_to_team(monster)
        #
        # except ValueError:
        #     print("Invalid input. Please enter a valid team size.")

        monsters = get_all_monsters()

        while True:
            try:
                team_size = int(input("How many monsters are there? "))
                if team_size <= 0 or team_size > self.TEAM_LIMIT:
                    print("Team size must between 1 to {}.".format(self.TEAM_LIMIT))
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid team size.")

        selected_monsters = ArrayR(team_size)
        sel_index = 0

        print("MONSTERS Available:")
        for index, monster_class in enumerate(monsters, 1):
            spawnable_status = "✔️" if monster_class.can_be_spawned() else "❌"
            print(f"{index}: {monster_class.get_name()} [{spawnable_status}]")

        while sel_index < team_size:
            try:
                selected_index = int(input("Which monster are you spawning? "))
                if 1 <= selected_index <= len(monsters):
                    selected_monster_class = monsters[selected_index - 1]
                    if selected_monster_class.can_be_spawned():
                        if sel_index < self.TEAM_LIMIT:
                            selected_monsters[sel_index] = selected_monster_class
                            sel_index += 1
                            print(f"{selected_monster_class.get_name()} added to the team.")
                        else:
                            print("Team is already full.")
                    else:
                        print("This monster cannot be spawned. Please select another.")
                else:
                    print("Invalid monster index. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a valid monster index.")

        # Add the selected monsters to the team in the same order
        for monster in selected_monsters:
            self.add_to_team(monster)

    def select_provided(self, provided_monsters: Optional[ArrayR[type[MonsterBase]]] = None, **kwargs):
        """
        Generates a team based on a list of already provided monster classes.

        While the type hint imples the argument can be none, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        Example input:
        [Flamikin, Aquariuma, Gustwing] <- These are all classes.

        Example team if in TeamMode.FRONT:
        [Gustwing Instance, Aquariuma Instance, Flamikin Instance]
        """

        """
        Generates a team based on a list of already provided monster classes.

        While the type hint implies the argument can be None, this method should never be called without the list.
        Monsters should be added to the team in the same order as the provided array.

        :param provided_monsters: ArrayR of MonsterBase subclasses to form the initial team.
        :complexity: O(n), where n is the size of the provided_monsters array.
        """
        # self.team_data = ArrayR(self.TEAM_LIMIT)
        #
        # # Loop through the provided monsters and add them to the team
        # for monster_class in provided_monsters:
        #     if len(self.team_data) >= self.TEAM_LIMIT:
        #         break  # Stop if the team is already full
        #     new_monster = monster_class(simple_mode=True, level=1)
        #     self.add_to_team(new_monster)

        if provided_monsters is None:
            raise ValueError("No provided monsters found.")

        for monster_class in provided_monsters:
            if monster_class.can_be_spawned():
                self.add_to_team(monster_class())
            else:
                raise ValueError(f"Invalid monster class provided: {monster_class}")

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

    def __len__(self):
        return self.team_count


if __name__ == "__main__":
    team = MonsterTeam(
        team_mode=MonsterTeam.TeamMode.OPTIMISE,
        selection_mode=MonsterTeam.SelectionMode.RANDOM,
        sort_key=MonsterTeam.SortMode.HP,
    )
    print(team)
    while len(team):
        print(team.retrieve_from_team())
