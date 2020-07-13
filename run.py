from app import app
from db import db


db.init_app(app)

# This decorator will cause the method to be called before any requests made to the app
# sqlalchemy knows which tables, and corresponding columns it must create
# since in the model classes, we've defined __tablename__ and all of the columns
# Note, all of the model classes extends the SQLAlchemy.Model class.
# The database / tables will be created only if it doesn't exist already.
# important to import the models for sqlalchemy where tables must be created
@app.before_first_request
def create_tables():
    db.create_all()