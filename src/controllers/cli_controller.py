from flask import Blueprint
from init import db, bcrypt
from models.user import User # Import the user model
from models.classes import Class

db_commands = Blueprint('db', __name__)

# Create Tables
@db_commands.cli.command('create')
def create_tables():
    db.create_all()
    print('Tables Created')

# Seed Tables
@db_commands.cli.command('seed')
def seed_tables():
    users = [
        User(
            name="Admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
            is_admin=True # This is the admin user
        ),
        User(
            name="Tom",
            email="tom@email.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
        ),
        User(
            name="Mark",
            email="mark@email.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
        ),
        User(
            name="Jack",
            email="jack@email.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8'),
        ),
        User(
            name="Peter",
            email="peter@email.com",
            password=bcrypt.generate_password_hash("123456").decode('utf8')
        )
    ]
    # Add to session
    db.session.add_all(users)

    # Add Class Data
    classes = [
        Class(
            title = "Pilates",
            description = "Pilates is the exercise of choice for those looking to strengthen, balance, and tone",
            capacity = "15",
            duration = "45mins",
            user = users[0]
        ),
        Class(
            title = "Yoga",
            description = "Make your body soft",
            capacity = "10",
            duration = "1hr",
            user = users[0]
        ),
        Class(
            title = "Boxing",
            description = "Challanges yourself!",
            capacity = "4",
            duration = "2hrs",
            user = users[0]
        )
    ]
    db.session.add_all(classes)

    # Commit
    db.session.commit()
    print("Table Seeded")

# Drop Tables
@db_commands.cli.command('drop')
def drop_tables():
    db.drop_all()
    print('Tables Dropped')