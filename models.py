from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # Fixed: Added backref='author' and lazy='dynamic' for proper relationship
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    # Fixed: Removed parentheses - pass the function reference, not its result
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Fixed: Added foreign key constraint to properly link to User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

