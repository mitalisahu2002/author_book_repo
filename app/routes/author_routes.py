from flask import Flask,request
from flask_jwt_extended import jwt_required
from app.services.author_services import autor_bookjoin ,gettindeleted_author,gettingall_author, search_author ,sorted_author,add_author , add_authorid , delete , book_add , add_author_book , filter_ondate
from app.utils.utils import admin_required
from flask import Blueprint

author_bp = Blueprint('author', __name__)

@author_bp.route('/authors', methods=['GET'])
def get_authors():
    page = request.args.get('page', 1, type=int)  
    per_page = request.args.get('per_page', 10, type=int)  

    return add_author(page,per_page)

@author_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    return add_authorid(author_id)

@author_bp.route('/authors', methods=['POST'])
@jwt_required()
@admin_required
def add_author_with_books():
    data = request.get_json()
    return add_author_book(data)
    
@author_bp.route('/authors/<int:author_id>/books', methods=['PUT'])
@jwt_required()
def add_book(author_id):
    data = request.get_json()
    title = data['title']
    return book_add(author_id,title)

@author_bp.route('/authors/<int:author_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_author(author_id):
    return delete(author_id)

@author_bp.route('/authors_ondate', methods=['GET'])
def get_authors_ondate():
    created_on = request.args.get('created_on')
    return filter_ondate(created_on)

@author_bp.route('/authors_sorted', methods=['GET'])
def get_sorted_authors():
    return sorted_author()

@author_bp.route('/authors_search', methods=['GET'])
def search_authors():
    search_term = request.args.get('search_term')
    return search_author(search_term)

@author_bp.route('/authorsall', methods=['GET'])
def allauthorsapi():
    search_term = request.args.get('search_term','')
    created_on = request.args.get('created_on','')
    sort_by = request.args.get('sort_by', 'desc') 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    return gettingall_author(page,per_page,search_term,sort_by,created_on)
@author_bp.route('/authorsdeleted', methods=['GET'])
def deletedauthor():
    search_term = request.args.get('search_term','')
    created_on = request.args.get('created_on','')
    sort_by = request.args.get('sort_by', 'desc') 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)
    return gettindeleted_author(page,per_page,search_term,sort_by,created_on)

@author_bp.route('/author_join',methods=['GET'])
def join_author():
    search_term = request.args.get('search_term','')
    created_on = request.args.get('created_on','')
    book_title = request.args.get('book_title','')
    sort_by = request.args.get('sort_by', 'desc') 
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    return autor_bookjoin(page,per_page,search_term,sort_by,created_on,book_title)