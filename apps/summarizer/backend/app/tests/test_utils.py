"""Unitary tests of routes"""
from fastapi.testclient import TestClient

from backend.app.api.main import app


client = TestClient(app)


def test_insert_article_valid_url():
    """
    Test inserting an article with a valid Wikipedia URL.

    This test checks if the endpoint correctly processes a valid Wikipedia URL
    and returns a response containing an ID and information message.

    Asserts:
        - The status code of the response is 200.
        - The response JSON contains the keys 'id' and 'info'.
    """
    response = client.post("/summarizer/insert_article", json={
        "wikipedia_url": "https://en.wikipedia.org/wiki/Nikola_Tesla",
        "number_of_words": 1000
    })
    assert response.status_code == 200
    assert "id" in response.json()
    assert "info" in response.json()


def test_insert_article_invalid_url():
    """
    Test inserting an article with an invalid Wikipedia URL.

    This test checks if the endpoint correctly identifies an invalid Wikipedia
    URL and returns a 400 status code with an appropriate error message.

    Asserts:
        - The status code of the response is 400.
        - The response JSON contains the expected error message.
    """
    response = client.post("/summarizer/insert_article", json={
        "wikipedia_url": "https://invalid.url/wiki/Nikola_Tesla",
        "number_of_words": 1000
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Error: Invalid Wikipedia URL format"}


def test_get_summary_not_found():
    """
    Test retrieving a summary with a non-existent UUID.

    This test checks if the endpoint correctly handles a request for a summary
    that does not exist and returns a 404 status code with an appropriate
    error message.

    Asserts:
        - The status code of the response is 404.
        - The response JSON contains the expected error message.
    """
    response = client.get("/summarizer/get_summary/invalid-uuid")
    assert response.status_code == 404
    assert response.json() == {"detail": "Summary not found"}
