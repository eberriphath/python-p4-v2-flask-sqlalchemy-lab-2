from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# ----------------------------
# Customer Model
# ----------------------------
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # NOT NULL required

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='customer', cascade="all, delete-orphan")

    # Association proxy to get items directly
    items = association_proxy('reviews', 'item')

    # Serialization rules
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

# ----------------------------
# Item Model
# ----------------------------
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # NOT NULL required
    price = db.Column(db.Float, nullable=False)  # NOT NULL required

    # Relationship to Review
    reviews = db.relationship('Review', back_populates='item', cascade="all, delete-orphan")

    # Serialization rules
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

# ----------------------------
# Review Model
# ----------------------------
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)  # NOT NULL required

    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    # Relationships
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')

    # Serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews',)

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'
