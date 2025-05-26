class TableauPile:
    def __init__(self):
        self.hidden_cards = []
        self.visible_cards = []
        self.is_selected = False

    def add_initial_cards(self, cards):
        if not cards:
            return
        if len(cards) == 1:
            self.visible_cards = [cards[0]]
            self.visible_cards[0].flip()
            return
        self.hidden_cards = cards[:-1]
        visible_card = cards[-1]
        visible_card.flip()
        self.visible_cards = [visible_card]

    def can_place_card(self, card):
        if not self.visible_cards:
            if card.rank == "K":
                return True
        last_card = self.visible_cards[-1]
        if last_card.rank_id - card.rank_id == 1 and last_card.color != card.color:
            return True
        return False

    def can_place_stack(self, stack):
        if not self.visible_cards:
            if stack.peek_top_card().rank == "K":
                return True
        last_card = self.visible_cards[-1]
        stack_top_card = stack.peek_top_card()
        if last_card.rank_id - stack_top_card.rank_id == 1 and last_card.color != stack_top_card.color:
            return True
        return False

    def debug(self):
        print("Tableau Pile Debug:")
        print(f"Visible Cards: {[str(card) for card in self.visible_cards]}")
        print(f"Hidden Cards: {[str(card) for card in self.hidden_cards]}")
        print(f"Total Visible Cards: {len(self.visible_cards)}")
        print(f"Total Hidden Cards: {len(self.hidden_cards)}")
