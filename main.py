from game.characters.fighter import Fighter
from game.classes.game_state import GameState, Difficulty
from game.gameplay.battle import battle
from game.items.healing_item import HealingItem
from game.monsters.goblin import Goblin


def main():
    game_state = GameState(Difficulty.DEADLY, [Fighter("Bob", 3, 10), Fighter("Bill", 4, 10)], 0,
                           [HealingItem("Potion of Lesser Healing", 1, 4)])
    battle(
        game_state,
        [Goblin(1), Goblin(1), Goblin(1), Goblin(1)]
    )


if __name__ == '__main__':
    main()
