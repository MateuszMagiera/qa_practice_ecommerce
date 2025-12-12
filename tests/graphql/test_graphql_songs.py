import allure
import pytest
from playwright.sync_api import APIRequestContext, expect

GRAPHQL_URL = "http://localhost:5000/graphql"

@allure.feature("GraphQL API")
class TestGraphQLSongs:
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
