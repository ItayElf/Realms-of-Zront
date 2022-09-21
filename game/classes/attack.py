from dataclasses import dataclass, field

from game.classes.traits import ATrait


@dataclass
class Attack:
    name: str
    damage: tuple[int, int]
    targets: int = 1
    traits: list[ATrait] = field(default_factory=list)

    def has(self, trait: ATrait) -> bool:
        """Returns whether the attack has a specific attribute"""
        return trait in self.traits
