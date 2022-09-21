from abc import ABC
from dataclasses import dataclass

from game.classes.entity import Entity

xp_chart = {
    1: 300,
    2: 900,
    3: 2700,
    4: 6500,
    5: 14000,
    6: 23000,
    7: 34000,
    8: 48000,
    9: 64000,
}


@dataclass
class Character(Entity, ABC):
    """Base class for game characters"""
    xp: int = 0

    def __post_init__(self):
        if self.__class__ == Character:
            raise TypeError("Cannot instantiate abstract class.")

    def level_up(self):
        """Checks if the character needs to level up and does so if needed"""
        if self.xp >= xp_chart[self.level]:
            self.level += 1

    @property
    def xp_to_level_up(self):
        """Returns how much xp is needed to level up"""
        return xp_chart[self.level]
