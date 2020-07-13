from db import db


class StoreModel(db.Model):
    # Specify the db table name for sqlalchemy to link with this model
    __tablename__ = 'stores'

    # Specify the table columns for sqlalchemy to link with this model
    # The column variables must match with the instance attributes for
    # sqlalchemy to save to the database
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    # Evaluate lazily so it doesn't take up too much resource everytime a store is created
    items = db.relationship('ItemModel', lazy='dynamic')
    item_count = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.item_count = len(self.items.all())  # Need to figure out how to do this!

    def json(self):
        return {'name': self.name,
                'items': [item.json() for item in self.items.all()],
                'item_count': self.item_count}

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

    def update_item_count(self):
        self.item_count = len(self.items.all())
        self.save_to_db()
