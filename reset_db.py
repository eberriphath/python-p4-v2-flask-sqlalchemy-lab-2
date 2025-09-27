# reset_db.py
from server.app import app, db  # make sure this path matches your folder structure

with app.app_context():
    db.drop_all()
    db.create_all()
    print("✅ Database reset complete.")
