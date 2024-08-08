from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from faker import Faker
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['JWT_SECRET_KEY'] = '2a471f3357ce40230b9f670bd05ec405384d502a70bbc3bf98d4509f4620e96a'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
fake = Faker()

# Import models using relative import
from app import Admin, Manufacturer, Client, Category, Product, Order, OrderDetails, Receipt, Cart, CartItem, Supply, SupplyOrder, Sales

# Create the database tables within the app context
with app.app_context():
    db.create_all()

    # Seed data for Admin
    admin1 = Admin(Username='admin1', Email=fake.email(), Password=bcrypt.generate_password_hash('password1').decode('utf-8'))
    admin2 = Admin(Username='admin2', Email=fake.email(), Password=bcrypt.generate_password_hash('password2').decode('utf-8'))
    db.session.add(admin1)
    db.session.add(admin2)

    # Seed data for Manufacturers
    manufacturers = []
    for _ in range(5):
        manufacturer = Manufacturer(
            Username=fake.user_name(),
            Email=fake.email(),
            Password=bcrypt.generate_password_hash('password').decode('utf-8'),
            Companyname=fake.company(),
            Contactinfo=fake.phone_number()
        )
        manufacturers.append(manufacturer)
    db.session.add_all(manufacturers)

    # Seed data for Clients
    clients = []
    for _ in range(10):
        client = Client(
            Username=fake.user_name(),
            Email=fake.email(),
            Password=bcrypt.generate_password_hash('password').decode('utf-8'),
            Shipping_address=fake.address()
        )
        clients.append(client)
    db.session.add_all(clients)

    # Commit to generate IDs for Admins, Manufacturers, and Clients
    db.session.commit()

    # Seed data for Categories
    categories = []
    for _ in range(5):
        category = Category(
            name=fake.word(),
            description=fake.sentence()
        )
        categories.append(category)
    db.session.add_all(categories)
    db.session.commit()

    # Seed data for Products
    products = []
    for _ in range(20):
        product = Product(
            Productname=fake.word(),
            productdescription=fake.sentence(),
            description=fake.sentence(),
            availability='In Stock',
            price=random.randint(1000, 10000),
            CategoryID=random.choice(categories).ID,
            manufacturerID=random.choice(manufacturers).ID,
            ImageURL=fake.image_url()
        )
        products.append(product)
    db.session.add_all(products)
    db.session.commit()

    # Seed data for Orders
    orders = []
    for client in clients:
        order = Order(
            ClientID=client.ID,
            order_date=datetime.utcnow(),
            status='Pending',
            total=random.randint(1000, 5000)
        )
        orders.append(order)
    db.session.add_all(orders)
    db.session.commit()

    # Seed data for OrderDetails
    order_details = []
    for order in orders:
        for _ in range(3):
            order_detail = OrderDetails(
                OrderID=order.ID,
                ProductID=random.choice(products).ID,
                quantity=random.randint(1, 5),
                price=random.randint(100, 1000)
            )
            order_details.append(order_detail)
    db.session.add_all(order_details)
    db.session.commit()

    # Seed data for Receipts
    receipts = []
    for order in orders:
        receipt = Receipt(
            OrderID=order.ID,
            ClientID=order.ClientID,
            ReceiptDate=datetime.utcnow(),
            Total=order.total,
            Payment=order.total
        )
        receipts.append(receipt)
    db.session.add_all(receipts)
    db.session.commit()

    # Seed data for Cart and CartItems
    carts = []
    for client in clients:
        cart = Cart(ClientID=client.ID, CreateAt=datetime.utcnow())
        carts.append(cart)
    db.session.add_all(carts)
    db.session.commit()  # Commit Cart data first to generate IDs
    
    # Seed CartItems using the committed Cart IDs
    cart_items = []
    for cart in carts:
        for _ in range(3):
            cart_item = CartItem(
                CartID=cart.ID,
                ProductID=random.choice(products).ID,
                quantity=random.randint(1, 5)
            )
            cart_items.append(cart_item)
    db.session.add_all(cart_items)
    db.session.commit()

    # Seed data for Supplies
    supplies = []
    for _ in range(10):
        supply = Supply(
            AdminID=random.choice([admin1.ID, admin2.ID]),
            ManufacturerID=random.choice(manufacturers).ID,
            supply_name=fake.word(),
            quantity_ordered=random.randint(10, 100),
            order_date=datetime.utcnow(),
            ProductID=random.choice(products).ID
        )
        supplies.append(supply)
    db.session.add_all(supplies)
    db.session.commit()

    # Seed data for SupplyOrders
    supply_orders = []
    for _ in range(10):
        supply_order = SupplyOrder(
            ProductID=random.choice(products).ID,
            orderDate=datetime.utcnow(),
            quantity=random.randint(10, 100),
            total_price=random.randint(1000, 10000)
        )
        supply_orders.append(supply_order)
    db.session.add_all(supply_orders)
    db.session.commit()

    # Seed data for Sales
    sales = []
    for receipt in receipts:
        sale = Sales(
            ReceiptID=receipt.ID,
            AdminID=random.choice([admin1.ID, admin2.ID]),
            TotalAmount=receipt.Total,
            ClientID=receipt.ClientID,
            Sale_date=datetime.utcnow()
        )
        sales.append(sale)
    db.session.add_all(sales)
    db.session.commit()

    print("Database seeded with fake data!")
