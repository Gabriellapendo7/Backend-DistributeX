from flask import request, jsonify, url_for, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Admin, Manufacturer, Client
from utils.email import send_reset_email
from utils.security import generate_reset_token, verify_reset_token
from . import auth_bp

@auth_bp.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.json
    admin = Admin.query.filter_by(Username=data['username']).first()
    if admin and check_password_hash(admin.Password, data['password']):
        access_token = create_access_token(identity={'role': 'admin', 'id': admin.ID})
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

@auth_bp.route('/client/login', methods=['POST'])
def client_login():
    data = request.json
    client = Client.query.filter_by(Username=data['username']).first()
    if client and check_password_hash(client.Password, data['password']):
        access_token = create_access_token(identity={'role': 'client', 'id': client.ID})
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

@auth_bp.route('/manufacturer/login', methods=['POST'])
def manufacturer_login():
    data = request.json
    manufacturer = Manufacturer.query.filter_by(Username=data['username']).first()
    if manufacturer and check_password_hash(manufacturer.Password, data['password']):
        access_token = create_access_token(identity={'role': 'manufacturer', 'id': manufacturer.ID})
        return jsonify(access_token=access_token), 200
    return jsonify({'msg': 'Bad username or password'}), 401

@auth_bp.route('/reset_password', methods=['POST'])
def reset_request():
    data = request.json
    user = None
    if 'role' in data:
        if data['role'] == 'admin':
            user = Admin.query.filter_by(Email=data['email']).first()
        elif data['role'] == 'manufacturer':
            user = Manufacturer.query.filter_by(Email=data['email']).first()
        elif data['role'] == 'client':
            user = Client.query.filter_by(Email=data['email']).first()
        print(user.ID)
    if user:
        token = generate_reset_token(user.ID)
        send_reset_email(user, token)
        return jsonify({'msg': 'Password reset email sent'}), 200

    return jsonify({'msg': 'User not found'}), 404

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if request.method == 'GET':
        user_id = verify_reset_token(token)
        if not user_id:
            return jsonify({'msg': 'Invalid or expired token'}), 400
        return jsonify({'msg': 'Password reset successful'}), 200

    data = request.json
    user_id = verify_reset_token(token, expiration=10)
    if not user_id:
        return jsonify({'msg': 'Invalid or expired token'}), 400

    user = Admin.query.get(user_id) or Manufacturer.query.get(user_id) or Client.query.get(user_id)
    if user:
        user.Password = generate_password_hash(data['password'])
        db.session.commit()
        return jsonify({'msg': 'Password reset successful'}), 200

    return jsonify({'msg': 'User not found'}), 404

@auth_bp.route('/admin/register', methods=['POST'])
def register_admin():
    data = request.json

    if Admin.query.filter_by(Username=data['username']).first():
        return jsonify({'msg': 'Username already exists'}), 400
    if Admin.query.filter_by(Email=data['email']).first():
        return jsonify({'msg': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_admin = Admin(
        Username=data['username'],
        Email=data['email'],
        Password=hashed_password
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({'msg': 'Admin registered successfully'}), 201

@auth_bp.route('/manufacturer/register', methods=['POST'])
def register_manufacturer():
    data = request.json
    if Manufacturer.query.filter_by(Username=data['username']).first():
        return jsonify({'msg': 'Username already exists'}), 400
    if Manufacturer.query.filter_by(Email=data['email']).first():
        return jsonify({'msg': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_manufacturer = Manufacturer(
        Username=data['username'],
        Email=data['email'],
        Password=hashed_password,
        Companyname=data.get('companyname', ''),
        Contactinfo=data.get('contactinfo', '')
    )
    db.session.add(new_manufacturer)
    db.session.commit()
    return jsonify({'msg': 'Manufacturer registered successfully'}), 201

@auth_bp.route('/client/register', methods=['POST'])
def register_client():
    data = request.json
    if Client.query.filter_by(Username=data['username']).first():
        return jsonify({'msg': 'Username already exists'}), 400
    if Client.query.filter_by(Email=data['email']).first():
        return jsonify({'msg': 'Email already exists'}), 400

    hashed_password = generate_password_hash(data['password'])
    new_client = Client(
        Username=data['username'],
        Email=data['email'],
        Password=hashed_password,
        Shipping_address=data.get('shipping_address', '')
    )
    db.session.add(new_client)
    db.session.commit()
    return jsonify({'msg': 'Client registered successfully'}), 201