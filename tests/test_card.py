import unittest
from core.Card import Card


class TestCard(unittest.TestCase):
    def test_valid_card_black_suit(self):
        card = Card(suit_symbol="♠", rank="A")
        self.assertEqual(card.suit_symbol, "♠")
        self.assertEqual(card.rank, "A")
        self.assertEqual(card.color, "black")

    def test_valid_card_red_suit(self):
        card = Card(suit_symbol="♥", rank="10")
        self.assertEqual(card.suit_symbol, "♥")
        self.assertEqual(card.rank, "10")
        self.assertEqual(card.color, "red")

    def test_invalid_suit_symbol(self):
        with self.assertRaises(ValueError) as context:
            Card(suit_symbol="X", rank="A")
        self.assertEqual(str(context.exception), "Invalid suit symbol. Use ♠, ♣, ♦, or ♥.")

    def test_invalid_rank(self):
        with self.assertRaises(ValueError) as context:
            Card(suit_symbol="♠", rank="1")
        self.assertEqual(str(context.exception), "Invalid rank. Use A, 2-10, J, Q, or K.")

    def test_invalid_suit_and_rank(self):
        with self.assertRaises(ValueError):
            Card(suit_symbol="X", rank="1")
