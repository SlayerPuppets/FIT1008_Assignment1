from __future__ import annotations
import abc

from stats import Stats

class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level:int=1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        raise NotImplementedError

    def get_level(self):
        """The current level of this monster instance"""
        raise NotImplementedError

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        raise NotImplementedError

    def get_hp(self):
        """Get the current HP of this monster instance"""
        raise NotImplementedError

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        raise NotImplementedError

    def get_attack(self):
        """Get the attack of this monster instance"""
        raise NotImplementedError

    def get_defense(self):
        """Get the defense of this monster instance"""
        raise NotImplementedError

    def get_speed(self):
        """Get the speed of this monster instance"""
        raise NotImplementedError

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        raise NotImplementedError

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        raise NotImplementedError

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        # Step 2: Apply type effectiveness
        # Step 3: Ceil to int
        # Step 4: Lose HP
        raise NotImplementedError

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        raise NotImplementedError

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        raise NotImplementedError

    ### NOTE
    # Below is provided by the factory - classmethods
    # You do not need to implement them
    # And you can assume they have implementations in the above methods.

    @classmethod
    @abc.abstractmethod
    def get_name(cls) -> str:
        """Returns the name of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_description(cls) -> str:
        """Returns the description of the Monster - Same for all monsters of the same type."""
        pass

    @classmethod
    @abc.abstractmethod
    def get_evolution(cls) -> type[MonsterBase]:
        """
        Returns the class of the evolution of the Monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_element(cls) -> str:
        """
        Returns the element of the Monster.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def can_be_spawned(cls) -> bool:
        """
        Returns whether this monster type can be spawned on a team.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_simple_stats(cls) -> Stats:
        """
        Returns the simple stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass

    @classmethod
    @abc.abstractmethod
    def get_complex_stats(cls) -> Stats:
        """
        Returns the complex stats class for this monster, if it exists.
        Same for all monsters of the same type.
        """
        pass
