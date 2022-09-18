import rich.table
from rich.console import Console

console = Console()


class Table(rich.table.Table):
    """Wrapper around the rich table"""

    def print(self, *args, **kwargs):
        console.print(self, *args, **kwargs)


def prich(*args, **kwargs):
    return console.print(*args, **kwargs)


def clear():
    return console.clear()
