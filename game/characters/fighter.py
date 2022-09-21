from game.classes.attack import Attack
from game.classes.character import Character
from game.classes.traits import CTrait, ATrait


class Fighter(Character):

    @property
    def traits(self) -> list[CTrait]:
        return [CTrait.FRONTLINE]

    @property
    def max_hp(self) -> int:
        return 5 + 5 * self.level

    @property
    def initiative(self) -> int:
        return 1 + self.level

    @property
    def dodge(self) -> float:
        return 0.2

    @property
    def attacks(self) -> list[Attack]:
        a = [Attack("Longsword", (1 + self.level // 3, 6 + self.level // 3))]
        if self.level >= 2:
            a.append(Attack("Stunning Strike", (1 + (self.level - 1) // 3, 4 + (self.level - 1) // 3),
                            traits=[ATrait.STUNNING]))
        return a
