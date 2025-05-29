# Klasa InputHandler (Abstrakcyjna)

`InputHandler` jest abstrakcyjną klasą bazową (`ABC` - Abstract Base Class) zdefiniowaną przy użyciu modułu `abc`. Służy jako interfejs (szablon) dla konkretnych klas obsługujących różne rodzaje wejścia od gracza (np. z klawiatury, myszy, kontrolera).

Klasy dziedziczące po `InputHandler` muszą zaimplementować wszystkie metody oznaczone jako `@abstractmethod`.

## Dziedziczenie

*   `ABC`: Klasa bazowa z modułu `abc`, umożliwiająca definiowanie klas abstrakcyjnych i metod abstrakcyjnych.

## Metody

### `@abstractmethod`
### `get_player_action(self)`
Jest to metoda abstrakcyjna, która musi zostać zaimplementowana przez każdą konkretną podklasę `InputHandler`. Jej zadaniem jest odczytanie akcji wykonanej przez gracza i zwrócenie jej w zdefiniowanym formacie (np. jako string reprezentujący komendę lub stałą).

*   **Zachowanie (oczekiwane w podklasach):**
    *   Nasłuchuje na wejście od gracza (np. naciśnięcie klawisza).
    *   Mapuje to wejście na predefiniowaną akcję gry (np. "ACTION_MOVE_LEFT", "ACTION_USE").
    *   Zwraca identyfikator tej akcji. Jeśli żadna akcja nie została wykryta (np. w trybie nieblokującym), może zwracać `None` lub pusty ciąg znaków, w zależności od implementacji.
*   **Zwraca (oczekiwane w podklasach):**
    *   `str` lub inny typ danych: Identyfikator akcji gracza (np. "ACTION_QUIT", "ACTION_MOVE_RIGHT").
    *   Może zwracać `None` lub pusty ciąg, jeśli nie wykryto żadnej akcji.

**Uwaga:** Ponieważ jest to metoda abstrakcyjna, sama klasa `InputHandler` nie dostarcza jej implementacji. Służy jedynie jako kontrakt dla klas pochodnych.