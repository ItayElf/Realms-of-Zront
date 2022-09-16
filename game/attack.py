from dataclasses import dataclass


@dataclass
class Attack:
    name: str
    damage: tuple[int, int]
    targets: int = 1
