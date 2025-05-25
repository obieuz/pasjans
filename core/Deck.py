from core.Card import Card
from core.CardStack import CardStack
from core.Shuffler import Shuffler


class Deck(CardStack):
    def __init__(self):
        super().__init__()
        self.create_deck()
        self.shuffler = Shuffler()

    def create_deck(self):
        suits = ["♠", "♣", "♦", "♥"]
        ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        self.cards = self.shuffler.shuffle(self.cards)

    def deal_card(self):
        if not self.cards:
            return None
        return self.cards.pop()

    def __str__(self):
        return f"Deck with {len(self.cards)} cards."

