import random

from rich import box

from game.classes.character import Character
from game.utils import clear, Table, prich


def battle(characters: list[Character], monsters: list[Character]):
    """Starts a battle between characters and monsters"""
    turn_order = list(sorted(characters + monsters, key=lambda x: x.initiative, reverse=True))
    while True:
        clear()
        turn_order = list(filter(lambda x: x.current_hp > 0, turn_order))
        characters = list(filter(lambda x: x.current_hp > 0, characters))
        monsters = list(filter(lambda x: x.current_hp > 0, monsters))
        if not characters:
            prich("Battle was lost.")
            input()
            return
        if not monsters:
            prich("Battle won!")
            input()
            return
        show_turn_order(turn_order)
        if turn_order[0] in characters:
            options(turn_order, monsters)
        else:
            monster_attack(turn_order, characters)


def monster_attack(turn_order: list[Character], characters: list[Character]):
    """Performs an attack with the current monster"""
    c = turn_order[0]
    prich(f"[bold]{c.name}[/] used [bold]{c.attack.name}[/].")
    targets: list[Character] = []
    available = characters.copy()
    while len(targets) < c.attack.targets:
        t = random.choice(available)
        available.remove(t)
        targets.append(t)
    for t in targets:
        resolve_attack(c, t)
    cycle(turn_order)
    input()


def player_attack(turn_order: list[Character], monsters: list[Character]):
    """Performs an attack with the player character"""
    c = turn_order[0]
    prich(
        f"[bold]{c.attack.name}[/]: {c.attack.targets} [white bold]target(s)[/], {c.attack.damage[0]} - {c.attack.damage[1]} [white bold]damage[/].")
    targets: list[Character] = []
    available = monsters.copy()
    while len(targets) < c.attack.targets:
        prich(f"Choose target no. {len(targets) + 1}:")
        for j, m in enumerate(sorted(available, key=lambda x: x.initiative, reverse=True)):
            prich(f"{j + 1}. {m.name} ({m.current_hp}/{m.max_hp} HP)")
        ans = input("> ")
        if not ans.isdigit() or int(ans) - 1 not in range(len(available)):
            prich("Invalid choice.")
            input()
            return
        targets.append(available[int(ans) - 1])
        available.remove(available[int(ans) - 1])
    for t in targets:
        resolve_attack(c, t)
    cycle(turn_order)
    input()


def resolve_attack(attacker: Character, defender: Character):
    """Resolves an attack between two characters"""
    if random.random() < defender.dodge:
        prich(f"{defender.name} avoided the attack.")
        return
    damage = random.randint(*attacker.attack.damage)
    prich(f"{defender.name} took {damage} damage.")
    defender.current_hp -= damage
    if defender.current_hp <= 0:
        prich(f"{defender.name} died.")


def options(turn_order: list[Character], monsters: list[Character]):
    """Shows available options"""
    prich("1. Attack\n2. Pass")
    ans = input("> ")
    if ans == "1":
        player_attack(turn_order, monsters)
    elif ans == "2":
        prich(f"{turn_order[0].name} passed its turn.")
        input()
        cycle(turn_order)
    else:
        prich("Invalid option.")
        input()


def show_turn_order(turn_order: list[Character]):
    table = Table(title="Turn Order", box=box.SIMPLE, title_style="bold italic")
    table.add_column("Name")
    table.add_column("Initiative")
    table.add_column("Hitpoints")
    table.add_column("Damage")
    table.add_column("Dodge")
    for c in turn_order:
        s = "bold" if c == turn_order[0] else ""
        name = c.name if c.name == c.__class__.__name__ else f"{c.name} ({c.__class__.__name__})"
        table.add_row(name, str(c.initiative), f"{c.current_hp}/{c.max_hp}",
                      f"{c.attack.damage[0]} - {c.attack.damage[1]}", f"{int(c.dodge * 100)}%", style=s)
    table.print(justify="center")


def cycle(turn_order: list[Character]):
    c = turn_order[0]
    turn_order.remove(c)
    turn_order.append(c)
