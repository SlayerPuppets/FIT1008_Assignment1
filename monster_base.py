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
        self.already_evo = False

    def get_level(self):
        """The current level of this monster instance"""
        return self.level

    def level_up(self):
        """Increase the level of this monster instance by 1"""
        HP_sub = self.get_max_hp() - self.get_hp()
        self.level += 1
        self.set_hp(self.get_max_hp() - HP_sub)
        self.already_evo = True

    def get_hp(self):
        """Get the current HP of this monster instance"""
        return self.hp

    def set_hp(self, val):
        """Set the current HP of this monster instance"""
        self.hp = val

    def get_attack(self):
        """Get the attack of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().attack

        else:
            return self.get_complex_stats().attack

    def get_defense(self):
        """Get the defense of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().defense

        else:
            return self.get_complex_stats().defense

    def get_speed(self):
        """Get the speed of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().speed

        else:
            return self.get_complex_stats().speed

    def get_max_hp(self):
        """Get the maximum HP of this monster instance"""
        if self.simple_mode:
            return self.get_simple_stats().max_hp

        else:
            return self.get_complex_stats().max_hp

    def alive(self) -> bool:
        """Whether the current monster instance is alive (HP > 0 )"""
        return self.get_hp() != 0

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
        return self.get_evolution() is not None and self.alive() and self.already_evo

    def evolve(self) -> MonsterBase:
        """Evolve this monster instance by returning a new instance of a monster class."""
        if self.ready_to_evolve():
            evolution_class = self.get_evolution()
            new_monster = evolution_class(simple_mode=self.simple_mode, level=self.level)
            new_monster.set_hp(new_monster.get_max_hp() - (self.get_max_hp()-self.get_hp()))  # Preserve HP
            return new_monster
        else:
            return self

    def __str__(self):
        return ("LV." + str(self.get_level()) + " " + self.get_name() + ", " + str(self.get_hp()) +
                     "/" + str(self.get_max_hp()) + " HP")


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
