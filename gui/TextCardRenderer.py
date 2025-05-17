from gui.AbstractCardRenderer import AbstractCardRenderer


class TextCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        color_code = "\033[31m" if card.color == "red" else ""
        reset_code = "\033[0m" if card.color == "red" else ""
        rank_spacing_top = " " if card.rank != "10" else ""
        return f"""{color_code}[{card.rank}{rank_spacing_top}{card.suit_symbol}]{reset_code}"""

    def render_top_of_the_card(self, card):
        color_code = "\033[31m" if card.color == "red" else ""
        reset_code = "\033[0m" if card.color == "red" else ""
        rank_spacing_top = " " if card.rank == "10" else ""
        return f"""{color_code}[{card.rank}{rank_spacing_top}{card.suit_symbol}]{reset_code}"""

    def render_card_column(self, cards):
        card_column = ""
        for card in cards:
            card_column += self.render_card(card) + "\n"
        return card_column
