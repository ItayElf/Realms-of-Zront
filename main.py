from game.characters.fighter import Fighter
from game.gameplay.battle import battle
from game.monsters.goblin import Goblin


def main():
    battle(
        [Fighter("Bob", 1, 10, 0), Fighter("Bill", 1, 10, 0)],
        [Goblin(1), Goblin(1), Goblin(1), Goblin(1)]
    )


if __name__ == '__main__':
    main()
