from core.Card import Card
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer
import curses

class GameManager:
    def __init__(self):
        self.CardRenderer = GraphicCardRenderer()

    def start_game(self):
        curses.wrapper(self.run_game)

        # card = Card(suit_symbol="♠", rank="10")
        # print(self.CardRenderer.render_card(card))
    def run_game(self, stdscr):
        stdscr.clear()

        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # Set up the window
        stdscr.addstr(0, 0, "Welcome to the Game!", curses.color_pair(2))
        stdscr.addstr(1, 0, "Press any key to exit...", curses.color_pair(1))

        # Refresh the screen to show changes
        stdscr.refresh()

        # Create a card
        card = Card(suit_symbol="♠", rank="10")
        # Render the card using the TextCardRenderer
        card_rendered = self.CardRenderer.render_card(card)
        # Display the rendered card
        stdscr.addstr(3, 0, card_rendered, curses.color_pair(1))

        # Wait for user input
        stdscr.getch()