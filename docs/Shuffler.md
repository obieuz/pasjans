# Klasa Shuffler

Odpowiada za tasowanie listy kart. Implementuje algorytm tasowania Fishera-Yatesa (znany również jako algorytm Knuth shuffle) z niestandardowym generatorem liczb pseudolosowych opartym na aktualnym czasie.

## Importy

*   `time` (konkretnie funkcja `time`): Używana do generowania ziarna (seed) dla niestandardowej funkcji `random_index`.

## Atrybuty

Klasa `Shuffler` w swojej obecnej formie nie definiuje żadnych atrybutów instancji w metodzie `__init__`.

## Metody

### `__init__(self)`
Konstruktor klasy.

*   **Zachowanie:**
    *   W obecnej implementacji metoda `__init__` jest pusta (`pass`) i nie wykonuje żadnych operacji inicjalizujących.

### `shuffle(self, cards)`
Tasuje podaną listę kart w miejscu, używając algorytmu Fishera-Yatesa.

*   **Parametry:**
    *   `cards` (`list`): Lista obiektów (w domyśle obiektów `Card`) do potasowania.
*   **Zachowanie:**
    1.  Iteruje przez listę `cards` od końca do początku (od indeksu `len(cards) - 1` do `1`).
    2.  W każdej iteracji `i`:
        *   Generuje losowy indeks `j` w zakresie od `0` do `i` (włącznie) za pomocą metody `self.random_index(0, i)`.
        *   Zamienia miejscami elementy `cards[i]` i `cards[j]`.
    3.  Po zakończeniu pętli lista `cards` jest potasowana.
*   **Zwraca:**
    *   `list`: Ta sama lista `cards`, która została przekazana jako argument, ale z elementami w losowej kolejności. Modyfikacja odbywa się w miejscu, ale metoda również zwraca referencję do tej listy.

### `random_index(self, start, end)`
Generuje pseudolosowy indeks całkowity w podanym zakresie `[start, end]` (włącznie).

*   **Parametry:**
    *   `start` (`int`): Dolna granica zakresu (włącznie).
    *   `end` (`int`): Górna granica zakresu (włącznie).
*   **Zachowanie:**
    1.  Pobiera aktualny czas systemowy w sekundach od epoki (`time()`).
    2.  Mnoży go przez 1 000 000, aby uzyskać większą precyzję i zamienia na liczbę całkowitą.
    3.  Oblicza resztę z dzielenia tej wartości przez długość zakresu (`end - start + 1`). Wynik tej operacji (`seed`) będzie liczbą z przedziału `[0, end - start]`.
    4.  Dodaje `start` do `seed`, aby przesunąć wynik do pożądanego zakresu `[start, end]`.
*   **Zwraca:**
    *   `int`: Pseudolosowy indeks całkowity z zakresu `[start, end]`.

**Uwaga dotycząca losowości:**
Metoda `random_index` używa prostego generatora opartego na czasie systemowym. Dla większości zastosowań w grach karcianych może to być wystarczające, ale nie jest to kryptograficznie bezpieczny generator liczb pseudolosowych. Szybkie, kolejne wywołania tej funkcji w bardzo krótkim odstępie czasu mogą potencjalnie generować powtarzalne sekwencje, jeśli precyzja `time()` i operacji arytmetycznych nie jest wystarczająca do zapewnienia unikalnych ziaren. W Pythonie standardową biblioteką do generowania liczb losowych jest moduł `random`, który oferuje bardziej zaawansowane i zazwyczaj lepiej przetestowane algorytmy (np. `random.randint(start, end)`).