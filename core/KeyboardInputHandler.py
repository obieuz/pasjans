import curses
from abc import ABC

from core.InputHandler import InputHandler


class KeyboardInputHandler(InputHandler, ABC):
    def __init__(self, drawer):
        self.drawer = drawer
        self.selected_pile_type = None
        self.selected_pile_index = 0
        self.selected_card_in_tableau_index = None

    def get_player_action(self):
        key = self.drawer.screen.getch()
        if key == ord('q'):
            return "quit"
        elif key == ord('h'):
            return "help"
        elif key == ord('r'):
            return "restart"
        elif key == ord('s'):
            return "save"
        elif key == ord('l'):
            return "load"
        elif key == curses.KEY_UP:
            return "move_up"
        elif key == curses.KEY_DOWN:
            return "move_down"
        elif key == curses.KEY_LEFT:
            return "move_left"
        elif key == curses.KEY_RIGHT:
            return "move_right"
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            return "use"
        else:
            return None
