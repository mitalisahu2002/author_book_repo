import pytest
from flask import Flask, request
from run import app  

def add_author(page, per_page):
    return {"page": page, "per_page": per_page, "authors": []}  

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_authors(client):
    response = client.get('author/authors')
    assert response.status_code == 200
    data = response.get_json()


# @pytest.fixture
# def mock_author_data():
#     return Author(id=1, name="Test Author", updated_on=datetime.utcnow())

# @pytest.fixture
# def mock_db_session(mock_author_data):
#     db.session.query = MagicMock()
#     db.session.query(Author).get = MagicMock(return_value=mock_author_data)
#     db.session.add = MagicMock()
#     db.session.commit = MagicMock()
#     return db.session
# def test_book_add_success(mock_author_data, mock_db_session):
#     author_id = mock_author_data.id
#     title = "New Book"

#     with patch('app.services.author_services.jsonify') as mock_jsonify:
#         mock_jsonify.return_value = {'title': title, 'author_id': author_id}

#         response_body, status_code = book_add(author_id, title)

#     assert status_code == 201
#     assert response_body['title'] == title
#     assert response_body['author_id'] == author_id

