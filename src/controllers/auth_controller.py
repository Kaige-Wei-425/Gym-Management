from flask import Blueprint, request
from init import db, bcrypt
from models.user import User, user_shcema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token
from datetime import timedelta
from psycopg2 import errorcodes

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# User registration
@auth_bp.route('/register', methods=["POST"])
def user_registeration():
    try:
        # Data that get from the request body
        user_fields = request.get_json()

        # Pass the values to the new User object
        user = User (
            name=user_fields.get('name'),
            email=user_fields.get('email'),
            # Use the hashed password above for database
        )
        password = user_fields.get('password')
        # Check whether the password exist in the request body
        if password:
            # Hash the password (from the request body) using bcrypt
            user.password = bcrypt.generate_password_hash(password).decode('utf8')
        # Add to the session
        db.session.add(user)
        # Commit
        db.session.commit()
        # Return the profile to the user
        return user_shcema.dump(user), 201

    # Handle Execptions
    except Exception as excp:
        # Check whether the email or password in the request body are empty
        if excp.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"Error": f"{excp.orig.diag.column_name} cannot be empty"}
        # Check whether the email address is already exist in the database
        if excp.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"Error": "Your email address has been occupied"}, 409

@auth_bp.route("/login", methods=["POST"])
def login_user():
    # Extract fields from body of the request
    user_fields = request.get_json()
    # Find the user by email address
    stmt = db.select(User).filter_by(email=user_fields.get("email"))
    user = db.session.scalar(stmt)
    # If user exist and password matches
    if user and bcrypt.check_password_hash(user.password, user_fields.get("password")):
        # Create JWT
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=0.5)) # Set the time of user loign 
        # Return the user info
        return {"email": user.email, "token": token, "is_admin": user.is_admin}
    # Else
    else:
        # Return error
        return {"Error": "Invalid email or password"}, 401
