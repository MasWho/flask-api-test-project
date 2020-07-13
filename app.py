from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.items import Items, Item
from resources.store import Stores, Store
from db import db


# Define app
app = Flask(__name__)
# Turn off flask sqlalchemy tracking to save resource
# sqlalchmy has its own tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mason'  # Key for authetication
api = Api(app)

# JWT (JSON web token) creates a new endpoint /auth
# A username and password will be sent to /auth
# JWT extension then sends the username and password to the authenticate function
# If user authentication is successful, a JWT token is returned
# The JWT token is then sent to the identity function, which then gets corresponding user represented by the JWT token
jwt = JWT(app, authenticate, identity)

# Add item resources to API
api.add_resource(Items, '/items')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')

# Add store resources to API
api.add_resource(Stores, '/stores')
api.add_resource(Store, '/store/<string:name>')


if __name__ == '__main__':
    # Initialise SQLAlchemy
    db.init_app(app)

    # Run app
    app.run(port=5000, debug=True)
