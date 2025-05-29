# Klasa TableauPile

Reprezentuje jeden z siedmiu stosów roboczych (tableau) na planszy w grze Pasjans (Klondike). Na tych stosach karty są układane w porządku malejącym, naprzemiennie kolorami. Część kart na stosie tableau jest zakryta, a część odkryta.

## Atrybuty

*   `hidden_cards` (`list`): Lista obiektów klasy `Card`, przechowująca zakryte karty na tym stosie tableau.
*   `visible_cards` (`list`): Lista obiektów klasy `Card`, przechowująca odkryte karty na tym stosie tableau. Karty te są dostępne dla gracza do przenoszenia.
*   `is_selected` (`bool`): Flaga wskazująca, czy cały stos (lub jego aktywna część) jest aktualnie zaznaczony przez kursor nawigacji. Domyślnie `False`.

## Metody

### `__init__(self)`
Konstruktor klasy. Inicjalizuje nowy, pusty stos tableau.

*   **Zachowanie:**
    *   Ustawia `self.hidden_cards` na pustą listę.
    *   Ustawia `self.visible_cards` na pustą listę.
    *   Ustawia `self.is_selected` na `False`.

### `add_initial_cards(self, cards)`
Dodaje początkowy zestaw kart do stosu tableau podczas setupu gry. Ostatnia karta z przekazanej listy jest odkrywana, a pozostałe są zakryte.

*   **Parametry:**
    *   `cards` (`list`): Lista obiektów `Card` do dodania.
*   **Zachowanie:**
    *   Jeśli lista `cards` jest pusta, nic nie robi.
    *   Jeśli lista `cards` zawiera jedną kartę, ta karta jest dodawana do `self.visible_cards` i odkrywana (`card.flip()`).
    *   Jeśli lista `cards` zawiera więcej niż jedną kartę:
        *   Wszystkie karty oprócz ostatniej są przypisywane do `self.hidden_cards`.
        *   Ostatnia karta jest odkrywana (`card.flip()`) i dodawana jako jedyny element do `self.visible_cards`.

### `add_cards(self, cards)`
Dodaje listę (już odkrytych) kart na wierzch stosu widocznych kart. Używane podczas przenoszenia kart z innego stosu na ten stos tableau.

*   **Parametry:**
    *   `cards` (`list`): Lista obiektów `Card` (oczekuje się, że są już odkryte) do dodania.
*   **Zachowanie:**
    *   Jeśli lista `cards` nie jest pusta, rozszerza `self.visible_cards` o elementy z tej listy.

### `can_place_card(self, card)`
Sprawdza, czy pojedyncza karta może zostać umieszczona na wierzchu widocznych kart tego stosu tableau, zgodnie z zasadami Pasjansa.

*   **Parametry:**
    *   `card` (`Card`): Karta, której możliwość umieszczenia jest sprawdzana.
*   **Zachowanie:**
    1.  **Jeśli stos widocznych kart (`self.visible_cards`) jest pusty:**
        *   Karta jest akceptowana tylko wtedy, gdy jej ranga to Król (`card.rank == "K"`).
    2.  **Jeśli stos widocznych kart nie jest pusty:**
        *   Pobiera ostatnią kartę z `self.visible_cards` (`last_card`).
        *   Karta jest akceptowana, jeśli jej numeryczna ranga (`card.rank_id`) jest o jeden mniejsza niż numeryczna ranga `last_card` ORAZ jej kolor (`card.color`) jest różny od koloru `last_card`.
*   **Zwraca:**
    *   `bool`: `True`, jeśli karta może zostać umieszczona, `False` w przeciwnym razie.

### `can_place_stack(self, stack)`
Sprawdza, czy stos kart (reprezentowany przez obiekt `CardStack` lub podobny, który ma metodę `peek_top_card()`) może zostać umieszczony na wierzchu widocznych kart tego stosu tableau. Logika jest podobna do `can_place_card`, ale operuje na wierzchniej karcie przekazanego stosu.

*   **Parametry:**
    *   `stack` (obiekt z metodą `peek_top_card()`): Stos kart, którego możliwość umieszczenia jest sprawdzana (konkretnie jego wierzchnia karta).
*   **Zachowanie:**
    1.  **Jeśli stos widocznych kart (`self.visible_cards`) jest pusty:**
        *   Stos jest akceptowany, jeśli wierzchnia karta przekazanego `stack`-u ma rangę Króla.
    2.  **Jeśli stos widocznych kart nie jest pusty:**
        *   Pobiera ostatnią kartę z `self.visible_cards` (`last_card`).
        *   Pobiera wierzchnią kartę z przekazanego `stack`-u (`stack_top_card`).
        *   Stos jest akceptowany, jeśli numeryczna ranga `stack_top_card` jest o jeden mniejsza niż numeryczna ranga `last_card` ORAZ kolor `stack_top_card` jest różny od koloru `last_card`.
*   **Zwraca:**
    *   `bool`: `True`, jeśli stos może zostać umieszczony, `False` w przeciwnym razie.

### `flip_after_deleting(self)`
Odkrywa wierzchnią kartę ze stosu zakrytych kart (`self.hidden_cards`), jeśli stos widocznych kart (`self.visible_cards`) stał się pusty (a stos zakryty nie jest pusty).

*   **Zachowanie:**
    *   Jeśli `self.visible_cards` jest pusta ORAZ `self.hidden_cards` nie jest pusta:
        *   Usuwa ostatnią kartę z `self.hidden_cards`.
        *   Odkrywa tę kartę (`card.flip()`).
        *   Dodaje tę kartę jako jedyny element do `self.visible_cards`.

### `debug(self)`
Wyświetla informacje diagnostyczne o stanie stosu tableau na standardowe wyjście.

*   **Zachowanie:**
    *   Drukuje liczbę i reprezentacje tekstowe kart w `visible_cards` i `hidden_cards`.

### `remove_cards_to_index(self, index, cards_to_delete)`
Usuwa segment kart ze stosu widocznych kart (`self.visible_cards`), zaczynając od podanego `index`. Po usunięciu kart, jeśli to konieczne, wywołuje `flip_after_deleting()`.

*   **Parametry:**
    *   `index` (`int`): Indeks w `self.visible_cards`, od którego rozpoczyna się usuwanie.
    *   `cards_to_delete` (`int`): Liczba kart do usunięcia.
*   **Zachowanie:**
    1.  Sprawdza, czy `index` jest prawidłowy. Jeśli nie, drukuje komunikat i zwraca `None`.
    2.  **Jeśli `index > 0`:**
        *   `self.visible_cards` jest skracana tak, że zawiera tylko karty od początku do `index` (nie włącznie). Oznacza to, że wszystkie karty od `index` do końca są usuwane. Parametr `cards_to_delete` nie jest używany w tej gałęzi.
    3.  **Jeśli `index == 0`:**
        *   `self.visible_cards` jest ustawiana na segment zaczynający się od `index + cards_to_delete` do końca. Efektywnie usuwa pierwsze `cards_to_delete` kart.
    4.  Wywołuje `self.flip_after_deleting()` w celu potencjalnego odkrycia nowej karty, jeśli stos widocznych stał się pusty.
*   **Zwraca:**
    *   `None` (niejawnie, jeśli operacja przebiegnie pomyślnie lub jeśli `index` jest nieprawidłowy).

**Uwaga dotycząca `remove_cards_to_index`:** Logika tej metody, zwłaszcza gdy `index > 0`, usuwa wszystkie karty od `index` do końca, ignorując parametr `cards_to_delete`. Jeśli intencją jest usunięcie dokładnie `cards_to_delete` kart zaczynając od `index`, implementacja może wymagać dostosowania. Jednak w kontekście typowego użycia w Pasjansie (usuwanie całego "ogona" wybranych kart), obecne zachowanie dla `index > 0` jest poprawne, jeśli `index` oznacza pierwszą kartę w zabieranej grupie.