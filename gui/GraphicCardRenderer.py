from abc import ABC

from gui.AbstractCardRenderer import AbstractCardRenderer


class GraphicCardRenderer(AbstractCardRenderer):
    def __init__(self):
        pass

    def render_card(self, card):
        if not card:
            return None

        if not card.is_face_up:
            return [
                f"---------",
                f"|       |",
                f"| -   - |",
                f"|       |",
                f"| ----- |",
                f"|       |",
                f"---------"
            ]

        rank_spacing_top = "    " if card.rank == "10" else "     "
        rank_spacing_bottom = "    " if card.rank == "10" else "     "

        return [
            f"{card.suit_symbol}-------{card.suit_symbol}",
            f"| {card.rank}{rank_spacing_top}|",
            "|       |",
            f"|   {card.suit_symbol}   |",
            "|       |",
            f"|{rank_spacing_bottom}{card.rank} |",
            f"{card.suit_symbol}-------{card.suit_symbol}"
        ]

    def render_top_of_the_card(self, card):
        if not card:
            return None

        if not card.is_face_up:
            return [
                f"---------",
                f"| ?     |"
            ]

        rank_spacing = "    " if card.rank == "10" else "     "

        return [
            f"{card.suit_symbol}-------{card.suit_symbol}",
            f"| {card.rank}{rank_spacing}|"
        ]

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

    def render_blank_card(self, suit_symbol):
        return [
            f"{suit_symbol}-------{suit_symbol}",
            f"|       |",
            "|       |",
            f"|   {suit_symbol}   |",
            "|       |",
            f"|       |",
            f"{suit_symbol}-------{suit_symbol}"
        ]
