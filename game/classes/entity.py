from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from game.classes.attack import Attack
from game.classes.conditions import Condition
from game.classes.traits import CTrait


@dataclass
class Entity(ABC):
    """A base class for the character and monster classes"""
    name: str
    level: int
    current_hp: int
    conditions: set[Condition] = field(default_factory=set)

    def __post_init__(self):
        if self.__class__ == Entity:
            raise TypeError("Cannot instantiate abstract class.")

    def has_trait(self, trait: CTrait) -> bool:
        """Returns whether the entity has a specific trait"""
        return trait in self.traits

    def has_condition(self, condition: Condition) -> bool:
        """Returns whether the entity has a specific condition"""
        return condition in self.conditions

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

    @property
    @abstractmethod
    def traits(self) -> list[CTrait]:
        """Returns the traits of the entity"""
