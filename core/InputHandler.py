from abc import ABC, abstractmethod


class InputHandler(ABC):
    @abstractmethod
    def get_player_action(self, game_state):
        pass
