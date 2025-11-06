from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy extension
# When integrating with a Flask app, call `db.init_app(app)` and create the tables with `db.create_all()`

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)

    # Define the relationship to Post with a back reference 'author'
    posts = db.relationship('Post', backref='author', lazy='dynamic')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)

    # Correct default: pass the callable `datetime.utcnow` (without parentheses)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Correct foreign key: link Post.user_id to User.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post id={self.id} user_id={self.user_id} timestamp={self.timestamp}>"
