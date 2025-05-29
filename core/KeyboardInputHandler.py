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
            return "ACTION_QUIT"
        elif key == ord('r'):
            return "ACTION_RESTART"
        elif key == ord('l'):
            return "ACTION_LOAD"
        elif key == ord("d"):
            return "ACTION_DRAW_CARD"
        elif key == curses.KEY_UP:
            return "ACTION_MOVE_UP"
        elif key == curses.KEY_DOWN:
            return "ACTION_MOVE_DOWN"
        elif key == curses.KEY_LEFT:
            return "ACTION_MOVE_LEFT"
        elif key == curses.KEY_RIGHT:
            return "ACTION_MOVE_RIGHT"
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            return "ACTION_USE"
        elif key == curses.KEY_RESIZE:
            return "ACTION_RESIZE"
        else:
            return None
