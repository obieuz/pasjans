# Klasa CardStack

Reprezentuje stos kart, który może być używany jako podstawa dla różnych typów stosów w grach karcianych (np. stos roboczy, fundament). Klasa dostarcza podstawowe operacje na stosie, takie jak dodawanie, usuwanie kart, podglądanie wierzchniej karty oraz sprawdzanie, czy można na nim umieścić daną kartę.

## Atrybuty

*   `cards` (`list`): Lista obiektów klasy `Card`, przechowująca karty znajdujące się na tym stosie. Inicjalizowana jako pusta lista, jeśli nie podano kart w konstruktorze.
*   `is_selected` (`bool`): Flaga wskazująca, czy cały stos jest aktualnie zaznaczony (np. przez nawigację w grze). Domyślnie `False`.

## Metody

### `__init__(self, cards=None)`
Konstruktor klasy. Inicjalizuje nowy stos kart.

*   **Parametry:**
    *   `cards` (`list`, opcjonalny): Lista obiektów `Card` do początkowego umieszczenia na stosie. Domyślnie `None`, co skutkuje utworzeniem pustego stosu.
*   **Zachowanie:**
    *   Ustawia atrybut `self.cards` na podaną listę kart lub na nową, pustą listę, jeśli `cards` to `None`.
    *   Ustawia atrybut `self.is_selected` na `False`.

### `add_card(self, card)`
Dodaje pojedynczą kartę na wierzch stosu, jeśli jest to dozwolone przez logikę `can_accept_card`.

*   **Parametry:**
    *   `card` (`Card`): Obiekt karty do dodania.
*   **Zachowanie:**
    *   Sprawdza, czy karta może zostać zaakceptowana za pomocą `self.can_accept_card(card)`.
    *   Jeśli tak, dodaje kartę na koniec listy `self.cards`.

### `add_cards(self, cards)`
Dodaje listę kart na wierzch stosu, jeśli pierwsza karta z listy może zostać zaakceptowana.

*   **Parametry:**
    *   `cards` (`list`): Lista obiektów `Card` do dodania.
*   **Zachowanie:**
    *   Jeśli lista `cards` nie jest pusta, pobiera pierwszą kartę z tej listy.
    *   Sprawdza, czy ta pierwsza karta może zostać zaakceptowana za pomocą `self.can_accept_card(first_card)`.
    *   Jeśli tak, wszystkie karty z listy `cards` są dodawane na koniec listy `self.cards`.

### `remove_top_card(self)`
Usuwa i zwraca kartę z wierzchu stosu.

*   **Zachowanie:**
    *   Jeśli stos nie jest pusty (`not self.is_empty()`), usuwa ostatnią kartę z listy `self.cards` i ją zwraca.
*   **Zwraca:**
    *   `Card`: Usunięta karta, jeśli stos nie był pusty.
    *   `None`: Jeśli stos był pusty.

### `remove_cards(self, beginning_index)`
Usuwa i zwraca listę kart ze stosu, zaczynając od podanego indeksu aż do końca stosu.

*   **Parametry:**
    *   `beginning_index` (`int`): Indeks, od którego karty mają zostać usunięte.
*   **Zachowanie:**
    *   Sprawdza, czy `beginning_index` jest prawidłowym indeksem w liście `self.cards`.
    *   Karty od `beginning_index` do końca są usuwane ze stosu i zwracane jako nowa lista.
    *   Lista `self.cards` jest modyfikowana tak, aby zawierała tylko karty do `beginning_index`.
*   **Zwraca:**
    *   `list`: Lista usuniętych obiektów `Card`.
*   **Wyjątki:**
    *   `IndexError`: Jeśli `beginning_index` jest poza zakresem.

### `can_accept_card(self, card)`
Sprawdza, czy dana karta może zostać umieszczona na wierzchu tego stosu.
**Uwaga:** Logika tej metody w dostarczonym kodzie jest specyficzna:
1.  Jeśli stos jest pusty, akceptuje tylko Króla ("K").
2.  Jeśli stos nie jest pusty:
    *   Karta jest akceptowana, jeśli jej kolor (`suit_symbol`) jest **różny** od koloru karty na wierzchu stosu.
    *   ORAZ jej wartość (`rank_id`) jest o jeden mniejsza niż wartość karty na wierzchu stosu.
    *   (Oba powyższe warunki muszą być spełnione dla niepustego stosu).

*   **Parametry:**
    *   `card` (`Card`): Karta, której możliwość umieszczenia jest sprawdzana.
*   **Zachowanie:**
    *   Implementuje logikę opisaną powyżej.
*   **Zwraca:**
    *   `bool`: `True`, jeśli karta może zostać umieszczona na stosie, `False` w przeciwnym razie.

### `peek_top_card(self)`
Zwraca kartę z wierzchu stosu bez jej usuwania.

*   **Zachowanie:**
    *   Jeśli stos nie jest pusty, zwraca ostatni element z listy `self.cards`.
*   **Zwraca:**
    *   `Card`: Karta z wierzchu stosu, jeśli stos nie jest pusty.
    *   `None`: Jeśli stos jest pusty.

### `is_empty(self)`
Sprawdza, czy stos jest pusty.

*   **Zwraca:**
    *   `bool`: `True`, jeśli stos nie zawiera żadnych kart, `False` w przeciwnym razie.

### `__len__(self)`
Zwraca liczbę kart na stosie.

*   **Zwraca:**
    *   `int`: Liczba kart w `self.cards`.

### `get_all_cards(self)`
Zwraca kopię listy wszystkich kart znajdujących się na stosie.

*   **Zwraca:**
    *   `list`: Nowa lista zawierająca wszystkie obiekty `Card` z `self.cards`.