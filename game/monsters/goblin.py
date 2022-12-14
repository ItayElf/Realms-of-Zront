import random

from game.classes.attack import Attack
from game.classes.item import Item
from game.classes.monster import Monster
from game.classes.traits import CTrait


class Goblin(Monster):

    @property
    def loot(self) -> int | Item:
        return random.randint(0, 5)

    @property
    def traits(self) -> list[CTrait]:
        return []

    @property
    def xp_reward(self):
        return 25 * self.level

    @property
    def max_hp(self) -> int:
        return 3 + 2 * self.level

    @property
    def initiative(self) -> int:
        return 0 + self.level

    @property
    def dodge(self) -> float:
        return 0.1

    @property
    def attacks(self) -> list[Attack]:
        return [Attack("Dagger", (1, 3))]
