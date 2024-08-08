#app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '2a471f3357ce40230b9f670bd05ec405384d502a70bbc3bf98d4509f4620e96a'

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Models start here
class Admin(db.Model):
    __tablename__ = 'admin'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Companyname = db.Column(db.String(128))
    Contactinfo = db.Column(db.String(128))



class Client(db.Model):
    __tablename__ = 'client'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Shipping_address = db.Column(db.String(128))



class Category(db.Model):
    __tablename__ = 'category'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)



class Product(db.Model):
    __tablename__ = 'product'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Productname = db.Column(db.String(255), nullable=False)
    productdescription = db.Column(db.String(255), nullable=True)
    description = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.String(255), nullable=True)
    price = db.Column(db.BigInteger, nullable=False)
    CategoryID = db.Column(db.BigInteger, db.ForeignKey('category.ID'), nullable=False)
    manufacturerID = db.Column(db.BigInteger, db.ForeignKey('manufacturer.ID'), nullable=False)
    ImageURL = db.Column(db.String(255), nullable=True)
    supply_id = db.Column(db.BigInteger, db.ForeignKey('supply.ID'), nullable=True)



class Order(db.Model):
    __tablename__ = 'order'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClientID = db.Column(db.BigInteger, db.ForeignKey('client.ID'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    total = db.Column(db.BigInteger, nullable=False)



class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.BigInteger, db.ForeignKey('order.ID'), nullable=False)
    ProductID = db.Column(db.BigInteger, db.ForeignKey('product.ID'), nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)
    price = db.Column(db.BigInteger, nullable=False)



class Receipt(db.Model):
    __tablename__ = 'receipt'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.BigInteger, db.ForeignKey('order.ID'), nullable=False)
    ClientID = db.Column(db.BigInteger, db.ForeignKey('client.ID'), nullable=False)
    ReceiptDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Total = db.Column(db.BigInteger, nullable=False)
    Payment = db.Column(db.BigInteger, nullable=False)



class Cart(db.Model):
    __tablename__ = 'cart'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClientID = db.Column(db.BigInteger, db.ForeignKey('client.ID'), nullable=False)
    CreateAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)



class CartItem(db.Model):
    __tablename__ = 'cartitem'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CartID = db.Column(db.BigInteger, db.ForeignKey('cart.ID'), nullable=False)
    ProductID = db.Column(db.BigInteger, db.ForeignKey('product.ID'), nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)



class Supply(db.Model):
    __tablename__ = 'supply'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdminID = db.Column(db.BigInteger, db.ForeignKey('admin.ID'), nullable=False)
    ManufacturerID = db.Column(db.BigInteger, db.ForeignKey('manufacturer.ID'), nullable=False)
    supply_name = db.Column(db.String(255), nullable=False)
    quantity_ordered = db.Column(db.BigInteger, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ProductID = db.Column(db.BigInteger, db.ForeignKey('product.ID'), nullable=False)



class SupplyOrder(db.Model):
    __tablename__ = 'supply_order'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductID = db.Column(db.BigInteger, db.ForeignKey('product.ID'), nullable=False)
    orderDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)
    total_price = db.Column(db.BigInteger, nullable=False)



class Sales(db.Model):
    __tablename__ = 'sales'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ReceiptID = db.Column(db.BigInteger, db.ForeignKey('receipt.ID'), nullable=False)
    AdminID = db.Column(db.BigInteger, db.ForeignKey('admin.ID'), nullable=False)
    TotalAmount = db.Column(db.BigInteger, nullable=False)
    ClientID = db.Column(db.BigInteger, db.ForeignKey('client.ID'), nullable=False)
    Sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

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
# @jwt_required()
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
# @jwt_required()
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
# @jwt_required()
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
for cls in [Admin, Sales, Product, Order, SupplyOrder]:
    cls.to_dict = to_dict

if __name__ == '__main__':
    app.run(debug=True)
