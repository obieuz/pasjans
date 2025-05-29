# Klasa LeaderboardManager

Zarządza tabelą najlepszych wyników (leaderboard) gry. Odpowiada za wczytywanie wyników z pliku JSON, dodawanie nowych wyników, sortowanie ich, ograniczanie do maksymalnej liczby wpisów oraz zapisywanie z powrotem do pliku.

## Importy

*   `json`: Do serializacji i deserializacji danych tabeli wyników do/z formatu JSON.
*   `datetime`: Do generowania znaczników czasu dla nowych wpisów.
*   `Path` (z `pathlib`): Do obsługi ścieżek plików w sposób niezależny od systemu operacyjnego.
*   `List`, `Dict`, `Optional` (z `typing`): Do typowania.

## Stałe Klasowe

*   `DEFAULT_FILE_PATH` (`Path`): Domyślna ścieżka do pliku, w którym przechowywane są dane tabeli wyników. Wartość: `Path("leaderboard.json")`.
*   `MAX_ENTRIES` (`int`): Domyślna maksymalna liczba wpisów, które będą przechowywane w tabeli wyników. Wartość: `10`.

## Atrybuty Instancji

*   `filepath` (`Path`): Ścieżka do pliku JSON przechowującego dane tabeli wyników. Jeśli nie zostanie podana w konstruktorze, używana jest `DEFAULT_FILE_PATH`.
*   `max_entries` (`int`): Maksymalna liczba wpisów w tabeli wyników. Jeśli nie zostanie podana w konstruktorze, używana jest `MAX_ENTRIES`.
*   `leaderboard_data` (`List[Dict]`): Lista słowników, gdzie każdy słownik reprezentuje pojedynczy wpis w tabeli wyników (np. `{"nickname": "Gracz1", "moves": 100, "time_seconds": 120, "timestamp": "..."}`). Dane są wczytywane z pliku podczas inicjalizacji.

## Metody

### `__init__(self, filepath: Optional[Path] = None, max_entries: Optional[int] = None)`
Konstruktor klasy.

*   **Parametry:**
    *   `filepath` (`Optional[Path]`, domyślnie `None`): Ścieżka do pliku tabeli wyników. Jeśli `None`, używana jest `LeaderboardManager.DEFAULT_FILE_PATH`.
    *   `max_entries` (`Optional[int]`, domyślnie `None`): Maksymalna liczba wpisów w tabeli. Jeśli `None`, używana jest `LeaderboardManager.MAX_ENTRIES`.
*   **Zachowanie:**
    *   Ustawia atrybuty `self.filepath` i `self.max_entries` na podstawie przekazanych argumentów lub wartości domyślnych.
    *   Wywołuje metodę `self._load()` w celu wczytania danych tabeli wyników z pliku i przypisuje je do `self.leaderboard_data`.

### `_load(self) -> List[Dict]`
(Metoda prywatna) Wczytuje dane tabeli wyników z pliku JSON określonego przez `self.filepath`.

*   **Zachowanie:**
    *   Sprawdza, czy plik `self.filepath` istnieje. Jeśli nie, zwraca pustą listę.
    *   Próbuje otworzyć plik, odczytać jego zawartość i zdeserializować ją z formatu JSON.
    *   W przypadku błędu podczas odczytu pliku lub dekodowania JSON (`json.JSONDecodeError`, `IOError`), zwraca pustą listę.
*   **Zwraca:**
    *   `List[Dict]`: Lista wpisów tabeli wyników wczytana z pliku, lub pusta lista w przypadku braku pliku lub błędu.

### `_save(self)`
(Metoda prywatna) Zapisuje aktualne dane tabeli wyników (`self.leaderboard_data`) do pliku JSON określonego przez `self.filepath`.

*   **Zachowanie:**
    *   Próbuje otworzyć plik w trybie zapisu i zapisać `self.leaderboard_data` jako sformatowany JSON (z wcięciem 4 spacje, `ensure_ascii=False` dla poprawnego zapisu polskich znaków).
    *   W przypadku błędu `IOError` podczas zapisu, wyświetla komunikat o błędzie na standardowe wyjście, ale program kontynuuje działanie.
*   **Nie zwraca nic.**

### `get_scores(self) -> List[Dict]`
Zwraca listę wyników z tabeli.

*   **Zachowanie:**
    *   Wywołuje `self._load()` w celu ponownego wczytania danych z pliku. (Uwaga: może to być celowe, aby zawsze mieć najświeższe dane z pliku, ale jeśli inne instancje modyfikują plik, może to być nieefektywne lub prowadzić do nadpisania zmian w pamięci. Alternatywnie, mogłoby zwracać `self.leaderboard_data`).
*   **Zwraca:**
    *   `List[Dict]`: Lista wpisów tabeli wyników.

### `add_score(self, nickname: str, moves: int, time_seconds: int) -> bool`
Dodaje nowy wynik do tabeli wyników.

*   **Parametry:**
    *   `nickname` (`str`): Nazwa gracza.
    *   `moves` (`int`): Liczba ruchów wykonanych przez gracza.
    *   `time_seconds` (`int`): Czas gry w sekundach.
*   **Zachowanie:**
    1.  Tworzy nowy słownik `new_score_entry` zawierający `nickname`, `moves`, `time_seconds` oraz aktualny znacznik czasu (`timestamp`) w formacie ISO (z dokładnością do sekund).
    2.  Dodaje `new_score_entry` do listy `self.leaderboard_data`.
    3.  Sortuje listę `self.leaderboard_data` rosnąco według liczby ruchów (`moves`). Jeśli liczba ruchów jest taka sama, kolejność jest stabilna lub zależy od implementacji `sort`. Wartości `None` lub brakujące klucze "moves" są traktowane jako nieskończoność, co umieszcza je na końcu.
    4.  Przycina listę `self.leaderboard_data` do maksymalnej liczby wpisów określonej przez `self.max_entries`.
    5.  Wywołuje `self._save()` w celu zapisania zaktualizowanej tabeli wyników do pliku.
*   **Zwraca:**
    *   `bool`: `True`, jeśli `new_score_entry` znajduje się w `self.leaderboard_data` po operacjach sortowania i przycinania (tzn. wynik był wystarczająco dobry, aby znaleźć się w tabeli). `False` w przeciwnym razie.

### `@staticmethod`
### `format_time(seconds: int) -> str`
Metoda statyczna do formatowania czasu podanego w sekundach na czytelny format "MM:SS".

*   **Parametry:**
    *   `seconds` (`int`): Całkowita liczba sekund.
*   **Zachowanie:**
    *   Oblicza liczbę pełnych minut (`seconds // 60`).
    *   Oblicza pozostałą liczbę sekund (`seconds % 60`).
    *   Formatuje wynik jako `MM:SS`, gdzie obie wartości są dwucyfrowe z wiodącymi zerami (np. "02:05").
*   **Zwraca:**
    *   `str`: Sformatowany czas w postaci "MM:SS".