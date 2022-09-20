import random
from dataclasses import dataclass

from game.classes.item import Item


@dataclass
class HealingItem(Item):
    min_healing: int
    max_healing: int

    def heal(self) -> int:
        """Returns how much this item heals"""
        return random.randint(self.min_healing, self.max_healing)

    @property
    def description(self) -> str:
        return f"Heals {self.min_healing} to {self.max_healing} hitpoints."