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

    def add_cards(self,cards):
        if not cards:
            return
        self.visible_cards.extend(cards)

    def can_place_card(self, card):
        if len(self.visible_cards) == 0:
            if card.rank == "K":
                return True
            else:
                return False
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

    def flip_after_deleting(self):
        if len(self.visible_cards) == 0:
            if len(self.hidden_cards) == 0:
                return
            card = self.hidden_cards.pop()
            card.flip()
            self.visible_cards = [card]


    def debug(self):
        print("Tableau Pile Debug:")
        print(f"Visible Cards: {[str(card) for card in self.visible_cards]}")
        print(f"Hidden Cards: {[str(card) for card in self.hidden_cards]}")
        print(f"Total Visible Cards: {len(self.visible_cards)}")
        print(f"Total Hidden Cards: {len(self.hidden_cards)}")

    def remove_cards_to_index(self, index,cards_to_delete):
        if index < 0 or index >= len(self.visible_cards):
            print("Index out of range.")
            return None

        print(index)
        print(self.visible_cards[index+cards_to_delete:])

        self.visible_cards = self.visible_cards[index+cards_to_delete:]
        self.flip_after_deleting()
