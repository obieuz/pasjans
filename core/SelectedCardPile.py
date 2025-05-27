class SelectedCardPile:
    def __init__(self):
        self.cards = []

    def add_cards(self, cards):
        if isinstance(cards, list):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)

    def peek_top_card(self):
        if self.cards:
            return self.cards[-1]
        return None

