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

    def __init__(self, attack, defense, speed, max_hp) -> None:
        # TODO: Implement
        pass

    def get_attack(self):
        raise NotImplementedError

    def get_defense(self):
        raise NotImplementedError

    def get_speed(self):
        raise NotImplementedError

    def get_max_hp(self):
        raise NotImplementedError

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
