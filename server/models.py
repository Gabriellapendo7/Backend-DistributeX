from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Admin(db.Model):
    __tablename__ = 'admin'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    # Relationships
    supplies = db.relationship('Supply', backref='admin', lazy=True)
    sales = db.relationship('Sales', backref='admin', lazy=True)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Companyname = db.Column(db.String(128))
    Contactinfo = db.Column(db.String(128))
    # Relationships
    products = db.relationship('Product', backref='manufacturer', lazy=True)
    supplies = db.relationship('Supply', backref='manufacturer', lazy=True)

class Client(db.Model):
    __tablename__ = 'client'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Shipping_address = db.Column(db.String(128))
    # Relationships
    orders = db.relationship('Order', backref='client', lazy=True)
    receipts = db.relationship('Receipt', backref='client', lazy=True)
    carts = db.relationship('Cart', backref='client', lazy=True)
    sales = db.relationship('Sales', backref='client', lazy=True)

class Category(db.Model):
    __tablename__ = 'category'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Productname = db.Column(db.String(255), nullable=False)
    productdescription = db.Column(db.String(255), nullable=True)
    availability = db.Column(db.String(255), nullable=True)
    price = db.Column(db.BigInteger, nullable=False)
    CategoryID = db.Column(db.Integer, db.ForeignKey('category.ID'), nullable=False)
    ManufacturerID = db.Column(db.Integer, db.ForeignKey('manufacturer.ID'), nullable=False)
    ImageURL = db.Column(db.String(255), nullable=True)
    # Relationships
    supply_items = db.relationship('Supply', backref='product', lazy=True)
    order_details = db.relationship('OrderDetails', backref='product', lazy=True)
    cart_items = db.relationship('CartItem', backref='product', lazy=True)

class Order(db.Model):
    __tablename__ = 'order'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClientID = db.Column(db.Integer, db.ForeignKey('client.ID'), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    total = db.Column(db.BigInteger, nullable=False)
    # Relationships
    order_details = db.relationship('OrderDetails', backref='order', lazy=True)
    receipts = db.relationship('Receipt', backref='order', lazy=True)

class OrderDetails(db.Model):
    __tablename__ = 'orderdetails'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('order.ID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ID'), nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)
    price = db.Column(db.BigInteger, nullable=False)

class Receipt(db.Model):
    __tablename__ = 'receipt'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('order.ID'), nullable=False)
    ClientID = db.Column(db.Integer, db.ForeignKey('client.ID'), nullable=False)
    ReceiptDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    Total = db.Column(db.BigInteger, nullable=False)
    Payment = db.Column(db.BigInteger, nullable=False)
    # Relationships
    sales = db.relationship('Sales', backref='receipt', lazy=True)

class Cart(db.Model):
    __tablename__ = 'cart'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClientID = db.Column(db.Integer, db.ForeignKey('client.ID'), nullable=False)
    CreateAt = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Relationships
    cart_items = db.relationship('CartItem', backref='cart', lazy=True)

class CartItem(db.Model):
    __tablename__ = 'cartitem'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    CartID = db.Column(db.Integer, db.ForeignKey('cart.ID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ID'), nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)

class Supply(db.Model):
    __tablename__ = 'supply'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.ID'), nullable=False)
    ManufacturerID = db.Column(db.Integer, db.ForeignKey('manufacturer.ID'), nullable=False)
    supply_name = db.Column(db.String(255), nullable=False)
    quantity_ordered = db.Column(db.BigInteger, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ID'), nullable=False)

class SupplyOrder(db.Model):
    __tablename__ = 'supply_order'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ID'), nullable=False)
    orderDate = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    quantity = db.Column(db.BigInteger, nullable=False)
    total_price = db.Column(db.BigInteger, nullable=False)
    

class Sales(db.Model):
    __tablename__ = 'sales'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ReceiptID = db.Column(db.Integer, db.ForeignKey('receipt.ID'), nullable=False)
    AdminID = db.Column(db.Integer, db.ForeignKey('admin.ID'), nullable=False)
    TotalAmount = db.Column(db.BigInteger, nullable=False)
    ClientID = db.Column(db.Integer, db.ForeignKey('client.ID'), nullable=False)
    Sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

class Review(db.Model):
    __tablename__ = 'review'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ClientID = db.Column(db.Integer, db.ForeignKey('client.ID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('product.ID'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255), nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    client = db.relationship('Client', backref='reviews')
    product = db.relationship('Product', backref='reviews')