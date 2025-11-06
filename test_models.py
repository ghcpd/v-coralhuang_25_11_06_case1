import json
from datetime import datetime, timedelta
import time
import pytest
from flask import Flask
from models import db, User, Post

@pytest.fixture
def app():
    app = Flask(__name__)
    # Use a lightweight in-memory SQLite database for tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

def test_post_timestamp_and_relationship(app):
    # Create a User, then a Post referenced to that user
    user = User(username='alice')
    db.session.add(user)
    db.session.commit()

    # Create a New Post without passing timestamp; the default callable should set it
    post = Post(body='Testing post timestamp', user_id=user.id)
    db.session.add(post)
    db.session.commit()

    # Reload post from the database to ensure defaults were applied
    reload_post = Post.query.get(post.id)

    assert reload_post.timestamp is not None, 'Timestamp should not be None'
    assert isinstance(reload_post.timestamp, datetime), 'Timestamp should be a datetime instance'

    # The timestamp should be set to a recent time (within a few seconds)
    assert datetime.utcnow() - reload_post.timestamp < timedelta(seconds=10), 'Timestamp should be recent UTC time'

    # Relationship: post.author should be the User instance
    assert hasattr(reload_post, 'author'), 'Post should have an author relationship'
    assert reload_post.author.id == user.id, 'Post.author should return the correct User instance'
    assert reload_post.author.username == 'alice', 'Author username should match'
