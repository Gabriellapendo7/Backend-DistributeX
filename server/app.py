from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '2a471f3357ce40230b9f670bd05ec405384d502a70bbc3bf98d4509f4620e96a'

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models start here
class Admin(db.Model):
    __tablename__ = 'admins'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Sales(db.Model):
    __tablename__ = 'sales'
    sales_id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    sale_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    order_item_id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
# Models end here    

# Routes start here
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_admin = Admin(username=data['username'], password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify(message="Admin registered"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    admin = Admin.query.filter_by(username=data['username']).first()
    if admin and bcrypt.check_password_hash(admin.password, data['password']):
        access_token = create_access_token(identity={'admin_id': admin.admin_id})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401

@app.route('/sales', methods=['GET', 'POST'])
@jwt_required()
def manage_sales():
    if request.method == 'POST':
        data = request.get_json()
        current_user = get_jwt_identity()
        new_sale = Sales(
            receipt_id=data['receipt_id'],
            admin_id=current_user['admin_id'],
            total_amount=data['total_amount'],
            client_id=data['client_id'],
            sale_date=datetime.utcnow()
        )
        db.session.add(new_sale)
        db.session.commit()
        return jsonify(message="Sale recorded"), 201
    elif request.method == 'GET':
        sales = Sales.query.all()
        return jsonify([sale.to_dict() for sale in sales]), 200

@app.route('/products', methods=['GET', 'POST'])
@jwt_required()
def manage_products():
    if request.method == 'POST':
        data = request.get_json()
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            price=data['price'],
            stock=data['stock']
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(message="Product added"), 201
    elif request.method == 'GET':
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200

@app.route('/orders', methods=['GET', 'POST'])
@jwt_required()
def manage_orders():
    if request.method == 'POST':
        data = request.get_json()
        new_order = Order(
            client_id=data['client_id'],
            order_date=datetime.utcnow(),
            status=data['status'],
            total_amount=data['total_amount']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(message="Order placed"), 201
    elif request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
# Routes end here    

# changes SQLAlchemy objects to dictionaries
def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Adding the to_dict method to each model
for cls in [Admin, Sales, Product, Order, OrderItem]:
    cls.to_dict = to_dict

if __name__ == '__main__':
    app.run(debug=True)
