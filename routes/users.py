from flask import Blueprint, make_response, request
from models import User
from config import db
from helpers import commit_session

users_bp = Blueprint('users', __name__)

@users_bp.route('', methods=['GET'])  # Changed route to match '/api/users'
def get_users():
    users = User.query.all()
    return make_response([user.to_dict() for user in users], 200)

@users_bp.route('', methods=['POST'])  # Changed route to match '/api/users'
def create_user():
    user_data = request.get_json()
    try:
        new_user = User(
            username=user_data["username"],
            email=user_data["email"],
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", ""),
            shipping_address=user_data.get("shipping_address", ""),
            shipping_city=user_data.get("shipping_city", ""),
            shipping_state=user_data.get("shipping_state", ""),
            shipping_zip=user_data.get("shipping_zip", ""),
        )
        new_user.password = user_data["password"]
        db.session.add(new_user)
        commit_session(db.session)
        return make_response({"message": "User created successfully"}, 201)
    except Exception as error:
        db.session.rollback()
        return make_response({"error": "User creation failed: " + str(error)}, 500)

@users_bp.route('/delete', methods=['DELETE'])  # Adjusted route
def delete_user():
    data = request.get_json()
    if not all(key in data for key in ("username", "password")):
        return make_response({"error": "Username and password are required"}, 400)

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()
    if user and user.authenticate(password):
        db.session.delete(user)
        commit_session(db.session)
        return make_response({"message": "User deleted successfully"}, 200)
    else:
        return make_response({"error": "Invalid credentials"}, 401)

@users_bp.route('/update', methods=['PATCH'])  # Adjusted route
def update_user_password():
    data = request.get_json()
    if not all(key in data for key in ("username", "password", "newPassword")):
        return make_response({"error": "Required fields are missing"}, 400)

    username = data["username"]
    password = data["password"]
    new_password = data["newPassword"]

    user = User.query.filter_by(username=username).first()
    if user and user.authenticate(password):
        user.password = new_password
        commit_session(db.session)
        return make_response({"message": "Password updated successfully"}, 200)
    else:
        return make_response({"error": "Invalid credentials"}, 401)
