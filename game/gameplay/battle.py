import random

from rich import box

from game.classes.attack import Attack
from game.classes.character import Character
from game.classes.conditions import Condition
from game.classes.entity import Entity
from game.classes.game_state import GameState
from game.classes.item import Item
from game.classes.monster import Monster
from game.classes.traits import CTrait, ATrait
from game.items.healing_item import HealingItem
from game.utils import clear, Table, prich, wait


def battle(game_state: GameState, monsters: list[Monster]):
    """Starts a battle between characters and monsters"""
    turn_order: list[Entity] = list(sorted([*game_state.party, *monsters], key=lambda x: x.initiative, reverse=True))
    while True:
        clear()
        turn_order = list(filter(lambda x: x.current_hp > 0, turn_order))
        game_state.party = list(filter(lambda x: x.current_hp > 0, game_state.party))
        monsters = list(filter(lambda x: x.current_hp > 0, monsters))
        if is_game_over(turn_order):
            return
        show_turn_order(turn_order)
        if apply_conditions(turn_order):
            wait()
            cycle(turn_order)
        elif turn_order[0] in game_state.party:
            options(turn_order, monsters, game_state)
        else:
            monster_attack(turn_order, game_state.party)


def apply_conditions(turn_order: list[Entity]) -> bool:
    """Applies the conditions on the entity and returns whether the turn needs to be passed or not"""
    flag = False
    c = turn_order[0]
    if c.has_condition(Condition.STUNNED):
        flag = True
        c.conditions.remove(Condition.STUNNED)
        prich(f"[bold]{turn_order[0].name}[/] is stunned.")
    return flag


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


def get_available(pool: list[Entity]):
    if any([c.has_trait(CTrait.FRONTLINE) for c in pool]):
        return [c for c in pool if c.has_trait(CTrait.FRONTLINE)]
    return pool.copy()


def monster_attack(turn_order: list[Entity], characters: list[Character]):
    """Performs an attack with the current monster"""
    c = turn_order[0]
    attack = random.choice(c.attacks)
    prich(f"[bold]{c.name}[/] used [bold]{attack.name}[/].")
    targets: list[Character] = []
    available = get_available(characters)
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
        ts = " [bold]" + ", ".join(t.name.title() for t in a.traits) + ".[/]" if a.traits else ""
        prich(
            f"{i + 1}. [bold]{a.name}[/]: {a.targets} target(s), [cyan bold]{a.damage[0]}[/] - [cyan bold]{a.damage[1]}[/] damage.{ts}",
            highlight=False)
    ans = input("> ")
    if not ans.isdigit() or int(ans) - 1 not in range(len(c.attacks)):
        prich("Invalid choice.")
        wait()
        return 0, []
    attack = c.attacks[int(ans) - 1]
    targets: list[Entity] = []
    available = get_available(monsters)
    while available and len(targets) < attack.targets:
        prich(f"Choose target no. {len(targets) + 1}:", style="bold")
        for j, m in enumerate(sorted(available, key=lambda x: x.initiative, reverse=True)):
            prich(f"{j + 1}. [bold]{m.name}[/] ({m.current_hp}/{m.max_hp} HP)")
        ans = input("> ")
        if not ans.isdigit() or int(ans) - 1 not in range(len(available)):
            prich("Invalid choice.")
            wait()
            return 0, []
        targets.append(available[int(ans) - 1])
        available.remove(available[int(ans) - 1])
    prich(f"[bold]{c.name}[/] used [bold]{attack.name}[/].")
    xp = 0
    coins = 0
    items: list[Item] = []
    for t in targets:
        xp_got, loot = resolve_attack(attack, t)
        xp += xp_got
        if loot:
            if isinstance(loot, Item):
                items.append(loot)
                prich(f"[bold]{t.name}[/] dropped a [bold]{loot.name}[/].")
            else:
                coins += loot
                prich(f"[bold]{t.name}[/] dropped {coins} coins.")
    if xp:
        cs = list(filter(lambda x: isinstance(x, Character), turn_order))
        noc = len(cs)
        for c in cs:
            c: Character = c
            c.xp += xp // noc
            prich(f"[bold]{c.name}[/] got {xp // noc} xp! ({c.xp} / {c.xp_to_level_up} xp)")
    cycle(turn_order)
    wait()
    return coins, items


def resolve_attack(attack: Attack, defender: Entity) -> tuple[int, int | Item]:
    """Resolves an attack between two characters"""
    if random.random() < defender.dodge:
        prich(f"[bold]{defender.name}[/] avoided the attack.")
        return 0, 0
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
            return d.xp_reward, d.loot
    if attack.has(ATrait.STUNNING) and random.random() < 0.5:
        defender.conditions.add(Condition.STUNNED)
        prich(f"[bold]{defender.name}[/] is now [bold]stunned[/].")
    return 0, 0


def use_item(game_state: GameState, c: Entity):
    """Uses an item"""
    if not game_state.items:
        prich("No items.")
        return False
    prich("Choose an item:", style="bold")
    for i, a in enumerate(sorted(game_state.items, key=lambda x: x.name)):
        prich(
            f"{i + 1}. [bold]{a.name}[/]: {a.description}", )
    ans = input("> ")
    if not ans.isdigit() or int(ans) - 1 not in range(len(game_state.items)):
        prich("Invalid choice.")
        wait()
        return False
    item = list(sorted(game_state.items, key=lambda x: x.name))[int(ans) - 1]
    if isinstance(item, HealingItem):
        heal = item.heal()
        c.current_hp = min(c.max_hp, c.current_hp + heal)
        game_state.items.remove(item)
        prich(f"[bold]{c.name}[/] was healed for {heal} hitpoints. ({c.current_hp} / {c.max_hp})")
        wait()

    return True


def options(turn_order: list[Entity], monsters: list[Monster], game_state: GameState):
    """Shows available options"""
    prich(f"[bold]What should {turn_order[0].name} do?:[/]\n1. Attack\n2. Use an item\n3. Pass")
    ans = input("> ")
    if ans == "1":
        coins, items = player_attack(turn_order, monsters)
        game_state.money += coins
        game_state.items += items
    elif ans == "2":
        used = use_item(game_state, turn_order[0])
        if used:
            cycle(turn_order)
    elif ans == "3":
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
    table.add_column("Dodge")
    table.add_column("Traits")
    table.add_column("Conditions")
    for c in turn_order:
        s = "bold" if c is turn_order[0] else ""
        name = c.name if isinstance(c, Monster) else f"{c.name} ({c.__class__.__name__})"
        table.add_row(name, str(c.initiative), f"{c.current_hp}/{c.max_hp}", f"{int(c.dodge * 100)}%",
                      ",".join(t.name for t in c.traits).lower() if c.traits else "-",
                      ",".join(cd.name for cd in c.conditions).lower() if c.conditions else "-", style=s)
    table.print(justify="center")


def cycle(turn_order: list[Entity]):
    c = turn_order[0]
    turn_order.remove(c)
    turn_order.append(c)
