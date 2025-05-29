# Klasa AbstractCardRenderer (Abstrakcyjna)

`AbstractCardRenderer` jest abstrakcyjną klasą bazową (`ABC` - Abstract Base Class) zdefiniowaną przy użyciu modułu `abc`. Służy jako interfejs (szablon) dla konkretnych klas odpowiedzialnych za wizualne renderowanie (rysowanie) kart do gry w różnych kontekstach i stylach.

Klasy dziedziczące po `AbstractCardRenderer` muszą zaimplementować wszystkie metody oznaczone jako `@abstractmethod`.

## Dziedziczenie

*   `ABC`: Klasa bazowa z modułu `abc`, umożliwiająca definiowanie klas abstrakcyjnych i metod abstrakcyjnych.

## Metody

### `@abstractmethod`
### `render_card(self, card)`
Metoda abstrakcyjna, która powinna być zaimplementowana przez konkretne klasy renderujące. Jej zadaniem jest wyrenderowanie pełnego wizualnego przedstawienia pojedynczej karty.

*   **Parametry (oczekiwane w podklasach):**
    *   `card` (`Card`): Obiekt karty, która ma zostać wyrenderowana.
*   **Zachowanie (oczekiwane w podklasach):**
    *   Generuje kompletną wizualną reprezentację karty, uwzględniając jej rangę, kolor (symbol), oraz czy jest odkryta czy zakryta.
    *   Może zwracać tę reprezentację (np. jako listę stringów, obiekt graficzny) lub bezpośrednio ją rysować na jakimś medium (np. ekranie `curses`).
*   **Zwraca (oczekiwane w podklasach):**
    *   Zależy od implementacji; może nic nie zwracać (jeśli rysuje bezpośrednio) lub zwracać wyrenderowaną reprezentację.

### `@abstractmethod`
### `render_top_of_the_card(self, card)`
Metoda abstrakcyjna, której celem jest wyrenderowanie tylko górnej, widocznej części karty, tak jak jest to często przedstawiane w stosach kart, gdzie widoczny jest tylko niewielki fragment każdej karty oprócz wierzchniej.

*   **Parametry (oczekiwane w podklasach):**
    *   `card` (`Card`): Obiekt karty, której górna część ma zostać wyrenderowana.
*   **Zachowanie (oczekiwane w podklasach):**
    *   Generuje wizualną reprezentację tylko górnego fragmentu karty (np. ranga i kolor).
    *   Podobnie jak `render_card`, może zwracać reprezentację lub rysować bezpośrednio.
*   **Zwraca (oczekiwane w podklasach):**
    *   Zależy od implementacji.

### `@abstractmethod`
### `render_card_column(self, cards)`
Metoda abstrakcyjna przeznaczona do renderowania całej kolumny (stosu) kart, gdzie karty mogą na siebie nachodzić.

*   **Parametry (oczekiwane w podklasach):**
    *   `cards` (`list[Card]`): Lista obiektów `Card` reprezentujących kolumnę do wyrenderowania.
*   **Zachowanie (oczekiwane w podklasach):**
    *   Renderuje całą kolumnę kart, uwzględniając ich wzajemne położenie (np. w stosach tableau). Ostatnia karta w kolumnie może być w pełni widoczna, podczas gdy poprzednie mogą być częściowo zasłonięte.
    *   Może zwracać reprezentację lub rysować bezpośrednio.
*   **Zwraca (oczekiwane w podklasach):**
    *   Zależy od implementacji.

### `@abstractmethod`
### `render_blank_card(self, suit_symbol)`
Metoda abstrakcyjna, której zadaniem jest wyrenderowanie pustego miejsca na kartę, często używanego jako placeholder, na przykład dla pustych stosów fundamentowych. Może zawierać symbol oczekiwanego koloru.

*   **Parametry (oczekiwane w podklasach):**
    *   `suit_symbol` (`str`, opcjonalnie): Symbol koloru (np. "♠", "♥"), który może być wyświetlony na pustym miejscu jako wskazówka.
*   **Zachowanie (oczekiwane w podklasach):**
    *   Generuje wizualną reprezentację pustego miejsca na kartę. Może to być np. obramowanie karty z opcjonalnym symbolem koloru w środku.
    *   Może zwracać reprezentację lub rysować bezpośrednio.
*   **Zwraca (oczekiwane w podklasach):**
    *   Zależy od implementacji.

**Uwaga:** Ponieważ jest to klasa abstrakcyjna, sama `AbstractCardRenderer` nie dostarcza implementacji tych metod. Służy jedynie jako kontrakt dla klas pochodnych, które będą odpowiedzialne za konkretne sposoby rysowania kart.