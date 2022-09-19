import random

from rich import box

from game.classes.attack import Attack
from game.classes.character import Character
from game.classes.entity import Entity
from game.classes.monster import Monster
from game.utils import clear, Table, prich, wait


def battle(characters: list[Character], monsters: list[Monster]):
    """Starts a battle between characters and monsters"""
    turn_order: list[Entity] = list(sorted([*characters, *monsters], key=lambda x: x.initiative, reverse=True))
    while True:
        clear()
        turn_order = list(filter(lambda x: x.current_hp > 0, turn_order))
        characters = list(filter(lambda x: x.current_hp > 0, characters))
        monsters = list(filter(lambda x: x.current_hp > 0, monsters))
        if is_game_over(turn_order):
            return
        show_turn_order(turn_order)
        if turn_order[0] in characters:
            options(turn_order, monsters)
        else:
            monster_attack(turn_order, characters)


def is_game_over(turn_order: list[Entity]):
    if all([isinstance(a, Monster) for a in turn_order]):
        prich("Game Over.", style="red bold")
        wait()
        return True
    elif all([isinstance(a, Character) for a in turn_order]):
        prich("Battle won!", style="green bold")
        for c in turn_order:
            l = c.level
            c.level_up()  # type: ignore
            if l != c.level:
                prich(f"[bold]{c.name}[/] has leveled up to level {c.level}!")
        wait()
        return True
    return False


def monster_attack(turn_order: list[Entity], characters: list[Character]):
    """Performs an attack with the current monster"""
    c = turn_order[0]
    attack = random.choice(c.attacks)
    prich(f"[bold]{c.name}[/] used [bold]{attack.name}[/].")
    targets: list[Character] = []
    available = characters.copy()
    while len(targets) < attack.targets:
        t = random.choice(available)
        available.remove(t)
        targets.append(t)
    for t in targets:
        resolve_attack(attack, t)
    cycle(turn_order)
    wait()


def player_attack(turn_order: list[Entity], monsters: list[Monster]):
    """Performs an attack with the player character"""
    c = turn_order[0]  # type: ignore
    prich("Choose attack:", style="bold")
    for i, a in enumerate(c.attacks):
        prich(
            f"{i + 1}. [bold]{a.name}[/]: {a.targets} target(s), [cyan bold]{a.damage[0]}[/] - [cyan bold]{a.damage[1]}[/] damage.",
            highlight=False)
    ans = input("> ")
    if not ans.isdigit() or int(ans) - 1 not in range(len(c.attacks)):
        prich("Invalid choice.")
        wait()
        return
    attack = c.attacks[int(ans) - 1]
    targets: list[Entity] = []
    available = monsters.copy()
    while len(targets) < attack.targets:
        prich(f"Choose target no. {len(targets) + 1}:", style="bold")
        for j, m in enumerate(sorted(available, key=lambda x: x.initiative, reverse=True)):
            prich(f"{j + 1}. [bold]{m.name}[/] ({m.current_hp}/{m.max_hp} HP)")
        ans = input("> ")
        if not ans.isdigit() or int(ans) - 1 not in range(len(available)):
            prich("Invalid choice.")
            wait()
            return
        targets.append(available[int(ans) - 1])
        available.remove(available[int(ans) - 1])
    prich(f"[bold]{c.name}[/] used [bold]{attack.name}[/].")
    xp = 0
    for t in targets:
        xp += resolve_attack(attack, t)
    if xp:
        cs = list(filter(lambda x: isinstance(x, Character), turn_order))
        noc = len(cs)
        for c in cs:
            c: Character = c
            c.xp += xp // noc
            prich(f"[bold]{c.name}[/] got {xp // noc} xp! ({c.xp} / {c.xp_to_level_up} xp)")
    cycle(turn_order)
    wait()


def resolve_attack(attack: Attack, defender: Entity):
    """Resolves an attack between two characters"""
    if random.random() < defender.dodge:
        prich(f"[bold]{defender.name}[/] avoided the attack.")
        return
    damage = random.randint(*attack.damage)
    critical = random.random() < 0.05
    if critical:
        damage *= 2
    prich(f"[bold]{defender.name}[/] took {damage} damage{' (crit!)' if critical else ''}.")
    defender.current_hp -= damage
    if defender.current_hp <= 0:
        prich(f"[bold]{defender.name}[/] died.")
        if isinstance(defender, Monster):
            d: Monster = defender
            return d.xp_reward
    return 0


def options(turn_order: list[Entity], monsters: list[Monster]):
    """Shows available options"""
    prich("[bold]Select action:[/]\n1. Attack\n2. Pass")
    ans = input("> ")
    if ans == "1":
        player_attack(turn_order, monsters)
    elif ans == "2":
        prich(f"[bold]{turn_order[0].name}[/] passed its turn.")
        wait()
        cycle(turn_order)
    else:
        prich("Invalid option.")
        wait()


def show_turn_order(turn_order: list[Entity]):
    table = Table(title="Turn Order", box=box.SIMPLE, title_style="bold italic")
    table.add_column("Name")
    table.add_column("Initiative")
    table.add_column("Hitpoints")
    table.add_column("Damage")
    table.add_column("Dodge")
    for c in turn_order:
        s = "bold" if c == turn_order[0] else ""
        name = c.name if isinstance(c, Monster) else f"{c.name} ({c.__class__.__name__})"
        dmin = min(a.damage[0] for a in c.attacks)
        dmax = max(a.damage[1] for a in c.attacks)
        table.add_row(name, str(c.initiative), f"{c.current_hp}/{c.max_hp}",
                      f"{dmin} - {dmax}", f"{int(c.dodge * 100)}%", style=s)
    table.print(justify="center")


def cycle(turn_order: list[Entity]):
    c = turn_order[0]
    turn_order.remove(c)
    turn_order.append(c)
