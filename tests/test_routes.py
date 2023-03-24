import pytest

def test_get_all_books_with_no_records(client):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


def test_get_one_book(client, two_saved_books):
    # Act
    response = client.get("/books/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Purple Hibiscus",
        "description": "Family and becoming",
    }


def test_create_one_book(client):
    # Act
    response = client.post(
        "/books",
        json={"title": "Purple Hibiscus", "description": "Family and becoming"},
    )
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book Purple Hibiscus successfully added"


# When we have records, `read_all_books` returns a list containing a dictionary representing each `Book`
def test_get_all_books_with_two_records(client, two_saved_books):
    # Act
    response = client.get("/books")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Purple Hibiscus",
        "description": "Family and becoming",
    }
    assert response_body[1] == {
        "id": 2,
        "title": "Americanah",
        "description": "Immigration and becoming",
    }


# When we have records and a `title` query in the request arguments, `read_all_books` returns a list containing only the `Book`s which match the query
def test_get_all_books_with_title_query_matching_none(client, two_saved_books):
    # Act
    data = {"title": "Desert Book"}
    response = client.get("/books", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == []


# When we have records and a `title` query in the request arguments, `read_all_books` returns a list containing only the `Book`s which match the query
def test_get_all_books_with_title_query_matching_one(client, two_saved_books):
    # Act
    data = {"title": "Purple Hibiscus"}
    response = client.get("/books", query_string=data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0] == {
        "id": 1,
        "title": "Purple Hibiscus",
        "description": "Family and becoming",
    }


# When we call `read_one_book` with a numeric ID that doesn't have a record, we get the expected error message
def test_get_one_book_id_not_found(client, two_saved_books):
    # Act
    response = client.get("/books/3")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}


# When we call `read_one_book` with a non-numeric ID, we get the expected error message
def test_get_one_book_id_invalid(client, two_saved_books):
    # Act
    response = client.get("/books/cat")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": "Book cat invalid"}


def test_create_one_book_no_title(client):
    # Arrange
    test_data = {"description": "The Best!"}

    # Act & Assert
    with pytest.raises(KeyError, match='title'):
        response = client.post("/books", json=test_data)


def test_create_one_book_no_description(client):
    # Arrange
    test_data = {"title": "New Book"}

    # Act & Assert
    with pytest.raises(KeyError, match='description'):
        response = client.post("/books", json=test_data)


def test_create_one_book_with_extra_keys(client, two_saved_books):
    # Arrange
    test_data = {
        "extra": "some stuff",
        "title": "New Book",
        "description": "The Best!",
        "another": "last value"
    }

    # Act
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == "Book New Book successfully created"
