# Klasa Card

Reprezentuje pojedynczą kartę do gry. Przechowuje informacje o jej kolorze (symbolu), wartości (figurze) oraz stanie (odkryta/zakryta, zaznaczona).

## Atrybuty

*   `suit_symbol` (`str`): Symbol koloru karty (np. "♠", "♥", "♦", "♣").
*   `rank` (`str`): Wartość/figura karty (np. "A", "7", "K").
*   `rank_id` (`int`): Numeryczna reprezentacja wartości karty, pobierana ze słownika `ranks` (zakładamy, że `ranks` to globalny słownik mapujący np. `{'A': 1, '2': 2, ..., 'K': 13}`). Przydatna do porównywania wartości kart.
*   `is_face_up` (`bool`): Flaga wskazująca, czy karta jest odkryta (`True`) czy zakryta (`False`). Domyślnie `False`.
*   `is_selected` (`bool`): Flaga wskazująca, czy karta jest aktualnie zaznaczona przez kursor nawigacji (np. w stosie Tableau). Domyślnie `False`.
*   `top_left` (`tuple`): Krotka `(y, x)` przechowująca współrzędne lewego górnego rogu karty na ekranie, używane do rysowania. Inicjalizowana jako `(None, None)`.
*   `bottom_right` (`tuple`): Krotka `(y, x)` przechowująca współrzędne prawego dolnego rogu karty na ekranie, używane do rysowania. Inicjalizowana jako `(None, None)`.
*   `in_selection` (`bool`): Flaga wskazująca, czy karta jest częścią grupy kart aktualnie wybranych do przeniesienia (np. ze stosu Tableau na inny stos). Domyślnie `False`.
*   `color` (`str`): Kolor karty ("red" dla kierów ♥ i kar ♦, "black" dla pików ♠ i trefli ♣), używany do rysowania. Ustawiany automatycznie na podstawie `suit_symbol`.

## Metody

### `__init__(self, suit_symbol: str, rank: str)`
Konstruktor klasy. Inicjalizuje nową kartę z podanym kolorem i wartością.

*   **Parametry:**
    *   `suit_symbol` (`str`): Symbol koloru karty. Musi być jednym z: "♠", "♣", "♦", "♥".
    *   `rank` (`str`): Wartość/figura karty. Musi być kluczem w globalnym słowniku `ranks` (np. "A", "2", ..., "10", "J", "Q", "K").
*   **Zachowanie:**
    *   Ustawia atrybuty `suit_symbol`, `rank`, `rank_id` (na podstawie `ranks`).
    *   Inicjalizuje flagi `is_face_up`, `is_selected`, `in_selection` na `False`.
    *   Inicjalizuje współrzędne `top_left` i `bottom_right` na `(None, None)`.
    *   Automatycznie ustawia atrybut `color` na "red" lub "black" na podstawie `suit_symbol`.
*   **Wyjątki:**
    *   `ValueError`: Jeśli podany `suit_symbol` jest nieprawidłowy.
    *   `ValueError`: Jeśli podany `rank` jest nieprawidłowy (nie znajduje się w kluczach słownika `ranks`).

### `flip(self)`
Odwraca kartę, zmieniając jej stan z odkrytej na zakrytą lub odwrotnie.
Modyfikuje atrybut `self.is_face_up` (np. z `True` na `False` i vice versa).

### `__iter__(self)`
Umożliwia iterację po obiekcie karty. Zwraca iterator, który pozwala uzyskać rangę i symbol koloru karty.
Dzięki temu można użyć składni takiej jak `r, s = card_object`.

*   **Zwraca:** Iterator dla listy `[self.rank, self.suit_symbol]`.

### `__len__(self)`
Zwraca "długość" obiektu karty. W tym przypadku, pojedyncza karta ma długość 1.

*   **Zwraca:** `int` (zawsze wartość 1).