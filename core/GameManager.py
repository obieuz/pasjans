import os
import threading

from core.Card import Card
from rich.console import Console
from core.Deck import Deck
from core.FoundationPile import FoundationPile
from core.GameState import GameState
from core.KeyboardInputHandler import KeyboardInputHandler
from core.SelectedCardPile import SelectedCardPile
from core.StockPile import StockPile
from core.TableauPile import TableauPile
from gui.Drawer import Drawer
from gui.EndScreen import EndScreen
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.StartMenu import StartMenu
from gui.TextCardRenderer import TextCardRenderer
import curses
import copy
import time
from core.LeaderboardManager import LeaderboardManager
from core.Timer import Timer


class GameManager:
    def __init__(self):
        self.end_screen = None
        self.game_settings = None
        self.foundation_piles = None
        self.drawer = None
        self.tableau_piles = None
        self.stock_pile = None
        self.selected_card_pile = SelectedCardPile()
        self.deck = None
        self.difficulty = None
        self.console = Console()
        self.input_handler = None
        self.run = True
        self.number_of_moves = 0
        self.game_state_saver = GameState()
        self.move_order_horizontal_index = 0
        self.move_order_vertical_index = 0
        self.move_order = ["stack_pile-0"] + ["tableau_pile-" + str(i) for i in range(0, 7)] + ["foundation_pile-0"]
        self.is_won = False
        self.leaderboard_manager_instance = None
        self.timer = Timer()

        self._action_handlers = {
            "ACTION_QUIT": self._handle_quit,
            "ACTION_LOAD": self._handle_load,
            "ACTION_RESTART": self._handle_restart,
            "ACTION_MOVE_RIGHT": self._handle_move_right,
            "ACTION_MOVE_LEFT": self._handle_move_left,
            "ACTION_MOVE_UP": self._handle_move_up,
            "ACTION_MOVE_DOWN": self._handle_move_down,
            "ACTION_USE": self._handle_use,
            "ACTION_RESIZE": self._handle_resize,
            "ACTION_DRAW_CARD": self._handle_draw_card
        }

    def start_game(self):
        self.timer.reset_timer()
        self._clear_screen()
        menu = StartMenu(self.console)
        self.game_settings = menu.display()
        if not self.game_settings:
            print("Gra anulowana.")
            return
        self.difficulty = self.game_settings["difficulty"]
        self.leaderboard_manager_instance = LeaderboardManager()

        self.run = True
        self.deck = Deck()
        self.deck.shuffle()
        self.tableau_piles = []
        self.foundation_piles = []
        self.number_of_moves = 0
        self.is_won = False

        self.prepare_board()

        curses.wrapper(self.run_game)

        self._clear_screen()
        self.end_screen = EndScreen(self.console, self.leaderboard_manager_instance)
        if self.end_screen.display(self.is_won, self.game_settings["nickname"], self.number_of_moves,
                                   self.timer.get_time()):
            self._clear_screen()
            self.start_game()
        else:
            self._clear_screen()

    def run_game(self, screen):
        self.drawer = Drawer(screen, graphic_mode=self.game_settings["color_mode"])
        self.input_handler = KeyboardInputHandler(self.drawer)

        self.timer.start_timer()
        while self.run:
            self.drawer.draw_game_board(self.stock_pile, self.tableau_piles, self.foundation_piles,
                                        self.number_of_moves)

            action = self.input_handler.get_player_action()
            if action:
                self.process_action(action)

            if self.check_for_win():
                self.run = False
                self.is_won = True

        self.timer.stop_timer()

    def prepare_board(self):
        for i in range(7):
            tableau_pile = TableauPile()
            cards = []
            for j in range(i + 1):
                card = self.deck.deal_card()
                if card:
                    cards.append(card)
            tableau_pile.add_initial_cards(cards)
            self.tableau_piles.append(tableau_pile)

        for suit in ["♠", "♥", "♦", "♣"]:
            foundation_pile = FoundationPile(required_suit=suit)
            self.foundation_piles.append(foundation_pile)

        self.stock_pile = StockPile(self.deck.cards, self.difficulty)

    def process_action(self, action):

        if self.game_state_saver.last_number_of_move != self.number_of_moves:
            self.game_state_saver.push_state(
                copy.deepcopy(self.stock_pile),
                copy.deepcopy(self.tableau_piles),
                copy.deepcopy(self.foundation_piles),
                copy.deepcopy(self.selected_card_pile),
                copy.deepcopy(self.move_order),
                self.move_order_horizontal_index,
                self.move_order_vertical_index,
                self.number_of_moves,
                self.game_state_saver
            )

        handler = self._action_handlers.get(action)
        if handler:
            handler()

    def process_horizontal_move(self):
        self.clear_horizontal_selection()
        self.clear_vertical_selection()
        self.move_order_vertical_index = 0
        move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
        if move_order_item[0] == "tableau_pile":
            self.tableau_piles[int(move_order_item[1])].is_selected = True

        elif move_order_item[0] == "foundation_pile":
            self.foundation_piles[int(move_order_item[1])].is_selected = True

        elif move_order_item[0] == "stack_pile":
            self.stock_pile.is_selected = True

    def process_vertical_move(self):
        self.clear_vertical_selection()
        move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
        if move_order_item[0] == "tableau_pile":
            horizontal_index = int(move_order_item[1])
            self.tableau_piles[horizontal_index].visible_cards[
                self.move_order_vertical_index].is_selected = True

        elif move_order_item[0] == "foundation_pile":
            self.foundation_piles[self.move_order_vertical_index].is_selected = True

        elif move_order_item[0] == "stack_pile":
            if self.stock_pile.visible_cards:
                self.stock_pile.visible_cards[-1].is_selected = True

    def process_deleting_card(self):
        move_order_item = self.move_order[self.selected_card_pile.selected_from_horizontal_index].split("-")
        if move_order_item[0] == "tableau_pile":
            pile = self.tableau_piles[int(move_order_item[1])]
            pile.remove_cards_to_index(self.selected_card_pile.selected_from_vertical_index,
                                       len(self.selected_card_pile.cards))
        elif move_order_item[0] == "stack_pile":
            self.stock_pile.pop_card()
        for card in self.selected_card_pile.cards:
            card.in_selection = False

    def clear_selection(self):
        for card in self.selected_card_pile.cards:
            card.in_selection = False
        self.selected_card_pile.clean()

    def clear_horizontal_selection(self):
        for tableau_pile in self.tableau_piles:
            tableau_pile.is_selected = False
        for foundation_pile in self.foundation_piles:
            foundation_pile.is_selected = False
        self.stock_pile.is_selected = False

    def clear_vertical_selection(self):
        move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
        if move_order_item[0] == "tableau_pile":
            horizontal_index = int(move_order_item[1])
            for card in self.tableau_piles[horizontal_index].visible_cards:
                card.is_selected = False
        elif move_order_item[0] == "foundation_pile":
            for foundation_pile in self.foundation_piles:
                foundation_pile.is_selected = False
        elif move_order_item[0] == "stack_pile":
            for card in self.stock_pile.visible_cards:
                card.is_selected = False

    def load(self):
        state = self.game_state_saver.load_state()
        if state:
            self.stock_pile = state["stock_pile"]
            self.tableau_piles = state["tableau_piles"]
            self.foundation_piles = state["foundation_piles"]
            self.selected_card_pile = state["selected_card_pile"]
            self.move_order = state["move_order"]
            self.move_order_horizontal_index = state["move_order_horizontal_index"]
            self.move_order_vertical_index = state["move_order_vertical_index"]
            self.number_of_moves = state["number_of_moves"]

    def check_for_win(self):
        for foundation_pile in self.foundation_piles:
            if len(foundation_pile.cards) != 13:
                return False
        return True

    def _handle_quit(self):
        self.run = False

    def _handle_load(self):
        self.load()

    def _handle_restart(self):
        self.start_game()

    def _clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def _get_current_pile_info(self):
        current_move_target_str = self.move_order[self.move_order_horizontal_index]
        parts = current_move_target_str.split("-")
        pile_type_str = parts[0]
        pile_index_in_category = int(parts[1])
        return pile_type_str, pile_index_in_category

    def _handle_move_right(self):
        self.clear_vertical_selection()
        self.move_order_horizontal_index = (self.move_order_horizontal_index + 1) % len(self.move_order)
        self.process_horizontal_move()

    def _handle_move_left(self):
        self.clear_vertical_selection()
        self.move_order_horizontal_index = (self.move_order_horizontal_index - 1) % len(self.move_order)
        self.process_horizontal_move()

    def _handle_move_up(self):
        pile_type_str, pile_index_in_category = self._get_current_pile_info()
        if pile_type_str == "tableau_pile":
            if self.move_order_vertical_index > 0:
                self.move_order_vertical_index -= 1
        elif pile_type_str == "foundation_pile":
            if self.move_order_vertical_index > 0:
                self.move_order_vertical_index -= 1
            else:
                self.move_order_vertical_index = len(self.foundation_piles) - 1
        elif pile_type_str == "stack_pile":
            if self.move_order_vertical_index > 0:
                self.move_order_vertical_index -= 1
        self.process_vertical_move()

    def _handle_move_down(self):
        pile_type_str, pile_index_in_category = self._get_current_pile_info()
        if pile_type_str == "tableau_pile":
            if self.move_order_vertical_index < len(
                    self.tableau_piles[pile_index_in_category].visible_cards) - 1:
                self.move_order_vertical_index += 1
        elif pile_type_str == "foundation_pile":
            if self.move_order_vertical_index < len(self.foundation_piles) - 1:
                self.move_order_vertical_index += 1
            else:
                self.move_order_vertical_index = 0
        elif pile_type_str == "stack_pile":
            if self.move_order_vertical_index <= len(self.stock_pile.visible_cards):
                self.move_order_vertical_index += 1
        self.process_vertical_move()

    def _handle_use(self):
        pile_type_str, pile_index_in_category = self._get_current_pile_info()
        if self.selected_card_pile.is_empty():
            if pile_type_str == "tableau_pile":
                cards_to_add = self.tableau_piles[pile_index_in_category].visible_cards[self.move_order_vertical_index:]
                for card in cards_to_add:
                    card.in_selection = True
                self.selected_card_pile.add_cards(cards_to_add, self.move_order_horizontal_index,
                                                  self.move_order_vertical_index)
            elif pile_type_str == "stack_pile":
                if self.move_order_vertical_index == 0:
                    if len(self.stock_pile.visible_cards) == 0 and len(self.stock_pile.hidden_cards) == 0:
                        return
                    if self.stock_pile.is_empty():
                        self.stock_pile.shuffle_deck()
                    self.number_of_moves += 1
                    self.stock_pile.draw_card()
                else:
                    card_to_add = self.stock_pile.visible_cards[-1]
                    card_to_add.in_selection = True
                    self.selected_card_pile.add_cards([card_to_add], self.move_order_horizontal_index,
                                                      self.move_order_vertical_index + 1)
        else:
            if pile_type_str == "tableau_pile":
                if self.tableau_piles[pile_index_in_category].can_place_card(self.selected_card_pile.cards[0]):
                    self.number_of_moves += 1
                    self.process_deleting_card()
                    self.tableau_piles[pile_index_in_category].add_cards(self.selected_card_pile.cards)
                self.clear_selection()
            elif pile_type_str == "foundation_pile":
                if len(self.selected_card_pile.cards) == 0:
                    return
                if self.foundation_piles[self.move_order_vertical_index].can_accept_card(
                        self.selected_card_pile.cards[0]):
                    self.number_of_moves += 1
                    self.process_deleting_card()
                    self.foundation_piles[self.move_order_vertical_index].add_cards(self.selected_card_pile.cards)
                self.clear_selection()
            elif pile_type_str == "stack_pile":
                if len(self.stock_pile.visible_cards) == 0 and len(self.stock_pile.hidden_cards) == 0:
                    return
                if self.move_order_vertical_index != 0:
                    return
                if self.stock_pile.is_empty():
                    self.stock_pile.shuffle_deck()
                self.number_of_moves += 1

    def _handle_resize(self):
        self.drawer.resize_window()
        if self.drawer.screen_width <= 44:
            self.run = False
            print("Zbyt mały rozmiar okna. Proszę zwiększyć rozmiar okna.")
            return

        self.drawer.draw_game_board(self.stock_pile, self.tableau_piles, self.foundation_piles, self.number_of_moves)

    def _handle_draw_card(self):
        if self.stock_pile.is_empty():
            self.stock_pile.shuffle_deck()
        self.stock_pile.draw_card()
        self.number_of_moves += 1




