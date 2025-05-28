class GameState:
    def __init__(self):
        self.states = []
        self.first_time_used = False
        self.last_number_of_move = -1

    def push_state(self, stock_pile, tableau_piles, foundation_piles,selected_card_pile , move_order, move_order_horizontal_index, move_order_vertical_index, number_of_moves, game_state):
        if len(self.states) > 3:
            self.states.pop(0)
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

    def load_state(self):
        if not self.states:
            print("No states loaded")
            return None
        return self.states.pop(-2)
