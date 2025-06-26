# Uzywamy oficjalnego obrazu Pythona
FROM  python:3.11-slim

# Ustawiamy katalog roboczy
WORKDIR /app

# Skopiuj requirements do obrazu
COPY requirements.txt .

# zainstaluj zależności z requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# zainstaluj przeglądarki playwright w obrazie
RUN playwright install --with-deps

# skopiuj cały kod źródłowy do obrazu
COPY . .

# ustaw ścieżkę do modułów
ENV PYTHONPATH=/app

# domyślne polecenie (opcjonalnie)
CMD ["python","-m","pytest", "-s", "-v", "tests/"]