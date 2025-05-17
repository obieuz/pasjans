from abc import ABC, abstractmethod


class AbstractCardRenderer(ABC):
    @abstractmethod
    def render_card(self, card):
        pass

    @abstractmethod
    def render_top_of_the_card(self, card):
        pass

    @abstractmethod
    def render_card_column(self, cards):
        pass
