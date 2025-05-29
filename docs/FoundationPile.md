# Klasa FoundationPile

Reprezentuje jeden z czterech stosów fundamentowych w grze Pasjans (Klondike). Celem jest ułożenie na nim kart tego samego koloru w porządku rosnącym, od Asa do Króla. Klasa dziedziczy po `CardStack`, specjalizując logikę akceptowania kart.

## Dziedziczenie

*   `CardStack`: `FoundationPile` jest podklasą `CardStack` i dziedziczy jej atrybuty (`cards`, `is_selected`) oraz metody (np. `add_card`, `remove_top_card`, `is_empty`, `__len__`, `peek_top_card`).

## Atrybuty

Dziedziczone z `CardStack`:
*   `cards` (`list`): Lista obiektów klasy `Card`, przechowująca karty znajdujące się na tym stosie fundamentowym.
*   `is_selected` (`bool`): Flaga wskazująca, czy cały stos jest aktualnie zaznaczony.

Specyficzne dla `FoundationPile`:
*   `suit_symbol` (`str`): Symbol wymaganego koloru dla tego stosu fundamentowego (np. "♠", "♥", "♦", "♣"). Ustawiany podczas inicjalizacji.

## Metody

### `__init__(self, required_suit)`
Konstruktor klasy. Inicjalizuje nowy stos fundamentowy z określonym wymaganym kolorem.

*   **Parametry:**
    *   `required_suit` (`str`): Symbol koloru (np. "♠", "♥"), który będzie akceptowany przez ten stos fundamentowy.
*   **Zachowanie:**
    *   Wywołuje konstruktor klasy nadrzędnej `CardStack` (`super().__init__()`) w celu inicjalizacji atrybutu `self.cards`.
    *   Ustawia atrybut `self.suit_symbol` na podaną wartość `required_suit`.

### `can_accept_card(self, card)`
Przesłania metodę z `CardStack`. Określa, czy dana karta może zostać umieszczona na wierzchu tego stosu fundamentowego.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty, której możliwość umieszczenia jest sprawdzana.
*   **Zachowanie:**
    1.  **Jeśli stos jest pusty (`self.is_empty()`):**
        *   Karta jest akceptowana, jeśli jej ranga to As (`card.rank == "A"`) ORAZ jej symbol koloru (`card.suit_symbol`) jest zgodny z wymaganym kolorem stosu (`self.suit_symbol`).
    2.  **Jeśli stos nie jest pusty:**
        *   Sprawdza, czy symbol koloru karty (`card.suit_symbol`) jest różny od wymaganego koloru stosu (`self.suit_symbol`). Jeśli tak, karta nie jest akceptowana (zwraca `False`).
        *   Pobiera kartę z wierzchu stosu (`last_card = self.peek_top_card()`).
        *   Karta jest akceptowana, jeśli jej numeryczna ranga (`card.rank_id`) jest o jeden większa niż numeryczna ranga karty na wierzchu stosu (`last_card.rank_id + 1 == card.rank_id`).
*   **Zwraca:**
    *   `bool`: `True`, jeśli karta może zostać umieszczona na stosie fundamentowym zgodnie z zasadami Pasjansa, `False` w przeciwnym razie.