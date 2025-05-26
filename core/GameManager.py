from core.Card import Card
from core.Deck import Deck
from core.FoundationPile import FoundationPile
from core.StockPile import StockPile
from core.TableauPile import TableauPile
from gui.Drawer import Drawer
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer
import curses


class GameManager:
    def __init__(self):
        self.foundation_piles = None
        self.drawer = None
        self.tableau_piles = None
        self.CardRenderer = None
        self.stock_pile = None
        self.deck = None
        self.difficulty = "easy"

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
        screen.clear()

        self.drawer.draw_foundation_piles(self.foundation_piles)

        self.drawer.draw_tableau_piles(self.tableau_piles)

        card = Card(suit_symbol="♥", rank="A")
        card1 = Card(suit_symbol="♣", rank="K")
        card.flip()
        card1.flip()

        cards = [card,card1]

        self.stock_pile.visible_cards = cards

        for card in self.stock_pile.visible_cards:
            print(card)

        self.drawer.draw_stock_pile(self.stock_pile)

        # card1 = Card(suit_symbol="♥", rank="A")
        #
        # self.drawer.draw_card(card, 0, 0)
        #
        # self.drawer.draw_tableau_pile(self.tableau_piles[3], 5, 0, is_selected=False)



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

        for suit in ["♠", "♥", "♦", "♣"]:
            foundation_pile = FoundationPile(required_suit=suit)
            self.foundation_piles.append(foundation_pile)

        self.stock_pile = StockPile(self.deck.cards,self.difficulty)


