from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.models.user_models import db
from app.routes.user_routes import user_bp
from app.routes.author_routes import author_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flask-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/token'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()

app.register_blueprint(user_bp, url_prefix='/user')  
app.register_blueprint(author_bp, url_prefix='/author')


if __name__ == '__main__':
    app.run(debug=True)
