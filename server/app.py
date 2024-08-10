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
    role = data['role']

    if role == 'Admin':
        new_user = Admin(
            Username=data['username'], 
            Email=data['email'],       
            Password=hashed_password
        )
    elif role == 'Client':
        new_user = Client(
            Username=data['username'],
            Email=data['email'],
            Password=hashed_password,
            Shipping_address=data.get('shipping_address', '')  # Default to empty string if not provided
        )
    elif role == 'Manufacturer':
        new_user = Manufacturer(
            Username=data['username'],
            Email=data['email'],
            Password=hashed_password,
            Companyname=data.get('company_name', ''),  # Default to empty string if not provided
            Contactinfo=data.get('contact_info', '')    # Default to empty string if not provided
        )
    else:
        return jsonify(message="Invalid role"), 400

    db.session.add(new_user)
    db.session.commit()
    return jsonify(message=f"{role} registered successfully"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    admin = Admin.query.filter_by(Username=data['Username']).first()  # Use 'Username'
    if admin and bcrypt.check_password_hash(admin.Password, data['Password']):  # Use 'Password'
        access_token = create_access_token(identity={'admin_id': admin.ID})
        return jsonify(access_token=access_token), 200
    return jsonify(message="Invalid credentials"), 401


@app.route('/sales', methods=['GET', 'POST'])
#@jwt_required()
def manage_sales():
    if request.method == 'POST':
        data = request.get_json()
        current_user = get_jwt_identity()
        new_sale = Sales(
            ReceiptID=data['receipt_id'],
            AdminID=current_user['admin_id'],
            TotalAmount=data['total_amount'],
            ClientID=data['client_id'],
            Sale_date=datetime.utcnow()
        )
        db.session.add(new_sale)
        db.session.commit()
        return jsonify(message="Sale recorded"), 201
    elif request.method == 'GET':
        sales = Sales.query.all()
        return jsonify([sale.to_dict() for sale in sales]), 200

@app.route('/products', methods=['GET', 'POST'])
#@jwt_required()
def manage_products():
    if request.method == 'POST':
        data = request.get_json()
        new_product = Product(
            Productname=data['name'],
            productdescription=data.get('description'),
            price=data['price'],
            availability=data['stock'],
            CategoryID=data['category_id'],
            manufacturerID=data['manufacturer_id'],
            ImageURL=data.get('image_url')
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify(message="Product added"), 201
    elif request.method == 'GET':
        products = Product.query.all()
        return jsonify([product.to_dict() for product in products]), 200

@app.route('/orders', methods=['GET', 'POST'])
#@jwt_required()
def manage_orders():
    if request.method == 'POST':
        data = request.get_json()
        new_order = Order(
            ClientID=data['client_id'],
            order_date=datetime.utcnow(),
            status=data['status'],
            total=data['total_amount']
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(message="Order placed"), 201
    elif request.method == 'GET':
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200

@app.route('/order-details', methods=['GET', 'POST'])
#@jwt_required()
def manage_order_details():
    if request.method == 'POST':
        data = request.get_json()
        new_order_detail = OrderDetails(
            OrderID=data['order_id'],
            ProductID=data['product_id'],
            quantity=data['quantity'],
            price=data['price']
        )
        db.session.add(new_order_detail)
        db.session.commit()
        return jsonify(message="Order details added"), 201
    elif request.method == 'GET':
        order_details = OrderDetails.query.all()
        return jsonify([detail.to_dict() for detail in order_details]), 200

@app.route('/clients', methods=['GET', 'POST'])
#@jwt_required()
def manage_clients():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_client = Client(
            Username=data['username'],
            Email=data['email'],
            Password=hashed_password,
            Shipping_address=data.get('shipping_address')
        )
        db.session.add(new_client)
        db.session.commit()
        return jsonify(message="Client registered"), 201
    elif request.method == 'GET':
        clients = Client.query.all()
        return jsonify([client.to_dict() for client in clients]), 200

@app.route('/categories', methods=['GET', 'POST'])
#@jwt_required()
def manage_categories():
    if request.method == 'POST':
        data = request.get_json()
        new_category = Category(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(new_category)
        db.session.commit()
        return jsonify(message="Category added"), 201
    elif request.method == 'GET':
        categories = Category.query.all()
        return jsonify([category.to_dict() for category in categories]), 200

@app.route('/carts', methods=['GET', 'POST'])
#@jwt_required()
def manage_carts():
    if request.method == 'POST':
        data = request.get_json()
        new_cart = Cart(
            ClientID=data['client_id'],
            CreateAt=datetime.utcnow()
        )
        db.session.add(new_cart)
        db.session.commit()
        return jsonify(message="Cart created"), 201
    elif request.method == 'GET':
        carts = Cart.query.all()
        return jsonify([cart.to_dict() for cart in carts]), 200

@app.route('/cart-items', methods=['GET', 'POST'])
#@jwt_required()
def manage_cart_items():
    if request.method == 'POST':
        data = request.get_json()
        new_cart_item = CartItem(
            CartID=data['cart_id'],
            ProductID=data['product_id'],
            quantity=data['quantity']
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify(message="Cart item added"), 201
    elif request.method == 'GET':
        cart_items = CartItem.query.all()
        return jsonify([item.to_dict() for item in cart_items]), 200

@app.route('/supplies', methods=['GET', 'POST'])
#@jwt_required()
def manage_supplies():
    if request.method == 'POST':
        data = request.get_json()
        new_supply = Supply(
            AdminID=data['admin_id'],
            ManufacturerID=data['manufacturer_id'],
            supply_name=data['supply_name'],
            quantity_ordered=data['quantity_ordered'],
            order_date=datetime.utcnow(),
            ProductID=data['product_id']
        )
        db.session.add(new_supply)
        db.session.commit()
        return jsonify(message="Supply added"), 201
    elif request.method == 'GET':
        supplies = Supply.query.all()
        return jsonify([supply.to_dict() for supply in supplies]), 200

@app.route('/manufacturers', methods=['GET', 'POST'])
#@jwt_required()
def manage_manufacturers():
    if request.method == 'POST':
        data = request.get_json()
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        new_manufacturer = Manufacturer(
            Username=data['username'],
            Email=data['email'],
            Password=hashed_password,
            Companyname=data.get('company_name'),
            Contactinfo=data.get('contact_info')
        )
        db.session.add(new_manufacturer)
        db.session.commit()
        return jsonify(message="Manufacturer registered"), 201
    elif request.method == 'GET':
        manufacturers = Manufacturer.query.all()
        return jsonify([manufacturer.to_dict() for manufacturer in manufacturers]), 200

@app.route('/supply-orders', methods=['GET', 'POST'])
#@jwt_required()
def manage_supply_orders():
    if request.method == 'POST':
        data = request.get_json()
        new_supply_order = SupplyOrder(
            ProductID=data['product_id'],
            orderDate=datetime.utcnow(),
            quantity=data['quantity'],
            total_price=data['total_price']
        )
        db.session.add(new_supply_order)
        db.session.commit()
        return jsonify(message="Supply order added"), 201
    elif request.method == 'GET':
        supply_orders = SupplyOrder.query.all()
        return jsonify([order.to_dict() for order in supply_orders]), 200

@app.route('/receipts', methods=['GET', 'POST'])
#@jwt_required()
def manage_receipts():
    if request.method == 'POST':
        data = request.get_json()
        new_receipt = Receipt(
            OrderID=data['order_id'],
            ClientID=data['client_id'],
            ReceiptDate=datetime.utcnow(),
            Total=data['total'],
            Payment=data['payment']
        )
        db.session.add(new_receipt)
        db.session.commit()
        return jsonify(message="Receipt created"), 201
    elif request.method == 'GET':
        receipts = Receipt.query.all()
        return jsonify([receipt.to_dict() for receipt in receipts]), 200
# Routes end here    
    

# Utility function to convert SQLAlchemy models to dictionaries
def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Adding the to_dict method to each model
models = [Admin, Manufacturer, Client, Category, Product, Order, OrderDetails, Receipt, Cart, CartItem, Supply, SupplyOrder, Sales]
for cls in models:
    cls.to_dict = to_dict

if __name__ == '__main__':
    app.run(debug=True)
