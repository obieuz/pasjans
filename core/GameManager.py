from core.Card import Card
from core.Deck import Deck
from core.FoundationPile import FoundationPile
from core.GameState import GameState
from core.KeyboardInputHandler import KeyboardInputHandler
from core.SelectedCardPile import SelectedCardPile
from core.StockPile import StockPile
from core.TableauPile import TableauPile
from gui.Drawer import Drawer
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer
import curses


class KeyBoardInputHandler:
    pass


class GameManager:
    def __init__(self):
        self.foundation_piles = None
        self.drawer = None
        self.tableau_piles = None
        self.CardRenderer = None
        self.stock_pile = None
        self.selected_card_pile = SelectedCardPile()
        self.deck = None
        self.difficulty = "easy"
        self.input_handler = None
        self.run = True
        self.game_state_saver = GameState()
        self.move_order_horizontal_index = 0
        self.move_order_vertical_index = 0
        self.move_order = ["stack_pile-0"] + ["tableau_pile-" + str(i) for i in range(0, 7)] + ["foundation_pile-0"]

    def start_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.CardRenderer = GraphicCardRenderer()
        self.tableau_piles = []
        self.foundation_piles = []

        self.prepare_board()

        curses.wrapper(self.run_game)

    def run_game(self, screen):
        self.drawer = Drawer(self.CardRenderer, screen, graphic_mode="default")
        self.input_handler = KeyboardInputHandler(self.drawer)

        while self.run:

            self.drawer.draw_game_board(
                self.stock_pile,
                self.tableau_piles,
                self.foundation_piles
            )

            action = self.input_handler.get_player_action()
            if action:
                self.process_action(action)


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
        if action == "quit":
            self.run = False
        elif action == "help":
            self.drawer.show_help()
        elif action == "load":
            self.go_back()
        elif action == "restart":
            self.start_game()
        elif action == "move_right":
            self.clear_vertical_selection()
            self.move_order_horizontal_index = (self.move_order_horizontal_index + 1) % len(self.move_order)
            self.process_horizontal_move()
        elif action == "move_left":
            self.clear_vertical_selection()
            self.move_order_horizontal_index = (self.move_order_horizontal_index - 1) % len(self.move_order)
            self.process_horizontal_move()
        elif action == "move_up":
            move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
            if move_order_item[0] == "tableau_pile":
                if self.move_order_vertical_index > 0:
                    self.move_order_vertical_index -= 1
            elif move_order_item[0] == "foundation_pile":
                if self.move_order_vertical_index > 0:
                    self.move_order_vertical_index -= 1
                else:
                    self.move_order_vertical_index = len(self.foundation_piles) - 1
            elif move_order_item[0] == "stack_pile":
                if self.move_order_vertical_index > 0:
                    self.move_order_vertical_index -= 1
            self.process_vertical_move()
        elif action == "move_down":
            move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
            if move_order_item[0] == "tableau_pile":
                if self.move_order_vertical_index < len(
                        self.tableau_piles[self.move_order_horizontal_index - 1].visible_cards) - 1:
                    self.move_order_vertical_index += 1
            elif move_order_item[0] == "foundation_pile":
                if self.move_order_vertical_index < len(self.foundation_piles) - 1:
                    self.move_order_vertical_index += 1
                else:
                    self.move_order_vertical_index = 0
            elif move_order_item[0] == "stack_pile":
                if self.move_order_vertical_index <= len(self.stock_pile.visible_cards):
                    self.move_order_vertical_index += 1
            self.process_vertical_move()
        elif action == "use":
            move_order_item = self.move_order[self.move_order_horizontal_index].split("-")
            if self.selected_card_pile.is_empty():
                if move_order_item[0] == "tableau_pile":
                    horizontal_index = int(move_order_item[1])

                    cards_to_add = self.tableau_piles[horizontal_index].visible_cards[self.move_order_vertical_index:]
                    for card in cards_to_add:
                        card.in_selection = True
                    self.selected_card_pile.add_cards(cards_to_add, self.move_order_horizontal_index, self.move_order_vertical_index)
                if move_order_item[0] == "stack_pile":
                    if self.move_order_vertical_index == 0:
                        if self.stock_pile.is_empty():
                            self.stock_pile.shuffle_deck()
                        else:
                            self.stock_pile.draw_card()
                    else:
                        card_to_add = self.stock_pile.visible_cards[-1]
                        print(card_to_add)
                        card_to_add.in_selection = True
                        self.selected_card_pile.add_cards([card_to_add], self.move_order_horizontal_index, self.move_order_vertical_index+1)

            else:
                if move_order_item[0] == "tableau_pile":
                    horizontal_index = int(move_order_item[1])
                    if self.tableau_piles[horizontal_index].can_place_card(self.selected_card_pile.cards[0]):
                        self.process_deleting_card()
                        self.tableau_piles[horizontal_index].add_cards(self.selected_card_pile.cards)
                        self.selected_card_pile.cards = []
                    else:
                        self.selected_card_pile.clean()
                elif move_order_item[0] == "foundation_pile":
                    if len(self.selected_card_pile.cards) == 0:
                        return
                    if self.foundation_piles[self.move_order_vertical_index].can_accept_card(self.selected_card_pile.cards[0]):
                        self.process_deleting_card()
                        self.foundation_piles[self.move_order_vertical_index].add_cards(self.selected_card_pile.cards)
                        self.selected_card_pile.cards = []
                    else:
                        self.selected_card_pile.clean()
                elif move_order_item[0] == "stack_pile":
                    if self.move_order_vertical_index != 0:
                        return
                    if self.stock_pile.is_empty():
                        self.stock_pile.shuffle_deck()
                    else:
                        self.stock_pile.draw_card()

        if action != "load":
            self.game_state_saver.push_state(
                self.stock_pile,
                self.tableau_piles,
                self.foundation_piles,
                self.move_order,
                self.move_order_horizontal_index,
                self.move_order_vertical_index
            )

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
            print("Horizontal index:", horizontal_index)
            self.tableau_piles[horizontal_index].visible_cards[
                self.move_order_vertical_index].is_selected = True

        elif move_order_item[0] == "foundation_pile":
            self.foundation_piles[self.move_order_vertical_index].is_selected = True

        elif move_order_item[0] == "stack_pile":
            if self.stock_pile.visible_cards:
                self.stock_pile.visible_cards[-1].is_selected = True

    def process_deleting_card(self):
        print(f"Horizontal - {self.selected_card_pile.selected_from_horizontal_index}")
        print(f"Vertical - {self.selected_card_pile.selected_from_vertical_index}")
        move_order_item = self.move_order[self.selected_card_pile.selected_from_horizontal_index].split("-")
        if move_order_item[0] == "tableau_pile":
            pile = self.tableau_piles[int(move_order_item[1])]
            pile.remove_cards_to_index(self.selected_card_pile.selected_from_vertical_index,len(self.selected_card_pile.cards))
        elif move_order_item[0] == "stack_pile":
            print("Removing card from stock pile")
            self.stock_pile.pop_card()

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

    def go_back(self):
        state = self.game_state_saver.load_state()
        if state:
            self.stock_pile = state["stock_pile"]
            self.tableau_piles = state["tableau_piles"]
            self.foundation_piles = state["foundation_piles"]
            self.move_order = state["move_order"]
            self.move_order_horizontal_index = state["move_order_horizontal_index"]
            self.move_order_vertical_index = state["move_order_vertical_index"]

            self.process_horizontal_move()

            self.drawer.draw_game_board(
                self.stock_pile,
                self.tableau_piles,
                self.foundation_piles
            )

        else:
            print("Nie ma stanu do załadowania.")
