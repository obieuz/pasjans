# Klasa Timer

Prosty timer (stoper) działający w osobnym wątku, pozwalający na mierzenie upływającego czasu w sekundach. Może być uruchamiany, zatrzymywany i resetowany.

## Importy

*   `threading`: Do uruchamiania licznika czasu w osobnym wątku, aby nie blokować głównego wątku aplikacji.
*   `time`: Do użycia funkcji `time.sleep()` w celu odliczania sekund.

## Atrybuty

*   `_seconds` (`int`): Wewnętrzny licznik przechowujący liczbę sekund, która upłynęła od uruchomienia lub ostatniego resetu timera. Nazwa z pojedynczym podkreśleniem sugeruje, że jest to atrybut przeznaczony do użytku wewnętrznego. Inicjalizowany na `0`.
*   `running` (`bool`): Flaga kontrolująca działanie wątku timera. Gdy `True`, wątek kontynuuje odliczanie. Gdy `False`, wątek kończy swoje działanie. Inicjalizowana na `True`.

## Metody

### `__init__(self)`
Konstruktor klasy.

*   **Zachowanie:**
    *   Inicjalizuje `self._seconds` na `0`.
    *   Inicjalizuje `self.running` na `True`.

### `start_timer(self)`
Uruchamia timer w osobnym wątku. Wątek ten co sekundę inkrementuje licznik `_seconds`.

*   **Zachowanie:**
    1.  Definiuje wewnętrzną funkcję `update_time()`:
        *   Funkcja ta działa w pętli `while self.running`.
        *   W każdej iteracji pętli:
            *   Czeka 1 sekundę (`time.sleep(1)`).
            *   Inkrementuje `self._seconds` o 1.
    2.  Tworzy nowy obiekt `threading.Thread`, którego celem (`target`) jest funkcja `update_time`.
    3.  Ustawia wątek jako `daemon=True`. Oznacza to, że wątek timera zostanie automatycznie zakończony, gdy główny program (wszystkie wątki nie-daemon) zakończy działanie.
    4.  Uruchamia wątek za pomocą `timer_thread.start()`.

### `stop_timer(self)`
Zatrzymuje działanie timera.

*   **Zachowanie:**
    *   Ustawia flagę `self.running` na `False`. To spowoduje, że pętla w funkcji `update_time` (działająca w osobnym wątku) zakończy się przy następnej iteracji.

### `reset_timer(self)`
Resetuje licznik czasu do zera. Nie zatrzymuje timera, jeśli jest uruchomiony.

*   **Zachowanie:**
    *   Ustawia `self._seconds` na `0`.

### `get_time(self)`
Zwraca aktualnie zmierzony czas w sekundach.

*   **Zwraca:**
    *   `int`: Liczba sekund zarejestrowana przez timer (`self._seconds`).