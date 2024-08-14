from datetime import datetime
from app import create_app, db
from werkzeug.security import generate_password_hash
from models import Admin, Manufacturer, Client, Category, Product, Order, OrderDetails, Receipt, Cart, CartItem, Supply, SupplyOrder, Sales, Review

def seed_db():
    # Create initial data for Admins
    admins = [
        Admin(Username='admin1', Email='admin1@example.com', Password=generate_password_hash('password123')),
        Admin(Username='admin2', Email='admin2@example.com', Password=generate_password_hash('password123')),
        Admin(Username='admin3', Email='admin3@example.com', Password=generate_password_hash('password123')),
        Admin(Username='admin4', Email='admin4@example.com', Password=generate_password_hash('password123')),
        Admin(Username='admin5', Email='admin5@example.com', Password=generate_password_hash('password123'))
    ]

    # Create initial data for Manufacturers
    manufacturers = [
        Manufacturer(Username='manufacturer1', Email='manufacturer1@example.com', Password='hashed_password1', Companyname='Cookware Co', Contactinfo='123-456-7890'),
        Manufacturer(Username='manufacturer2', Email='manufacturer2@example.com', Password='hashed_password2', Companyname='Bakeware Ltd', Contactinfo='098-765-4321'),
        Manufacturer(Username='manufacturer3', Email='manufacturer3@example.com', Password='hashed_password3', Companyname='Kitchen Essentials', Contactinfo='111-222-3333'),
        Manufacturer(Username='manufacturer4', Email='manufacturer4@example.com', Password='hashed_password4', Companyname='ProChef Supplies', Contactinfo='444-555-6666'),
        Manufacturer(Username='manufacturer5', Email='manufacturer5@example.com', Password='hashed_password5', Companyname='Gourmet Tools', Contactinfo='777-888-9999')
    ]

    # Create initial data for Clients
    clients = [
        Client(Username='client1', Email='client1@example.com', Password='hashed_password1', Shipping_address='123 Cook St'),
        Client(Username='client2', Email='client2@example.com', Password='hashed_password2', Shipping_address='456 Bake Ave'),
        Client(Username='client3', Email='client3@example.com', Password='hashed_password3', Shipping_address='789 Kitchen Blvd'),
        Client(Username='client4', Email='client4@example.com', Password='hashed_password4', Shipping_address='101 Chef Rd'),
        Client(Username='client5', Email='client5@example.com', Password='hashed_password5', Shipping_address='202 Gourmet Pkwy')
    ]

    # Create initial data for Categories
    categories = [
        Category(name='Cookware', description='Pots, pans, and other cooking utensils'),
        Category(name='Bakeware', description='Baking trays, molds, and other bakeware items'),
        Category(name='Kitchen Tools', description='Knives, cutting boards, and other kitchen tools'),
        Category(name='Small Appliances', description='Blenders, mixers, and other small kitchen appliances'),
        Category(name='Gourmet Ingredients', description='High-quality ingredients and specialty food items')
    ]

    # Create initial data for Products
    products = [
        Product(Productname='Stainless Steel Pan', productdescription='Durable and versatile cooking pan', availability='In stock', price=2999, CategoryID=1, ManufacturerID=1, ImageURL='http://example.com/stainless_steel_pan.jpg'),
        Product(Productname='Non-stick Baking Tray', productdescription='Perfect for baking without the mess', availability='In stock', price=1499, CategoryID=2, ManufacturerID=2, ImageURL='http://example.com/non_stick_baking_tray.jpg'),
        Product(Productname='Chef Knife', productdescription='High-quality knife for precise cutting', availability='In stock', price=4999, CategoryID=3, ManufacturerID=3, ImageURL='http://example.com/chef_knife.jpg'),
        Product(Productname='Stand Mixer', productdescription='Essential for all your baking needs', availability='In stock', price=9999, CategoryID=4, ManufacturerID=4, ImageURL='http://example.com/stand_mixer.jpg'),
        Product(Productname='Truffle Oil', productdescription='Gourmet oil infused with truffle', availability='In stock', price=2499, CategoryID=5, ManufacturerID=5, ImageURL='http://example.com/truffle_oil.jpg')
    ]

    # Create initial data for Orders
    orders = [
        Order(ClientID=1, order_date=datetime.now(), status='Shipped', total=2999),
        Order(ClientID=2, order_date=datetime.now(), status='Processing', total=1499),
        Order(ClientID=3, order_date=datetime.now(), status='Delivered', total=4999),
        Order(ClientID=4, order_date=datetime.now(), status='Shipped', total=9999),
        Order(ClientID=5, order_date=datetime.now(), status='Processing', total=2499)
    ]

    # Create initial data for OrderDetails
    order_details = [
        OrderDetails(OrderID=1, ProductID=1, quantity=1, price=2999),
        OrderDetails(OrderID=2, ProductID=2, quantity=1, price=1499),
        OrderDetails(OrderID=3, ProductID=3, quantity=1, price=4999),
        OrderDetails(OrderID=4, ProductID=4, quantity=1, price=9999),
        OrderDetails(OrderID=5, ProductID=5, quantity=1, price=2499)
    ]

    # Create initial data for Receipts
    receipts = [
        Receipt(OrderID=1, ClientID=1, ReceiptDate=datetime.now(), Total=2999, Payment=2999),
        Receipt(OrderID=2, ClientID=2, ReceiptDate=datetime.now(), Total=1499, Payment=1499),
        Receipt(OrderID=3, ClientID=3, ReceiptDate=datetime.now(), Total=4999, Payment=4999),
        Receipt(OrderID=4, ClientID=4, ReceiptDate=datetime.now(), Total=9999, Payment=9999),
        Receipt(OrderID=5, ClientID=5, ReceiptDate=datetime.now(), Total=2499, Payment=2499)
    ]

    # Create initial data for Carts
    carts = [
        Cart(ClientID=1),
        Cart(ClientID=2),
        Cart(ClientID=3),
        Cart(ClientID=4),
        Cart(ClientID=5)
    ]

    # Create initial data for CartItems
    cart_items = [
        CartItem(CartID=1, ProductID=1, quantity=1),
        CartItem(CartID=2, ProductID=2, quantity=1),
        CartItem(CartID=3, ProductID=3, quantity=1),
        CartItem(CartID=4, ProductID=4, quantity=1),
        CartItem(CartID=5, ProductID=5, quantity=1)
    ]

    # Create initial data for Supplies
    supplies = [
        Supply(AdminID=1, ManufacturerID=1, supply_name='Stainless Steel Pans', quantity_ordered=100, ProductID=1),
        Supply(AdminID=2, ManufacturerID=2, supply_name='Non-stick Baking Trays', quantity_ordered=150, ProductID=2),
        Supply(AdminID=3, ManufacturerID=3, supply_name='Chef Knives', quantity_ordered=200, ProductID=3),
        Supply(AdminID=4, ManufacturerID=4, supply_name='Stand Mixers', quantity_ordered=50, ProductID=4),
        Supply(AdminID=5, ManufacturerID=5, supply_name='Truffle Oils', quantity_ordered=120, ProductID=5)
    ]

    # Create initial data for SupplyOrders
    supply_orders = [
        SupplyOrder(ProductID=1, orderDate=datetime.now(), quantity=100, total_price=299900),
        SupplyOrder(ProductID=2, orderDate=datetime.now(), quantity=150, total_price=224850),
        SupplyOrder(ProductID=3, orderDate=datetime.now(), quantity=200, total_price=999800),
        SupplyOrder(ProductID=4, orderDate=datetime.now(), quantity=50, total_price=499950),
        SupplyOrder(ProductID=5, orderDate=datetime.now(), quantity=120, total_price=299880)
    ]

    # Create initial data for Sales
    sales = [
        Sales(ReceiptID=1, AdminID=1, TotalAmount=2999, ClientID=1),
        Sales(ReceiptID=2, AdminID=2, TotalAmount=1499, ClientID=2),
        Sales(ReceiptID=3, AdminID=3, TotalAmount=4999, ClientID=3),
        Sales(ReceiptID=4, AdminID=4, TotalAmount=9999, ClientID=4),
        Sales(ReceiptID=5, AdminID=5, TotalAmount=2499, ClientID=5)
    ]
    
    # Create initial data for Reviews
    reviews = [
        Review(ClientID=1, ProductID=1, rating=5, comment='Great quality pan!', review_date=datetime.now()),
        Review(ClientID=2, ProductID=2, rating=4, comment='Perfect baking tray for cookies.', review_date=datetime.now()),
        Review(ClientID=3, ProductID=3, rating=5, comment='This knife is very sharp and durable.', review_date=datetime.now()),
        Review(ClientID=4, ProductID=4, rating=4, comment='The stand mixer works like a charm!', review_date=datetime.now()),
        Review(ClientID=5, ProductID=5, rating=5, comment='Truffle oil adds a gourmet touch to dishes.', review_date=datetime.now())
    ]
    
    # Add and commit all the data to the database
    db.session.add_all(admins + manufacturers + clients + categories + products + orders + order_details + receipts + carts + cart_items + supplies + supply_orders + sales + reviews)
    db.session.commit()

if __name__ == '__main__':
    app = create_app()  # Initialize your app
    with app.app_context():
        seed_db()
