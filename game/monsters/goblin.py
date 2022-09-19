from game.classes.attack import Attack
from game.classes.monster import Monster


class Goblin(Monster):

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
