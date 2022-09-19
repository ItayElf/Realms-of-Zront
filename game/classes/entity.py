from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from game.classes.attack import Attack


@dataclass
class Entity(ABC):
    """A base class for the character and monster classes"""
    name: str
    level: int
    current_hp: int

    def __post_init__(self):
        if self.__class__ == Entity:
            raise TypeError("Cannot instantiate abstract class.")

    @property
    @abstractmethod
    def max_hp(self) -> int:
        """Returns the maximum hitpoints of the entity"""

    @property
    @abstractmethod
    def initiative(self) -> int:
        """Returns the initiative of the entity"""

    @property
    @abstractmethod
    def dodge(self) -> float:
        """Returns the dodge of the entity"""

    @property
    @abstractmethod
    def attacks(self) -> list[Attack]:
        """Returns the attacks of the entity"""
