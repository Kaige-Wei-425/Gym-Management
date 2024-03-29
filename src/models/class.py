from init import db, ma
from marshmallow import fields

# Create the class model
class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    capacity = db.Column(db.String)
    duration = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # first argument: specifies the class which the table is related. Second argument: create two-way relationship
    user = db.relationship('User', back_populates='classes')

# Create class schema in different cases  
class ClassSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["name", "email"]) # refer to the schema
    class Meta:
        fields = ("id", "title", "description", "capacity", "duration", "user")

# For handling single class
class_shcema = ClassSchema()
# For handling multiple classes
classes_shcema = ClassSchema(many=True)