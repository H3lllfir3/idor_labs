from faker import Faker
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String

from app import User, DATABASE_URL, Base

fake = Faker()


engine = create_engine(DATABASE_URL)

# Create the database schema
Base.metadata.create_all(engine)

# Insert the default user data
default_user_data = {
    'username': 'example_user',
    'name': 'arman',
    'email': 'arman@example.com',
    'password': 'password123',
    'address': '123 Main St',
    'phone': '555-123-4567'
}

# Insert random fake user data
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
conn = engine.connect()

query = sqlalchemy.insert(User).values(**default_user_data)
conn.execute(query)

for _ in range(9):
    user_data = {
        'username': fake.user_name(),
        'name': fake.name().split(' ')[0],
        'email': fake.email(),
        'password': fake.password(),
        'address': fake.address(),
        'phone': fake.phone_number()
    }
    query = sqlalchemy.insert(User).values(**user_data)
    conn.execute(query)

# Commit the transaction and close the connection
conn.close()
