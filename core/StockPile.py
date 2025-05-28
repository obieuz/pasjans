from core.CardStack import CardStack
from core.Deck import Deck
from core.Shuffler import Shuffler


class StockPile(CardStack):
    def __init__(self, cards, difficulty):
        super().__init__(cards)
        self.shuffler = Shuffler()
        if difficulty == "easy":
            self.cards_to_draw = 1
        else:
            self.cards_to_draw = 3
        self.visible_cards = []
        self.hidden_cards = cards

    def draw_card(self):
        for _ in range(self.cards_to_draw):
            if self.is_empty():
                self.shuffle_deck()
            card = self.remove_top_card()
            if card is None:
                self.shuffle_deck()
                return
            card.flip()
            self.visible_cards.append(card)


    def remove_top_card(self):
        if not self.hidden_cards:
            return None
        return self.hidden_cards.pop()

    def is_empty(self):
        return len(self.hidden_cards) == 0

    def shuffle_deck(self):
        self.hidden_cards = self.visible_cards
        self.visible_cards = []
        for card in self.hidden_cards:
            card.flip()
        self.hidden_cards = self.shuffler.shuffle(self.hidden_cards)

    def pop_card(self):
        if len(self.visible_cards) == 0:
            self.shuffle_deck()
            return
        self.visible_cards.pop()


