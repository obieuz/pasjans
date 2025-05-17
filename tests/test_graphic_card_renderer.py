import unittest

from core.Card import Card
from gui.GraphicCardRenderer import GraphicCardRenderer


class TestGraphicCardRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = GraphicCardRenderer()

    def test_render_card_with_valid_card(self):
        card = Card(rank="A", suit_symbol="♠")
        expected_output = """
        ♠-------♠
        | A     |
        |       |
        |   ♠   |
        |       |
        |     A |
        ♠-------♠
        """
        self.assertEqual(self.renderer.render_card(card).strip(), expected_output.strip())

    def test_render_card_with_none(self):
        self.assertIsNone(self.renderer.render_card(None))

    def test_render_top_of_the_card_with_valid_card(self):
        card = Card(rank="K", suit_symbol="♥")
        expected_output = """
        ♥-------♥
        | K     |"""
        self.assertEqual(self.renderer.render_top_of_the_card(card).strip(), expected_output.strip())

    def test_render_top_of_the_card_with_none(self):
        self.assertIsNone(self.renderer.render_top_of_the_card(None))

    def test_render_card_column_with_valid_cards(self):
        cards = [
            Card(rank="2", suit_symbol="♦"),
            Card(rank="3", suit_symbol="♣")
        ]
        expected_output = """
        ♦-------♦
        | 2     |
        ♣-------♣
        | 3     |"""
        self.assertEqual(self.renderer.render_card_column(cards).strip(), expected_output.strip())

    def test_render_card_column_with_empty_list(self):
        self.assertIsNone(self.renderer.render_card_column([]))

    def test_render_card_column_with_none(self):
        self.assertIsNone(self.renderer.render_card_column(None))