from flask import Blueprint, jsonify
from flask_restful import Api, Resource, reqparse
from models import Manufacturer, db

manufacturer_bp = Blueprint('manufacturer', __name__)
api = Api(manufacturer_bp)

class ManufacturerResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('Username', type=str, required=True, help='Username cannot be blank')
        self.parser.add_argument('Email', type=str, required=True, help='Email cannot be blank')
        self.parser.add_argument('Password', type=str, required=True, help='Password cannot be blank')
        self.parser.add_argument('Companyname', type=str, required=True, help='Company name cannot be blank')
        self.parser.add_argument('Contactinfo', type=str, required=True, help='Contact info cannot be blank')

    def post(self):
        args = self.parser.parse_args()
        manufacturer = Manufacturer(
            Username=args['Username'],
            Email=args['Email'],
            Password=args['Password'],
            Companyname=args['Companyname'],
            Contactinfo=args['Contactinfo']
        )
        db.session.add(manufacturer)
        db.session.commit()
        return {'message': 'Manufacturer created successfully.'}, 201

    def get(self, manufacturer_id):
        manufacturer = Manufacturer.query.get_or_404(manufacturer_id)
        return {
            'ID': manufacturer.ID,
            'Username': manufacturer.Username,
            'Email': manufacturer.Email,
            'Companyname': manufacturer.Companyname,
            'Contactinfo': manufacturer.Contactinfo
        }


api.add_resource(ManufacturerResource, '/manufacturer', '/manufacturer/<int:manufacturer_id>')
