import abc

from data_structures.referential_array import ArrayR


class Stats(abc.ABC):

    @abc.abstractmethod
    def get_attack(self):
        pass

    @abc.abstractmethod
    def get_defense(self):
        pass

    @abc.abstractmethod
    def get_speed(self):
        pass

    @abc.abstractmethod
    def get_max_hp(self):
        pass


class SimpleStats(Stats):
    """Unless stated otherwise, all methods in this classes are O(1) best/worst case."""

    def __init__(self, attack, defense, speed, max_hp) -> None:
        # TODO: Implement
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.max_hp = max_hp

    def get_attack(self):
        return self.attack

    def get_defense(self):
        return self.defense

    def get_speed(self):
        return self.speed

    def get_max_hp(self):
        return self.max_hp


class ComplexStats(Stats):

    def __init__(
            self,
            attack_formula: ArrayR[str],
            defense_formula: ArrayR[str],
            speed_formula: ArrayR[str],
            max_hp_formula: ArrayR[str],
    ) -> None:
        # TODO: Implement
        pass

    def get_attack(self, level: int):
        raise NotImplementedError

    def get_defense(self, level: int):
        raise NotImplementedError

    def get_speed(self, level: int):
        raise NotImplementedError

    def get_max_hp(self, level: int):
        raise NotImplementedError
