import curses
import os
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer


def get_terminal_size():
    rows, columns = os.get_terminal_size()
    return rows, columns


class Drawer:
    def __init__(self, stdscr, graphic_mode="default"):
        self.screen_width = None
        self.screen_height = None
        self.primary_color = 1
        self.secondary_color = 2
        self.selected_color = 3
        self.foreground_color = 5
        self.background_color = curses.COLOR_GREEN
        self.card_background_color = curses.COLOR_WHITE
        self.numbers_of_cards_in_stock_pile = 3

        self.screen = stdscr

        self.screen_height, self.screen_width = self.screen.getmaxyx()
        self.card_renderer = GraphicCardRenderer(self.screen_width)

        curses.start_color()
        curses.init_pair(4, self.foreground_color, self.background_color)

        self.screen.bkgd(' ', curses.color_pair(4))
        self.screen.clear()
        self.screen.refresh()
        self.column_gap = self.min_column_gap = 3
        self.row_gap = self.min_row_gap = 3

        if isinstance(self.card_renderer, GraphicCardRenderer):
            self.card_hidden_height = 2
            self.card_width = 9
            self.card_height = 7
        if isinstance(self.card_renderer, TextCardRenderer):
            self.card_hidden_height = 1
            self.card_width = 3
            self.card_height = 1

        if self.screen_width < 150:
            self.card_width = 5
            self.card_height = 5

        if self.screen_width < 70:
            self.card_hidden_height = 1
            self.card_renderer = TextCardRenderer()
            self.card_width = 3
            self.card_height = 1


        self.calculate_gaps()

        if graphic_mode == "default":
            curses.init_pair(1, curses.COLOR_RED, self.card_background_color)
            curses.init_pair(2, curses.COLOR_BLACK, self.card_background_color)
            curses.init_pair(3, curses.COLOR_CYAN, self.card_background_color)
            curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)

    def draw_game_board(self, stock_pile, tableau_piles, foundation_piles, number_of_moves):
        self.screen.clear()
        self.screen.refresh()

        self.draw_foundation_piles(foundation_piles)

        self.draw_stock_pile(stock_pile)

        self.draw_tableau_piles(tableau_piles)

        self.draw_moves(number_of_moves)

        self.screen.refresh()

    def draw_card(self, card, x=0, y=0, is_first=False):
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

        card.top_left = (x, y)
        card.bottom_right = (x + self.card_width, y + self.card_height)

        for i, line in enumerate(lines):
            color = self.foreground_color
            if not card.is_face_up:
                color = self.foreground_color

            elif card.is_selected or card.in_selection:
                color = self.selected_color

            elif card.color == "red":
                color = self.primary_color

            elif card.color == "black":
                color = self.secondary_color

            self.screen.addstr(y + i, x, line, curses.color_pair(color))

    def draw_tableau_pile(self, tableau_pile, x=0, y=0):
        if len(tableau_pile.visible_cards) == 0 and len(tableau_pile.hidden_cards) == 0:
            self.draw_blank_card("?", x, y)
            if tableau_pile.is_selected:
                self.draw_border_around_object(x, y, self.card_width + 2, self.card_height + 2)
            return
        elif len(tableau_pile.hidden_cards) == 0:
            cards = tableau_pile.visible_cards
        else:
            cards = tableau_pile.hidden_cards + tableau_pile.visible_cards
        if not cards:
            return None

        if tableau_pile.is_selected:
            self.draw_border_around_object(x, y, self.card_width + 2,
                                           len(cards) * self.card_hidden_height + self.card_height)

        for i, card in enumerate(cards):
            if i == len(cards) - 1:
                self.draw_card(card, x, y + i * self.card_hidden_height, True)
                continue
            self.draw_card(card, x, y + i * self.card_hidden_height)

    def draw_tableau_piles(self, tableau_piles):
        stock_pile_width = self.card_width + self.column_gap
        for i, tableau_pile in enumerate(tableau_piles):
            self.draw_tableau_pile(tableau_pile, stock_pile_width + i * (self.card_width + self.column_gap),
                                   self.row_gap)

    def draw_foundation_pile(self, foundation_pile, x=0, y=0):
        if foundation_pile.is_selected:
            self.draw_border_around_object(x, y, self.card_width + 2, self.card_height + 2)

        if foundation_pile.is_empty():
            self.draw_blank_card(foundation_pile.suit_symbol, x, y)
            return
        card = foundation_pile.peek_top_card()
        self.draw_card(card, x, y, is_first=True)

    def draw_foundation_piles(self, foundation_piles):
        starting_x = 8 * (self.card_width + self.column_gap)
        for i, foundation_pile in enumerate(foundation_piles):
            self.draw_foundation_pile(foundation_pile, starting_x, self.row_gap + i * (self.card_height + self.card_height))

    def draw_blank_card(self, suit_symbol, x=0, y=0):
        blank_card = self.card_renderer.render_blank_card(suit_symbol)
        if not isinstance(blank_card, list):
            lines = blank_card.splitlines()
        else:
            lines = blank_card

        for i, line in enumerate(lines):
            self.screen.addstr(y + i, x, line, curses.color_pair(self.foreground_color))

    def draw_stock_pile(self, stock_pile, x=1, y=0):
        y = self.row_gap

        if stock_pile.is_selected:
            self.draw_border_around_object(x, y, self.card_width + 2, self.card_height + 2)

        if stock_pile.is_empty():
            self.draw_blank_card("?", x, y)
        else:
            card = stock_pile.hidden_cards[-1]
            self.draw_card(card, x, y, True)

        if len(stock_pile.visible_cards) == 0:
            return

        card_gap = self.column_gap

        visible_cards = stock_pile.visible_cards[-self.numbers_of_cards_in_stock_pile:]

        for i, card in enumerate(visible_cards):
            if i == len(visible_cards) - 1:
                self.draw_card(card, x, y + card_gap + self.card_height + i * self.card_hidden_height, True)
                continue
            self.draw_card(card, x, y + card_gap + self.card_height + i * self.card_hidden_height, False)

    def draw_border_around_object(self, x, y, width, height):
        x = x - 1
        y = y - 1
        self.screen.addch(y, x, curses.ACS_ULCORNER)
        self.screen.addch(y, x + width - 1, curses.ACS_URCORNER)
        self.screen.addch(y + height - 1, x, curses.ACS_LLCORNER)
        self.screen.addch(y + height - 1, x + width - 1, curses.ACS_LRCORNER)

        for i in range(1, width - 1):
            self.screen.addch(y, x + i, curses.ACS_HLINE)
            self.screen.addch(y + height - 1, x + i, curses.ACS_HLINE)

        for i in range(1, height - 1):
            self.screen.addch(y + i, x, curses.ACS_VLINE)
            self.screen.addch(y + i, x + width - 1, curses.ACS_VLINE)

    def draw_moves(self, number_of_moves, x=0, y=0):
        moves_text = f"Liczba ruchów: {number_of_moves}"


        self.screen.addstr(y, (self.screen_width // 2) - (len(moves_text) // 2), moves_text,
                           curses.color_pair(self.secondary_color))

    def calculate_gaps(self):
        self.column_gap = (self.screen_width - self.card_width * 9 - 1) // 8
        self.row_gap = (self.screen_height - self.card_height * 12) // 2

        if self.column_gap < self.min_column_gap:
            self.column_gap = self.min_column_gap
        if self.row_gap < self.min_row_gap:
            self.row_gap = self.min_row_gap

    def resize_window(self):
        self.screen_height, self.screen_width = self.screen.getmaxyx()
        if isinstance(self.card_renderer, GraphicCardRenderer):
            self.card_renderer.screen_width = self.screen_width
        if 150 > self.screen_width > 70:
            self.card_width = 5
            self.card_height = 5
            self.min_row_gap = 3
            self.min_column_gap = 3

        elif self.screen_width <= 70:
            self.card_renderer = TextCardRenderer()
            self.card_width = 3
            self.card_height = 1
            self.min_row_gap = 1
            self.min_column_gap = 1

        curses.resize_term(self.screen_height, self.screen_width)
        self.calculate_gaps()
