import unittest

from core.Card import Card
from gui.TextCardRenderer import TextCardRenderer


class TestTextCardRenderer(unittest.TestCase):
    def setUp(self):
        self.renderer = TextCardRenderer()

    def test_render_card(self):
        card = Card("♠", "A")
        expected_output = "[A♠]"
        self.assertEqual(self.renderer.render_card(card), expected_output)

    def test_render_top_of_the_card(self):
        card = Card("♥", "K")
        expected_output = "[K♥]"
        self.assertEqual(self.renderer.render_top_of_the_card(card), expected_output)

    def test_render_card_column(self):
        cards = [Card("♦", "10"), Card("♣", "J")]
        expected_output = "[10♦]\n[J♣]\n"
        self.assertEqual(self.renderer.render_card_column(cards), expected_output)