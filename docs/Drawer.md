# Klasa Drawer

Odpowiada za rysowanie całego interfejsu graficznego gry Pasjans w terminalu przy użyciu biblioteki `curses`. Zarządza renderowaniem kart, stosów, informacji o grze oraz obsługuje dynamiczne dostosowywanie wyglądu do rozmiaru terminala.

## Importy

*   `curses`: Główna biblioteka do tworzenia interfejsów tekstowych w terminalu.
*   `os`: Używany do pobierania rozmiaru terminala (choć `curses` również to umożliwia).
*   `GraphicCardRenderer` (z `gui.GraphicCardRenderer`): Klasa odpowiedzialna za renderowanie kart w trybie "graficznym" (ASCII art).
*   `TextCardRenderer` (z `gui.TextCardRenderer`): Klasa odpowiedzialna za renderowanie kart w trybie tekstowym (np. "AS" dla Asa Pik).

## Funkcje Pomocnicze (poza klasą)

### `get_terminal_size()`
*   **Zachowanie:** Pobiera i zwraca aktualne wymiary terminala (liczba wierszy i kolumn).
*   **Zwraca:** `tuple (rows, columns)`.
    *   *Uwaga: Wewnątrz klasy `Drawer` używana jest metoda `self.screen.getmaxyx()` z `curses`, która realizuje to samo zadanie.*

## Atrybuty Instancji

### Wymiary i Konfiguracja Ekranu
*   `screen_width` (`int`): Szerokość ekranu terminala w znakach.
*   `screen_height` (`int`): Wysokość ekranu terminala w znakach.
*   `screen` (`curses.window`): Główny obiekt okna `curses` (`stdscr`), na którym odbywa się rysowanie.
*   `card_renderer` (`AbstractCardRenderer`): Instancja konkretnego renderera kart (`GraphicCardRenderer` lub `TextCardRenderer`) używanego do rysowania kart.

### Kolory
*   `primary_color` (`int`): Identyfikator pary kolorów `curses` dla głównego koloru (np. czerwone karty). Domyślnie `1`.
*   `secondary_color` (`int`): Identyfikator pary kolorów `curses` dla drugorzędnego koloru (np. czarne karty, tekst informacyjny). Domyślnie `2`.
*   `selected_color` (`int`): Identyfikator pary kolorów `curses` dla zaznaczonych elementów. Domyślnie `3`.
*   `foreground_color` (`int`): Identyfikator pary kolorów `curses` dla domyślnego koloru pierwszego planu (np. ramki kart, puste miejsca). Domyślnie `5`.
*   `background_color` (`int`): Kolor tła całego ekranu gry. Domyślnie `curses.COLOR_GREEN`.
*   `card_background_color` (`int`): Kolor tła samych kart. Domyślnie `curses.COLOR_WHITE`.

### Wymiary Kart i Odstępy
*   `numbers_of_cards_in_stock_pile` (`int`): Liczba kart widocznych jednocześnie ze stosu odkrytych kart StockPile. Domyślnie `3`.
*   `column_gap` (`int`): Aktualny odstęp (w znakach) między kolumnami stosów kart.
*   `min_column_gap` (`int`): Minimalny dopuszczalny odstęp między kolumnami. Domyślnie `3`.
*   `row_gap` (`int`): Aktualny odstęp (w wierszach) między rzędami stosów kart.
*   `min_row_gap` (`int`): Minimalny dopuszczalny odstęp między rzędami. Domyślnie `3`.
*   `card_hidden_height` (`int`): Wysokość (w wierszach) widocznej części zakrytej lub częściowo zasłoniętej karty w stosie. Zależy od trybu renderowania.
*   `card_width` (`int`): Szerokość (w znakach) pojedynczej karty. Zależy od trybu renderowania i szerokości ekranu.
*   `card_height` (`int`): Wysokość (w wierszach) w pełni widocznej pojedynczej karty. Zależy od trybu renderowania i szerokości ekranu.

## Metody

### `__init__(self, stdscr, graphic_mode="default")`
Konstruktor klasy. Inicjalizuje ekran `curses`, kolory, wymiary kart oraz wybiera odpowiedni renderer kart.

*   **Parametry:**
    *   `stdscr` (`curses.window`): Główny obiekt okna `curses`.
    *   `graphic_mode` (`str`, domyślnie `"default"`): Określa preferowany tryb renderowania. W obecnej implementacji wpływa głównie na inicjalizację par kolorów.
*   **Zachowanie:**
    1.  Inicjalizuje podstawowe atrybuty kolorów i domyślną liczbę kart widocznych w StockPile.
    2.  Przypisuje `stdscr` do `self.screen`.
    3.  Pobiera aktualne wymiary ekranu (`self.screen.getmaxyx()`).
    4.  Domyślnie tworzy instancję `GraphicCardRenderer`.
    5.  Inicjalizuje system kolorów `curses` (`curses.start_color()`).
    6.  Inicjalizuje parę kolorów dla tła ekranu (`curses.init_pair(4, ...)`).
    7.  Ustawia tło ekranu i czyści go.
    8.  Ustawia początkowe wartości `column_gap` i `row_gap`.
    9.  Na podstawie typu `card_renderer` (i szerokości ekranu) dostosowuje `card_hidden_height`, `card_width`, `card_height`. Automatycznie przełącza na `TextCardRenderer`, jeśli szerokość ekranu jest zbyt mała dla trybu graficznego.
    10. Wywołuje `self.calculate_gaps()` do obliczenia optymalnych odstępów.
    11. Jeśli `graphic_mode` jest `"default"`, inicjalizuje dodatkowe pary kolorów dla kart i zaznaczenia.

### `draw_game_board(self, stock_pile, tableau_piles, foundation_piles, number_of_moves)`
Główna metoda rysująca całą planszę gry.

*   **Parametry:**
    *   `stock_pile` (`StockPile`): Obiekt stosu dobierania.
    *   `tableau_piles` (`list[TableauPile]`): Lista stosów tableau.
    *   `foundation_piles` (`list[FoundationPile]`): Lista stosów fundamentowych.
    *   `number_of_moves` (`int`): Aktualna liczba ruchów wykonanych przez gracza.
*   **Zachowanie:**
    1.  Czyści ekran (`self.screen.clear()`, `self.screen.refresh()`).
    2.  Wywołuje metody pomocnicze do narysowania poszczególnych elementów:
        *   `self.draw_foundation_piles(foundation_piles)`
        *   `self.draw_stock_pile(stock_pile)`
        *   `self.draw_tableau_piles(tableau_piles)`
        *   `self.draw_moves(number_of_moves)`
    3.  Odświeża ekran, aby wyświetlić wszystkie zmiany (`self.screen.refresh()`).

### `draw_card(self, card, x=0, y=0, is_first=False)`
Rysuje pojedynczą kartę na podanych współrzędnych.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty do narysowania.
    *   `x` (`int`, domyślnie `0`): Współrzędna X lewego górnego rogu karty.
    *   `y` (`int`, domyślnie `0`): Współrzędna Y lewego górnego rogu karty.
    *   `is_first` (`bool`, domyślnie `False`): Flaga wskazująca, czy karta jest pierwszą (najbardziej wierzchnią) w stosie i powinna być narysowana w całości. Jeśli `False`, rysowana jest tylko górna część karty.
*   **Zachowanie:**
    1.  Jeśli `card` to `None`, nic nie robi.
    2.  Używa `self.card_renderer` do uzyskania reprezentacji tekstowej karty (`render_card` dla `is_first=True`, `render_top_of_the_card` dla `is_first=False`).
    3.  Zapisuje współrzędne `top_left` i `bottom_right` w obiekcie `card`.
    4.  Iteruje po liniach zwróconych przez renderer i rysuje je na ekranie (`self.screen.addstr`), używając odpowiedniej pary kolorów w zależności od stanu karty (odkryta/zakryta, zaznaczona, kolor czerwony/czarny).

### `draw_tableau_pile(self, tableau_pile, x=0, y=0)`
Rysuje pojedynczy stos tableau.

*   **Parametry:**
    *   `tableau_pile` (`TableauPile`): Obiekt stosu tableau do narysowania.
    *   `x`, `y`: Współrzędne lewego górnego rogu stosu.
*   **Zachowanie:**
    1.  Jeśli stos jest całkowicie pusty, rysuje puste miejsce (`self.draw_blank_card`).
    2.  Jeśli stos jest zaznaczony (`tableau_pile.is_selected`), rysuje wokół niego ramkę (`self.draw_border_around_object`).
    3.  Iteruje po kartach stosu (najpierw zakryte, potem odkryte) i rysuje każdą z nich za pomocą `self.draw_card`. Karty nachodzą na siebie o `self.card_hidden_height`. Ostatnia karta jest rysowana w całości.

### `draw_tableau_piles(self, tableau_piles)`
Rysuje wszystkie stosy tableau obok siebie.

*   **Parametry:**
    *   `tableau_piles` (`list[TableauPile]`): Lista stosów tableau.
*   **Zachowanie:**
    *   Oblicza pozycję X dla każdego stosu tableau, uwzględniając szerokość kart i `self.column_gap`.
    *   Wywołuje `self.draw_tableau_pile` dla każdego stosu.

### `draw_foundation_pile(self, foundation_pile, x=0, y=0)`
Rysuje pojedynczy stos fundamentowy.

*   **Parametry:**
    *   `foundation_pile` (`FoundationPile`): Obiekt stosu fundamentowego.
    *   `x`, `y`: Współrzędne lewego górnego rogu stosu.
*   **Zachowanie:**
    1.  Jeśli stos jest zaznaczony, rysuje ramkę.
    2.  Jeśli stos jest pusty, rysuje puste miejsce z symbolem koloru stosu (`self.draw_blank_card`).
    3.  Jeśli stos nie jest pusty, rysuje wierzchnią kartę w całości (`self.draw_card` z `is_first=True`).

### `draw_foundation_piles(self, foundation_piles)`
Rysuje wszystkie stosy fundamentowe.

*   **Parametry:**
    *   `foundation_piles` (`list[FoundationPile]`): Lista stosów fundamentowych.
*   **Zachowanie:**
    *   Oblicza pozycję X dla pierwszego stosu (zazwyczaj po prawej stronie planszy).
    *   Wywołuje `self.draw_foundation_pile` dla każdego stosu, umieszczając je jeden pod drugim.

### `draw_blank_card(self, suit_symbol, x=0, y=0)`
Rysuje reprezentację pustego miejsca na kartę.

*   **Parametry:**
    *   `suit_symbol` (`str`): Symbol koloru, który może być wyświetlony na pustym miejscu.
    *   `x`, `y`: Współrzędne.
*   **Zachowanie:**
    *   Używa `self.card_renderer.render_blank_card()` do uzyskania reprezentacji tekstowej.
    *   Rysuje linie na ekranie.

### `draw_stock_pile(self, stock_pile, x=1, y=0)`
Rysuje stos dobierania (StockPile), składający się ze stosu zakrytego i stosu odkrytego.

*   **Parametry:**
    *   `stock_pile` (`StockPile`): Obiekt stosu dobierania.
    *   `x`, `y`: Współrzędne.
*   **Zachowanie:**
    1.  Jeśli stos jest zaznaczony, rysuje ramkę wokół miejsca na stos zakryty.
    2.  Rysuje wierzchnią kartę stosu zakrytego (lub puste miejsce, jeśli jest pusty).
    3.  Jeśli są karty na stosie odkrytym (`stock_pile.visible_cards`), rysuje określoną ich liczbę (`self.numbers_of_cards_in_stock_pile`) pod stosem zakrytym. Karty te nachodzą na siebie, a ostatnia jest w pełni widoczna.

### `draw_border_around_object(self, x, y, width, height)`
Rysuje prostokątną ramkę wokół obiektu przy użyciu znaków ASCII do rysowania ramek (`curses.ACS_*`).

*   **Parametry:**
    *   `x`, `y`: Współrzędne lewego górnego rogu *wewnątrz* ramki.
    *   `width`, `height`: Szerokość i wysokość obszaru *wewnątrz* ramki. Ramka zostanie narysowana dookoła tego obszaru.
*   **Zachowanie:**
    *   Rysuje narożniki i linie poziome/pionowe tworzące ramkę.

### `draw_moves(self, number_of_moves, x=0, y=0)`
Wyświetla liczbę wykonanych ruchów na ekranie, zazwyczaj wyśrodkowaną u góry.

*   **Parametry:**
    *   `number_of_moves` (`int`): Liczba ruchów.
    *   `x`, `y`: Współrzędne (domyślnie wyśrodkowane).
*   **Zachowanie:**
    *   Tworzy tekst "Liczba ruchów: [liczba]".
    *   Rysuje tekst na ekranie.

### `calculate_gaps(self)`
Oblicza optymalne odstępy (pionowe i poziome) między stosami kart, aby zmieściły się na ekranie.

*   **Zachowanie:**
    *   Na podstawie szerokości/wysokości ekranu oraz szerokości/wysokości kart oblicza `self.column_gap` i `self.row_gap`.
    *   Dba o to, aby obliczone odstępy nie były mniejsze niż `self.min_column_gap` i `self.min_row_gap`.

### `resize_window(self)`
Obsługuje zdarzenie zmiany rozmiaru okna terminala. Dostosowuje wymiary kart, odstępy i potencjalnie tryb renderowania.

*   **Zachowanie:**
    1.  Pobiera nowe wymiary ekranu (`self.screen.getmaxyx()`).
    2.  Jeśli używany jest `GraphicCardRenderer`, aktualizuje jego atrybut `screen_width`.
    3.  W zależności od nowej szerokości ekranu:
        *   Jeśli szerokość jest średnia (np. 70-150), dostosowuje `card_width`, `card_height` i minimalne odstępy do mniejszych wartości.
        *   Jeśli szerokość jest bardzo mała (np. <= 70), przełącza na `TextCardRenderer` i ustawia odpowiednie, mniejsze wymiary kart oraz minimalne odstępy.
    4.  Wywołuje `curses.resize_term()` do poinformowania `curses` o zmianie rozmiaru.
    5.  Wywołuje `self.calculate_gaps()` w celu ponownego obliczenia odstępów dla nowego rozmiaru.