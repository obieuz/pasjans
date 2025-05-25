import curses

from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer


class Drawer:
    def __init__(self, card_renderer, stdscr, graphic_mode="default"):
        self.primary_color = 1
        self.secondary_color = 2
        self.selected_color = 3
        self.foreground_color = 5
        self.background_color = curses.COLOR_GREEN




        self.screen = stdscr

        curses.start_color()
        curses.init_pair(4, self.foreground_color, self.background_color)

        self.screen.bkgd(' ', curses.color_pair(4))
        self.screen.clear()
        self.screen.refresh()

        if isinstance(card_renderer, GraphicCardRenderer):
            self.card_width = 9
            self.card_height = 5
        if isinstance(card_renderer, TextCardRenderer):
            self.card_width = 5
            self.card_height = 1

        if graphic_mode == "default":
            curses.init_pair(1, curses.COLOR_RED, self.background_color)
            curses.init_pair(2, curses.COLOR_BLACK, self.background_color)
            curses.init_pair(3, curses.COLOR_CYAN, self.background_color)
            curses.init_pair(5, curses.COLOR_WHITE, self.background_color)

        self.card_renderer = card_renderer

    def draw_card(self, card, x=0, y=0, is_selected=False):
        if not card:
            return None
        rendered_card = self.card_renderer.render_card(card)

        lines = rendered_card.splitlines()

        for i, line in enumerate(lines):
            color = self.foreground_color
            if not card.is_face_up:
                color = self.foreground_color

            elif is_selected:
                color = self.selected_color

            elif card.color == "red":
                color = self.primary_color

            elif card.color == "black":
                color = self.secondary_color

            self.screen.addstr(y + i, x, rendered_card, curses.color_pair(color))

    def draw_tableau_pile(self, tableau_pile, x=0, y=0, is_selected=False):
        if len(tableau_pile.visible_cards) == 0 and len(tableau_pile.hidden_cards) == 0:
            print("Empty tableau pile")
            return
        elif len(tableau_pile.hidden_cards) == 0:
            cards = tableau_pile.visible_cards
        else:
            cards = tableau_pile.hidden_cards + tableau_pile.visible_cards
        if not cards:
            print("No cards in tableau pile")
            return None
        print(len(cards))

        for i, card in enumerate(cards):
            self.draw_card(card, x, y + i, is_selected)

    def draw_tableau_piles(self, tableau_piles, is_selected_index=None):
        is_selected = False
        for i, tableau_pile in enumerate(tableau_piles):
            if i == is_selected_index:
                is_selected = True
            self.draw_tableau_pile(tableau_pile, 0 + i * self.card_width, 0, is_selected)
