from init import db, ma
from marshmallow import fields

class Training(db.Model):
    __tablename__ = "trainings"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)

    # Reference foreign keys                    tablename of user: because database (postgresql) only knows tables
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) # User
    #                                            tablename of class
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"), nullable=False) # Class

    # Create relationships, provides by sqlalchemy
    #                      User: the model        trainings: the training on the user table, a user can create multiple trainings
    user = db.relationship("User", back_populates="trainings")
    one_class = db.relationship("Class", back_populates="trainings")

class TrainingSchema(ma.Schema):
    user = fields.Nested('UserSchema', only=["name", "email"])
    one_class = fields.Nested('ClassSchema', exclude=['trainings'])

    class Meta:
        fields = ('id', 'comment', 'user', 'one_class')


training_schema = TrainingSchema()
trainings_schema = TrainingSchema(many=True)