import pytest
from unittest.mock import MagicMock 
from flask import Flask
from datetime import datetime
from app.services.author_services import gettingall_author,db,search_author,add_authorid, Author , add_author_book , Book , filter_ondate ,add_author

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/new'  
    db.init_app(app)
    from app.routes.author_routes import author_bp
    app.register_blueprint(author_bp)
    return app

@pytest.fixture(scope='function')
def client(app):
    with app.app_context():  
        db.create_all()  
        yield app.test_client()  
        db.session.remove()  
        db.drop_all()  

@pytest.fixture
def mock_author():
    mock_author = MagicMock(spec=Author)
    
    mock_author.id = 1
    mock_author.name = "Test Author"
    mock_author.created_on = datetime.utcnow()
    mock_author.books = [
        MagicMock(spec=Book, title="Book 1", author_id=mock_author.id),
        MagicMock(spec=Book, title="Book 2", author_id=mock_author.id)
    ]
    mock_author.to_dict.return_value = {
        'id': mock_author.id,
        'name': mock_author.name,
        'created_on': mock_author.created_on.isoformat(),
        'books': [book.title for book in mock_author.books]
    }
    return mock_author

def test_get_author_found(client, mock_author):
    author_id = 1
    db.session.query = MagicMock(return_value=MagicMock(get=MagicMock(return_value=mock_author)))

    response = add_authorid(author_id)  

    assert response.status_code == 200

    assert response.json['id'] == mock_author.id
    assert response.json['name'] == mock_author.name
    assert response.json['created_on'] == mock_author.created_on.isoformat()



@pytest.fixture
def author_data():
    return {
        'name': 'Author Name',
        'books': [
            {'title': 'Book 1'},
            {'title': 'Book 2'}
        ]
    }

def test_add_author_with_books(client, author_data):

    result = add_author_book(author_data)  
    assert result[1] == 201  
    assert result[0].json['name'] == 'Author Name'  
    assert 'id' in result[0].json  
    
    

def test_filter_ondate_with_date(client):
    mock_author1 = MagicMock(spec=Author)
    mock_author1.to_dict.return_value = {'id': 1, 'name': 'Author 1', 'created_on': '2025-01-01', 'books': []}
    
    mock_author2 = MagicMock(spec=Author)
    mock_author2.to_dict.return_value = {'id': 2, 'name': 'Author 2', 'created_on': '2025-01-01', 'books': []}

    mock_query = MagicMock()
    mock_query.filter.return_value.all = MagicMock(return_value=[mock_author1, mock_author2])

    db.session.query = MagicMock(return_value=mock_query)

    result = filter_ondate('2025-01-01')

    assert result.status_code == 200  
    authors = result.get_json()  
    assert len(authors) == 2  

    assert authors[0]['name'] == 'Author 1'
    assert authors[1]['name'] == 'Author 2'



def test_search_author(client):
    mock_author1 = MagicMock(spec=Author)
    mock_author1.to_dict.return_value = {'id': 1, 'name': 'Test Author', 'created_on': '2025-01-01', 'books': []}
    
    mock_query = MagicMock()
    mock_query.filter.return_value.all = MagicMock(return_value=[mock_author1])

    db.session.query = MagicMock(return_value=mock_query)
    result = search_author("Test Author")
    
    assert result.status_code == 200  
    authors = result.get_json()  
    assert len(authors) == 1  


def test_pagination_add_author(client):
    mock_author1 = MagicMock(spec=Author)
    mock_author1.to_dict.return_value = {'id': 1, 'name': 'Author 1', 'created_on': '2025-01-01', 'books': []}
    
    mock_author2 = MagicMock(spec=Author)
    mock_author2.to_dict.return_value = {'id': 2, 'name': 'Author 2', 'created_on': '2025-01-01', 'books': []}

    mock_query = MagicMock()
    mock_query.paginate.return_value.items = [mock_author1, mock_author2]  
    
    db.session.query = MagicMock(return_value=mock_query)

    result = add_author(1, 2)

    assert result.status_code == 200  

    authors = result.get_json()['authors']  
    assert len(authors) == 2  


def test_getting_all_author(client):
    mock_author1 = MagicMock(spec=Author)
    mock_author1.to_dict.return_value = {'id': 1, 'name': 'Author 1', 'created_on': '2025-01-01', 'books': []}
    
    mock_author2 = MagicMock(spec=Author)
    mock_author2.to_dict.return_value = {'id': 2, 'name': 'Author 2', 'created_on': '2025-01-01', 'books': []}

    mock_pagination = MagicMock()
    mock_pagination.items = [mock_author1, mock_author2]
    
    mock_query = MagicMock()
    mock_query.filter.return_value = mock_query  
    mock_query.order_by.return_value = mock_query  
    mock_query.paginate.return_value = mock_pagination  

    db.session.query = MagicMock(return_value=mock_query)

    result = gettingall_author(1, 2, "", "", '2025-01-01')

    assert result.status_code == 200  

    authors = result.get_json()['authors']  
    assert len(authors) == 2

