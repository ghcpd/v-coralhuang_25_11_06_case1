from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User model representing blog authors."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    # Fixed: Added backref='author' to establish reciprocal relationship with Post model
    # lazy='dynamic' allows efficient querying of user's posts
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'


class Post(db.Model):
    """Post model representing user-generated blog posts."""
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    # Fixed: Changed default=datetime.utcnow() to default=datetime.utcnow (without parentheses)
    # This ensures the function is called each time a new Post is created, not at import time
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # Fixed: Added db.ForeignKey('user.id') to establish proper foreign key constraint
    # This ensures referential integrity and enables SQLAlchemy relationship tracking
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post by {self.author.username if self.author else "Unknown"} at {self.timestamp}>'
