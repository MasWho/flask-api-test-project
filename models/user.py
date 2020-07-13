from db import db


class UserModel(db.Model):
    # Specify the db table name for sqlalchemy to link with this model
    __tablename__ = 'users'

    # Specify the table columns for sqlalchemy to link with this model
    # The column variables must match with the instance attributes for
    # # sqlalchemy to save to the database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        # No need to have id here since id is a primary key in database
        # This means that id is auto incrementing in the db
        # We do not need to explicitly define the id in the model
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        # Connect to the DB and find the user by username
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        # Connect to the DB and find the user by id
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
