# Klasa Deck

Reprezentuje standardową talię 52 kart do gry. Dziedziczy po klasie `CardStack`, rozszerzając jej funkcjonalność o tworzenie pełnej talii, tasowanie oraz rozdawanie kart.

## Dziedziczenie

*   `CardStack`: `Deck` jest podklasą `CardStack` i dziedziczy jej atrybuty (`cards`, `is_selected`) oraz metody (np. `is_empty`, `__len__`).

## Atrybuty

Dziedziczone z `CardStack`:
*   `cards` (`list`): Lista obiektów klasy `Card`, reprezentująca karty w talii.
*   `is_selected` (`bool`): Flaga wskazująca, czy cała talia jest zaznaczona (zazwyczaj nieużywane dla pełnej talii przed rozdaniem, ale dziedziczone).

Dodatkowe atrybuty:
*   `shuffler`: Obiekt klasy `Shuffler` (zakładamy, że istnieje taka klasa), odpowiedzialny za implementację algorytmu tasowania kart.

## Metody

### `__init__(self)`
Konstruktor klasy. Inicjalizuje nową talię kart.

*   **Zachowanie:**
    *   Wywołuje konstruktor klasy nadrzędnej `CardStack` (`super().__init__()`) w celu inicjalizacji atrybutu `self.cards` jako pustej listy.
    *   Wywołuje metodę `self.create_deck()` w celu zapełnienia talii standardowymi 52 kartami.
    *   Tworzy instancję obiektu `Shuffler` i przypisuje ją do `self.shuffler`.

### `create_deck(self)`
Tworzy standardową, uporządkowaną talię 52 kart i dodaje je do atrybutu `self.cards`.

*   **Zachowanie:**
    *   Definiuje standardowe kolory (`suits = ["♠", "♣", "♦", "♥"]`) i wartości (`ranks = ["A", ..., "K"]`).
    *   Iteruje przez wszystkie kombinacje kolorów i wartości, tworząc dla każdej z nich nowy obiekt `Card`.
    *   Każda nowo utworzona karta jest dodawana do listy `self.cards`.

### `shuffle(self)`
Tasuje karty w talii.

*   **Zachowanie:**
    *   Wywołuje metodę `shuffle` obiektu `self.shuffler`, przekazując jej aktualną listę kart (`self.cards`).
    *   Zastępuje listę `self.cards` potasowaną listą zwróconą przez `self.shuffler.shuffle()`.

### `deal_card(self)`
Pobiera (usuwa) i zwraca jedną kartę z "wierzchu" talii (ostatni element listy `self.cards`).

*   **Zachowanie:**
    *   Jeśli talia nie jest pusta (lista `self.cards` zawiera elementy), usuwa ostatnią kartę z listy i ją zwraca.
*   **Zwraca:**
    *   `Card`: Obiekt karty pobranej z talii.
    *   `None`: Jeśli talia jest pusta.

### `__str__(self)`
Zwraca reprezentację tekstową obiektu talii, informującą o liczbie kart w talii.

*   **Zwraca:**
    *   `str`: Łańcuch znaków w formacie "Deck with X cards.", gdzie X to aktualna liczba kart w talii.