from flask_sqlalchemy import SQLAlchemy

# A SQLAlchemy object will link to a flask app
# Then look at all of the objects we specify
# Then it will map the objects to the rows in a database
db = SQLAlchemy()
