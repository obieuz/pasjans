# Klasa SelectedCardPile

Reprezentuje tymczasowy "stos" lub grupę kart, które zostały wybrane przez gracza i są w trakcie przenoszenia z jednego miejsca na planszy na inne. Przechowuje nie tylko same karty, ale również informację o ich pierwotnym położeniu, co jest przydatne do logiki usuwania kart z ich źródła.

## Atrybuty

*   `cards` (`list`): Lista obiektów klasy `Card`, przechowująca aktualnie wybrane przez gracza karty. Inicjalizowana jako pusta lista.
*   `selected_from_horizontal_index` (`int` lub `None`): Indeks horyzontalny (zgodny z `GameManager.move_order`), z którego stosu (lub grupy stosów) karty zostały wybrane. Inicjalizowany na `None`.
*   `selected_from_vertical_index` (`int` lub `None`): Indeks wertykalny, wskazujący na konkretną kartę (w przypadku `TableauPile`) lub konkretny stos (w przypadku `FoundationPile`), z którego karty zostały wybrane. Inicjalizowany na `None`.

## Metody

### `__init__(self)`
Konstruktor klasy. Inicjalizuje pusty stos wybranych kart oraz informacje o ich pochodzeniu.

*   **Zachowanie:**
    *   Ustawia `self.cards` na pustą listę.
    *   Ustawia `self.selected_from_horizontal_index` na `None`.
    *   Ustawia `self.selected_from_vertical_index` na `None`.

### `add_cards(self, cards, horizontal_index=None, vertical_index=None)`
Dodaje jedną lub więcej kart do `SelectedCardPile` i zapisuje informacje o ich pochodzeniu.

*   **Parametry:**
    *   `cards` (`Card` lub `list[Card]`): Pojedynczy obiekt `Card` lub lista obiektów `Card` do dodania.
    *   `horizontal_index` (`int` lub `None`, domyślnie `None`): Horyzontalny indeks źródła kart.
    *   `vertical_index` (`int` lub `None`, domyślnie `None`): Wertykalny indeks źródła kart.
*   **Zachowanie:**
    *   Jeśli `cards` jest listą, rozszerza `self.cards` o elementy z tej listy.
    *   Jeśli `cards` jest pojedynczym obiektem `Card`, dodaje go do `self.cards`.
    *   Ustawia `self.selected_from_vertical_index` na wartość `vertical_index`.
    *   Ustawia `self.selected_from_horizontal_index` na wartość `horizontal_index`.

### `peek_top_card(self)`
Zwraca ostatnią kartę dodaną do `SelectedCardPile` (wierzchołek "stosu" wybranych kart) bez jej usuwania. W kontekście przenoszenia wielu kart z tableau, będzie to najniżej położona (najbardziej wierzchnia w grze) karta z wybranej grupy.

*   **Zachowanie:**
    *   Jeśli `self.cards` nie jest pusta, zwraca ostatni element listy.
*   **Zwraca:**
    *   `Card`: Ostatnia karta w `self.cards`.
    *   `None`: Jeśli `self.cards` jest pusta.

### `is_empty(self)`
Sprawdza, czy `SelectedCardPile` nie zawiera żadnych kart.

*   **Zwraca:**
    *   `bool`: `True`, jeśli `self.cards` jest pusta, `False` w przeciwnym razie.

### `clean(self)`
Czyści `SelectedCardPile`, usuwając wszystkie karty i resetując informacje o ich pochodzeniu. Wywoływana zazwyczaj po pomyślnym przeniesieniu kart lub anulowaniu wyboru.

*   **Zachowanie:**
    *   Czyści listę `self.cards` (staje się pusta).
    *   Ustawia `self.selected_from_horizontal_index` na `None`.
    *   Ustawia `self.selected_from_vertical_index` na `None`.