from dataclasses import dataclass
from enum import Enum

from game.classes.character import Character
from game.classes.item import Item


class Difficulty(Enum):
    EASY = 1
    NORMAL = 2
    HARD = 3
    DEADLY = 4


@dataclass
class GameState:
    """A class that represents the current state of the game"""
    difficulty: Difficulty
    party: list[Character]
    money: int
    items: list[Item]
