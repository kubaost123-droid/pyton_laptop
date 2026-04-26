# Projekt - mini-framework do uruchamiania symulacji numerycznych w Pythonie

## Cel projektu

Celem projektu jest napisanie w Pythonie niewielkiego, ale sensownie zaprojektowanego środowiska do uruchamiania symulacji numerycznych, analizy ich przebiegu oraz wizualizacji wyników.

Projekt ma służyć jako praktyczne ćwiczenie z:
- klas i obiektów,
- klas abstrakcyjnych,
- dziedziczenia,
- `dataclass`,
- podziału programu na logiczne komponenty,
- projektowania czytelnego API.

Nie chodzi o to, aby cały program był napisany "na siłę obiektowo". W projekcie klasy powinny być użyte tam, gdzie rzeczywiście pomagają uporządkować kod. Drobne obliczenia pomocnicze mogą być realizowane zwykłymi funkcjami.

---

## Ogólny opis zadania

Należy zaimplementować **mini-framework do uruchamiania symulacji numerycznych**. Program powinien pozwalać na:

- zdefiniowanie parametrów symulacji,
- zdefiniowanie stanu początkowego układu,
- uruchomienie symulacji krok po kroku,
- zapis historii stanów układu,
- obliczanie statystyk w kolejnych krokach,
- obliczenie statystyk końcowych,
- wygenerowanie co najmniej jednej wizualizacji wyników i zapisanie jej do pliku graficznego.

Projekt powinien być zaprojektowany modułowo. Poszczególne elementy programu powinny odpowiadać za różne aspekty działania symulacji, a nie być zebrane w jednym bardzo długim pliku lub w jednej klasie.

---

## Wymagania obowiązkowe

### 1. Architektura obiektowa
Projekt musi zawierać następujące elementy:

#### Klasa sterująca i klasy abstrakcyjne
Projekt musi zawierać następujące elementy:

1. `Simulation` - zwykła klasa odpowiedzialna za spięcie całego przebiegu symulacji. Powinna przechowywać potrzebne komponenty, uruchamiać pętlę symulacji oraz budować wynik końcowy.
2. `StepRule` - abstrakcyjna klasa odpowiedzialna za obliczanie kolejnego kroku symulacji.
3. `StepAnalyzer` - abstrakcyjna klasa odpowiedzialna za obliczanie statystyk dla pojedynczego kroku.
4. `FinalAnalyzer` - abstrakcyjna klasa odpowiedzialna za obliczanie statystyk końcowych całej symulacji.
5. `Visualizer` - abstrakcyjna klasa odpowiedzialna za tworzenie wizualizacji wyników.

Klasa `Simulation` nie musi być abstrakcyjna. Jej rolą jest koordynacja działania pozostałych komponentów. Natomiast klasy `StepRule`, `StepAnalyzer`, `FinalAnalyzer` i `Visualizer` powinny definiować sensowny interfejs przy pomocy metod abstrakcyjnych.

#### Konkretne implementacje
Należy zaimplementować co najmniej:

- jedną klasę `Simulation`,
- jedną konkretną klasę dziedziczącą po `StepRule`,
- jedną konkretną klasę dziedziczącą po `StepAnalyzer`,
- jedną konkretną klasę dziedziczącą po `FinalAnalyzer`,
- jedną konkretną klasę dziedziczącą po `Visualizer`.

---

### 2. Wymagane `dataclass`
Projekt musi zawierać co najmniej następujące klasy danych utworzone jako `dataclass`:

1. `SimulationConfig` - parametry wejściowe symulacji.
2. `SimulationState` - stan całego układu w pojedynczym kroku, w tym także stan początkowy.
3. `StepStatistics` - statystyki obliczane dla pojedynczego kroku.
4. `FinalStatistics` - statystyki końcowe całej symulacji.
5. `SimulationResult` - obiekt przechowujący pełen wynik symulacji.

Uwaga: nazwy takie jak `SimulationConfig`, `SimulationState`, `StepStatistics`, `FinalStatistics` czy `SimulationResult` są jedynie nazwami przykładowymi. W praktyce każda konkretna symulacja będzie zwykle korzystać z własnych, dedykowanych klas danych, dostosowanych do jej modelu i reprezentacji stanu, np. `OscillatorConfig`, `OscillatorState`, `GridSIRState` itp.

### Co powinny reprezentować te klasy

#### `SimulationConfig`
Powinna przechowywać parametry modelu i parametry uruchomienia, np.:
- liczbę kroków,
- krok czasowy `dt`,
- rozmiar układu,
- prawdopodobieństwa lub stałe modelu,
- ziarno generatora losowego.

#### `SimulationState`
Powinna przechowywać pełny stan układu w danym kroku, np.:
- numer kroku,
- czas,
- położenie i prędkość,
- stan siatki,
- dodatkowe informacje potrzebne do aktualizacji układu.

#### `StepStatistics`
Powinna przechowywać wielkości wyliczane dla pojedynczego kroku, np.:
- energię,
- liczbę elementów w danym stanie,
- średnią odległość,
- inne obserwable zależne od modelu.

#### `FinalStatistics`
Powinna przechowywać zagregowane wyniki końcowe, np.:
- maksimum wybranej wielkości,
- czas osiągnięcia maksimum,
- wartość końcową,
- średnią z całego przebiegu,
- błąd lub dryf energii.

#### `SimulationResult`
Powinna przechowywać pełny wynik symulacji, np.:
- używaną konfigurację,
- listę stanów kolejnych kroków,
- listę statystyk krokowych,
- statystyki końcowe.

---

### 3. Przebieg symulacji
Program powinien umożliwiać:

- utworzenie konfiguracji symulacji,
- utworzenie stanu początkowego,
- uruchomienie pętli symulacji,
- generowanie kolejnych stanów układu przy pomocy obiektu `StepRule`,
- obliczanie statystyk dla każdego kroku przy pomocy obiektu `StepAnalyzer`,
- zapisanie wyniku w obiekcie `SimulationResult`.
- obliczenie statystyk końcowych przy pomocy obiektu `FinalAnalyzer`,

Klasa `Simulation` powinna pełnić rolę koordynatora: uruchamiać poszczególne komponenty, pilnować kolejności działań i spinać całość w jeden przebieg.

---

### 4. Wizualizacja
Projekt musi generować co najmniej **jedną wizualizację wyników** i zapisywać ją do pliku graficznego, np. PNG.

Wizualizacja powinna być tworzona przez osobny obiekt klasy dziedziczącej po `Visualizer`.

Przykładowe wizualizacje:
- wykres położenia w funkcji czasu,
- wykres energii w funkcji czasu,
- wykres liczby osobników w stanach `S`, `I`, `R`,
- obraz stanu siatki w wybranym kroku,
- portret fazowy,
- histogram wybranej wielkości.

---

### 5. Dokumentacja
Projekt musi zawierać plik `README.md`, w którym należy krótko opisać:

- jaki model został zaimplementowany,
- jak uruchomić program,
- jakie klasy zostały zdefiniowane,
- jakie wykresy lub obrazy są generowane.

---

## Wymagania dodatkowe na wyższą ocenę

Na wyższą ocenę można zaimplementować na przykład:

- więcej niż jedną konkretną symulację,
- więcej niż jedną metodę obliczania kolejnego kroku,
- więcej niż jeden wizualizator dla tych samych danych,
- zapis wyników do pliku tekstowego lub CSV,
- możliwość wczytywania konfiguracji z pliku,
- animację przebiegu symulacji,

---

## Uwagi projektowe

W projekcie należy wyraźnie rozróżnić:

- **parametry symulacji** (`SimulationConfig`),
- **stan układu** (`SimulationState`),
- **statystyki pojedynczego kroku** (`StepStatistics`),
- **statystyki końcowe** (`FinalStatistics`).

To rozróżnienie jest istotne. Parametry mówią, **jak działa model**, natomiast stan mówi, **w jakiej sytuacji układ znajduje się w danym kroku**.

W projekcie liczy się przede wszystkim **sensowność architektury**, a nie liczba klas. Prosty, czytelny i logiczny projekt jest lepszy niż przesadnie rozbudowany system z wieloma zbędnymi abstrakcjami.

---

# Przykładowe symulacje do przetestowania frameworka

Poniżej znajdują się dwa przykładowe modele, które można zaimplementować w ramach projektu.

---

## Przykład 1 - oscylator harmoniczny lub tłumiony

### Opis modelu
Rozważamy punkt materialny o położeniu `x(t)` i prędkości `v(t)`, poruszający się pod wpływem siły sprężystości, a opcjonalnie także tłumienia.

Najprostszy wariant to oscylator harmoniczny:

`m x'' = -k x`

Wariant rozszerzony może uwzględniać tłumienie:

`m x'' = -k x - c v`

Można przejść do układu równań pierwszego rzędu:

- `x' = v`
- `v' = -(k/m) x` dla oscylatora bez tłumienia,
- `v' = -(k/m) x - (c/m) v` dla oscylatora tłumionego.

### Założenia
- Symulacja przebiega w dyskretnych krokach czasowych `dt`.
- Stan układu w danym kroku zawiera co najmniej czas, położenie i prędkość.
- Stan początkowy jest zadany przez użytkownika, np. `x(0)` i `v(0)`.
- Kolejne kroki są wyznaczane numerycznie przez wybraną metodę aktualizacji.

### Możliwa dynamika
Można zaimplementować jedną z prostych metod numerycznych, np.:
- metodę Eulera,
- metodę Verlet,

W każdym kroku należy z bieżącego stanu obliczyć nowy stan układu.

### Przykładowe elementy stanu i statystyk

#### `SimulationState`
Może zawierać:
- numer kroku,
- czas `t`,
- położenie `x`,
- prędkość `v`.

#### `StepStatistics`
Może zawierać:
- energię kinetyczną,
- energię potencjalną,
- energię całkowitą.

#### `FinalStatistics`
Może zawierać:
- maksymalne wychylenie,
- końcową energię,
- średnią energię całkowitą.

### Możliwe wizualizacje
- wykres `x(t)`,
- wykres `v(t)`,
- wykres energii w funkcji czasu,
- portret fazowy `v(x)`.

---

## Przykład 2 - model SIR na siatce kwadratowej

### Opis modelu
Rozważamy epidemię rozprzestrzeniającą się na dwuwymiarowej siatce kwadratowej. Każda komórka siatki reprezentuje jednego osobnika i może znajdować się w jednym z trzech stanów:

- `S` - podatny na zakażenie,
- `I` - zakażony,
- `R` - usunięty z procesu zakażania, np. ozdrowiały lub odporny.

Model jest dyskretny zarówno w przestrzeni, jak i w czasie.

### Założenia modelu
- Układ jest reprezentowany przez siatkę `width x height`.
- W każdym kroku czasowym wszystkie komórki są aktualizowane według ustalonej reguły.
- Na początku symulacji większość komórek jest w stanie `S`, a niewielka liczba komórek w stanie `I`.
- Stan `R` oznacza, że dana komórka nie zakaża się ponownie.

### Sąsiedztwo
Należy jasno określić, które komórki sąsiadują ze sobą. Możliwe warianty:

- **sąsiedztwo von Neumanna** - góra, dół, lewo, prawo,
- **sąsiedztwo Moore'a** - osiem najbliższych komórek.

W projekcie wystarczy wybrać jeden wariant, ale należy go opisać.

### Przykładowa dynamika
W każdym kroku czasu:

1. Komórka w stanie `S` może przejść do stanu `I`, jeśli ma zakażonego sąsiada. Zakażenie zachodzi z zadanym prawdopodobieństwem `p_infect`. Jeżeli komórka ma kilku sąsiadów w stanie `I`, to każdy z nich stara się ją zakazić z prawdopodobieństwem `p_infect`.
2. Komórka w stanie `I` przechodzi do stanu `R` z prawdopodobieństwem `p_recovery`.
4. Komórka w stanie `R` pozostaje w tym stanie do końca symulacji.


### Stan początkowy
Stan początkowy należy jawnie zdefiniować. Możliwe przykłady:
- pojedyncza zakażona komórka w środku siatki,
- kilka losowo wybranych komórek zakażonych,
- określony procent początkowo zakażonych komórek.

### Dynamika synchroniczna

W symulacjach SIR należy przyjąć **dynamikę synchroniczną**. Oznacza to, że w danym kroku czasowym nowy stan całego układu jest wyznaczany **na podstawie stanu układu z poprzedniego kroku**, a wszystkie komórki są aktualizowane jednocześnie. Innymi słowy, przy obliczaniu stanu w chwili `t + 1` nie wolno korzystać z częściowo już zaktualizowanej siatki z tego samego kroku.

W praktyce oznacza to zwykle konieczność utworzenia nowej siatki lub jej kopii pomocniczej: najpierw dla wszystkich komórek wyznacza się ich stan w następnym kroku, a dopiero po zakończeniu tych obliczeń zastępuje się starą siatkę nową. Takie podejście zapobiega sytuacji, w której kolejność przeglądania komórek wpływałaby na wynik symulacji.

### Periodyczne warunki brzegowe

W modelach należy zastosować **periodyczne warunki brzegowe**. Oznacza to, że siatkę traktujemy tak, jakby była „zawinięta” w torus: komórki leżące przy jednej krawędzi mają sąsiadów po przeciwnej stronie siatki.

Przykładowo:
- dla komórki z pierwszego wiersza sąsiadem „nad nią” jest odpowiednia komórka z ostatniego wiersza,
- dla komórki z ostatniej kolumny sąsiadem „na prawo” jest odpowiednia komórka z pierwszej kolumny.

Dzięki temu każda komórka ma taką samą liczbę sąsiadów, a brzegi układu nie są wyróżnione. Implementacyjnie najwygodniej realizuje się to zwykle za pomocą operacji modulo przy wyznaczaniu indeksów sąsiednich komórek.

### Przykładowe elementy stanu i statystyk

#### `SimulationState`
Może zawierać:
- numer kroku,
- czas,
- siatkę stanów komórek,

#### `StepStatistics`
Może zawierać:
- liczbę komórek w stanie `S`,
- liczbę komórek w stanie `I`,
- liczbę komórek w stanie `R`,
- liczbę nowych zakażeń w danym kroku.

#### `FinalStatistics`
Może zawierać:
- maksymalną liczbę zakażonych,
- numer kroku lub czas osiągnięcia maksimum,
- całkowitą liczbę komórek, które przeszły infekcję,
- krok wygaśnięcia epidemii, jeśli do niego doszło.

### Możliwe wizualizacje
- obraz siatki dla wybranego kroku,
- seria obrazów pokazujących rozwój epidemii,
- wykres `S(t), I(t), R(t)`,
- wykres liczby nowych zakażeń w funkcji czasu.

---

## Sugestia dotycząca testowania projektu

Podczas testowania projektu warto sprawdzić, czy framework działa poprawnie dla co najmniej jednego z dwóch modeli opisanych powyżej. Mile widziane jest zaimplementowanie obu modeli, ale nie jest to wymagane.

---

## Kryteria oceny

Przykładowe kryteria oceny projektu:

1. **Poprawność działania programu**
   - czy symulacja działa poprawnie,
   - czy wyniki są spójne z założeniami modelu.

2. **Jakość projektu kodu**
   - czy klasy i moduły mają sensowny podział odpowiedzialności,
   - czy kod jest czytelny i logicznie zorganizowany.

3. **Wykorzystanie elementów programowania obiektowego**
   - czy sensownie rozdzielono rolę klasy `Simulation` i pozostałych komponentów,
   - czy poprawnie wykorzystano klasy abstrakcyjne i dziedziczenie,
   - czy `dataclass` są użyte we właściwych miejscach.

4. **Analiza i prezentacja wyników**
   - czy projekt oblicza statystyki,
   - czy generuje poprawne wizualizacje.

5. **Dokumentacja i estetyka oddania projektu**
   - czy istnieje `README.md`,
   - czy sposób uruchomienia programu jest jasno opisany.

---

## Podsumowanie

Projekt ma być przykładem **sensownego użycia programowania obiektowego w Pythonie**. Nie chodzi o maksymalnie rozbudowaną hierarchię klas, lecz o czytelne rozdzielenie ról:

- obiekt `Simulation` steruje przebiegiem programu i spina wszystkie komponenty,
- reguła kroku wyznacza kolejne stany,
- analizatory obliczają statystyki,
- wizualizatory odpowiadają za prezentację wyników,
- `dataclass` przechowują uporządkowane dane opisujące konfigurację, stan i wyniki.

Projekt powinien być prosty, logiczny i łatwy do rozwijania.
