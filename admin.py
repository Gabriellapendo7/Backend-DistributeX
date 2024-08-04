from flask import Blueprint, request, jsonify
from app import db
from models import Admin

admin_bp = Blueprint('admin_bp', __name__)

@admin_bp.route('/', methods=['GET'])
def get_admins():
    admins = Admin.query.all()
    return jsonify([admin.to_dict() for admin in admins])

@admin_bp.route('/<int:id>', methods=['GET'])
def get_admin(id):
    admin = Admin.query.get_or_404(id)
    return jsonify(admin.to_dict())

@admin_bp.route('/', methods=['POST'])
def create_admin():
    data = request.get_json()
    new_admin = Admin(
        Username=data['Username'],
        Email=data['Email'],
        Password=data['Password']
    )
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(new_admin.to_dict()), 201

@admin_bp.route('/<int:id>', methods=['PUT'])
def update_admin(id):
    data = request.get_json()
    admin = Admin.query.get_or_404(id)
    admin.Username = data['Username']
    admin.Email = data['Email']
    admin.Password = data['Password']
    db.session.commit()
    return jsonify(admin.to_dict())

@admin_bp.route('/<int:id>', methods=['DELETE'])
def delete_admin(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    return '', 204
