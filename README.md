# Framework Automatyzacji Testów (UI & API)

Jest to zaawansowany framework do automatyzacji testów, stworzony w celu demonstracji umiejętności w zakresie testowania aplikacji webowych (UI) oraz API. Projekt wykorzystuje nowoczesne narzędzia i dobre praktyki, takie jak Page Object Model, CI/CD, konteneryzacja oraz zaawansowane raportowanie.

Testowana aplikacja: [QA Practice - E-commerce & API](https://qa-practice.netlify.app/)

**Automatycznie generowany raport z testów jest dostępny tutaj:** [**Link do Raportu Allure**](https://mateuszmagiera.github.io/qa_practice_ecommerce/)

---

## Użyte Technologie

*   **Język:** Python 3.11
*   **Framework Testowy:** Pytest
*   **Automatyzacja UI & API:** Playwright
*   **Raportowanie:** Allure Framework
*   **CI/CD:** GitHub Actions
*   **Konteneryzacja:** Docker

---

## Architektura Projektu

Framework został zbudowany w oparciu o sprawdzone wzorce projektowe, aby zapewnić jego skalowalność, czytelność i łatwość w utrzymaniu:

*   **Page Object Model (POM):** Logika interakcji z poszczególnymi stronami aplikacji jest zamknięta w dedykowanych klasach (np. `LoginPage`, `CartPage`), co oddziela ją od logiki testów.
*   **Separacja Danych:** Dane testowe i wrażliwe (np. dane logowania) są przechowywane w osobnych plikach, co ułatwia zarządzanie i zwiększa bezpieczeństwo.
*   **Custom Fixtures:** Projekt wykorzystuje niestandardowe fixtury Pytest (np. do automatycznego logowania zapytań API), aby unikać duplikacji kodu i upraszczać testy.

---

## Instalacja i Konfiguracja

1.  **Sklonuj repozytorium:**
    ```sh
    git clone https://github.com/MateuszMagiera/qa_practice_ecommerce.git
    cd qa_practice_ecommerce
    ```

2.  **Stwórz i aktywuj środowisko wirtualne (zalecane):**
    ```sh
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Zainstaluj zależności:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Zainstaluj przeglądarki dla Playwright:**
    ```sh
    playwright install --with-deps
    ```

---

## Uruchamianie Testów Lokalnie

### 1. Uruchomienie serwera API (wymagane dla testów API)

Testy API wymagają uruchomienia lokalnego serwera API w kontenerze Docker.

```sh
docker run -d --rm --name qa-practice-api -p8887:8081 rvancea/qa-practice-api:latest
```

> **Uwaga:** Jeśli kontener o tej nazwie już istnieje, zatrzymaj go komendą `docker stop qa-practice-api` przed ponownym uruchomieniem.

### 2. Uruchomienie testów Pytest

*   **Uruchomienie wszystkich testów (UI i API):**
    ```sh
    pytest
    ```

*   **Uruchomienie tylko testów UI:**
    ```sh
    pytest tests/ui/
    ```

*   **Uruchomienie tylko testów API:**
    ```sh
    pytest tests/api/
    ```

---

## Raportowanie z Allure

### 1. Uruchomienie testów z kolekcjonowaniem wyników

```sh
pytest --alluredir=allure-results
```

### 2. Generowanie i przeglądanie raportu

*   **Opcja A: Szybki podgląd (serwer tymczasowy)**
    ```sh
    allure serve allure-results
    ```

*   **Opcja B: Serwer stały (zalecane do pracy lokalnej)**
    1.  W jednym terminalu uruchom serwer HTTP, który będzie hostował raport:
        ```sh
        python -m http.server 8000 --directory allure-report
        ```
    2.  Po każdym uruchomieniu testów, w drugim terminalu wygeneruj raport, nadpisując starą wersję:
        ```sh
        allure generate allure-results --clean -o allure-report
        ```
    3.  Otwórz raport w przeglądarce pod adresem `http://localhost:8000`. Po prostu odśwież stronę, aby zobaczyć nowe wyniki.

---

## Uruchamianie Testów z użyciem Dockera

1.  **Zbuduj obraz Docker:**
    ```sh
    docker build -t playwright-tests .
    ```

2.  **Uruchom testy w kontenerze:**
    ```sh
    docker run --rm -it playwright-tests
    ```
    > **Uwaga:** Aby testy API działały wewnątrz kontenera, musi on mieć dostęp do serwera API. Wymaga to zaawansowanej konfiguracji sieci Docker (np. `docker-compose`).

---

## Integracja z CI/CD (GitHub Actions)

Projekt jest w pełni zintegrowany z GitHub Actions. Workflow jest uruchamiany:
*   Po każdym `push` i `pull_request` do gałęzi `main` lub `master`.
*   Automatycznie dwa razy dziennie (o 8:00 i 20:00 UTC) w ramach symulacji testów regresji.

Po każdym uruchomieniu, raport Allure jest automatycznie generowany i publikowany na GitHub Pages.