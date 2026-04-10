# 🛒 E-commerce Test Automation Framework

An end-to-end test automation framework covering **UI**, **REST API**, and **GraphQL** testing for the [QA Practice](https://qa-practice.razvanvancea.ro/) e-commerce application.

📊 **Live Allure Report →** [mateuszmagiera.github.io/qa_practice_ecommerce](https://mateuszmagiera.github.io/qa_practice_ecommerce/)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| Test framework | Pytest 8 (`pytest-playwright`) |
| Browser / API automation | Playwright |
| Reporting | Allure Framework |
| CI/CD | GitHub Actions → Allure on GitHub Pages |
| Containerization | Docker & Docker Compose |
| Secrets management | `.env` + `python-dotenv` (git-ignored) |

---

## Project Structure

```
├── .github/workflows/       # CI pipelines (smoke, regression, full CI)
├── POM/pages/                # Page Object Model classes (LoginPage, HomePage, CartPage)
├── locators/pages/           # Locator modules — no hardcoded selectors in POM
├── data/                     # Test data (products, error messages)
├── super_secure/credentials/ # Credential loader (reads from environment variables)
├── utils/                    # Helper functions (e.g. price calculator)
├── tests/
│   ├── api/                  # REST API tests (GET / POST /api/v1/employees)
│   ├── graphql/              # GraphQL tests (songs query)
│   ├── llm/                  # AI/LLM tests (OpenAI — disabled by default)
│   └── ui/                   # UI tests (login, cart, mocking, screenshot-on-failure)
├── config.py                 # Central URL config with env var overrides
├── docker-compose.yml        # Orchestrates API + GraphQL + test runner
├── Dockerfile                # Test runner image
├── pytest.ini                # Pytest settings, custom markers
├── requirements.txt          # Pinned dependencies
└── .env.example              # Template for environment variables
```

### Key Design Decisions

- **Page Object Model** — interaction logic lives in `POM/pages/`, selectors in `locators/pages/`, tests only call high-level methods.
- **Centralized config** — all URLs in `config.py`, overridable via environment variables. No hardcoded URLs in tests.
- **Allure-wrapped API context** — custom `AllureLoggingAPIRequestContext` in `conftest.py` automatically logs every API request/response to the Allure report.
- **Screenshot on failure** — UI tests automatically capture a full-page screenshot and attach it to Allure when they fail.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (for API & GraphQL backends)
- Allure CLI ([install guide](https://docs.qameta.io/allure/#_installing_a_commandline)) — only needed for local report viewing

### 1. Clone & install

```sh
git clone https://github.com/MateuszMagiera/qa_practice_ecommerce.git
cd qa_practice_ecommerce
python -m venv .venv

# Windows
.\.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
playwright install --with-deps
```

### 2. Configure environment variables

Copy the template and fill in your credentials:

```sh
cp .env.example .env
```

`.env` contents:

```dotenv
# Credentials for the app under test
CORRECT_EMAIL=your_valid_email@example.com
CORRECT_PASSWORD=your_valid_password
INCORRECT_EMAIL=wrong@example.com
INCORRECT_PASSWORD=wrong_password

# URLs (defaults work for local Docker setup)
BASE_URL=https://qa-practice.razvanvancea.ro
API_BASE_URL=http://127.0.0.1:8887
GRAPHQL_URL=http://127.0.0.1:5000/graphql
```

> **Note:** `.env` is git-ignored and will never be committed. In CI, these values are loaded from GitHub Secrets.

### 3. Start backend services

```sh
docker compose up -d api graphql
```

This starts:
- **REST API** on `http://localhost:8887` (`rvancea/qa-practice-api`)
- **GraphQL API** on `http://localhost:5000/graphql` (`rvancea/qa-practice-graphql`)

Both services include health checks — Docker Compose waits until they're ready.

---

## Running Tests

### By scope

```sh
pytest                      # all tests
pytest tests/ui/            # UI tests only
pytest tests/api/           # REST API tests only
pytest tests/graphql/       # GraphQL tests only
```

### By test strategy (markers)

Tests are classified with custom pytest markers to support different CI stages:

| Marker | Purpose | Count |
|---|---|---|
| `smoke` | Critical-path tests — fast feedback on every PR | 8 |
| `regression` | Full suite — nightly or on-demand | 21 |
| _(no marker)_ | Demo/utility tests (e.g. intentional-failure screenshot demo) | 1 |

```sh
pytest -m smoke             # ~30 sec — login, add to cart, API health, GraphQL health
pytest -m regression        # full regression — all production tests
```

### With Allure reporting

```sh
pytest --alluredir=allure-results
allure serve allure-results                    # quick preview (temporary server)
# or
allure generate allure-results -o allure-report --clean
python -m http.server 8000 --directory allure-report   # persistent local server
```

---

## Running with Docker Compose (fully containerized)

Run the entire stack — backends + test runner — with a single command:

```sh
docker compose up --build --abort-on-container-exit
```

This will:
1. Start the API and GraphQL containers (with health checks)
2. Build the test runner image
3. Execute all tests inside the container
4. Output Allure results to `./allure-results/` and screenshots to `./screenshots/`

---

## CI/CD

The project uses three GitHub Actions workflows:

| Workflow | Trigger | What it runs |
|---|---|---|
| **`ci.yml`** | Push / PR to `main` | Full test suite → Allure report deployed to GitHub Pages |
| **`smoke.yml`** | Push / PR to `main` | `pytest -m smoke` — fast gate for every change |
| **`regression.yml`** | Manual (`workflow_dispatch`) | `pytest -m regression` — full regression on demand |

All workflows:
- Spin up API & GraphQL backends as service containers
- Install Python, dependencies, and Playwright browsers
- Upload Allure results as artifacts

Secrets required in GitHub repo settings: `CORRECT_EMAIL`, `CORRECT_PASSWORD`, `INCORRECT_EMAIL`, `INCORRECT_PASSWORD`.

---

## Allure Report

The latest report is automatically published after each CI run:

**→ [mateuszmagiera.github.io/qa_practice_ecommerce](https://mateuszmagiera.github.io/qa_practice_ecommerce/)**

Features visible in the report:
- Structured by `@allure.feature` / `@allure.story` (e.g. *Authentication*, *Shopping Cart*, *API: Employees*)
- Step-by-step breakdown with `allure.step()`
- Full API request/response logging (automatic, via custom wrapper)
- Screenshots attached on UI test failure
