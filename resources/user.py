from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    # Define required payload contents
    parser = reqparse.RequestParser()
    parser.add_argument(
        name='username',
        type=str,
        required=True,
        help="User name is required."
    )
    parser.add_argument(
        name='password',
        type=str,
        required=True,
        help="Password is required."
    )

    def post(self):
        # Check to see if user already exist
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already exist."}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201


if __name__ == "__main__":
    pass
