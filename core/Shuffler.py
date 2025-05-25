from time import time


class Shuffler:
    def __init__(self):
        pass

    def shuffle(self, cards):
        for i in range(len(cards) - 1, 0, -1):
            j = self.random_index(0, i)
            cards[i], cards[j] = cards[j],cards[i]
        return cards

    def random_index(self, start, end):
        seed = int(time() * 1000000) % (end - start + 1)
        return start + seed
