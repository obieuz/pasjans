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
        self.card_background_color = curses.COLOR_WHITE

        self.screen = stdscr

        curses.start_color()
        curses.init_pair(4, self.foreground_color, self.background_color)

        self.screen.bkgd(' ', curses.color_pair(4))
        self.screen.clear()
        self.screen.refresh()
        self.column_gap = 3
        self.row_gap = 3

        if isinstance(card_renderer, GraphicCardRenderer):
            self.card_hidden_height = 2
            self.card_width = 9
            self.card_height = 7
        if isinstance(card_renderer, TextCardRenderer):
            self.card_hidden_height = 1
            self.card_width = 5
            self.card_height = 1

        if graphic_mode == "default":
            curses.init_pair(1, curses.COLOR_RED, self.card_background_color)
            curses.init_pair(2, curses.COLOR_BLACK, self.card_background_color)
            curses.init_pair(3, curses.COLOR_CYAN, self.card_background_color)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

        self.card_renderer = card_renderer

    def draw_card(self, card, x=0, y=0, is_first=False, is_selected=False):
        if not card:
            return None
        if is_first:
            rendered_card = self.card_renderer.render_card(card)
        else:
            rendered_card = self.card_renderer.render_top_of_the_card(card)

        if not isinstance(rendered_card, list):
            lines = rendered_card.splitlines()
        else:
            lines = rendered_card

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

            self.screen.addstr(y + i, x, line, curses.color_pair(color))

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

        for i, card in enumerate(cards):
            if i == len(cards) - 1:
                self.draw_card(card, x, y + i * self.card_hidden_height, True, is_selected)
                continue
            self.draw_card(card, x, y + i * self.card_hidden_height, is_selected)

    def draw_tableau_piles(self, tableau_piles, is_selected_index=None):
        stock_pile_width = self.card_width + self.column_gap
        is_selected = False
        for i, tableau_pile in enumerate(tableau_piles):
            if i == is_selected_index:
                is_selected = True
            self.draw_tableau_pile(tableau_pile, stock_pile_width + i * (self.card_width + self.column_gap), self.row_gap, is_selected)

    def draw_foundation_pile(self, foundation_pile, x=0, y=0, is_selected=False):
        if foundation_pile.is_empty():
            self.draw_blank_card(foundation_pile.suit_symbol, x, y)
            return
        card = foundation_pile.peek_top_card()
        self.draw_card(card, x, y, is_first=True, is_selected=is_selected)

    def draw_foundation_piles(self, foundation_piles, is_selected_index=None):
        starting_x = 7 * (self.card_width + self.column_gap) + self.card_width + self.column_gap
        is_selected = False
        for i, foundation_pile in enumerate(foundation_piles):
            if i == is_selected_index:
                is_selected = True
            self.draw_foundation_pile(foundation_pile, starting_x, self.row_gap + i * (self.card_height+self.row_gap) , is_selected)

    def draw_blank_card(self, suit_symbol, x=0, y=0):
        blank_card = self.card_renderer.render_blank_card(suit_symbol)
        if not isinstance(blank_card, list):
            lines = blank_card.splitlines()
        else:
            lines = blank_card

        for i, line in enumerate(lines):
            self.screen.addstr(y + i, x, line, curses.color_pair(self.foreground_color))

    def draw_stock_pile(self, stock_pile, x=0,y=0):
        y = self.row_gap
        if stock_pile.is_empty():
            self.draw_blank_card("?", x, y)
        else:
            card = stock_pile.hidden_cards[-1]
            self.draw_card(card, x, y,True, is_selected=False)

        if len(stock_pile.visible_cards) == 0:
            return

        for i, card in enumerate(stock_pile.visible_cards):
            if i == len(stock_pile.visible_cards) - 1:
                self.draw_card(card, x, y + self.card_height + i * self.card_hidden_height, True, False)
                continue
            self.draw_card(card, x, y + self.card_height + i * self.card_hidden_height, False)



