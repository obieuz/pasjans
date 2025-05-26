class CardStack:
    def __init__(self, cards=None):
        self.cards = cards if cards is not None else []
        self.is_selected = False

    def add_card(self, card):
        if self.can_accept_card(card):
            self.cards.append(card)

    def add_cards(self, cards):
        first_card = cards[0] if cards else None
        if first_card and self.can_accept_card(first_card):
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

    def can_accept_card(self, card):
        if self.is_empty():
            if card.rank == "K":
                return True
        last_card = self.peek_top_card()
        if last_card.suit == card.suit:
            return False
        if last_card.rank_id - card.rank_id == 1:
            return True



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