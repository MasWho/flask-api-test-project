from werkzeug.security import safe_str_cmp
from models.user import UserModel


# Function to authenticate a user with corresponding password
# If successful, return the user to generate the JWT
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


# If the user requests an endpoint and need authentication
# the function will use the user ID in the payload
# If user id from payload matches a user ID in database, then assume JWT is correct
# user logged in
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
