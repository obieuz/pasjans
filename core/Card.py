class Card:
    def __init__(self, suit_symbol: str, rank: str):
        self.suit_symbol = suit_symbol
        self.rank = rank

        if suit_symbol not in ["♠", "♣", "♦", "♥"]:
            raise ValueError("Invalid suit symbol. Use ♠, ♣, ♦, or ♥.")

        if rank not in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]:
            raise ValueError("Invalid rank. Use A, 2-10, J, Q, or K.")

        if suit_symbol in ["♠", "♣"]:
            self.color = "black"
        else:
            self.color = "red"
