from init import db, ma
from marshmallow import fields

# Create the user models
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    classes = db.relationship('Class', back_populates='user', cascade='all, delete') # If delete a user, delete all its related classes

# Create user schema in different cases  
class UserSchema(ma.Schema):
    classes = fields.List(fields.Nested('ClassSchema', exclude=['users']))
    class Meta:
        fields = ("id", "name", "email", "password", "is_admin", "classes")

# For handling single user
user_shcema = UserSchema(exclude=["password"])
# For handling multiple users
users_shcema = UserSchema(many=True, exclude=["password"])