from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config import db


class Admin(db.Model):
    __tablename__ = 'admin'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)





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
    supply_name = db.Column(db.String(255), nullable=False)
    quantity_ordered = db.Column(db.BigInteger, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.ID'), nullable=False)


class Manufacturer(db.Model):
    __tablename__ = 'manufacturer'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    Username = db.Column(db.String(64), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Password = db.Column(db.String(128), nullable=False)
    Companyname = db.Column(db.String(128))
    Contactinfo = db.Column(db.String(128))
    
    
    supplies = db.relationship('Supply', backref='manufacturer', lazy=True)





class SupplyOrder(db.Model):
    __tablename__ = 'supply_order'
    
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_information = db.Column(db.Text, nullable=False)
    delivery_schedule = db.Column(db.DateTime, nullable=False)
    pricing_and_payment = db.Column(db.String, nullable=False)
    shipping_information = db.Column(db.Text, nullable=False)
    product_information = db.Column(db.Text, nullable=False)
    order_details = db.Column(db.Text, nullable=False)
    
    ProductID = db.Column(db.BigInteger, db.ForeignKey('product.ID'), nullable=False)
    product = db.relationship("Product", backref="supply_orders")  




class Sales(db.Model):
    __tablename__ = 'sales'
    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ReceiptID = db.Column(db.BigInteger, db.ForeignKey('receipt.ID'), nullable=False)
    AdminID = db.Column(db.BigInteger, db.ForeignKey('admin.ID'), nullable=False)
    TotalAmount = db.Column(db.BigInteger, nullable=False)
    ClientID = db.Column(db.BigInteger, db.ForeignKey('client.ID'), nullable=False)
    Sale_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


if __name__ == '__main__':
    from config import create_app  
    app = create_app()  
    with app.app_context():
        db.create_all()  
    app.run(debug=True)