from abc import ABC, abstractmethod
from dataclasses import dataclass

from game.classes.attack import Attack

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
class Character(ABC):
    """Base class for game characters"""
    name: str
    level: int
    xp: float
    current_hp: int

    def __post_init__(self):
        if self.__class__ == Character:
            raise TypeError("Cannot instantiate abstract class.")

    def level_up(self):
        """Checks if the character needs to level up and does so if needed"""
        if self.xp >= xp_chart[self.level]:
            self.level += 1

    @property
    @abstractmethod
    def max_hp(self) -> int:
        """Returns the maximum hitpoints of the character"""

    @property
    @abstractmethod
    def initiative(self) -> int:
        """Returns the initiative of the character"""

    @property
    @abstractmethod
    def dodge(self) -> float:
        """Returns the dodge of the character"""

    @property
    @abstractmethod
    def attacks(self) -> list[Attack]:
        """Returns the attacks of the character"""
