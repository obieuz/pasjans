# Klasa GameState

Odpowiada za zarządzanie historią stanów gry, umożliwiając implementację funkcji "cofnij ruch". Przechowuje ograniczoną liczbę ostatnich stanów gry, pozwalając graczowi na powrót do poprzednich konfiguracji planszy.

## Atrybuty

*   `states` (`list`): Lista słowników, gdzie każdy słownik reprezentuje jeden zapisany stan gry. Działa jak bufor cykliczny o ograniczonej pojemności (domyślnie do 4 ostatnich stanów). Każdy słownik zawiera kluczowe elementy stanu gry, takie jak stosy kart, pozycję kursora, liczbę ruchów.
*   `last_number_of_move` (`int`): Przechowuje numer ruchu, przy którym ostatnio zapisano stan gry. Służy do zapobiegania cofaniu się do tego samego stanu, z którego właśnie wykonano operację "cofnij", oraz do obsługi sytuacji, gdy gracz chce cofnąć kilka ruchów pod rząd. Inicjalizowany na `-1`.

## Metody

### `__init__(self)`
Konstruktor klasy. Inicjalizuje wewnętrzne struktury danych do przechowywania stanów gry.

*   **Zachowanie:**
    *   Ustawia `self.states` na pustą listę.
    *   Ustawia `self.last_number_of_move` na `-1`.

### `push_state(self, stock_pile, tableau_piles, foundation_piles, selected_card_pile, move_order, move_order_horizontal_index, move_order_vertical_index, number_of_moves, game_state)`
Zapisuje aktualny stan gry na stosie historii.

*   **Parametry:**
    *   `stock_pile` (`StockPile`): Aktualny stan stosu dobierania.
    *   `tableau_piles` (`list`): Lista aktualnych stanów stosów tableau.
    *   `foundation_piles` (`list`): Lista aktualnych stanów stosów fundamentowych.
    *   `selected_card_pile` (`SelectedCardPile`): Aktualny stan stosu wybranych kart.
    *   `move_order` (`list`): Aktualna kolejność nawigacji.
    *   `move_order_horizontal_index` (`int`): Aktualny horyzontalny indeks nawigacji.
    *   `move_order_vertical_index` (`int`): Aktualny wertykalny indeks nawigacji.
    *   `number_of_moves` (`int`): Aktualna liczba wykonanych ruchów.
    *   `game_state` (`GameState`): Referencja do instancji samego obiektu `GameState` (może być używane w bardziej złożonych scenariuszach, np. gdyby stan zawierał inne metadane o procesie zapisywania/ładowania).
*   **Zachowanie:**
    1.  Tworzy słownik `state` zawierający wszystkie przekazane parametry, reprezentujące kompletny, zamrożony stan gry w danym momencie. Zakłada się, że przekazywane obiekty (jak `stock_pile`, `tableau_piles`) są głębokimi kopiami, aby uniknąć modyfikacji zapisanego stanu przez późniejsze zmiany w grze.
    2.  Aktualizuje `self.last_number_of_move` na wartość `number_of_moves` z właśnie zapisywanego stanu.
    3.  Dodaje utworzony słownik `state` na koniec listy `self.states`.
    4.  Jeśli liczba zapisanych stanów w `self.states` przekroczy 4, usuwa najstarszy stan (pierwszy element listy), utrzymując w ten sposób bufor o stałej, ograniczonej wielkości.

### `load_state(self)`
Wczytuje (usuwa i zwraca) ostatnio zapisany stan gry ze stosu historii, umożliwiając cofnięcie ruchu.

*   **Zachowanie:**
    1.  Jeśli lista `self.states` jest pusta, nie ma stanów do wczytania, więc zwraca `None`.
    2.  Sprawdza, czy `self.last_number_of_move` jest równe liczbie ruchów zapisanej w ostatnim stanie na liście (`self.states[-1]["number_of_moves"]`).
        *   **Jeśli tak:** Oznacza to, że gracz próbuje cofnąć ruch bezpośrednio po poprzednim cofnięciu, do stanu, który był "przed" tym ostatnio wczytanym. Aby uniknąć utknięcia w pętli lub wczytania tego samego stanu, który właśnie został zastosowany:
            *   Jeśli na liście `self.states` jest więcej niż jeden stan, usuwa ostatni stan (ten, który odpowiada `self.last_number_of_move`).
            *   Resetuje `self.last_number_of_move` do `-1` (aby kolejne cofnięcie było traktowane jako "świeże").
            *   Usuwa i zwraca (teraz już) ostatni stan z `self.states`. Jeśli po usunięciu lista jest pusta, zwraca `None`.
        *   **Jeśli nie:** Oznacza to standardowe cofnięcie do poprzedniego, unikalnego stanu.
            *   Resetuje `self.last_number_of_move` do `-1`.
            *   Usuwa i zwraca ostatni stan z `self.states`. Jeśli lista jest pusta, zwraca `None`.
*   **Zwraca:**
    *   `dict`: Słownik reprezentujący wczytany stan gry (jeśli operacja się powiodła).
    *   `None`: Jeśli nie ma stanów do wczytania lub w specyficznych warunkach opisanych powyżej, gdy lista stanów staje się pusta.