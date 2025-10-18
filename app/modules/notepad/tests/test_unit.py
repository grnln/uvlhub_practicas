import pytest

from app import db
from app.modules.auth.models import User
from app.modules.conftest import login, logout

@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    """
    with test_client.application.app_context():
        user_test = User(email = "user@example.com", password = "test1234")
        db.session.add(user_test)
        db.session.commit()
    yield test_client

def test_sample_assertion(test_client):
    """
    Sample test to verify that the test framework and environment are working correctly.
    It does not communicate with the Flask application; it only performs a simple assertion to
    confirm that the tests in this module can be executed.
    """
    greeting = "Hello, World!"
    assert greeting == "Hello, World!", "The greeting does not coincide with 'Hello, World!'"

def test_list_empty_notepad_get(test_client):
    """
    Tests access to the empty notepad list via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"You have no notepads." in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_get_notepad_create(test_client):
    """
    Tests accessibility of the notepad creation screen via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get("/notepad/create")
    assert response.status_code == 200, "The notepad creation page could not be accessed."
    assert b"Title" in response.data, "The expected content is not present on the page."
    assert b"Body" in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_notepad_create(test_client):
    """
    Tests the notepad creation functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": "sample title", "body": "sample body"})
    assert response.status_code == 302, "Could not create a sample notepad."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"sample title" in response.data, "The expected content is not present on the page."
    assert b"sample body" in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_notepad_create_invalid(test_client):
    """
    Tests failure of the notepad creation functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": None, "body": None})
    assert response.status_code == 200, "Creation functionality did not fail when fields are set to invalid values."
    assert b"Title" in response.data, "The expected content is not present on the page."
    assert b"Body" in response.data, "The expected content is not present on the page."
    
    logout(test_client)

def test_get_notepad_edit(test_client):
    """
    Tests accessibility of the notepad edition functionality via GET request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": "sample title", "body": "sample body"})
    assert response.status_code == 302, "Could not create a sample notepad."

    response = test_client.get("/notepad/edit/1")
    assert response.status_code == 200, "The notepad edition page could not be accessed."
    assert b"Title" in response.data, "The expected content is not present on the page."
    assert b"Body" in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_notepad_edit(test_client):
    """
    Tests the notepad edition functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": "sample title", "body": "sample body"})
    assert response.status_code == 302, "Could not create a sample notepad."

    response = test_client.post("/notepad/edit/1", data = {"title": "sample title edited", "body": "sample body edited"})
    assert response.status_code == 302, "Could not edit sample notepad."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"sample title edited" in response.data, "The expected content is not present on the page."
    assert b"sample body edited" in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_notepad_edit_invalid(test_client):
    """
    Tests failure of the notepad edition functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": "sample title", "body": "sample body"})
    assert response.status_code == 302, "Could not create a sample notepad."

    response = test_client.post("/notepad/edit/1", data = {"title": None, "body": None})
    assert response.status_code == 302, "Edition did not fail when fields are set to invalid values."

    response = test_client.get("/notepad")
    assert response.status_code == 200, "The notepad page could not be accessed."
    assert b"sample title" in response.data, "The expected content is not present on the page."
    assert b"sample body" in response.data, "The expected content is not present on the page."

    logout(test_client)

def test_notepad_delete(test_client):
    """
    Tests the notepad deletion functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/create", data = {"title": "sample title", "body": "sample body"})
    assert response.status_code == 302, "Could not create a sample notepad."

    response = test_client.post("/notepad/delete/1")
    assert response.status_code == 302, "Could not delete sample notepad."

    logout(test_client)

def test_notepad_delete_none(test_client):
    """
    Tests failure of the notepad deletion functionality via POST request.
    """
    login_response = login(test_client, "user@example.com", "test1234")
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.post("/notepad/delete/1")
    assert response.status_code == 404, "Deletion did not fail when no notepads are available."

    logout(test_client)
