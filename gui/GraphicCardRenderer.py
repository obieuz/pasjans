from gui.AbstractCardRenderer import AbstractCardRenderer


class GraphicCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        if not card:
            return None
        return f"""
        {card.suit_symbol}-------{card.suit_symbol}
        | {card.rank}     |
        |       |
        |   {card.suit_symbol}   |
        |       |
        |     {card.rank} |
        {card.suit_symbol}-------{card.suit_symbol}
        """

    def render_top_of_the_card(self, card):
        if not card:
            return None
        return f"""
        {card.suit_symbol}-------{card.suit_symbol}
        | {card.rank}     |"""

    def render_card_column(self, cards):
        if not cards:
            return None
        card_column = ""
        for card in cards:
            card_column += self.render_top_of_the_card(card)
        return card_column
