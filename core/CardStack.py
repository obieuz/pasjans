class CardStack:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []

    def add_card(self, card):
        self.cards.append(card)

    def add_cards(self, cards):
        self.cards.extend(cards)

    def remove_top_card(self):
        if not self.is_empty():
            return self.cards.pop()
        return None

    def remove_cards(self, beginning_index):
        if beginning_index < 0 or beginning_index >= len(self.cards):
            raise IndexError("Beginning index is out of bounds.")
        removed_cards = self.cards[beginning_index:]
        self.cards = self.cards[:beginning_index]
        return removed_cards

    def peek_top_card(self):
        if not self.is_empty():
            return self.cards[-1]
        return None

    def is_empty(self):
        return len(self.cards) == 0

    def __len__(self):
        return len(self.cards)

    def get_all_cards(self):
        return list(self.cards)