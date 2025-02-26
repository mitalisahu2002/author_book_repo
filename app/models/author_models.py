from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)  
    updated_on = db.Column(db.DateTime, nullable=True)  
    deleted = db.Column(db.Boolean,default=False)
    books = db.relationship('Book', backref='author', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_on': self.created_on.isoformat() if self.created_on else None,  
            'books': [book.to_dict() for book in self.books]
        }


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id
        }
