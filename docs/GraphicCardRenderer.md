# Klasa GraphicCardRenderer

Konkretna implementacja `AbstractCardRenderer`, która renderuje karty do gry jako ASCII art. Dostosowuje wygląd kart (rozmiar i szczegółowość) w zależności od dostępnej szerokości ekranu.

## Dziedziczenie

*   `AbstractCardRenderer`: `GraphicCardRenderer` jest podklasą `AbstractCardRenderer` i implementuje jej abstrakcyjne metody.

## Importy

*   `ABC` (z `abc`) - nie jest bezpośrednio importowany w tym pliku, ale jest używany w klasie bazowej.
*   `AbstractCardRenderer` (z `gui.AbstractCardRenderer`)

## Atrybuty Instancji

*   `screen_width` (`int`): Szerokość ekranu terminala w znakach. Używana do decydowania, czy renderować standardowe czy mniejsze (small) wersje kart.

## Metody

### `__init__(self, screen_width)`
Konstruktor klasy.

*   **Parametry:**
    *   `screen_width` (`int`): Aktualna szerokość ekranu terminala.
*   **Zachowanie:**
    *   Przypisuje przekazaną wartość `screen_width` do atrybutu `self.screen_width`.

### `render_card(self, card) -> list[str] | None`
Implementacja metody z `AbstractCardRenderer`. Renderuje pełne przedstawienie pojedynczej karty jako ASCII art.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty do wyrenderowania.
*   **Zachowanie:**
    1.  Jeśli `card` to `None`, zwraca `None`.
    2.  Jeśli `self.screen_width < 150`, wywołuje `self.render_card_small(card)` i zwraca jej wynik.
    3.  **Dla karty zakrytej (standardowy rozmiar):** Zwraca predefiniowaną listę stringów reprezentującą rewers karty.
    4.  **Dla karty odkrytej (standardowy rozmiar):**
        *   Oblicza odstępy (`rank_spacing_top`, `rank_spacing_bottom`) dla poprawnego wyrównania rangi "10".
        *   Zwraca listę stringów tworzących ASCII art awersu karty, zawierający jej symbol koloru, rangę i symbol koloru w centralnej części.
*   **Zwraca:**
    *   `list[str]`: Lista stringów, gdzie każdy string to jedna linia ASCII artu karty.
    *   `None`: Jeśli `card` jest `None`.

### `render_top_of_the_card(self, card) -> list[str] | None`
Implementacja metody z `AbstractCardRenderer`. Renderuje tylko górną, widoczną część karty (np. w stosie).

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty.
*   **Zachowanie:**
    1.  Jeśli `card` to `None`, zwraca `None`.
    2.  Jeśli `self.screen_width < 150`, wywołuje `self.render_small_top_of_the_card(card)` i zwraca jej wynik.
    3.  **Dla karty zakrytej (standardowy rozmiar):** Zwraca predefiniowaną listę stringów reprezentującą górną część rewersu.
    4.  **Dla karty odkrytej (standardowy rozmiar):**
        *   Oblicza odstęp (`rank_spacing`) dla rangi "10".
        *   Zwraca listę stringów tworzących ASCII art górnej części awersu karty (symbol koloru i ranga).
*   **Zwraca:**
    *   `list[str]`: Lista stringów reprezentująca górną część karty.
    *   `None`: Jeśli `card` jest `None`.

### `render_card_column(self, cards) -> str | None`
Implementacja metody z `AbstractCardRenderer`. Renderuje całą kolumnę kart, sklejając reprezentacje poszczególnych kart.
*   *Uwaga: Ta metoda zwraca pojedynczy string, co może nie być zgodne z oczekiwaniami `Drawer`, który iteruje po liniach. Może wymagać dostosowania, jeśli `Drawer` oczekuje listy stringów dla kolumn.*

*   **Parametry:**
    *   `cards` (`list[Card]`): Lista kart w kolumnie.
*   **Zachowanie:**
    1.  Jeśli `cards` jest pusta lub `None`, zwraca `None`.
    2.  Iteruje po kartach w liście:
        *   Dla ostatniej karty w kolumnie, używa `self.render_card(card)`.
        *   Dla pozostałych kart, używa `self.render_top_of_the_card(card)`.
        *   Konkatenuje zwrócone stringi (lub listy stringów, jeśli renderery zwracają listy) do `card_column`.
*   **Zwraca:**
    *   `str`: Połączona reprezentacja tekstowa całej kolumny kart.
    *   `None`: Jeśli `cards` jest pusta lub `None`.

### `render_blank_card(self, suit_symbol) -> list[str]`
Implementacja metody z `AbstractCardRenderer`. Renderuje puste miejsce na kartę (placeholder).

*   **Parametry:**
    *   `suit_symbol` (`str`): Symbol koloru, który może być wyświetlony na pustym miejscu.
*   **Zachowanie:**
    1.  Jeśli `self.screen_width < 150`, wywołuje `self.render_small_blank_card(suit_symbol)` i zwraca jej wynik.
    2.  **Dla standardowego rozmiaru:** Zwraca predefiniowaną listę stringów tworzących ASCII art pustego miejsca, z symbolem koloru na krawędziach i w centrum.
*   **Zwraca:**
    *   `list[str]`: Lista stringów reprezentująca puste miejsce na kartę.

### `render_small_top_of_the_card(self, card) -> list[str] | None`
Metoda pomocnicza do renderowania górnej części karty w mniejszym rozmiarze (gdy `screen_width < 150`).

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty.
*   **Zachowanie:**
    1.  Jeśli `card` to `None`, zwraca `None`.
    2.  **Dla karty zakrytej (mały rozmiar):** Zwraca predefiniowaną listę stringów.
    3.  **Dla karty odkrytej (mały rozmiar):**
        *   Oblicza odstęp (`rank_spacing`).
        *   Zwraca listę stringów tworzących mniejszy ASCII art górnej części awersu.
*   **Zwraca:**
    *   `list[str]` lub `None`.

### `render_card_small(self, card) -> list[str] | None`
Metoda pomocnicza do renderowania pełnej karty w mniejszym rozmiarze.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty.
*   **Zachowanie:**
    1.  Jeśli `card` to `None`, zwraca `None`.
    2.  **Dla karty zakrytej (mały rozmiar):** Zwraca predefiniowaną listę stringów.
    3.  **Dla karty odkrytej (mały rozmiar):**
        *   Oblicza odstępy (`rank_spacing_top`, `rank_spacing_bottom`).
        *   Zwraca listę stringów tworzących mniejszy ASCII art pełnego awersu.
*   **Zwraca:**
    *   `list[str]` lub `None`.

### `render_small_blank_card(self, suit_symbol) -> list[str]`
Metoda pomocnicza do renderowania pustego miejsca na kartę w mniejszym rozmiarze.

*   **Parametry:**
    *   `suit_symbol` (`str`): Symbol koloru.
*   **Zachowanie:**
    *   Zwraca predefiniowaną listę stringów tworzących mniejszy ASCII art pustego miejsca.
*   **Zwraca:**
    *   `list[str]`.