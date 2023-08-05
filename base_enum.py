from enum import Enum

class BaseEnum(Enum):

    def __eq__(self, __value: object) -> bool:
        """
        Python, being an interpreted language,
        has issues when classes are imported from two different locations

        As such we define equality to work on a string comparison instead.
        """
        if self.__class__.__name__ == __value.__class__.__name__:
            return self.value == __value.value
        return False
