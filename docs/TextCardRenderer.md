# Klasa TextCardRenderer

Konkretna implementacja `AbstractCardRenderer`, która renderuje karty do gry jako prosty tekst, np. "AS" dla Asa Pik lub " ? " dla karty zakrytej. Jest to minimalistyczna reprezentacja, przydatna przy bardzo małych rozmiarach terminala lub gdy tryb graficzny jest niedostępny/niepożądany.

## Dziedziczenie

*   `AbstractCardRenderer`: `TextCardRenderer` jest podklasą `AbstractCardRenderer` i implementuje jej abstrakcyjne metody.

## Importy

*   `AbstractCardRenderer` (z `gui.AbstractCardRenderer`)

## Atrybuty Instancji

Klasa `TextCardRenderer` w swojej obecnej formie nie definiuje żadnych atrybutów instancji w metodzie `__init__`.

## Metody

### `__init__(self)`
Konstruktor klasy.

*   **Zachowanie:**
    *   W obecnej implementacji metoda `__init__` jest pusta (`pass`) i nie wykonuje żadnych operacji inicjalizujących.

### `render_card(self, card) -> str`
Implementacja metody z `AbstractCardRenderer`. Renderuje pojedynczą kartę jako krótki ciąg tekstowy.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty do wyrenderowania.
*   **Zachowanie:**
    1.  **Dla karty zakrytej (`not card.is_face_up`):** Zwraca string `" ? "`.
    2.  **Dla karty odkrytej:**
        *   Oblicza `rank_spacing_top`: dodaje spację, jeśli ranga karty nie jest "10" (aby wyrównać długość stringa dla "10" vs inne rangi).
        *   Zwraca sformatowany string składający się z rangi karty, ewentualnej spacji i symbolu koloru karty (np. `"K♠"`, `"10♥"`).
*   **Zwraca:**
    *   `str`: Tekstowa reprezentacja karty.

### `render_top_of_the_card(self, card) -> str`
Implementacja metody z `AbstractCardRenderer`. W tej implementacji renderowanie "górnej części karty" jest identyczne z renderowaniem całej karty tekstowej.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty.
*   **Zachowanie:**
    *   Wywołuje `self.render_card(card)` i zwraca jej wynik.
*   **Zwraca:**
    *   `str`: Tekstowa reprezentacja karty.

### `render_card_column(self, cards) -> str`
Implementacja metody z `AbstractCardRenderer`. Renderuje kolumnę kart, gdzie każda karta jest reprezentowana tekstowo w nowej linii.

*   **Parametry:**
    *   `cards` (`list[Card]`): Lista kart w kolumnie.
*   **Zachowanie:**
    1.  Inicjalizuje pusty string `card_column`.
    2.  Iteruje po każdej karcie w liście `cards`:
        *   Renderuje kartę za pomocą `self.render_card(card)`.
        *   Dodaje wynik do `card_column` wraz ze znakiem nowej linii (`\n`).
*   **Zwraca:**
    *   `str`: Wieloliniowy string, gdzie każda linia to tekstowa reprezentacja jednej karty z kolumny.

### `render_blank_card(self, suit_symbol) -> str`
Implementacja metody z `AbstractCardRenderer`. Renderuje puste miejsce na kartę jako tekst.

*   **Parametry:**
    *   `suit_symbol` (`str`): Symbol koloru, który może być wyświetlony na pustym miejscu.
*   **Zachowanie:**
    *   Zwraca sformatowany string składający się ze znaku zapytania, spacji i symbolu koloru (np. `"? ♠"`).
*   **Zwraca:**
    *   `str`: Tekstowa reprezentacja pustego miejsca na kartę.