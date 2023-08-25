import abc

from data_structures.referential_array import ArrayR
from data_structures.stack_adt import ArrayStack


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
        self.attack_formula = attack_formula
        self.defense_formula = defense_formula
        self.speed_formula = speed_formula
        self.max_hp_formula = max_hp_formula

    def evaluate_expression(self, formula: ArrayR[str], level: int):
        stack = ArrayStack(len(formula))
        for expr in formula:
            if expr.isnumeric():
                stack.push(int(expr))
            elif expr == "level":
                stack.push(level)
            else:
                if expr in ['sqrt', 'middle']:
                    op3 = None
                    if expr == 'middle':
                        op3 = stack.pop()
                    op2 = stack.pop()
                    op1 = stack.pop() if not expr == 'sqrt' else op2
                    op2 = op3 if expr == 'sqrt' else op2
                else:
                    op2 = stack.pop()
                    op1 = stack.pop()
                if expr == '+':
                    stack.push(op1 + op2)
                elif expr == '-':
                    stack.push(op1 - op2)
                elif expr == '*':
                    stack.push(op1 * op2)
                elif expr == '/':
                    stack.push(op1 // op2)  # Integer division
                elif expr == 'power':
                    stack.push(op1 ** op2)
                elif expr == 'sqrt':
                    stack.push(int(op1 ** 0.5))
                elif expr == 'middle':
                    values = [op1, op2, op3]
                    values.sort()
                    stack.push(values[1])
        return stack.pop()

    def get_attack(self, level: int):
        return self.evaluate_expression(self.attack_formula, level)

    def get_defense(self, level: int):
        return self.evaluate_expression(self.defense_formula, level)

    def get_speed(self, level: int):
        return self.evaluate_expression(self.speed_formula, level)

    def get_max_hp(self, level: int):
        return self.evaluate_expression(self.max_hp_formula, level)
