from game.attack import Attack
from game.characters.character import Character


class Fighter(Character):

    @property
    def max_hp(self) -> int:
        return 5 + 5 * self.level

    @property
    def initiative(self) -> int:
        return 1 + self.level

    @property
    def dodge(self) -> float:
        return 0.3

    @property
    def attack(self) -> Attack:
        return Attack("Longsword", (1, 6))
