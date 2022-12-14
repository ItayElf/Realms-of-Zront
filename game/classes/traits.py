from enum import Enum


class CTrait(Enum):
    """Characters traits"""
    FRONTLINE = "Other entities cannot be hit while this entity is alive."


class ATrait(Enum):
    """Attack traits"""
    STUNNING = "This attack has 50% to stun the enemy."
