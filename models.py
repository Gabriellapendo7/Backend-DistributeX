from flask_sqlalchemy import SQLAlchemy  

db = SQLAlchemy()  

class Manufacturer(db.Model):  
    __tablename__ = 'manufacturer'  
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String, nullable=False)  
    contact_info = db.Column(db.String, nullable=True)  

class Product(db.Model):  
    __tablename__ = 'product'  
    
    id = db.Column(db.Integer, primary_key=True)  
    name = db.Column(db.String, nullable=False)  
    description = db.Column(db.String, nullable=True)  
    price = db.Column(db.Float, nullable=False)  
    stock_quantity = db.Column(db.Integer, nullable=False)  

class Supply(db.Model):  
    __tablename__ = 'supply'  
    
    id = db.Column(db.Integer, primary_key=True)  
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)  
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  
    quantity = db.Column(db.Integer, nullable=False)  
    
    manufacturer = db.relationship("Manufacturer", backref="supplies")  
    product = db.relationship("Product", backref="supplies")  

class SupplyOrder(db.Model):  
    __tablename__ = 'supply_order'  
    
    id = db.Column(db.Integer, primary_key=True)  
    supply_id = db.Column(db.Integer, db.ForeignKey('supply.id'), nullable=False)  
    order_date = db.Column(db.DateTime, nullable=False)  
    
    supply = db.relationship("Supply", backref="supply_orders")