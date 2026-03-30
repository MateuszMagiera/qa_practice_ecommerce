import allure
import pytest
from playwright.sync_api import APIRequestContext, expect
from config import GRAPHQL_URL
from utils.schema_validator import assert_valid_schema

@pytest.mark.regression
@allure.feature("GraphQL API")
class TestGraphQLSongs:
    @pytest.mark.smoke
    @allure.story("Query Songs")
    @allure.title("Test getting all songs")
    @allure.description("This test verifies that the list of all songs can be correctly retrieved via GraphQL.")
    def test_get_all_songs(self, api_request_context: APIRequestContext):
        """
        Tests fetching all songs using a GraphQL query.
        """
        query = """
            query GetAllSongs {
                songs {
                    id
                    title
                    album
                    author {
                        name
                        homeTown
                    }
                }
            }
        """

        with allure.step(f"Sending a GraphQL query for all songs to {GRAPHQL_URL}"):
            response = api_request_context.post(GRAPHQL_URL, data={'query': query})

        with allure.step("Verifying the server response"):
            expect(response).to_be_ok()
            
            response_data = response.json()
            
            assert 'errors' not in response_data, f"GraphQL returned errors: {response_data.get('errors')}"
            
            assert 'data' in response_data, "Response does not contain 'data' key"
            assert 'songs' in response_data['data'], "'data' key does not contain 'songs' key"
            
            songs = response_data['data']['songs']
            assert isinstance(songs, list), "'songs' field is not a list"
            assert len(songs) > 0, "The list of songs is empty"

        with allure.step("Verifying the data structure of the first song"):
            first_song = songs[0]
            assert 'id' in first_song
            assert 'title' in first_song
            assert 'album' in first_song
            assert 'author' in first_song
            assert isinstance(first_song['author'], dict)
            assert 'name' in first_song['author']
            assert 'homeTown' in first_song['author']

    @allure.story("Contract Testing")
    @allure.title("Validate GraphQL songs response against JSON Schema")
    @allure.description(
        "Validates the entire GraphQL response against a JSON Schema contract. "
        "Checks the data.songs structure, field presence, types, and nested author object."
    )
    def test_get_all_songs_schema(self, api_request_context: APIRequestContext):
        """Contract test — validates GraphQL response structure via JSON Schema."""
        query = """
            query GetAllSongs {
                songs {
                    id
                    title
                    album
                    author {
                        name
                        homeTown
                    }
                }
            }
        """

        with allure.step(f"Sending a GraphQL query for all songs to {GRAPHQL_URL}"):
            response = api_request_context.post(GRAPHQL_URL, data={'query': query})

        with allure.step("Verify response is OK and contains no errors"):
            expect(response).to_be_ok()
            response_data = response.json()
            assert 'errors' not in response_data, f"GraphQL returned errors: {response_data.get('errors')}"

        assert_valid_schema(response_data, "graphql_songs_response.json")

