# Klasa StockPile

Reprezentuje stos kart do dobierania (stock) oraz stos kart odkrytych (waste/talon) w grze Pasjans (Klondike). Gracz dobiera karty ze stosu zakrytego, które następnie lądują (odkryte) na stosie widocznym. Gdy stos zakryty się wyczerpie, stos widoczny jest odwracany, tasowany i staje się nowym stosu zakrytym.

## Dziedziczenie

*   `CardStack`: `StockPile` jest podklasą `CardStack`. Dziedziczy jej atrybuty (`cards`, `is_selected`), ale w dużej mierze zarządza kartami poprzez własne atrybuty `hidden_cards` i `visible_cards`.

## Importy

*   `CardStack` (z `core.CardStack`)
*   `Deck` (z `core.Deck`) - nieużywany bezpośrednio w kodzie `StockPile`, ale może być powiązany z inicjalizacją.
*   `Shuffler` (z `core.Shuffler`)

## Atrybuty

Dziedziczone z `CardStack`:
*   `cards` (`list`): Inicjalizowany w `super().__init__(cards)`, ale `StockPile` głównie operuje na `hidden_cards` i `visible_cards`.
*   `is_selected` (`bool`): Flaga wskazująca, czy stos jest zaznaczony.

Specyficzne dla `StockPile`:
*   `shuffler` (`Shuffler`): Obiekt używany do tasowania kart podczas odświeżania stosu.
*   `cards_to_draw` (`int`): Liczba kart dobieranych jednorazowo ze stosu zakrytego. Zależy od poziomu trudności (1 dla "easy", 3 dla innych).
*   `visible_cards` (`list`): Lista obiektów `Card`, reprezentująca stos kart odkrytych (waste/talon), z którego gracz może brać karty.
*   `hidden_cards` (`list`): Lista obiektów `Card`, reprezentująca stos kart zakrytych (stock), z którego dobierane są karty. Początkowo zawiera wszystkie karty przeznaczone dla stosu dobierania.

## Metody

### `__init__(self, cards, difficulty)`
Konstruktor klasy.

*   **Parametry:**
    *   `cards` (`list`): Lista obiektów `Card` stanowiących początkowy zestaw kart dla stosu dobierania (zazwyczaj pozostałe karty z talii po rozdaniu na tableau).
    *   `difficulty` (`str`): Poziom trudności gry (np. "easy"). Wpływa na `self.cards_to_draw`.
*   **Zachowanie:**
    *   Wywołuje konstruktor klasy nadrzędnej `CardStack` (`super().__init__(cards)`), inicjalizując odziedziczony atrybut `self.cards`.
    *   Tworzy instancję `Shuffler`.
    *   Ustawia `self.cards_to_draw` na 1, jeśli `difficulty` to "easy", w przeciwnym razie na 3.
    *   Inicjalizuje `self.visible_cards` jako pustą listę.
    *   Przypisuje przekazaną listę `cards` do `self.hidden_cards`.

### `draw_card(self)`
Dobiera określoną liczbę kart (`self.cards_to_draw`) ze stosu zakrytego (`self.hidden_cards`) i przenosi je, odkrywając, do stosu widocznego (`self.visible_cards`).

*   **Zachowanie:**
    1.  Pętla wykonuje się `self.cards_to_draw` razy.
    2.  W każdej iteracji:
        *   Jeśli stos zakryty (`self.hidden_cards`) jest pusty (sprawdzane przez `self.is_empty()`), wywoływana jest metoda `self.shuffle_deck()` w celu odświeżenia stosu zakrytego z kart widocznych.
        *   Pobierana jest karta z wierzchu stosu zakrytego za pomocą `self.remove_top_card()`.
        *   Jeśli pobrana `card` jest `None` (co mogłoby się zdarzyć, jeśli nawet po `shuffle_deck()` stos zakryty pozostał pusty, np. gdy cała talia jest na planszy), stos jest ponownie odświeżany (`self.shuffle_deck()`) i metoda kończy działanie dla bieżącej iteracji dobierania (lub całkowicie, jeśli to jedyna karta do dobrania).
        *   Pobrana karta jest odwracana (`card.flip()`), stając się widoczną.
        *   Karta jest dodawana do `self.visible_cards`.

### `remove_top_card(self)`
Przesłania metodę z `CardStack`. Usuwa i zwraca kartę z wierzchu stosu *zakrytych* kart (`self.hidden_cards`).

*   **Zachowanie:**
    *   Jeśli `self.hidden_cards` jest pusta, zwraca `None`.
    *   W przeciwnym razie usuwa ostatnią kartę z `self.hidden_cards` i ją zwraca.
*   **Zwraca:**
    *   `Card`: Usunięta karta lub `None`, jeśli stos zakryty był pusty.

### `is_empty(self)`
Przesłania metodę z `CardStack`. Sprawdza, czy stos *zakrytych* kart (`self.hidden_cards`) jest pusty.

*   **Zwraca:**
    *   `bool`: `True`, jeśli `self.hidden_cards` jest pusta, `False` w przeciwnym razie.

### `shuffle_deck(self)`
Odświeża stos zakryty. Wszystkie karty ze stosu widocznego (`self.visible_cards`) są przenoszone z powrotem do stosu zakrytego (`self.hidden_cards`), odwracane (aby były zakryte) i tasowane.

*   **Zachowanie:**
    1.  Zawartość `self.visible_cards` jest przypisywana do `self.hidden_cards`.
    2.  `self.visible_cards` jest czyszczona (staje się pustą listą).
    3.  Każda karta w `self.hidden_cards` (teraz byłe `visible_cards`) jest odwracana (`card.flip()`), aby stała się zakryta.
    4.  Lista `self.hidden_cards` jest tasowana za pomocą `self.shuffler.shuffle()`.

### `pop_card(self)`
Usuwa i zwraca kartę z wierzchu stosu *widocznych* kart (`self.visible_cards`). Ta metoda jest używana, gdy gracz chce wziąć kartę ze stosu odkrytego, aby umieścić ją na planszy.

*   **Zachowanie:**
    *   Jeśli `self.visible_cards` jest pusta:
        *   Wywołuje `self.shuffle_deck()`. (To zachowanie jest nieco nietypowe dla operacji "pop" z pustego stosu widocznego, sugerując, że jeśli gracz próbuje wziąć kartę, a stos widoczny jest pusty, system próbuje go najpierw odświeżyć).
        *   Kończy działanie (nic nie zwraca w tym przypadku, ponieważ karta nie została pobrana).
    *   Jeśli `self.visible_cards` nie jest pusta, usuwa ostatnią kartę z `self.visible_cards` i (niejawnie) ją zwraca (choć w Pythonie metoda `pop()` listy zwraca usunięty element, ta metoda `pop_card` nie ma instrukcji `return` dla tego przypadku, co oznacza, że zwróci `None`). *Poprawka: Metoda list.pop() zwraca wartość, ale ta funkcja nie ma explicit return dla tego przypadku, więc zwróci None. Jeśli celem jest zwrócenie karty, powinno być `return self.visible_cards.pop()`.*