from flask import Flask,request
import logging
from flask_jwt_extended import jwt_required
from app.services.user_service import register_user, login_user 
from app.utils.utils import admin_required
from flask import Blueprint, current_app

user_bp = Blueprint('user', __name__)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"), 
        logging.StreamHandler()  
    ]
)


@user_bp.route("/registration", methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    role = data['role']
    
    current_app.logger.info(f"User registration attempt: {username}, Role: {role}")

    return register_user(username, password, role)

@user_bp.route("/login", methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    current_app.logger.info(f"User login attempt: {username}")
    
    return login_user(username, password)
