import uuid
import random
from faker import Faker
from sqlalchemy.orm import Session
from src.core.db import SessionLocal, engine, Base
from src.models.product_model import Product  
from src.models.department_model import Department
from src.models.user_model import User 
from src.models.department_model import Department
from src.models.ticket_model import Ticket
from src.models.order_model import Order
from src.models.orderItem_model import OrderItem

# fake = Faker()

# # Step 1: Create tables
# Base.metadata.create_all(bind=engine)

# # Step 2: Open DB session
# db: Session = SessionLocal()


# # Predefined product names
# product_names = [
#     "Laptop", "Mouse", "Keyboard", "Monitor", "Headphones",

#     "Notebook", "Pen", "Backpack", "Lamp", "USB Cable"
# ]

# # Step 3: Generate random products
# products = []
# for name in product_names:
#     product = Product(
#         id=uuid.uuid4(),
#         name=name,
#         description=fake.sentence(nb_words=15),
#         price=round(random.uniform(10.0, 500.0), 2)
#     )
#     products.append(product)

# # Step 4: Insert into DB
# db.add_all(products)
# db.commit()
# print("Inserted 20 random products successfully!")





# # Step 3: Define four e-commerce departments
# department_data = [
#     {"name": "Sales", "email": "sales@ecommerce.com"},
#     {"name": "Support", "email": "support@ecommerce.com"},
#     {"name": "Logistics", "email": "logistics@ecommerce.com"},
#     {"name": "Finance", "email": "finance@ecommerce.com"}
# ]

# departments = []

# # Step 4: Generate Department instances
# for dep in department_data:
#     department = Department(
#         id=uuid.uuid4(),
#         name=dep["name"],
#         email=dep["email"]
#     )
#     departments.append(department)

# # Step 5: Insert into DB
# db.add_all(departments)
# db.commit()

# print("Inserted 4 departments successfully!")



# users = []

# # Step 3: Generate 5 random users
# for _ in range(5):
#     user = User(
#         id=uuid.uuid4(),
#         name=fake.name(),
#         email=fake.unique.email()
#     )
#     users.append(user)

# # Step 4: Insert into DB
# db.add_all(users)
# db.commit()

# print("Inserted 5 random users successfully!")


# for _ in range(5):
#     user = User(
#         id=uuid.uuid4(),
#         name=fake.name(),
#         email=fake.unique.email()
#     )
#     users.append(user)

# # Step 4: Insert into DB
# db.add_all(users)
# db.commit()

from src.core.db import SessionLocal

session: Session = SessionLocal()

users = session.query(User).all()

for user in users:
    print(user.id)