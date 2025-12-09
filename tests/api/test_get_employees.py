import pytest
import allure
from playwright.sync_api import APIRequestContext, expect

API_BASE_URL = "http://localhost:8887"
EMPLOYEES_ENDPOINT = "/api/v1/employees"

@allure.feature("API: Employees")
class TestGetAPI:
    @allure.story("Get All Employees")
    @allure.title("Test GET /api/v1/employees endpoint")
    @allure.description("This test verifies that the API returns a list of all employees successfully.")
    def test_get_employees(self, api_request_context: APIRequestContext):
        """
        Tests the GET /api/v1/employees endpoint to retrieve all employees.
        """
        with allure.step(f"Send GET request to {EMPLOYEES_ENDPOINT}"):
            response = api_request_context.get(f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}")

        with allure.step("Verify the response"):
            expect(response).to_be_ok()

            assert 'application/json' in response.headers['content-type'].lower(), "Content-Type header should contain 'application/json'"
            employees_data = response.json()

            assert isinstance(employees_data, list), f"Expected response to be a list, but got {type(employees_data)}"
            assert len(employees_data) > 0, "The employees list should not be empty"

            first_employee = employees_data[0]
            assert "id" in first_employee
            assert "firstName" in first_employee
            assert "lastName" in first_employee
            assert "email" in first_employee

    @allure.story("Get Employees")
    @allure.title("Test GET /api/v1/employees endpoint with bad request")
    @allure.description("This test verifies that the API returns a proper error code when sending bad request")
    def test_get_employees_with_unsupported_method(self, api_request_context: APIRequestContext):
        with allure.step(f"Send DELETE request to {EMPLOYEES_ENDPOINT}"):
            # We send a DELETE request to an endpoint that only supports GET
            response = api_request_context.delete(f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}")
        with allure.step("Verify the response"):
            # We expect a 405 Method Not Allowed status
            assert response.status == 405, f"Expected status 405, but got {response.status}"


    @allure.story("Get Employees")
    @allure.title("Test GET /api/v1/employees endpoint id")
    @allure.description("This test verifies if items returned as the response are of correct types")
    def test_get_employees_verify_id(self, api_request_context: APIRequestContext):
        with allure.step(f"Verify if response fields are of correct types"):
            response = api_request_context.get(f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}")
            for item in response.json():
                assert isinstance(item['id'], int), f"Expected id to be an integer, but got {type(item['id'])}"
                assert isinstance(item['firstName'], str), f"Expected firstName to be a string, but got {type(item['firstName'])}"
                assert isinstance(item['lastName'], str), f"Expected lastName to be a string, but got {type(item['lastName'])}"
                assert isinstance(item['email'], str), f"Expected email to be a string, but got {type(item['email'])}"
                assert isinstance(item['dob'], str), f"Expected email to be a string, but got {type(item['dob'])}"
                assert '@' in item['email'], f"Expected email to contain '@', but got {item['email']}'"
                assert '-' in item['dob'], f"Expected dob to contain '-', but got {item['dob']}'"
