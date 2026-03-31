import os

# Base URLs — loaded from environment variables with sensible defaults for local development.
BASE_URL = os.environ.get("BASE_URL", "https://qa-practice.netlify.app")
API_BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8887")
GRAPHQL_URL = os.environ.get("GRAPHQL_URL", "http://127.0.0.1:5000/graphql")
