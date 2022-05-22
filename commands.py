from app import db, app
from app.models import User, Todo

with app.app_context():
    db.create_all()