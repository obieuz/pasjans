from core.Card import Card
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer


class GameManager:
    def __init__(self):
        self.CardRenderer = TextCardRenderer()

    def start_game(self):
        print("Game started!")

        cards = [
            Card(suit_symbol="♠", rank="10"),
            Card(suit_symbol="♦", rank="K"),
            Card(suit_symbol="♦", rank="10"),
        ]

        draw_cards = self.CardRenderer.render_card_column(cards)

        print(draw_cards)

        # card = Card(suit_symbol="♠", rank="10")
        # print(self.CardRenderer.render_card(card))
