from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.table import Table
from rich.padding import Padding
from rich.align import Align

class StartMenu:
    def __init__(self,console):
        self.console = console
        self.settings = {}

    def _ask_nickname(self):
        table = Table.grid(expand=False, padding=(0,1))
        table.add_column(style="cyan", justify="right")
        table.add_column(style="magenta")
        self.console.print(Align.center(table))
        nickname = Prompt.ask("[bold green]   └─ Podaj Nickname[/bold green]", default="Gracz1")
        if not nickname.strip():
            nickname = "Gracz1"
        self.settings["nickname"] = nickname
        self.console.print()

    def _ask_difficulty(self):
        self.console.print(Align.center(Text("Wybierz poziom trudności:", style="bold green")))
        difficulty_choices = ["Łatwy (dobieranie 1 karty)", "Trudny (dobieranie 3 kart)"]
        difficulty_display = "\n".join([f"  [{i+1}] {choice}" for i, choice in enumerate(difficulty_choices)])
        self.console.print(Align.center(Panel(difficulty_display, border_style="dim blue")))

        while True:
            choice = IntPrompt.ask(
                "[bold green]   └─ Wybierz numer[/bold green]",
                choices=[str(i+1) for i in range(len(difficulty_choices))],
                show_choices=False
            )
            if 1 <= choice <= len(difficulty_choices):
                self.settings["difficulty_raw"] = difficulty_choices[choice-1]
                self.settings["difficulty"] = "easy" if choice == 1 else "hard"
                break
            else:
                self.console.print("[prompt.invalid]Nieprawidłowy wybór.")
        self.console.print()

    def _ask_color_mode(self):
        self.console.print(Align.center(Text("Tryb kolorystyczny :", style="bold green")))
        self.settings["color_mode"] = "default"
        if Confirm.ask("[bold green]   └─ Użyć trybu monochromatycznego (czarno-biały)?[/bold green]", default=False):
            self.settings["color_mode"] = "mono"
        self.console.print()

    def display(self):
        """Wyświetla całe menu i zwraca zebrane ustawienia lub None, jeśli anulowano."""
        self.console.clear()
        title = Text("♠ ♥ ♦ ♣ Pasjans w Konsoli ♣ ♦ ♥ ♠", style="bold white on blue", justify="center")
        self.console.print(Align.center(title))
        self.console.print()

        description = Panel(
            Text("Witaj w tekstowej wersji Pasjansa!\n"
                 "Ustaw poniższe opcje, aby rozpocząć rozgrywkę.", justify="center"),
            title="[bold cyan]Informacje[/bold cyan]",
            border_style="green",
            padding=(1, 2)
        )
        self.console.print(Align.center(description))
        self.console.print()

        self._ask_nickname()
        self._ask_difficulty()
        self._ask_color_mode()

        self.console.print(Padding(Align.center(Panel(
            Text(f"OK, {self.settings['nickname']}! Jesteś gotów do gry na poziomie {self.settings['difficulty_raw']}.\n"
                 f"Tryb kolorów: {self.settings['color_mode']}.", justify="center"),
            title="[bold yellow]Podsumowanie[/bold yellow]",
            border_style="yellow"
        )), (1,0)))

        if Confirm.ask("\n[bold white on green] Rozpocząć grę? [/bold white on green]", default=True):
            self.console.clear()
            return self.settings
        else:
            self.console.clear()
            self.console.print(Align.center(Text("Anulowano uruchomienie gry. Do zobaczenia!", style="bold red")))
            return None