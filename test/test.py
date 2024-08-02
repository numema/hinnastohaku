from terminal_markup import render
from rich.console import Console
console = Console()

with console.status('Working..'):
    decision = (input('\ntest: ')).lower()
if decision[0] != 'n':
    print(render(f'[color=red]{decision}[/color]'))