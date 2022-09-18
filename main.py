from game.characters.fighter import Fighter
from game.gameplay.battle import battle
from game.monsters.goblin import Goblin


def main():
    battle([Fighter("Bob", 1, 0, 10)], [Goblin("Goblin", 1, 0, 5)])


if __name__ == '__main__':
    main()
