# Klasa KeyboardInputHandler

Konkretna implementacja `InputHandler`, która odczytuje wejście gracza z klawiatury przy użyciu biblioteki `curses`. Mapuje naciśnięcia klawiszy na predefiniowane akcje gry.

## Dziedziczenie

*   `InputHandler`: `KeyboardInputHandler` jest podklasą `InputHandler` i implementuje jej abstrakcyjną metodę `get_player_action`.
*   `ABC`: Dziedziczenie po `ABC` (Abstract Base Class) jest tutaj zadeklarowane, ale klasa ta jest konkretną implementacją, a nie klasą abstrakcyjną samą w sobie, ponieważ implementuje wszystkie wymagane metody abstrakcyjne z `InputHandler`.

## Atrybuty

*   `drawer` (`Drawer`): Referencja do obiektu `Drawer`, który zarządza ekranem `curses`. `KeyboardInputHandler` używa `drawer.screen` do odczytywania naciśnięć klawiszy.
*   `selected_pile_type` (`any`): Inicjalizowany na `None`. W przedstawionym kodzie nie jest używany w metodzie `get_player_action`. Może być przeznaczony do przechowywania informacji o typie aktualnie wybranego stosu.
*   `selected_pile_index` (`int`): Inicjalizowany na `0`. W przedstawionym kodzie nie jest używany w metodzie `get_player_action`. Może być przeznaczony do przechowywania indeksu aktualnie wybranego stosu.
*   `selected_card_in_tableau_index` (`any`): Inicjalizowany na `None`. W przedstawionym kodzie nie jest używany w metodzie `get_player_action`. Może być przeznaczony do przechowywania indeksu wybranej karty w stosie tableau.

## Metody

### `__init__(self, drawer)`
Konstruktor klasy.

*   **Parametry:**
    *   `drawer` (`Drawer`): Obiekt `Drawer` (lub inny obiekt posiadający atrybut `screen` będący obiektem ekranu `curses`), który będzie używany do odczytu wejścia.
*   **Zachowanie:**
    *   Przypisuje przekazany obiekt `drawer` do atrybutu `self.drawer`.
    *   Inicjalizuje atrybuty `selected_pile_type`, `selected_pile_index` oraz `selected_card_in_tableau_index` ich wartościami domyślnymi.

### `get_player_action(self)`
Implementacja metody abstrakcyjnej z `InputHandler`. Odczytuje pojedyncze naciśnięcie klawisza z ekranu `curses` i mapuje je na odpowiednią stałą reprezentującą akcję gry.

*   **Zachowanie:**
    1.  Wywołuje `self.drawer.screen.getch()` w celu pobrania kodu naciśniętego klawisza. Jest to operacja blokująca, czekająca na akcję użytkownika.
    2.  Na podstawie wartości `key` (kodu klawisza) zwraca odpowiedni ciąg znaków (string) reprezentujący akcję:
        *   `'q'`: Zwraca `"ACTION_QUIT"`
        *   `'r'`: Zwraca `"ACTION_RESTART"`
        *   `'l'`: Zwraca `"ACTION_LOAD"`
        *   `'d'`: Zwraca `"ACTION_DRAW_CARD"` (potencjalnie do dobierania karty ze stosu)
        *   `curses.KEY_UP`: Zwraca `"ACTION_MOVE_UP"` (strzałka w górę)
        *   `curses.KEY_DOWN`: Zwraca `"ACTION_MOVE_DOWN"` (strzałka w dół)
        *   `curses.KEY_LEFT`: Zwraca `"ACTION_MOVE_LEFT"` (strzałka w lewo)
        *   `curses.KEY_RIGHT`: Zwraca `"ACTION_MOVE_RIGHT"` (strzałka w prawo)
        *   `curses.KEY_ENTER` lub `10` lub `13`: Zwraca `"ACTION_USE"` (klawisz Enter)
        *   `curses.KEY_RESIZE`: Zwraca `"ACTION_RESIZE"` (zdarzenie zmiany rozmiaru okna)
    3.  Jeśli naciśnięty klawisz nie pasuje do żadnej z powyższych opcji, zwraca `None`.
*   **Zwraca:**
    *   `str`: Ciąg znaków identyfikujący akcję gracza (np. `"ACTION_QUIT"`, `"ACTION_MOVE_UP"`) lub
    *   `None`: Jeśli naciśnięty klawisz nie jest przypisany do żadnej akcji.