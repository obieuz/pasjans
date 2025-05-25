Jasne, stworzenie czytelnego kodu dla gry karcianej takiej jak Pasjans to świetny cel. Kluczem jest dobra organizacja obiektowa.

Oto propozycja klas i ich typów, która powinna pomóc Ci w uporządkowaniu kodu, zwłaszcza w kontekście stosów kart:

1.  **`Karta` (Card)**
    *   **Atrybuty:**
        *   `kolor` (suit): Np. "Kier" (♥), "Karo" (♦), "Trefl" (♣), "Pik" (♠). Możesz użyć stringów lub stworzyć `Enum`.
        *   `ranga` (rank): Np. "As", "2", "3", ..., "10", "Walet", "Dama", "Król". Również stringi lub `Enum`. Możesz też przechowywać wartość numeryczną (As=1, Walet=11, Dama=12, Król=13) dla łatwiejszych porównań.
        *   `jest_odkryta` (is_face_up): Boolean (True/False). Domyślnie False.
    *   **Metody:**
        *   `__init__(self, kolor, ranga)`: Konstruktor.
        *   `__str__(self)` lub `__repr__(self)`: Do wyświetlania karty (np. "A♥" lub "[ ]" jeśli zakryta).
        *   `odkryj(self)`: Ustawia `jest_odkryta = True`.
        *   `zakryj(self)`: Ustawia `jest_odkryta = False`.
        *   `wartosc(self)`: Zwraca numeryczną wartość rangi.
        *   `kolor_karty(self)`: Zwraca "czerwony" lub "czarny" na podstawie koloru.

2.  **`StosKart` (CardStack) - Klasa bazowa/abstrakcyjna (opcjonalnie, ale może być użyteczna)**
    *   Chociaż Python nie wymusza klas abstrakcyjnych tak jak Java czy C#, można zdefiniować klasę bazową dla różnych typów stosów.
    *   **Atrybuty:**
        *   `karty` (cards): Lista obiektów `Karta`.
    *   **Metody:**
        *   `__init__(self)`: Inicjalizuje pustą listę `karty`.
        *   `dodaj_karte(self, karta)`: Dodaje kartę na wierzch stosu.
        *   `usun_karte(self)`: Usuwa i zwraca kartę z wierzchu stosu (jeśli niepusty).
        *   `gorna_karta(self)`: Zwraca kartę z wierzchu bez usuwania (jeśli niepusty).
        *   `jest_pusty(self)`: Zwraca True jeśli stos jest pusty.
        *   `__len__(self)`: Zwraca liczbę kart na stosie.
        *   `__str__(self)`: Podstawowa reprezentacja stosu.

3.  **`Talia` (Deck) - dziedziczy po `StosKart` lub używa go przez kompozycję**
    *   **Atrybuty:**
        *   Dziedziczy `karty` z `StosKart`.
    *   **Metody:**
        *   `__init__(self)`: Tworzy standardową talię 52 kart (wszystkie `jest_odkryta = False`).
        *   `potasuj(self)`: Tasuje karty w talii (`random.shuffle`).
        *   `rozdaj_karte(self)`: Alias dla `usun_karte()`.

4.  **`StosRoboczy` (TableauPile)** - stosy na głównym polu gry (7 stosów)
    *   To jest miejsce, gdzie masz jawne i niejawne karty.
    *   **Atrybuty:**
        *   `karty_zakryte` (hidden_cards): Lista obiektów `Karta`.
        *   `karty_odkryte` (visible_cards): Lista obiektów `Karta`.
    *   **Metody:**
        *   `__init__(self)`: Inicjalizuje puste listy `karty_zakryte` i `karty_odkryte`.
        *   `dodaj_poczatkowe_karty(self, lista_kart, ilosc_odkrytych=1)`: Dodaje listę kart, gdzie ostatnia `ilosc_odkrytych` (zazwyczaj 1) jest odkrywana i trafia do `karty_odkryte`, reszta do `karty_zakryte`.
        *   `moze_przyjac_karte(self, karta_do_polozenia)`: Sprawdza, czy `karta_do_polozenia` może być położona na wierzchu `karty_odkryte` (inna barwa, o jeden niższa ranga). Jeśli `karty_odkryte` są puste, sprawdza czy `karta_do_polozenia` to Król.
        *   `moze_przyjac_stos(self, stos_kart_do_polozenia)`: Sprawdza, czy pierwsza karta ze `stos_kart_do_polozenia` może być położona.
        *   `dodaj_karty(self, lista_kart_do_polozenia)`: Dodaje listę odkrytych kart na wierzch `karty_odkryte`.
        *   `wez_odkryte_karty(self, od_karty: Karta)`: Zwraca listę kart od podanej `od_karty` (włącznie) do końca `karty_odkryte` i usuwa je.
        *   `wez_gorna_karte(self)`: Zwraca i usuwa górną kartę z `karty_odkryte`.
        *   `odkryj_nastepna(self)`: Jeśli `karty_odkryte` są puste i `karty_zakryte` nie są, przenosi ostatnią kartę z `karty_zakryte` do `karty_odkryte` i ją odkrywa.
        *   `gorna_odkryta_karta(self)`: Zwraca ostatnią kartę z `karty_odkryte` (jeśli istnieje).
        *   `wyswietl(self)` lub `__str__(self)`: Wyświetla stos, np. `[ ] [ ] [ ] A♥ K♦ Q♣ J♠`.
        *   `jest_pusty(self)`: Zwraca `True` jeśli obie listy są puste.
        *   `ilosc_kart(self)`: Zwraca sumę kart w obu listach.

5.  **`StosBazowy` (FoundationPile)** - 4 stosy, na które odkłada się karty od Asa do Króla
    *   Dziedziczy po `StosKart` lub ma listę `karty`.
    *   **Atrybuty:**
        *   `karty`: Lista obiektów `Karta` (wszystkie odkryte).
        *   `wymagany_kolor` (required_suit): Określa, jakiego koloru karty przyjmuje ten stos (ustawiane przy tworzeniu).
    *   **Metody:**
        *   `__init__(self, wymagany_kolor)`
        *   `moze_przyjac_karte(self, karta)`: Sprawdza, czy karta ma `wymagany_kolor` i czy jest następną w sekwencji (As na pusty, 2 na Asa, itd.).
        *   `dodaj_karte(self, karta)`: Jeśli `moze_przyjac_karte` zwraca True, dodaje kartę.
        *   `gorna_karta(self)`: Zwraca kartę z wierzchu.
        *   `__str__(self)`: Wyświetla górną kartę lub "[ ]" jeśli pusty.

6.  **`StosDobierania` (StockPile)** - stos, z którego dobiera się karty
    *   Dziedziczy po `StosKart` lub ma listę `karty`.
    *   **Atrybuty:**
        *   `karty`: Lista obiektów `Karta` (wszystkie zakryte).
    *   **Metody:**
        *   `__init__(self, lista_kart_z_talii)`
        *   `dobierz_karte(self)`: Usuwa i zwraca górną kartę (która trafi na `StosOdrzuconych`).
        *   `czy_pusty(self)`
        *   `__str__(self)`: Np. `[ X ]` jeśli niepusty, `[   ]` jeśli pusty.

7.  **`StosOdrzuconych` (WastePile/DiscardPile)** - stos, na który trafiają karty ze `StosDobierania`
    *   Dziedziczy po `StosKart` lub ma listę `karty`.
    *   **Atrybuty:**
        *   `karty`: Lista obiektów `Karta` (wszystkie odkryte).
    *   **Metody:**
        *   `dodaj_karte(self, karta)`: Karta jest odkrywana przed dodaniem.
        *   `wez_gorna_karte(self)`: Usuwa i zwraca górną kartę (jeśli jest zagrywana).
        *   `gorna_karta(self)`: Zwraca górną kartę.
        *   `przenies_do_stosu_dobierania(self)`: Zwraca wszystkie swoje karty (odwrócone na zakryte), aby mogły wrócić do `StosDobierania`. Czyści sam siebie.
        *   `__str__(self)`: Wyświetla górną kartę lub kilka górnych kart.

8.  **`Gra` (Game)**
    *   **Atrybuty:**
        *   `talia` (deck): Obiekt `Talia`.
        *   `stos_dobierania` (stock): Obiekt `StockPile`.
        *   `stos_odrzuconych` (waste): Obiekt `WastePile`.
        *   `stosy_bazowe` (foundations): Lista 4 obiektów `FoundationPile`.
        *   `stosy_robocze` (tableaus): Lista 7 obiektów `TableauPile`.
    *   **Metody:**
        *   `__init__(self)`: Tworzy wszystkie potrzebne stosy.
        *   `nowa_gra(self)`:
            *   Tworzy i tasuje talię.
            *   Rozdaje karty na stosy robocze (odpowiednia liczba zakrytych, jedna odkryta).
            *   Pozostałe karty umieszcza w `stos_dobierania`.
        *   `wyswietl_stan_gry(self)`: Wyświetla wszystkie stosy.
        *   `dobierz_ze_stosu(self)`: Logika dobierania ze `StosDobierania` do `StosOdrzuconych` (np. 1 lub 3 karty). Obsługuje resetowanie, gdy `StosDobierania` jest pusty.
        *   `przenies_karte(self, zrodlo, cel, karta_opcjonalnie=None, ilosc_kart_opcjonalnie=1)`: Główna logika ruchów. Musi identyfikować typy stosów źródłowych i docelowych, aby zastosować odpowiednie reguły. Np.
            *   `przenies_z_odrzuconych_do_roboczego(self, indeks_roboczy)`
            *   `przenies_z_odrzuconych_do_bazowego(self, indeks_bazowy)`
            *   `przenies_z_roboczego_do_bazowego(self, indeks_roboczy_zrodlo, indeks_bazowy)`
            *   `przenies_z_roboczego_do_roboczego(self, indeks_roboczy_zrodlo, indeks_roboczy_cel, karta_startowa_przenoszenia)`
            *   `przenies_z_bazowego_do_roboczego(self, indeks_bazowy, indeks_roboczy)` (rzadziej używane, ale możliwe)
        *   `sprawdz_wygrana(self)`: Sprawdza, czy wszystkie karty są na stosach bazowych.
        *   `petla_gry(self)`: Główna pętla obsługująca interakcję z użytkownikiem i logikę gry.

**Użycie `Enum` dla kolorów i rang (zalecane):**

```python
from enum import Enum, auto # auto dla wartości rang

class Kolor(Enum):
    KIER = "♥"
    KARO = "♦"
    TREFL = "♣"
    PIK = "♠"

    @property
    def barwa(self): # 'color' in English
        if self in (Kolor.KIER, Kolor.KARO):
            return "czerwony"
        return "czarny"

class Ranga(Enum):
    AS = (1, "A")
    DWA = (2, "2")
    TRZY = (3, "3")
    CZTERY = (4, "4")
    PIEC = (5, "5")
    SZESC = (6, "6")
    SIEDEM = (7, "7")
    OSIEM = (8, "8")
    DZIEWIEC = (9, "9")
    DZIESIEC = (10, "10")
    WALET = (11, "W") # lub J
    DAMA = (12, "D")  # lub Q
    KROL = (13, "K")

    def __init__(self, wartosc, symbol):
        self.wartosc = wartosc
        self.symbol = symbol

    def __lt__(self, other): # Potrzebne do porównań typu ranga1 < ranga2
        if self.__class__ is other.__class__:
            return self.wartosc < other.wartosc
        return NotImplemented
```

**Przykład implementacji `Karta` z Enumami:**

```python
class Karta:
    def __init__(self, kolor: Kolor, ranga: Ranga):
        self.kolor = kolor
        self.ranga = ranga
        self.jest_odkryta = False

    def __str__(self):
        if self.jest_odkryta:
            return f"{self.ranga.symbol}{self.kolor.value}"
        return "[ ]" # Lub inny symbol dla zakrytej karty

    def __repr__(self):
        return f"Karta({self.kolor.name}, {self.ranga.name}, {'odkryta' if self.jest_odkryta else 'zakryta'})"

    def odkryj(self):
        self.jest_odkryta = True

    def zakryj(self):
        self.jest_odkryta = False

    @property
    def wartosc(self):
        return self.ranga.wartosc

    @property
    def barwa_koloru(self): # np. "czerwony" / "czarny"
        return self.kolor.barwa
```

**Kluczowe dla `StosRoboczy` (TableauPile):**

```python
class StosRoboczy:
    def __init__(self):
        self.karty_zakryte: list[Karta] = []
        self.karty_odkryte: list[Karta] = []

    def dodaj_karte_na_spod_zakrytych(self, karta: Karta):
        """Używane przy początkowym rozdaniu"""
        karta.zakryj()
        self.karty_zakryte.append(karta)

    def dodaj_karte_na_wierzch_odkrytych(self, karta: Karta):
        """Używane przy początkowym rozdaniu dla ostatniej karty lub przy przenoszeniu"""
        karta.odkryj()
        self.karty_odkryte.append(karta)

    def odkryj_nastepna(self):
        if not self.karty_odkryte and self.karty_zakryte:
            karta_do_odkrycia = self.karty_zakryte.pop()
            karta_do_odkrycia.odkryj()
            self.karty_odkryte.append(karta_do_odkrycia)
            return True
        return False

    def gorna_odkryta_karta(self) -> Karta | None:
        return self.karty_odkryte[-1] if self.karty_odkryte else None

    def mozna_polozyc(self, karta_do_polozenia: Karta) -> bool:
        gorna = self.gorna_odkryta_karta()
        if not gorna: # Pusty stos roboczy
            return karta_do_polozenia.ranga == Ranga.KROL
        # Reguła: inna barwa, o jeden niższa ranga
        return (karta_do_polozenia.barwa_koloru != gorna.barwa_koloru and
                karta_do_polozenia.wartosc == gorna.wartosc - 1)

    def dodaj_stos_odkrytych(self, stos_kart: list[Karta]):
        """Dodaje listę kart (np. przenoszony pod-stos) na wierzch odkrytych"""
        # Zakładamy, że reguły zostały sprawdzone wcześniej
        self.karty_odkryte.extend(stos_kart)

    def wez_od_karty(self, karta_startowa: Karta) -> list[Karta] | None:
        """Zwraca i usuwa stos kart zaczynający się od karty_startowa"""
        try:
            idx = self.karty_odkryte.index(karta_startowa)
            przenoszony_stos = self.karty_odkryte[idx:]
            self.karty_odkryte = self.karty_odkryte[:idx]
            # Po usunięciu stosu, jeśli zostały tylko zakryte, odkryj jedną
            self.odkryj_nastepna()
            return przenoszony_stos
        except ValueError: # Karta nie znaleziona w odkrytych
            return None

    def __str__(self):
        zakryte_str = " ".join(["[ ]"] * len(self.karty_zakryte))
        odkryte_str = " ".join([str(k) for k in self.karty_odkryte])
        if zakryte_str and odkryte_str:
            return f"{zakryte_str} {odkryte_str}"
        return zakryte_str or odkryte_str or "<pusty>"
```

Taka struktura pozwoli Ci na logiczne rozdzielenie odpowiedzialności. Klasa `StosRoboczy` będzie centralnym punktem dla zarządzania widocznością kart. Pamiętaj o testowaniu każdej klasy osobno w miarę jej tworzenia. Powodzenia!