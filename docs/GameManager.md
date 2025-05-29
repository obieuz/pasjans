# Klasa GameManager

Główna klasa zarządzająca logiką gry Pasjans. Odpowiada za inicjalizację gry, główną pętlę gry, przetwarzanie akcji gracza, zarządzanie stanem gry oraz interakcję z innymi komponentami, takimi jak plansza, stosy kart, menu i system zapisu/odczytu.

## Atrybuty

### Główne komponenty gry
*   `end_screen`: Obiekt klasy `EndScreen`, odpowiedzialny za wyświetlanie ekranu końcowego gry.
*   `game_settings`: Słownik przechowujący ustawienia gry (np. trudność, nick gracza, tryb kolorów) pobrane z `StartMenu`.
*   `foundation_piles`: Lista obiektów `FoundationPile`, reprezentująca stosy fundamentowe.
*   `drawer`: Obiekt klasy `Drawer`, odpowiedzialny za rysowanie interfejsu gry w konsoli.
*   `tableau_piles`: Lista obiektów `TableauPile`, reprezentująca stosy tableau (kolumny robocze).
*   `stock_pile`: Obiekt klasy `StockPile`, reprezentujący stos kart do dobierania.
*   `selected_card_pile`: Obiekt klasy `SelectedCardPile`, przechowujący aktualnie wybrane przez gracza karty.
*   `deck`: Obiekt klasy `Deck`, reprezentujący talię kart.
*   `console`: Obiekt klasy `Console`, używany do interakcji z konsolą (np. przez `StartMenu`, `EndScreen`).
*   `input_handler`: Obiekt klasy `KeyboardInputHandler`, odpowiedzialny za odczytywanie akcji gracza z klawiatury.
*   `game_state_saver`: Obiekt klasy `GameState`, umożliwiający zapisywanie i wczytywanie stanu gry.
*   `leaderboard_manager_instance`: Obiekt klasy `LeaderboardManager`, zarządzający tabelą wyników.
*   `timer`: Obiekt klasy `Timer`, śledzący czas gry.

### Stan gry i nawigacja
*   `difficulty`: Poziom trudności gry (wpływa np. na liczbę kart dobieranych ze stosu).
*   `run`: Flaga logiczna (boolean), kontrolująca główną pętlę gry. Ustawienie na `False` kończy grę.
*   `number_of_moves`: Licznik wykonanych przez gracza ruchów.
*   `move_order_horizontal_index`: Indeks określający aktualnie wybrany "horyzontalnie" stos lub grupę stosów na planszy (zgodnie z `move_order`).
*   `move_order_vertical_index`: Indeks określający aktualnie wybraną kartę w pionie w obrębie wybranego stosu (dla `tableau_piles`) lub konkretny stos fundamentowy (gdy `move_order_horizontal_index` wskazuje na grupę `foundation_pile`).
*   `move_order`: Lista stringów definiująca kolejność nawigacji horyzontalnej między stosami. Domyślnie: `["stack_pile-0"] + ["tableau_pile-0" ... "tableau_pile-6"] + ["foundation_pile-0"]`.
*   `is_won`: Flaga logiczna (boolean), wskazująca, czy gra została wygrana.

### Słownik handlerów akcji
*   `_action_handlers`: Słownik mapujący stałe reprezentujące akcje (np. `"ACTION_QUIT"`) na odpowiednie metody obsługujące te akcje (np. `_handle_quit`).

## Metody

### `__init__(self)`
Konstruktor klasy. Inicjalizuje wszystkie atrybuty domyślnymi wartościami lub nowymi instancjami odpowiednich klas.

### `start_game(self)`
Rozpoczyna nową grę.
1.  Resetuje timer.
2.  Czyści ekran konsoli.
3.  Wyświetla menu startowe (`StartMenu`) i pobiera ustawienia gry. Jeśli ustawienia nie zostaną zwrócone (anulowanie), kończy działanie.
4.  Inicjalizuje menedżera tabeli wyników (`LeaderboardManager`).
5.  Resetuje flagi i liczniki (`run`, `number_of_moves`, `is_won`).
6.  Tworzy i tasuje nową talię kart (`Deck`).
7.  Inicjalizuje puste stosy tableau i fundamentowe.
8.  Przygotowuje planszę do gry za pomocą `prepare_board()`.
9.  Uruchamia główną pętlę gry w kontekście `curses` poprzez `curses.wrapper(self.run_game)`.
10. Po zakończeniu `run_game`, czyści ekran.
11. Wyświetla ekran końcowy (`EndScreen`). Jeśli gracz zdecyduje się zagrać ponownie, rekurencyjnie wywołuje `start_game()`. W przeciwnym razie czyści ekran i kończy.

### `run_game(self, screen)`
Główna pętla gry, uruchamiana w kontekście `curses`.
*   Argument `screen`: Obiekt ekranu `curses`.
1.  Inicjalizuje `Drawer` (do rysowania) i `KeyboardInputHandler` (do obsługi wejścia).
2.  Uruchamia timer.
3.  W pętli (dopóki `self.run` jest `True`):
    *   Rysuje aktualny stan planszy (`drawer.draw_game_board`).
    *   Pobiera akcję gracza (`input_handler.get_player_action`).
    *   Jeśli akcja została wykonana, przetwarza ją za pomocą `process_action(action)`.
    *   Sprawdza warunek zwycięstwa (`check_for_win()`). Jeśli spełniony, ustawia `self.run = False` i `self.is_won = True`.
4.  Zatrzymuje timer.

### `prepare_board(self)`
Przygotowuje planszę do gry:
1.  Tworzy 7 stosów tableau (`TableauPile`):
    *   Dla każdego stosu `i` (od 0 do 6) dobiera `i+1` kart z talii.
    *   Dodaje te karty do stosu tableau. Ostatnia karta jest odkryta.
2.  Tworzy 4 stosy fundamentowe (`FoundationPile`), po jednym dla każdego koloru (`♠`, `♥`, `♦`, `♣`).
3.  Inicjalizuje stos dobierania (`StockPile`) pozostałymi kartami z talii i ustawionym poziomem trudności.

### `process_action(self, action)`
Przetwarza akcję wykonaną przez gracza.
1.  Jeśli liczba ruchów zmieniła się od ostatniego zapisu stanu, zapisuje aktualny stan gry (`game_state_saver.push_state`).
2.  Pobiera odpowiednią metodę obsługującą akcję ze słownika `_action_handlers`.
3.  Jeśli handler istnieje, wywołuje go.

### `process_horizontal_move(self)`
Aktualizuje stan selekcji po ruchu horyzontalnym.
1.  Czyści poprzednią selekcję horyzontalną (`clear_horizontal_selection()`) i pionową (`clear_vertical_selection()`).
2.  Resetuje `move_order_vertical_index` do 0.
3.  Na podstawie `move_order[self.move_order_horizontal_index]` identyfikuje typ i indeks docelowego stosu.
4.  Ustawia flagę `is_selected = True` na odpowiednim stosie (tableau, fundamentowym lub stosie dobierania).

### `process_vertical_move(self)`
Aktualizuje stan selekcji po ruchu pionowym.
1.  Czyści poprzednią selekcję pionową (`clear_vertical_selection()`).
2.  Na podstawie `move_order[self.move_order_horizontal_index]` identyfikuje typ i indeks aktualnie wybranego horyzontalnie stosu.
3.  Jeśli jest to stos tableau, zaznacza kartę na pozycji `self.move_order_vertical_index` w `visible_cards`.
4.  Jeśli jest to grupa stosów fundamentowych, zaznacza stos fundamentowy o indeksie `self.move_order_vertical_index`.
5.  Jeśli jest to stos dobierania i ma widoczne karty, zaznacza ostatnią widoczną kartę (symulując wybór karty ze szczytu stosu odkrytych kart).

### `process_deleting_card(self)`
Usuwa karty z ich poprzedniego miejsca po tym, jak zostały pomyślnie przeniesione.
1.  Identyfikuje stos, z którego karty zostały wybrane, na podstawie `self.selected_card_pile.selected_from_horizontal_index` i `self.move_order`.
2.  Jeśli był to stos tableau, usuwa odpowiednią liczbę kart od `self.selected_card_pile.selected_from_vertical_index`.
3.  Jeśli był to stos dobierania, usuwa kartę ze szczytu (`stock_pile.pop_card()`).
4.  Dla każdej karty w `selected_card_pile` ustawia `card.in_selection = False`.

### `clear_selection(self)`
Czyści aktualnie wybrane karty.
1.  Dla każdej karty w `self.selected_card_pile.cards` ustawia `card.in_selection = False`.
2.  Czyści `self.selected_card_pile` (`selected_card_pile.clean()`).

### `clear_horizontal_selection(self)`
Usuwa zaznaczenie horyzontalne ze wszystkich stosów.
*   Ustawia `is_selected = False` dla wszystkich stosów tableau, fundamentowych i stosu dobierania.

### `clear_vertical_selection(self)`
Usuwa zaznaczenie pionowe (karty lub konkretnego stosu fundamentowego).
1.  Identyfikuje typ stosu na podstawie `move_order[self.move_order_horizontal_index]`.
2.  Jeśli tableau, odznacza wszystkie widoczne karty w tym stosie.
3.  Jeśli fundament, odznacza wszystkie stosy fundamentowe (choć w praktyce `process_vertical_move` dla fundamentów operuje na `is_selected` samego stosu, a nie kart w nim).
4.  Jeśli stos dobierania, odznacza wszystkie widoczne karty w nim.

### `load(self)`
Wczytuje zapisany stan gry z `game_state_saver`.
*   Jeśli stan jest dostępny, przywraca: `stock_pile`, `tableau_piles`, `foundation_piles`, `selected_card_pile`, `move_order`, `move_order_horizontal_index`, `move_order_vertical_index`, `number_of_moves`.

### `check_for_win(self)`
Sprawdza, czy warunki zwycięstwa zostały spełnione.
*   Zwraca `True`, jeśli każdy ze stosów fundamentowych zawiera 13 kart. W przeciwnym razie `False`.

### `_clear_screen(self)`
Metoda pomocnicza do czyszczenia ekranu konsoli. Używa `os.system("cls")` dla Windows lub `os.system("clear")` dla innych systemów.

### `_get_current_pile_info(self)`
Zwraca informacje o aktualnie wskazywanym przez kursor (nawigację) stosie.
*   Na podstawie `self.move_order[self.move_order_horizontal_index]` parsuje typ stosu (string, np. "tableau_pile") i jego indeks w danej kategorii (int).
*   Zwraca krotkę: `(typ_stosu_str, indeks_stosu_w_kategorii)`.

### `_handle_quit(self)`
Obsługuje akcję wyjścia z gry.
*   Ustawia `self.run = False`.

### `_handle_load(self)`
Obsługuje akcję wczytania gry.
*   Wywołuje `self.load()`.

### `_handle_restart(self)`
Obsługuje akcję restartu gry.
*   Wywołuje `self.start_game()`.

### `_handle_move_right(self)`
Obsługuje ruch kursora w prawo.
1.  Czyści selekcję pionową.
2.  Inkrementuje `self.move_order_horizontal_index` (z zawijaniem modulo długość `self.move_order`).
3.  Wywołuje `self.process_horizontal_move()` w celu aktualizacji wizualnej selekcji.

### `_handle_move_left(self)`
Obsługuje ruch kursora w lewo.
1.  Czyści selekcję pionową.
2.  Dekrementuje `self.move_order_horizontal_index` (z zawijaniem modulo długość `self.move_order`).
3.  Wywołuje `self.process_horizontal_move()` w celu aktualizacji wizualnej selekcji.

### `_handle_move_up(self)`
Obsługuje ruch kursora w górę.
1.  Pobiera informacje o aktualnym stosie za pomocą `_get_current_pile_info()`.
2.  Jeśli aktywny jest stos tableau i `move_order_vertical_index > 0`, dekrementuje go.
3.  Jeśli aktywne są stosy fundamentowe:
    *   Jeśli `move_order_vertical_index > 0`, dekrementuje go.
    *   W przeciwnym razie (jest na pierwszym fundamencie), zawija na ostatni (`len(self.foundation_piles) - 1`).
4.  Jeśli aktywny jest stos dobierania i `move_order_vertical_index > 0`, dekrementuje go (poruszanie się między opcją dobrania karty a wybraną kartą).
5.  Wywołuje `self.process_vertical_move()` w celu aktualizacji wizualnej selekcji.

### `_handle_move_down(self)`
Obsługuje ruch kursora w dół.
1.  Pobiera informacje o aktualnym stosie za pomocą `_get_current_pile_info()`.
2.  Jeśli aktywny jest stos tableau i `move_order_vertical_index` jest mniejszy niż indeks ostatniej widocznej karty, inkrementuje go.
3.  Jeśli aktywne są stosy fundamentowe:
    *   Jeśli `move_order_vertical_index` jest mniejszy niż indeks ostatniego stosu fundamentowego, inkrementuje go.
    *   W przeciwnym razie (jest na ostatnim fundamencie), zawija na pierwszy (0).
4.  Jeśli aktywny jest stos dobierania i `move_order_vertical_index` jest mniejszy lub równy liczbie widocznych kart (umożliwiając dojście do "pozycji" dobrania nowej karty), inkrementuje go.
5.  Wywołuje `self.process_vertical_move()` w celu aktualizacji wizualnej selekcji.

### `_handle_use(self)`
Obsługuje akcję "użyj" (Enter/Spacja), która może oznaczać wybranie kart lub odłożenie wybranych kart.
1.  Pobiera informacje o aktualnym stosie za pomocą `_get_current_pile_info()`.
2.  **Jeśli `self.selected_card_pile` jest pusty (wybieranie kart):**
    *   **Tableau Pile:**
        *   Pobiera karty od `self.move_order_vertical_index` do końca z `visible_cards` aktywnego stosu tableau.
        *   Zaznacza te karty (`card.in_selection = True`).
        *   Dodaje je do `self.selected_card_pile` wraz z informacją o ich pochodzeniu.
    *   **Stock Pile:**
        *   Jeśli `self.move_order_vertical_index == 0` (kursor na opcji dobrania/przetasowania):
            *   Jeśli stos dobierania (ukryte i widoczne karty) jest pusty, nic nie rób.
            *   Jeśli stos jest pusty (brak widocznych kart, ale mogą być ukryte), przetasowuje (`stock_pile.shuffle_deck()`).
            *   Inkrementuje `self.number_of_moves`.
            *   Dobiera kartę (`stock_pile.draw_card()`).
        *   Jeśli `self.move_order_vertical_index != 0` (kursor na karcie ze stosu widocznych kart):
            *   Pobiera ostatnią kartę z `stock_pile.visible_cards`.
            *   Zaznacza ją i dodaje do `self.selected_card_pile`.
3.  **Jeśli `self.selected_card_pile` zawiera karty (odkładanie kart):**
    *   **Tableau Pile:**
        *   Sprawdza, czy pierwsza z wybranych kart może być umieszczona na docelowym stosie tableau (`tableau_piles[pile_index_in_category].can_place_card()`).
        *   Jeśli tak:
            *   Inkrementuje `self.number_of_moves`.
            *   Usuwa wybrane karty z ich pierwotnego miejsca (`self.process_deleting_card()`).
            *   Dodaje wybrane karty do docelowego stosu tableau.
        *   Czyści selekcję (`self.clear_selection()`).
    *   **Foundation Pile:**
        *   Jeśli nie ma wybranych kart, nic nie rób.
        *   Sprawdza, czy pierwsza (i jedyna, jeśli ruch na fundament jest poprawny) z wybranych kart może być umieszczona na docelowym stosie fundamentowym (`foundation_piles[self.move_order_vertical_index].can_accept_card()`).
        *   Jeśli tak:
            *   Inkrementuje `self.number_of_moves`.
            *   Usuwa wybrane karty z ich pierwotnego miejsca.
            *   Dodaje wybrane karty do docelowego stosu fundamentowego.
        *   Czyści selekcję.
    *   **Stock Pile:** (Generalnie nie odkłada się kart na Stock Pile w standardowym Klondike, ale logika może obsłużyć próbę)
        *   Jeśli stos dobierania (ukryte i widoczne karty) jest pusty, nic nie rób.
        *   Jeśli `self.move_order_vertical_index != 0` (nie próbuje się odłożyć na miejsce dobrania), nic nie rób.
        *   Jeśli stos jest pusty, przetasowuje.
        *   Inkrementuje `self.number_of_moves`.
        *   (Uwaga: oryginalny kod nie ma tu logiki odkładania na stock, jedynie dobierania, co sugeruje, że ta gałąź `else` dla Stock Pile może być uproszczona lub dotyczyć sytuacji, gdy `selected_card_pile` jest pusty, a próbuje się użyć stosu, który jest pusty, aby go przetasować).

### `_handle_resize(self)`
Obsługuje zdarzenie zmiany rozmiaru okna konsoli.
1.  Wywołuje `self.drawer.resize_window()` w celu dostosowania wymiarów rysowania.
2.  Sprawdza, czy szerokość ekranu nie jest zbyt mała (np. `<= 44`). Jeśli tak:
    *   Ustawia `self.run = False` (kończy grę).
    *   Wyświetla komunikat o zbyt małym oknie.
    *   Kończy działanie metody.
3.  Jeśli rozmiar jest odpowiedni, przerysowuje planszę gry.