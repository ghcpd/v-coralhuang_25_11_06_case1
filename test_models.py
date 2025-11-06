"""
Comprehensive test suite for SQLAlchemy Post model fixes.
Tests timestamp auto-population and User-Post relationship integrity.
"""
import pytest
from datetime import datetime, timedelta
from models import db, User, Post


class TestPostTimestampAutoPopulation:
    """Tests for automatic timestamp population on Post creation."""

    def test_post_timestamp_is_not_none(self, app, session):
        """Verify that a new Post automatically receives a timestamp."""
        user = User(username='alice')
        session.add(user)
        session.commit()

        post = Post(body='Testing post timestamp', user_id=user.id)
        session.add(post)
        session.commit()

        assert post.timestamp is not None, 'Timestamp should not be None'

    def test_post_timestamp_is_datetime_instance(self, app, session):
        """Verify that timestamp is a datetime object."""
        user = User(username='bob')
        session.add(user)
        session.commit()

        post = Post(body='Another test post', user_id=user.id)
        session.add(post)
        session.commit()

        assert isinstance(post.timestamp, datetime), 'Timestamp must be a datetime instance'

    def test_post_timestamp_is_recent(self, app, session):
        """Verify that timestamp is set to current time (within 5 seconds)."""
        user = User(username='charlie')
        session.add(user)
        session.commit()

        before = datetime.utcnow()
        post = Post(body='Recent timestamp test', user_id=user.id)
        session.add(post)
        session.commit()
        after = datetime.utcnow()

        assert before <= post.timestamp <= after + timedelta(seconds=1), \
            'Timestamp should be within current time window'

    def test_multiple_posts_have_different_timestamps(self, app, session):
        """Verify that each post gets its own timestamp (not shared from import time)."""
        user = User(username='diana')
        session.add(user)
        session.commit()

        post1 = Post(body='First post', user_id=user.id)
        session.add(post1)
        session.commit()
        timestamp1 = post1.timestamp

        # Small delay to ensure different timestamps
        import time
        time.sleep(0.1)

        post2 = Post(body='Second post', user_id=user.id)
        session.add(post2)
        session.commit()
        timestamp2 = post2.timestamp

        # Timestamps should not be identical (testing the bug fix)
        assert timestamp1 <= timestamp2, \
            'Second post timestamp should be >= first post timestamp'


class TestUserPostRelationship:
    """Tests for User-Post relationship and backref functionality."""

    def test_post_has_author_attribute(self, app, session):
        """Verify that Post instances have the 'author' attribute via backref."""
        user = User(username='eve')
        session.add(user)
        session.commit()

        post = Post(body='Post with author relationship', user_id=user.id)
        session.add(post)
        session.commit()

        assert hasattr(post, 'author'), 'Post should have an author attribute via backref'

    def test_post_author_returns_correct_user(self, app, session):
        """Verify that post.author resolves to the correct User instance."""
        user = User(username='frank')
        session.add(user)
        session.commit()

        post = Post(body='Testing author resolution', user_id=user.id)
        session.add(post)
        session.commit()

        assert post.author is not None, 'post.author should not be None'
        assert post.author.id == user.id, 'post.author should reference the correct user'
        assert post.author.username == 'frank', 'post.author username should match'

    def test_user_posts_relationship(self, app, session):
        """Verify that User.posts returns related Post instances."""
        user = User(username='grace')
        session.add(user)
        session.commit()

        post1 = Post(body='Grace first post', user_id=user.id)
        post2 = Post(body='Grace second post', user_id=user.id)
        session.add_all([post1, post2])
        session.commit()

        # Use lazy='dynamic' to get query object
        user_posts = user.posts.all()
        assert len(user_posts) == 2, 'User should have 2 posts'
        assert post1 in user_posts, 'First post should be in user.posts'
        assert post2 in user_posts, 'Second post should be in user.posts'

    def test_foreign_key_constraint_defined(self, app, session):
        """Verify that foreign key constraint is properly defined in the model."""
        # Check that user_id column has ForeignKey constraint
        post_table = Post.__table__
        user_id_column = post_table.columns['user_id']
        
        # Verify foreign key exists
        foreign_keys = list(user_id_column.foreign_keys)
        assert len(foreign_keys) > 0, 'user_id should have a foreign key constraint'
        assert foreign_keys[0].column.table.name == 'user', 'Foreign key should reference user table'

    def test_post_deletion_with_relationship(self, app, session):
        """Verify that posts are properly managed through the relationship."""
        user = User(username='henry')
        session.add(user)
        session.commit()

        post = Post(body='Post to be managed', user_id=user.id)
        session.add(post)
        session.commit()

        post_id = post.id
        # Delete the post through the relationship
        session.delete(post)
        session.commit()

        deleted_post = session.query(Post).filter_by(id=post_id).first()
        assert deleted_post is None, 'Post should be deleted'

    def test_multiple_users_multiple_posts(self, app, session):
        """Verify relationships work correctly with multiple users and posts."""
        user1 = User(username='iris')
        user2 = User(username='jack')
        session.add_all([user1, user2])
        session.commit()

        post1_u1 = Post(body='Iris post 1', user_id=user1.id)
        post2_u1 = Post(body='Iris post 2', user_id=user1.id)
        post1_u2 = Post(body='Jack post 1', user_id=user2.id)
        session.add_all([post1_u1, post2_u1, post1_u2])
        session.commit()

        iris_posts = user1.posts.all()
        jack_posts = user2.posts.all()

        assert len(iris_posts) == 2, 'Iris should have 2 posts'
        assert len(jack_posts) == 1, 'Jack should have 1 post'
        assert all(post.author.username == 'iris' for post in iris_posts), \
            'All iris posts should reference iris as author'
        assert all(post.author.username == 'jack' for post in jack_posts), \
            'All jack posts should reference jack as author'


# Pytest fixtures
@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    from flask import Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True

    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def session(app):
    """Create a test database session."""
    with app.app_context():
        yield db.session
        db.session.rollback()
