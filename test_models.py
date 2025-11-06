import json
from datetime import datetime, timedelta
import os
import sys
import pytest
from flask import Flask

# Ensure project root is on sys.path so `from models import ...` works during pytest
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from models import db, User, Post

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


def test_post_timestamp_and_relationship(app):
    user = User(username='alice')
    db.session.add(user)
    db.session.commit()

    post = Post(body='Testing post timestamp', user_id=user.id)
    db.session.add(post)
    db.session.commit()

    reload_post = Post.query.get(post.id)

    assert reload_post.timestamp is not None, 'Timestamp should not be None'
    assert isinstance(reload_post.timestamp, datetime), 'Timestamp should be a datetime instance'

    assert datetime.utcnow() - reload_post.timestamp < timedelta(seconds=10), 'Timestamp should be recent UTC time'

    assert hasattr(reload_post, 'author'), 'Post should have an author relationship'
    assert reload_post.author.id == user.id, 'Post.author should return the correct User instance'
    assert reload_post.author.username == 'alice', 'Author username should match'
