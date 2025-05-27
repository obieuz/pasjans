class GameState:
    def __init__(self):
        self.states = []
        self.first_time_used = False

    def push_state(self, stock_pile, tableau_piles, foundation_piles, move_order, move_order_horizontal_index, move_order_vertical_index):
        if len(self.states) > 3:
            self.states.pop(0)
        state = {
            "stock_pile": stock_pile,
            "tableau_piles": tableau_piles,
            "foundation_piles": foundation_piles,
            "move_order": move_order,
            "move_order_horizontal_index": move_order_horizontal_index,
            "move_order_vertical_index": move_order_vertical_index
        }
        self.states.append(state)

    def load_state(self):
        if not self.first_time_used:
            self.first_time_used = True
            self.states.pop()
        if not self.states:
            return None
        return self.states.pop()
