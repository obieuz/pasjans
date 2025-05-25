from core.Card import Card
from core.Deck import Deck
from core.TableauPile import TableauPile
from gui.Drawer import Drawer
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer
import curses


class GameManager:
    def __init__(self):
        self.drawer = None
        self.tableau_piles = None
        self.CardRenderer = None
        self.deck = None

    def start_game(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.CardRenderer = TextCardRenderer()
        self.tableau_piles = []

        self.prepare_board()

        curses.wrapper(self.run_game)

    def run_game(self, screen):
        self.drawer = Drawer(self.CardRenderer, screen, graphic_mode="default")
        screen.clear()

        # card = Card(suit_symbol="♠", rank="10")
        #
        # card1 = Card(suit_symbol="♥", rank="A")
        #
        # self.drawer.draw_card(card, 0, 0)
        #
        # self.drawer.draw_tableau_pile(self.tableau_piles[3], 5, 0, is_selected=False)
        self.drawer.draw_tableau_piles(self.tableau_piles)

        screen.refresh()

        screen.getch()

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
        self.tableau_piles.reverse()
