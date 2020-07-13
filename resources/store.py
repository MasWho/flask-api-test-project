from flask_restful import Resource
from flask_jwt import jwt_required
from models.store import StoreModel


# Define all the resources and their available requests
class Stores(Resource):
    # Get all available stores
    def get(self):
        # Use sqlalchemy to return all rows in a table
        # It returns a iterable of model objects
        stores = StoreModel.query.all()
        return {'stores': [store.json() for store in stores]}, 200


# No need to use jsonify with flask_restful
class Store(Resource):
    # Get a single store
    # This decorator enforces authentication for a request
    # The JWT token generated must in the header of the request
    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.update_item_count()  # Everytime an item get's created, update item count
            return store.json(), 200
        return {"error": f"couldn't find store '{name}'"}, 404  # Return status code 404: page not found

    # Create a single item
    def post(self, name):
        # Check if item already exist in database
        if StoreModel.find_by_name(name):
            return {"message": f"{name} already exist in database."}
        # req_data = Item.parser.parse_args()
        store = StoreModel(name)
        try:
            store.save_to_db()
        except Exception as e:
            return {"message": f"Failed with error: {e}"}, 500  # 500: Internal server error
        return store.json(), 201  # 201: successfully created

    # Delete a single item
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            try:
                store.delete_from_db()
            except Exception as e:
                return {"message": f"Failed with error: {e}"}, 500
            else:
                return {"message": f"{name} deleted."}, 200
        return {"message": f"couldn't find store '{name}'"}, 404
