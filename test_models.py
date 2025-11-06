import pytest
from flask import Flask
from models import db, User, Post
from datetime import datetime, timedelta


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app


def test_post_timestamp_and_relationship(app):
    with app.app_context():
        # Create a user
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()

        # Create a post tied to the user's id
        post = Post(body='Testing post timestamp', user_id=user.id)
        db.session.add(post)
        db.session.commit()

        # Timestamp should be populated and recent (within 5 seconds)
        assert post.timestamp is not None, 'Timestamp should not be None'
        assert datetime.utcnow() - post.timestamp < timedelta(seconds=5), 'Timestamp should be recent UTC time'

        # Relationship: post.author should resolve to the user
        assert post.author is not None, 'Post should have an author relationship'
        assert post.author.id == user.id

        # And user.posts should include the post
        assert post in user.posts.all()
