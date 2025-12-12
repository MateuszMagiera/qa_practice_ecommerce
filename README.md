# Test Automation Framework (UI & API)

This is an advanced test automation framework created to demonstrate skills in testing web applications (UI) and APIs. The project utilizes modern tools and best practices such as the Page Object Model, CI/CD, containerization, and advanced reporting.

Application under test: [QA Practice - E-commerce & API](https://qa-practice.netlify.app/)

**An automatically generated test report is available here:** [**Link to Allure Report**](https://mateuszmagiera.github.io/qa_practice_ecommerce/)

---

## Technologies Used

*   **Language:** Python 3.11
*   **Test Framework:** Pytest
*   **UI & API Automation:** Playwright
*   **Reporting:** Allure Framework
*   **CI/CD:** GitHub Actions
*   **Containerization:** Docker

---

## Project Architecture

The framework is built based on proven design patterns to ensure its scalability, readability, and ease of maintenance:

*   **Page Object Model (POM):** The logic for interacting with individual application pages is encapsulated in dedicated classes (e.g., `LoginPage`, `CartPage`), which separates it from the test logic.
*   **Data Separation:** Test data and sensitive information (e.g., login credentials) are stored in separate files, which facilitates management and increases security.
*   **Custom Fixtures:** The project uses custom Pytest fixtures (e.g., for automatically logging API requests) to avoid code duplication and simplify tests.

---

## Installation and Configuration

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/MateuszMagiera/qa_practice_ecommerce.git
    cd qa_practice_ecommerce
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```sh
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Install browsers for Playwright:**
    ```sh
    playwright install --with-deps
    ```

---

## Running Tests Locally

### 1. Run the API server (required for API tests)

API tests require running a local API server in a Docker container.

```sh
docker run -d --rm --name qa-practice-api -p8887:8081 rvancea/qa-practice-api:latest
```

> **Note:** If a container with this name already exists, stop it with the command `docker stop qa-practice-api` before restarting it.

### 2. Run Pytest tests

*   **Run all tests (UI and API):**
    ```sh
    pytest
    ```

*   **Run only UI tests:**
    ```sh
    pytest tests/ui/
    ```

*   **Run only API tests:**
    ```sh
    pytest tests/api/
    ```

---

## Reporting with Allure

### 1. Run tests with results collection

```sh
pytest --alluredir=allure-results
```

### 2. Generate and view the report

*   **Option A: Quick preview (temporary server)**
    ```sh
    allure serve allure-results
    ```

*   **Option B: Persistent server (recommended for local work)**
    1.  In one terminal, run an HTTP server that will host the report:
        ```sh
        python -m http.server 8000 --directory allure-report
        ```
    2.  After each test run, in a second terminal, generate the report, overwriting the old version:
        ```sh
        allure generate allure-results --clean -o allure-report
        ```
    3.  Open the report in your browser at `http://localhost:8000`. Simply refresh the page to see the new results.

---

## Running Tests with Docker

1.  **Build the Docker image:**
    ```sh
    docker build -t playwright-tests .
    ```

2.  **Run tests in the container:**
    ```sh
    docker run --rm -it playwright-tests
    ```
    > **Note:** For API tests to work inside the container, it must have access to the API server. This requires advanced Docker network configuration (e.g., `docker-compose`).

---

## CI/CD Integration (GitHub Actions)

The project is fully integrated with GitHub Actions. The workflow is triggered:
*   On every `push` and `pull_request` to the `main` or `master` branch.
*   Automatically twice a day (at 8:00 and 20:00 UTC) as a simulation of regression tests.

After each run, the Allure report is automatically generated and published to GitHub Pages.