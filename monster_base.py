from __future__ import annotations
import abc
from elements import EffectivenessCalculator, Element
from stats import Stats


class MonsterBase(abc.ABC):

    def __init__(self, simple_mode=True, level: int = 1) -> None:
        """
        Initialise an instance of a monster.

        :simple_mode: Whether to use the simple or complex stats of this monster
        :level: The starting level of this monster. Defaults to 1.
        """
        """The method is simple assignment of variables, which makes it complexity O(1) best/worst cases"""
        self.simple_mode = simple_mode
        self.level = level
        self.hp = self.get_max_hp()

        if self.simple_mode:
            simple_stats = self.get_simple_stats()
            self.attack = simple_stats.get_attack()
            self.defense = simple_stats.get_defense()
            self.speed = simple_stats.get_speed()
            self.max_hp = simple_stats.get_max_hp()
        else:
            complex_stats = self.get_complex_stats()
            self.attack = complex_stats.get_attack(level)
            self.defense = complex_stats.get_defense(level)
            self.speed = complex_stats.get_speed(level)
            self.max_hp = complex_stats.get_max_hp(level)

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        self.level += 1

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        return self.attack

    def get_defense(self):
        """Get the defense of this monster instance"""
        return self.defense

    def get_speed(self):
        """Get the speed of this monster instance"""
        return self.speed

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        return self.max_hp

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        raise NotImplementedError

    def attack(self, other: MonsterBase):
        """Attack another monster instance"""
        # Step 1: Compute attack stat vs. defense stat
        attack_stat = self.get_attack()
        defense_stat = self.get_defense()

        if defense_stat < attack_stat / 2:
            damage = attack_stat - defense_stat
        elif defense_stat < attack_stat:
            damage = attack_stat * 5 / 8 - defense_stat / 4
        else:
            damage = attack_stat / 4
        # Step 2: Apply type effectiveness
        attacker_element = Element.from_string(self.get_element())
        defender_element = Element.from_string(other.get_element())
        type_effectiveness = EffectivenessCalculator.get_effectiveness(attacker_element, defender_element)
        effective_damage = damage * type_effectiveness
        # Step 3: Ceil to int
        effective_damage = int(round(effective_damage))
        # Step 4: Lose HP
        other.set_hp(other.get_hp() - effective_damage)

    def ready_to_evolve(self) -> bool:
        """Whether this monster is ready to evolve. See assignment spec for specific logic."""
        return self.get_evolution() is not None and self.level != 1

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if self.ready_to_evolve():
            evolution_class = self.get_evolution()
            new_monster = evolution_class(simple_mode=self.simple_mode, level=self.level)
            new_monster.set_hp(self.get_hp())  # Preserve HP
            return new_monster
        else:
            return self

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
