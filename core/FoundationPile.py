from core.CardStack import CardStack


class FoundationPile(CardStack):
    def __init__(self, required_suit):
        super().__init__()
        self.suit_symbol = required_suit

    def can_accept_card(self, card):
        if self.is_empty():
            return card.rank == "A" and card.suit_symbol == self.suit_symbol
        else:
            if card.suit_symbol != self.suit_symbol:
                return False
            last_card = self.peek_top_card()
            return last_card.rank_id + 1 == card.rank_id


