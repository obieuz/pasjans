from gui.AbstractCardRenderer import AbstractCardRenderer


class TextCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        if not card.is_face_up:
            return " ? "
        rank_spacing_top = " " if card.rank != "10" else ""
        return f"""{card.rank}{rank_spacing_top}{card.suit_symbol}"""

    def render_top_of_the_card(self, card):
        return self.render_card(card)

    def render_card_column(self, cards):
        card_column = ""
        for card in cards:
            card_column += self.render_card(card) + "\n"
        return card_column

    def render_blank_card(self, suit_symbol):
        return f"? {suit_symbol}"
