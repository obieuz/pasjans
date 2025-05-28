class GameState:
    def __init__(self):
        self.states = []
        self.first_time_used = False
        self.last_number_of_move = -1

    def push_state(self, stock_pile, tableau_piles, foundation_piles,selected_card_pile , move_order, move_order_horizontal_index, move_order_vertical_index, number_of_moves, game_state):
        state = {
            "stock_pile": stock_pile,
            "tableau_piles": tableau_piles,
            "foundation_piles": foundation_piles,
            "selected_card_pile": selected_card_pile,
            "move_order": move_order,
            "move_order_horizontal_index": move_order_horizontal_index,
            "move_order_vertical_index": move_order_vertical_index,
            "number_of_moves": number_of_moves,
            "game_state": game_state
        }
        self.last_number_of_move = number_of_moves
        self.states.append(state)

        if len(self.states) > 4:
            self.states.pop(0)

    def load_state(self):
        if len(self.states) == 0:
            return None
        if self.last_number_of_move == self.states[-1]["number_of_moves"]:
            if len(self.states) > 1:
                self.states = self.states[:-1]
            self.last_number_of_move = -1
            return self.states.pop()
        else:
            self.last_number_of_move = -1
            return self.states.pop() if self.states else None
