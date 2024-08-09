from flask import Blueprint, make_response, request, jsonify
from models import Manufacturer
from config import db, bcrypt 
from helpers import commit_session  

manufacturer_auth_bp = Blueprint('manufacturer_auth', __name__)

@manufacturer_auth_bp.route('/manufacturers', methods=['POST'])
def create_manufacturer():
    manufacturer_data = request.get_json()
    try:
        hashed_password = bcrypt.generate_password_hash(manufacturer_data["password"]).decode('utf-8')
        new_manufacturer = Manufacturer(
            Username=manufacturer_data["username"],
            Email=manufacturer_data["email"],
            Companyname=manufacturer_data.get("companyname", ""),
            Contactinfo=manufacturer_data.get("contactinfo", ""),
            Password=hashed_password
        )
        db.session.add(new_manufacturer)
        commit_session(db.session)

        return make_response({"message": "Manufacturer registered successfully"}, 201)
    except Exception as error:
        db.session.rollback()
        return make_response({"error": "Manufacturer registration failed: " + str(error)}, 500)

@manufacturer_auth_bp.route('/manufacturers/login', methods=['POST'])
def login_manufacturer():
    data = request.get_json()

    if not all(key in data for key in ("email", "password")):
        return make_response({"error": "Email and password are required"}, 400)

    email = data["email"]
    password = data["password"]

    # Fetch the manufacturer from the database using the provided email
    manufacturer = Manufacturer.query.filter_by(Email=email).first()

    if manufacturer is None:
        return make_response({"error": "Email not found"}, 404)

    # Check if the provided password matches the stored password
    if bcrypt.check_password_hash(manufacturer.Password, password):
        # Create the response object and set cookies with the manufacturer ID and username
        response = make_response(jsonify({
            "message": "Login successful",
            "manufacturer_id": manufacturer.ID,
            "username": manufacturer.Username  
        }), 200)
        
        # Set cookies with the manufacturer ID and username
        response.set_cookie('manufacturer_id', str(manufacturer.ID), httponly=True)
        response.set_cookie('manufacturer_username', manufacturer.Username, httponly=True)
        
        return response
    else:
        return make_response({"error": "Invalid credentials"}, 401)
