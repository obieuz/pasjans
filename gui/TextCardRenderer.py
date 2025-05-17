from gui.AbstractCardRenderer import AbstractCardRenderer


class TextCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        return f"""[{card.rank}{card.suit_symbol}]"""

    def render_top_of_the_card(self, card):
        return f"""[{card.rank}{card.suit_symbol}]"""

    def render_card_column(self, cards):
        card_column = ""
        for card in cards:
            card_column += self.render_card(card) + "\n"
        return card_column
