from gui.AbstractCardRenderer import AbstractCardRenderer


class GraphicCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        if not card:
            return None

        rank_spacing_top = "    " if card.rank == "10" else "     "
        rank_spacing_bottom = "    " if card.rank == "10" else "     "

        return f"""
{card.suit_symbol}-------{card.suit_symbol}
| {card.rank}{rank_spacing_top}|
|       |
|   {card.suit_symbol}   |
|       |
|{rank_spacing_bottom}{card.rank} |
{card.suit_symbol}-------{card.suit_symbol}"""

    def render_top_of_the_card(self, card):
        if not card:
            return None

        rank_spacing = "    " if card.rank == "10" else "     "

        return f"""
{card.suit_symbol}-------{card.suit_symbol}
| {card.rank}{rank_spacing}|"""

    def render_card_column(self, cards):
        if not cards:
            return None
        card_column = ""
        for index, card in enumerate(cards):
            if index == len(cards) - 1:
                card_column += self.render_card(card)
                continue
            card_column += self.render_top_of_the_card(card)
        return card_column
