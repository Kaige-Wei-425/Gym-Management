from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db

from models.classes import Class, classes_shcema, class_shcema
from models.training import Training, training_schema

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

# Delete a class by id
@class_bp.route("/<int:class_id>", methods=["DELETE"])
@jwt_required()
def delete_class(class_id):
    # Make sure that only the authorised user can delete the product
    # is_admin = authoriseAsAdmin()
    # if not is_admin:
    #     return {"Error": "Not authorised to delete the product"}, 403

    stmt = db.select(Class).where(Class.id==class_id)
    a_class = db.session.scalar(stmt)
    if a_class:
        db.session.delete(a_class)
        db.session.commit()
        return {"msg": f"Class {a_class.title} has been deleted successfully"}
    else:
        return {"Error": f"Class with id {class_id} does not exist"}, 404

# Update class
@class_bp.route("/<int:class_id>", methods=["PUT", "PATCH"])
def update_class(class_id):
    # Find the class from the db to update
    stmt = db.select(Class).filter_by(id=class_id)
    a_class = db.session.scalar(stmt)
    # Get the data to be updated - received from the body of the request
    class_fields = request.get_json()

    if a_class:
        # Update the attributes
        # if "name" is null in product_field use the existing value
        a_class.name = class_fields.get("title") or a_class.title
        a_class.description = class_fields.get("description") or a_class.description
        a_class.capacity = class_fields.get("capacity") or a_class.capacity
        a_class.duration = class_fields.get("duration") or a_class.duration

        # Commit
        db.session.commit()
        # Return
        return class_shcema.dump(a_class), 201
    else:
        # Return
        return {"Error": f"Class: {class_id} does not exit"}, 404

# Create training on the class
@class_bp.route("/<int:class_id>/trainings", methods=["POST"])
def create_training(class_id):
    body_data = request.get_json()
    stmt = db.select(Training).filter_by(id=class_id)
    one_class = db.session.scalar(stmt)
    # Check whether the class is exist
    if one_class:
        training = Training(
            comment = body_data.get('comment'),
            user_id = get_jwt_identity(),
            one_class = one_class.id
        )
        db.session.add(training)
        db.session.commit()
        return training_schema.dump(training), 201
    else:
        return {"Error": f"Training {class_id} does not exist!"}
    
# Delete training
