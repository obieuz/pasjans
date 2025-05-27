class SelectedCardPile:
    def __init__(self):
        self.cards = []
        self.selected_from_horizontal_index = None
        self.selected_from_vertical_index = None

    def add_cards(self, cards, horizontal_index=None, vertical_index=None):
        if isinstance(cards, list):
            self.cards.extend(cards)
        else:
            self.cards.append(cards)

        self.selected_from_vertical_index = vertical_index
        self.selected_from_horizontal_index = horizontal_index

    def peek_top_card(self):
        if self.cards:
            return self.cards[-1]
        return None

    def is_empty(self):
        return len(self.cards) == 0

