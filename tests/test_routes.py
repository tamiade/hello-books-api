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
        "description": "Family and becoming"
    }

def test_create_one_book(client):
    # Act
    response = client.post("/books", json={
        "title": "Purple Hibiscus",
        "description": "Family and becoming"
        })
    response_body = response.get_json()
    
    # Assert
    assert response.status_code == 201
    assert response_body == "Book Purple Hibiscus successfully added"