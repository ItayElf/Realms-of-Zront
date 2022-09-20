from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Item(ABC):
    name: str

    def __post_init__(self):
        if self.__class__ == Item:
            raise TypeError("Cannot instantiate abstract class.")

    @property
    @abstractmethod
    def description(self) -> str:
        """returns the description of the item"""
