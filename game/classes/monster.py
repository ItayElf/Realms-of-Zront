from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from game.classes.entity import Entity


@dataclass
class Monster(Entity, ABC):
    current_hp: int = field(init=False)
    name: str = field(init=False)

    def __post_init__(self):
        if self.__class__ == Monster:
            raise TypeError("Cannot instantiate abstract class.")
        self.current_hp = self.max_hp
        self.name = self.__class__.__name__

    @property
    @abstractmethod
    def xp_reward(self) -> int:
        """Returns the xp gained by killing the monster"""
