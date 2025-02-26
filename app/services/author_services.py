import bcrypt
from datetime import datetime
from flask_jwt_extended import create_access_token
from app.models.author_models import db ,Author, Book
from sqlalchemy import  and_
from flask import jsonify


def add_authorid(author_id):
    author = db.session.query(Author).get(author_id)
    if author:
        return jsonify(author.to_dict())
    return jsonify({"message": "Author not found"}), 404

def delete(author_id):
    author = db.session.query(Author).get(author_id)
    if not author:
        return {"error": "not found"}, 404
    author.deleted = True 
    #db.session.delete(author)
    db.session.commit()
    return jsonify({'message': "deleted successfully"}), 200
def book_add(author_id,title):
    author = db.session.query(Author).get(author_id)
    if not author:
        return {"message": "Author not found"}, 404
    author.updated_on = datetime.utcnow()
    db.session.commit()
    new_book = Book(title=title, author_id=author.id)
    db.session.add(new_book)
    db.session.commit()
    return jsonify(new_book.to_dict()), 201

def add_author_book(data):
    new_author = Author(name=data['name'])
    db.session.add(new_author)
    db.session.commit()

    for book_data in data['books']:
        if not book_data.get('title'):
            return jsonify({'error': 'Each book must have a title'}), 400
        new_book = Book(title=book_data['title'], author_id=new_author.id)
        db.session.add(new_book)

    db.session.commit()
    return jsonify(new_author.to_dict()), 201

def filter_ondate(created_on):
    
    if created_on:
        
        created_on = datetime.strptime(created_on, '%Y-%m-%d').date()

        authors = db.session.query(Author).filter(db.func.date(Author.created_on) == created_on).all()
    else:
        authors = db.session.query(Author).all()

    return jsonify([author.to_dict() for author in authors])

def sorted_author():
    authors = db.session.query(Author).order_by(Author.created_on.desc()).all()
    return jsonify([author.to_dict() for author in authors])
def search_author(search_term):
    if not search_term:
        return jsonify({"message": "Search term is required."}), 400

    authors = db.session.query(Author).filter(Author.name.like(f'%{search_term}%')).all()

    return jsonify([author.to_dict() for author in authors])
def add_author(page , per_page):
    authors = db.session.query(Author).paginate(page=page, per_page=per_page, error_out=False)  
    
    author_list = [author.to_dict() for author in authors.items]
    
    return jsonify({
        'authors': author_list
    })

def gettingall_author(page,per_page,search_term,sort_by,created_on):
    authors_query = db.session.query(Author).filter(Author.deleted == False)  

    if created_on:
        created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
        authors_query = authors_query.filter(db.func.date(Author.created_on) == created_on)

    if search_term:
        authors_query = authors_query.filter(Author.name.like(f'%{search_term}%'))

    if sort_by == 'desc':
        authors_query = authors_query.order_by(Author.name.desc())
    else:
        authors_query = authors_query.order_by(Author.name.asc())

    authors_paginated = authors_query.paginate(page=page, per_page=per_page, error_out=False)

    author_list = [author.to_dict() for author in authors_paginated.items]

    return jsonify({
        'authors': author_list
            })
def gettindeleted_author(page,per_page,search_term,sort_by,created_on):
    authors_query = db.session.query(Author).filter(Author.deleted == True)  

    if created_on:
        created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
        authors_query = authors_query.filter(db.func.date(Author.created_on) == created_on)

    if search_term:
        authors_query = authors_query.filter(Author.name.like(f'%{search_term}%'))

    if sort_by == 'desc':
        authors_query = authors_query.order_by(Author.name.desc())
    else:
        authors_query = authors_query.order_by(Author.name.asc())

    authors_paginated = authors_query.paginate(page=page, per_page=per_page, error_out=False)

    author_list = [author.to_dict() for author in authors_paginated.items]

    return jsonify({
        'authors': author_list
            })
def autor_bookjoin(page,per_page,search_term,sort_by,created_on,book_title):
    authors_query = db.session.query(Author,Book).join(Book).filter(Author.deleted == False)
    
    if created_on:
        created_on = datetime.strptime(created_on, '%Y-%m-%d').date()
        authors_query = authors_query.filter(db.func.date(Author.created_on) == created_on)
    
    if search_term or book_title:
        authors_query = authors_query.filter(
         and_(Author.name.like(f'%{search_term}%'),
            Book.title.like(f'%{book_title}%')
            ))

    if sort_by == 'desc':
        authors_query = authors_query.order_by(Author.name.desc())
    else:
        authors_query = authors_query.order_by(Author.name.asc())

    authors_paginated = authors_query.paginate(page=page, per_page=per_page, error_out=False)
    
    result = []
    for author, book in authors_paginated:
     rs = {
        "author_name": author.name,
        "author_id":author.id,
        "book_title": book.title  
        }
     result.append(rs)  

    return jsonify(result)