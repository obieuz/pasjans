import time
from typing import Optional

from core.LeaderboardManager import LeaderboardManager
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.padding import Padding
from rich.align import Align
from rich.prompt import Confirm
from rich.live import Live


class EndScreen:
    def __init__(self,console, leaderboard_mgr: LeaderboardManager):
        self.console = console
        self.leaderboard_mgr = leaderboard_mgr

    def _display_leaderboard(self, current_leaderboard: Optional[list] = None):
        leaderboard_data = self.leaderboard_mgr.get_scores()

        if not leaderboard_data:
            self.console.print(Align.center(Text("Leaderboard jest pusty.", style="italic yellow")))
            return

        table = Table(title="🏆 Leaderboard 🏆", title_style="bold magenta", border_style="blue")
        table.add_column("Miejsce", style="dim cyan", width=7, justify="center")
        table.add_column("Nickname", style="bold white", min_width=15)
        table.add_column("Ruchy", style="green", justify="center")
        table.add_column("Czas", style="yellow", justify="center")

        for i, entry in enumerate(leaderboard_data):
            table.add_row(
                f"{i + 1}.",
                entry["nickname"],
                str(entry["moves"]),
                self.leaderboard_mgr.format_time(entry["time_seconds"])
            )
        self.console.print(Padding(Align.center(table), (1, 0)))

    def display(self, game_won: bool, nickname: str, moves_count: int, elapsed_time_seconds: int) -> bool:
        """
        Wyświetla ekran końcowy.
        Zwraca True, jeśli gracz chce zagrać ponownie, False w przeciwnym razie.
        """
        self.console.clear()
        formatted_time = self.leaderboard_mgr.format_time(elapsed_time_seconds)

        if game_won:
            title_text = Text("🎉 ZWYCIĘSTWO! 🎉", style="bold white on green", justify="center")
            panel_title = "[bold green]Gratulacje![/bold green]"
            panel_border_style = "green"
            main_message = f"Brawo, {nickname}! Ukończyłeś Pasjansa."
            current_leaderboard = self.leaderboard_mgr.add_score(nickname, moves_count,
                                                                               elapsed_time_seconds)
        else:
            title_text = Text("GAME OVER", style="bold white on red", justify="center")
            panel_title = "[bold red]Niestety...[/bold red]"
            panel_border_style = "red"
            main_message = f"Przykro mi, {nickname}. Tym razem się nie udało."
            current_leaderboard = None

        self.console.print(Align.center(title_text))
        self.console.print()

        stats_text = Text(
            f"{main_message}\n\n"
            f"Twoje statystyki:\n"
            f"  Liczba ruchów: [bold yellow]{moves_count}[/bold yellow]\n"
            f"  Czas gry: [bold yellow]{formatted_time}[/bold yellow]",
            justify="center"
        )

        summary_panel = Panel(
            stats_text,
            title=panel_title,
            border_style=panel_border_style,
            padding=(1, 2)
        )
        self.console.print(Align.center(summary_panel))
        self.console.print()

        if game_won:
            self._display_leaderboard(current_leaderboard)
        self.console.print()

        play_again = Confirm.ask("[bold cyan]Czy chcesz zagrać jeszcze raz?[/bold cyan]", default=True)

        if play_again:
            with Live(console=self.console, refresh_per_second=4, transient=True) as live:
                for i in range(3, 0, -1):
                    live.update(Align.center(Text(f"Nowa gra za {i}...", style="bold yellow")))
                    time.sleep(1)
            self.console.clear()
        else:
            self.console.clear()
            self.console.print(Align.center(Text("Dzięki za grę! Do zobaczenia! 👋", style="bold magenta")))
            time.sleep(2)
            self.console.clear()

        return play_again