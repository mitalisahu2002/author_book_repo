import bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token
#from models.user_models import db,  User
from app.models.user_models import db , User
#from app import db
from flask import jsonify

def register_user(username, password, role):
    if role not in ['admin', 'user']:
        return {"message": "role can be user or admin only"}, 400

    existing_user = db.session.query(User).filter_by(username=username).first()
    if existing_user:
        return {"message": "username already taken"}, 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(username=username, password=hashed_password.decode('utf-8'), role=role)
    db.session.add(new_user)
    db.session.commit()

    return {"message": "user created successfully"}, 201

def login_user(username, password):
    user = db.session.query(User).filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        expires = timedelta(seconds=3000)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)

        return {"access_token": access_token, "role": user.role}, 200

    return {"message": "invalid credentials"}, 401
