from core.Card import Card
from gui.GraphicCardRenderer import GraphicCardRenderer
from gui.TextCardRenderer import TextCardRenderer


class GameManager:
    def __init__(self):
        self.CardRenderer = TextCardRenderer()

    def start_game(self):
        print("Game started!")

        cards = [
            Card(suit_symbol="♠", rank="A"),
            Card(suit_symbol="♣", rank="K"),
            Card(suit_symbol="♦", rank="Q"),
        ]

        draw_cards = self.CardRenderer.render_card_column(cards)

        print(draw_cards)

        # Example of using CardRenderer to render a card
        # rank = "A"
        # suit_symbol = "♠"
        # card = self.CardRenderer.render_card(rank, suit_symbol)
        # print(card)
