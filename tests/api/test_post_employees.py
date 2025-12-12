import allure
import pytest
from playwright.sync_api import APIRequestContext, expect

API_BASE_URL = "http://localhost:8887"
EMPLOYEES_ENDPOINT = "/api/v1/employees"

@allure.feature("API: Employees POST")
class TestPostEmployees:
    @allure.story("Create Employees")
    @allure.title("Test POST /api/v1/employees endpoint")
    @allure.description("This test verifies that the API accepts POST request and allows creating new employees")
    def test_create_correct_employee(self, api_request_context: APIRequestContext):
        """
        Tests the POST /api/v1/employees endpoint to create new employees.
        """
        new_employee_data = {
            "firstName": "John",
            "lastName": "Doe",
            "email": "john.doe@example.com",
            "dob": "1990-01-15"
        }

        with allure.step(f"Send POST request to {EMPLOYEES_ENDPOINT}"):
            response = api_request_context.post(
                f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}",
                data=new_employee_data
            )

        with allure.step("Verify the response"):
            # This API returns 201 Created with an empty body.
            # We should verify the status code directly.
            assert response.status == 201, f"Expected status 201 Created, but got {response.status}"

        with allure.step("Verify that the new employee was actually created"):
            # Send a GET request to verify the employee list contains the new employee
            get_response = api_request_context.get(f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}")
            expect(get_response).to_be_ok()
            employees_list = get_response.json()
            # Check if any employee in the list matches the one we created
            assert any(emp['firstName'] == new_employee_data['firstName'] and emp['lastName'] == new_employee_data['lastName'] for emp in employees_list), \
                "Newly created employee not found in the employees list"

    @pytest.mark.parametrize("invalid_payload, expected_error_message_part", [
        ({"lastName": "Doe", "email": "jane.doe@example.com", "dob": "1991-02-16"}, "firstName must not be blank"),
        ({"firstName": "Jane", "lastName": "Doe", "email": "not-an-email", "dob": "1991-02-16"}, "email must be a well-formed email address"),
        ({"firstName": "Jane", "lastName": "Doe", "email": "jane.doe@example.com", "dob": "invalid-date"}, "dob must be a date in yyyy-MM-dd format"),
        ({}, "firstName must not be blank") # Test with empty payload
    ])
    @allure.story("Create Employees - Negative Scenarios")
    @allure.title("Test POST with invalid data: {expected_error_message_part}")
    @allure.description("This test verifies that the API returns a 400 Bad Request for various invalid payloads.")
    def test_create_employee_with_invalid_data(self, api_request_context: APIRequestContext, invalid_payload: dict, expected_error_message_part: str):
        """
        Tests that the API correctly handles various invalid data inputs.
        """
        with allure.step(f"Send POST request with invalid payload: {invalid_payload}"):
            response = api_request_context.post(
                f"{API_BASE_URL}{EMPLOYEES_ENDPOINT}",
                data=invalid_payload,
                fail_on_error=False  # Allow us to inspect the 4xx response
            )

        with allure.step("Verify the 400 Bad Request response"):
            assert response.status == 400, f"Expected status 400, but got {response.status}"
            response_json = response.json()
            assert "message" in response_json, "Response JSON should contain a 'message' key"
            assert expected_error_message_part in response_json["message"], \
                f"Expected error message part '{expected_error_message_part}' not found in response: {response_json['message']}"