from flask import Blueprint, request, jsonify
from models import Manufacturer
from config import db, bcrypt
from helpers import validate_not_blank
from flask_bcrypt import generate_password_hash, check_password_hash

manufacturer_bp = Blueprint("manufacturer_bp", __name__)

@manufacturer_bp.route("/", methods=["POST"]) 
def signup():
    data = request.get_json()
    try:
        username = validate_not_blank(data["username"], "username")
        password = validate_not_blank(data["password"], "password")
        company_name = validate_not_blank(data["company_name"], "company_name")
        contact_info = validate_not_blank(data["contact_info"], "contact_info")

        existing_manufacturer = Manufacturer.query.filter_by(username=username).first()
        if existing_manufacturer:
            return jsonify({"error": "Username already exists"}), 400

        new_manufacturer = Manufacturer(
            username=username,
            company_name=company_name,
            company_info=contact_info
        )
        new_manufacturer.password = generate_password_hash(password)

        db.session.add(new_manufacturer)
        db.session.commit()

        return jsonify({"message": "Signup successful!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@manufacturer_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data received"}), 400
        
        username = validate_not_blank(data.get("username"), "username")
        password = validate_not_blank(data.get("password"), "password")

        manufacturer = Manufacturer.query.filter_by(username=username).first()
        if manufacturer and check_password_hash(manufacturer.password, password):
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 400
