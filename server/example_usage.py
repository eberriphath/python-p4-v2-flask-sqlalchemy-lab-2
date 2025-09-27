# example_usage.py
from models import db, Customer, Item, Review
from app import app  # make sure this imports your Flask app

with app.app_context():
    # ----------------------------
    # Reset database (optional)
    # ----------------------------
    db.drop_all()
    db.create_all()

    # ----------------------------
    # CREATE
    # ----------------------------
    # Add customers
    alice = Customer(name="Alice")
    bob = Customer(name="Bob")
    db.session.add_all([alice, bob])
    
    # Add items
    pizza = Item(name="Pizza", price=10.5)
    burger = Item(name="Burger", price=7.0)
    db.session.add_all([pizza, burger])
    
    db.session.commit()

    # Add reviews
    review1 = Review(comment="Delicious!", customer=alice, item=pizza)
    review2 = Review(comment="Too salty.", customer=bob, item=pizza)
    review3 = Review(comment="Perfect!", customer=alice, item=burger)
    
    db.session.add_all([review1, review2, review3])
    db.session.commit()

    print("\n--- After Creation ---")
    print(Customer.query.all())
    print(Item.query.all())
    print(Review.query.all())

    # ----------------------------
    # READ / Query relationships
    # ----------------------------
    print("\n--- Alice's Items via association_proxy ---")
    print(alice.items)  # [pizza, burger]

    print("\n--- Pizza Reviews ---")
    for r in pizza.reviews:
        print(f"{r.customer.name} said: {r.comment}")

    # ----------------------------
    # UPDATE
    # ----------------------------
    print("\n--- Updating Review ---")
    review2.comment = "Actually, it was okay."
    db.session.commit()
    print(Review.query.get(review2.id))

    # ----------------------------
    # DELETE
    # ----------------------------
    print("\n--- Deleting Review ---")
    db.session.delete(review3)
    db.session.commit()
    
    print("\n--- Remaining Reviews ---")
    print(Review.query.all())
