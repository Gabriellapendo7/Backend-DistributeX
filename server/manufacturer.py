from flask import Blueprint, request, jsonify
from app import db
from models import Manufacturer

manufacturer_bp = Blueprint('manufacturer_bp', __name__)

@manufacturer_bp.route('/', methods=['GET'])
def get_manufacturers():
    manufacturers = Manufacturer.query.all()
    return jsonify([manufacturer.to_dict() for manufacturer in manufacturers])

@manufacturer_bp.route('/<int:id>', methods=['GET'])
def get_manufacturer(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    return jsonify(manufacturer.to_dict())

@manufacturer_bp.route('/', methods=['POST'])
def create_manufacturer():
    data = request.get_json()
    new_manufacturer = Manufacturer(
        Username=data['Username'],
        Password=data['Password'],
        Companyname=data['Companyname'],
        Contactinfo=data['Contactinfo']
    )
    db.session.add(new_manufacturer)
    db.session.commit()
    return jsonify(new_manufacturer.to_dict()), 201

@manufacturer_bp.route('/<int:id>', methods=['PUT'])
def update_manufacturer(id):
    data = request.get_json()
    manufacturer = Manufacturer.query.get_or_404(id)
    manufacturer.Username = data['Username']
    manufacturer.Password = data['Password']
    manufacturer.Companyname = data['Companyname']
    manufacturer.Contactinfo = data['Contactinfo']
    db.session.commit()
    return jsonify(manufacturer.to_dict())

@manufacturer_bp.route('/<int:id>', methods=['DELETE'])
def delete_manufacturer(id):
    manufacturer = Manufacturer.query.get_or_404(id)
    db.session.delete(manufacturer)
    db.session.commit()
    return '', 204
