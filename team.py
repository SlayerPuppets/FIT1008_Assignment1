from __future__ import annotations
from enum import auto
from typing import Optional, TYPE_CHECKING

from base_enum import BaseEnum
from monster_base import MonsterBase
from random_gen import RandomGen
from helpers import get_all_monsters

from data_structures.referential_array import ArrayR
from data_structures.queue_adt import CircularQueue

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
        """The method is simple assignment of variables, which makes it complexity O(1) best/worst cases"""
        # Add any preinit logic here.
        self.backup_monsters = None
        self.team_mode = team_mode
        self.provided_monsters = None
        self.toggle = True  # True - Descending

        if team_mode == MonsterTeam.TeamMode.OPTIMISE:
            self.sort_key = kwargs.get('sort_key', None)

        if self.team_mode == MonsterTeam.TeamMode.FRONT or self.team_mode == MonsterTeam.TeamMode.BACK:
            self.team_data = CircularQueue(self.TEAM_LIMIT)
        elif self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            self.team_data = ArrayR(self.TEAM_LIMIT)
            self.team_count = 0

        if selection_mode == self.SelectionMode.RANDOM:
            self.select_randomly(**kwargs)
        elif selection_mode == self.SelectionMode.MANUAL:
            self.select_manually(**kwargs)
        elif selection_mode == self.SelectionMode.PROVIDED:
            self.select_provided(**kwargs)
        else:
            raise ValueError(f"selection_mode {selection_mode} not supported.")

    def _get_sort_value(self, monster: MonsterBase) -> int:
        """
        Retrieve the sorting value for the given monster based on the sort_key.

        :complexity: O(1)
        """
        # Check which attribute of the monster needs to be retrieved for sorting
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
        """
        Add a monster instance to the team based on the team_mode.

        :complexity: Best O(1), Worst O(n) where n is the length of the team.
        """
        # Check if the team has reached its limit
        if len(self) >= self.TEAM_LIMIT:
            raise ValueError("Team is already full!")

        # Depending on the team_mode, add the monster to the appropriate position in the team
        if self.team_mode == self.TeamMode.FRONT:
            old_data = [self.team_data.serve() for _ in range(len(self.team_data))]
            self.team_data.append(monster)
            for m in old_data:
                self.team_data.append(m)

        elif self.team_mode == self.TeamMode.BACK:
            # Use append() method of CircularQueue for BACK mode
            self.team_data.append(monster)

        elif self.team_mode == self.TeamMode.OPTIMISE:
            new_team = ArrayR(self.TEAM_LIMIT)
            inserted = False
            j = 0  # To track the index in the new_team Array
            for i in range(self.team_count):
                if self.toggle:
                    condition = not inserted and self._get_sort_value(monster) > self._get_sort_value(self.team_data[i])
                else:
                    condition = not inserted and self._get_sort_value(monster) < self._get_sort_value(self.team_data[i])

                if condition:
                    new_team[j] = monster
                    inserted = True
                    j += 1
                new_team[j] = self.team_data[i]
                j += 1
            if not inserted:
                new_team[j] = monster
            self.team_data = new_team
            self.team_count += 1

    def retrieve_from_team(self) -> MonsterBase:
        """
        Retrieve a monster instance from the team based on the team_mode.

        :complexity: O(n) where n is the length of the team.
        """
        # Check if the team is empty
        if len(self) == 0:
            raise ValueError("Team is empty")

        # Depending on the team_mode, retrieve the monster from the appropriate position in the team
        if self.team_mode in ArrayR(2).from_list([self.TeamMode.FRONT, self.TeamMode.BACK]):
            return self.team_data.serve()

        elif self.team_mode == self.TeamMode.OPTIMISE:
            monster = self.team_data[0]
            for i in range(1, self.team_count):
                self.team_data[i - 1] = self.team_data[i]

            self.team_data[self.team_count - 1] = None
            # Decrease the count of monsters
            self.team_count -= 1
            return monster

    def special(self) -> None:
        """
        Executes a special team operation based on the current team mode.

        :complexity: O(n) for all team modes where n is the number of monsters.
        """
        if self.team_mode == self.TeamMode.FRONT:
            # Determine how many elements need to be reversed.
            swaps = min(3, len(self.team_data))

            # Extract first 3 elements using CircularQueue methods.
            temp_arr_to_reverse = ArrayR(swaps)
            temp_arr_remaining = ArrayR(len(self.team_data) - swaps)

            for i in range(swaps):
                temp_arr_to_reverse[i] = self.team_data.serve()

            j = 0
            while not self.team_data.is_empty():
                temp_arr_remaining[j] = self.team_data.serve()
                j += 1

            # Now, add elements from temp_arr_to_reverse (in reverse order) to the team_data.
            for i in range(swaps - 1, -1, -1):
                self.team_data.append(temp_arr_to_reverse[i])
            for i in range(len(temp_arr_remaining)):
                self.team_data.append(temp_arr_remaining[i])

        elif self.team_mode == self.TeamMode.BACK:
            # Half the size of the team
            half_size = len(self.team_data) // 2
            # Store the first half in temp_arr1
            temp_arr1 = ArrayR(half_size)
            for i in range(half_size):
                temp_arr1[i] = self.team_data.serve()
            # Store the second half in temp_arr2
            temp_arr2 = ArrayR(len(self.team_data))
            index = 0
            while not self.team_data.is_empty():
                temp_arr2[index] = self.team_data.serve()
                index += 1
            # Create a new CircularQueue
            new_queue = CircularQueue(self.TEAM_LIMIT)
            # First, add the second half in reverse order
            for i in range(len(temp_arr2) - 1, -1, -1):
                new_queue.append(temp_arr2[i])
            # Then, add the first half
            for i in range(len(temp_arr1)):
                new_queue.append(temp_arr1[i])
            # Set the new queue to team_data
            self.team_data = new_queue

        elif self.team_mode == self.TeamMode.OPTIMISE:
            reversed_team_data = ArrayR(self.team_count)
            for i in range(self.team_count):
                reversed_team_data[i] = self.team_data[self.team_count - i - 1]
            self.team_data = reversed_team_data
            self.toggle = not self.toggle

    def regenerate_team(self) -> None:
        """
        Regenerates the team by recreating each monster instance and resetting their attributes.

        :complexity: O(n) for all team modes where n is the number of monsters.
        """
        # If an original team backup exists, regenerate from it
        if self.backup_monsters is not None:
            self.team_data = self.backup_monsters

        else:
            if self.team_mode == self.TeamMode.FRONT or self.team_mode == self.TeamMode.BACK:
                new_team = CircularQueue(self.TEAM_LIMIT)
                for _ in range(len(self.team_data)):
                    m = self.team_data.serve()
                    new_team.append(type(m)(m.simple_mode, level=1))

            elif self.team_mode == self.TeamMode.OPTIMISE:
                n = len(self.team_data)
                for i in range(1, n):
                    key = self.team_data[i]
                    j = i - 1
                    key_value = self._get_sort_value(key)

                    if self.toggle:  # Descending order
                        while j >= 0 and key_value > self._get_sort_value(self.team_data[j]):
                            self.team_data[j + 1] = self.team_data[j]
                            j -= 1
                    else:  # Ascending order
                        while j >= 0 and key_value < self._get_sort_value(self.team_data[j]):
                            self.team_data[j + 1] = self.team_data[j]
                            j -= 1
                    self.team_data[j + 1] = key
                self.toggle = not self.toggle

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
                        self.add_to_team(monsters[x]())
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

        """
        Allow user to manually select monsters to add to the team.
        Complexity Analysis:
        Time Complexity: O(n) where n is the greater of team size and total number of available monsters.
        """

        # Fetch all available monsters.
        monsters = get_all_monsters()  # O(n) due to _make_all_monster_classes()

        # Loop until valid team size input is received.
        while True:
            try:
                team_size = int(input("How many monsters are there? "))

                # Validate team size.
                if team_size <= 0 or team_size > self.TEAM_LIMIT:
                    print("Team size must between 1 to {}.".format(self.TEAM_LIMIT))
                else:
                    break
            except ValueError:
                print("Invalid input. Please enter a valid team size.")

        # Initialize the selected_monsters array to hold the selected monsters.
        selected_monsters = ArrayR(team_size)
        sel_index = 0

        # Display all available monsters along with their spawnable status.
        print("MONSTERS Available:")
        for index, monster_class in enumerate(monsters, 1):
            spawnable_status = "✔️" if monster_class.can_be_spawned() else "❌"
            print(f"{index}: {monster_class.get_name()} [{spawnable_status}]")

        # Loop to manually select the monsters.
        while sel_index < team_size:
            try:
                selected_index = int(input("Which monster are you spawning? "))

                # Check if selected index is valid.
                if 1 <= selected_index <= len(monsters):
                    selected_monster_class = monsters[selected_index - 1]

                    # Check if monster can be spawned.
                    if selected_monster_class.can_be_spawned():

                        # Add to the selected_monsters list if not exceeding team limit.
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

        # Add the selected monsters to the team in the same order.
        for monster in selected_monsters:
            self.add_to_team(monster())

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
        :complexity: O(n), where n is the size of the provided_monsters array.
        """

        # Check if provided_monsters is None, raise an error if it is.
        if provided_monsters is None:
            raise ValueError("No provided monsters found.")

        # Loop through each provided monster class and add to the team.
        for monster_class in provided_monsters:  # O(n)
            # Check if the monster class can be spawned.
            if monster_class.can_be_spawned():  # O(1)
                self.add_to_team(monster_class())  # O(1) [Assuming add_to_team is O(1)]
            else:
                # Raise an error if an invalid monster class is provided.
                raise ValueError(f"Invalid monster class provided: {monster_class}")

        # Create a copy of the original team based on its mode.
        self.backup_monsters = self.clone_team_data()  # O(n)

    def clone_team_data(self):
        """
        Clones the team data based on its mode and returns a deep copy.

        :complexity: O(n) where n is the number of monsters in the team.
        """
        if self.team_mode == MonsterTeam.TeamMode.OPTIMISE:
            # If team_mode is OPTIMISE, clone ArrayR
            cloned_team = ArrayR(self.TEAM_LIMIT)
            for i in range(len(self)):
                monster_instance = self.team_data[i]
                # Create a new instance for each monster
                cloned_team[i] = type(monster_instance)()

        elif self.team_mode in [MonsterTeam.TeamMode.FRONT, MonsterTeam.TeamMode.BACK]:
            # If team_mode is FRONT or BACK, clone CircularQueue
            cloned_team = CircularQueue(self.TEAM_LIMIT)
            temp_queue = CircularQueue(self.TEAM_LIMIT)

            # Empty the current queue into the temp_queue
            while not self.team_data.is_empty():
                monster_instance = self.team_data.serve()
                # Create a new instance for each monster and add to cloned_team and temp_queue
                new_monster = type(monster_instance)()
                cloned_team.append(new_monster)
                temp_queue.append(new_monster)

            # Restore the original queue from the temp_queue
            while not temp_queue.is_empty():
                self.team_data.append(temp_queue.serve())

        return cloned_team

    def choose_action(self, currently_out: MonsterBase, enemy: MonsterBase) -> Battle.Action:
        # This is just a placeholder function that doesn't matter much for testing.
        from battle import Battle
        if currently_out.get_speed() >= enemy.get_speed() or currently_out.get_hp() >= enemy.get_hp():
            return Battle.Action.ATTACK
        return Battle.Action.SWAP

    def __len__(self):
        """
        Time Complexity: O(n), simply return the size.
        """
        if self.team_mode == self.TeamMode.FRONT or self.team_mode == self.TeamMode.BACK:
            return len(self.team_data)
        elif self.team_mode == self.TeamMode.OPTIMISE:
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