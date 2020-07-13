from db import db


class ItemModel(db.Model):
    # Specify the db table name for sqlalchemy to link with this model
    __tablename__ = 'items'

    # Specify the table columns for sqlalchemy to link with this model
    # The column variables must match with the instance attributes for
    # sqlalchemy to save to the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # A foreign key links items in a table to primary key of another table for grouping
    # the foreign item identified by the foreign key cannot be deleted before all linked items are deleted
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price': self.price, 'store': self.store.name}

    @classmethod
    def find_by_name(cls, name):
        # Tell SQLAlchemy we are querying the database
        # i.e. SELECT * FROM __tablename__ WHERE name = name LIMIT 1
        # filter_by can work with multiple columns
        # Returns a class object containing all defined attributes
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        # Since this method is operating on the instance itself
        # Just add self to the db session.
        # If the class object instance is with an ID (primary key) that's already in the database
        # Then session.add(self) will update the row in the database
        # This renders the requirement of an 'update()' method to be obsolete
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
