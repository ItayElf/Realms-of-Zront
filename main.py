from game.characters.fighter import Fighter
from game.classes.game_state import GameState, Difficulty
from game.gameplay.battle import battle
from game.monsters.goblin import Goblin


def main():
    game_state = GameState(Difficulty.DEADLY, [Fighter("Bob", 1, 10, 0), Fighter("Bill", 1, 10, 0)], 0, [])
    battle(
        game_state,
        [Goblin(1), Goblin(1), Goblin(1), Goblin(1)]
    )


if __name__ == '__main__':
    main()
