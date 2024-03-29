from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db

from models.classes import Class, classes_shcema, class_shcema

# Create the blue print
class_bp = Blueprint('classes', __name__, url_prefix='/classes')

# Get all Classes
@class_bp.route('/')
# Function to view all the classes
def get_all_classes():
    stmt = db.select(Class) # SELECT * FROM classes;
    classes_list = db.session.scalars(stmt)
    # Return all the classes
    return classes_shcema.dump(classes_list)

# Get one class
@class_bp.route("/<int:class_id>")
def get_class(class_id):
    stmt = db.select(Class).filter_by(id=class_id)
    # use scalar instead of scalars because just select a single product
    a_class = db.session.scalar(stmt)

    # Check whether the id of class is exist
    if a_class:
        data = class_shcema.dump(a_class)
        return data
    else:
        return {"Error": f"Class: {class_id} does not exit"}, 404

# Create a class
@class_bp.route("/", methods=["POST"])
@jwt_required() # Only Admain can create a new class
def create_class():
    # Get the JSON formatted data from the request body
    class_fields = request.get_json()
    
    # Store the data into the database
    new_class = Class (
        title = class_fields.get("title"),
        description = class_fields.get("description"),
        capacity = class_fields.get("capacity"),
        duration = class_fields.get("duration"),
        # This ID will assign to the user whoever create the class
        user_id = get_jwt_identity()
    )

    # Add to session and commit
    db.session.add(new_class)
    db.session.commit()

    data = class_shcema.dump(new_class)
    return data, 201