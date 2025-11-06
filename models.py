from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # Define reciprocal relationship with Post using backref 'author'
    posts = db.relationship('Post', backref='author', lazy='dynamic')


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    # Pass the callable `datetime.utcnow` (no parentheses) so SQLAlchemy calls it at row insertion time
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Declare proper foreign key to link to User.id and make it non-nullable
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
