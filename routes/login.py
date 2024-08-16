from flask import Blueprint, make_response, request
from models import User

login_bp = Blueprint('login', __name__)



@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not all(key in data for key in ("username", "password")):
        return make_response({"error": "Username and password are required"}, 400)

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user and user.authenticate(password):
        return make_response({"message": "Login successful", "user_id": user.id}, 200)
    else:
        return make_response({"error": "Invalid credentials"}, 401)
