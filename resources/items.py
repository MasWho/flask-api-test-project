from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.items import ItemModel


# Define all the resources and their available requests
class Items(Resource):
    # Get all available items
    def get(self):
        # Use sqlalchemy to return all rows in a table
        # It returns a iterable of model objects
        items = ItemModel.query.all()
        return {'items': [item.json() for item in items]}, 200


# No need to use jsonify with flask_restful
class Item(Resource):
    # Create a class level parser for enforcing payload contents
    # The parser will be used to look through the payload
    # The arguments specified by the parser will be collected
    # This is useful that specific components in the payload is passed in as required
    parser = reqparse.RequestParser()
    # PUT and POST payload must contain 'price'
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is required."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item must be associated with a store_id."
                        )

    # Get a single item
    # This decorator enforces authentication for a request
    # The JWT token generated must in the header of the request
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {"error": f"couldn't find item '{name}'"}, 404  # Return status code 404: page not found

    # Create a single item
    def post(self, name):
        # Check if item already exist in database
        if ItemModel.find_by_name(name):
            return {"message": f"{name} already exist in database."}
        req_data = Item.parser.parse_args()
        item = ItemModel(name, **req_data)
        try:
            item.save_to_db()
            item.store.update_item_count()  # Everytime an item get's created, update item count
        except Exception as e:
            return {"message": f"Failed with error: {e}"}, 500  # 500: Internal server error
        return item.json(), 201  # 201: successfully created

    # Delete a single item
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            try:
                item.delete_from_db()
            except Exception as e:
                return {"message": f"Failed with error: {e}"}, 500
            else:
                return {"message": f"{name} deleted."}, 200
        return {"message": f"couldn't find item '{name}'"}, 404

    # Update a single item
    def put(self, name):
        req_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        # Insert new into db if item not found
        if item:
            item.price = req_data['price']
        # Update item price only if item found in db
        else:
            item = ItemModel(name, **req_data)
        item.save_to_db()
        item.store.update_item_count()  # Everytime an item get's created, update item count
        return item.json()
