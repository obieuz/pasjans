ranks = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13
}

class Card:
    def __init__(self, suit_symbol: str, rank: str):
        self.suit_symbol = suit_symbol
        self.rank = rank
        self.rank_id = ranks[rank]
        self.is_face_up = False
        self.is_selected = False
        self.top_left = (None, None)
        self.bottom_right = (None, None)

        if suit_symbol not in ["♠", "♣", "♦", "♥"]:
            raise ValueError("Zły symbol. Użyj ♠, ♣, ♦, albo ♥.")

        if rank not in ranks.keys():
            raise ValueError("Zła ranga. Użyj A, 2-10, J, Q, albo K.")

        if suit_symbol in ["♠", "♣"]:
            self.color = "black"
        else:
            self.color = "red"

    def flip(self):
        self.is_face_up = not self.is_face_up

    def __iter__(self):
        return iter([self.rank, self.suit_symbol])

    def __len__(self):
        return 1


