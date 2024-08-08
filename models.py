from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flask_cors import CORS
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///distributex.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(app, metadata=metadata)
CORS(app)


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



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)