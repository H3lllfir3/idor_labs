from faker import Faker
from app import db, User, app

fake = Faker()

# Create the database tables first
with app.app_context():
    db.create_all()

# Add default user data
with app.app_context():
    default_user = User(
        username='example_user',
        password='password123',
        address='123 Main St',
        phone='555-123-4567'
    )
    db.session.add(default_user)

    # Add random fake user data
    for _ in range(9):
        user = User(
            username=fake.user_name(),
            password=fake.password(),
            address=fake.address(),
            phone=fake.phone_number()
        )
        db.session.add(user)

    db.session.commit()
