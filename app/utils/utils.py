from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import jsonify
from app.models.user_models import db, User

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kargs):
        current_user_id = get_jwt_identity()
        user = db.session.query(User).get(current_user_id)

        if not user or user.role != 'admin':
            return jsonify({"message": "Access denied. Admins only."}), 403
        return f(*args, **kargs)

    return decorated_function
