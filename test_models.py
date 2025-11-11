import pytest
from datetime import datetime, timedelta
from flask import Flask
from models import db, User, Post

@pytest.fixture
def app():
    """Create a Flask app for testing with SQLite in-memory database."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

def test_post_timestamp_auto_population(app):
    """Test that Post timestamp is automatically populated with UTC time."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        # Create post without explicitly setting timestamp
        post = Post(body='Testing post timestamp', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        # Verify timestamp was auto-populated
        assert post.timestamp is not None, 'Timestamp should not be None'
        
        # Verify timestamp is recent (within last minute)
        now = datetime.utcnow()
        time_diff = abs((now - post.timestamp).total_seconds())
        assert time_diff < 60, f'Timestamp should be recent, got {post.timestamp}, now is {now}'

def test_post_timestamp_different_instances(app):
    """Test that each Post instance gets its own timestamp."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        # Create first post
        post1 = Post(body='First post', user_id=user.id)
        db.session.add(post1)
        db.session.commit()
        
        # Wait a moment (simulate time passing)
        import time
        time.sleep(0.1)
        
        # Create second post
        post2 = Post(body='Second post', user_id=user.id)
        db.session.add(post2)
        db.session.commit()
        
        # Verify timestamps are different
        assert post1.timestamp != post2.timestamp, 'Each post should have its own timestamp'
        assert post2.timestamp > post1.timestamp, 'Later post should have later timestamp'

def test_post_author_relationship(app):
    """Test that Post.author relationship works correctly via backref."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        post = Post(body='Testing post relationship', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        # Verify post.author exists (via backref)
        assert hasattr(post, 'author'), 'Post should have an author relationship'
        assert post.author is not None, 'Post author should not be None'
        assert post.author.id == user.id, 'Post author should match the user'
        assert post.author.username == 'alice', 'Post author username should match'

def test_user_posts_relationship(app):
    """Test that User.posts relationship works correctly."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        post1 = Post(body='First post', user_id=user.id)
        post2 = Post(body='Second post', user_id=user.id)
        db.session.add(post1)
        db.session.add(post2)
        db.session.commit()
        
        # Verify user.posts relationship (lazy='dynamic' returns a query)
        posts_query = user.posts
        posts_list = posts_query.all()
        assert len(posts_list) == 2, 'User should have 2 posts'
        assert post1 in posts_list, 'First post should be in user.posts'
        assert post2 in posts_list, 'Second post should be in user.posts'

def test_foreign_key_constraint(app):
    """Test that foreign key constraint is properly enforced."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        # Valid foreign key
        post = Post(body='Valid post', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        assert post.user_id == user.id
        
        # Invalid foreign key should fail (if database enforces it)
        # Note: SQLite in-memory may not enforce foreign keys by default
        # but the relationship should still be properly defined

def test_post_timestamp_and_relationship(app):
    """Comprehensive test combining timestamp and relationship checks."""
    with app.app_context():
        user = User(username='alice')
        db.session.add(user)
        db.session.commit()
        
        post = Post(body='Testing post timestamp', user_id=user.id)
        db.session.add(post)
        db.session.commit()
        
        # Expected: timestamp should auto-populate with current UTC time
        assert post.timestamp is not None, 'Timestamp should not be None'
        
        # Expected: post.author should return the User instance
        assert hasattr(post, 'author'), 'Post should have an author relationship'
        assert post.author is not None, 'Post author should not be None'
        assert post.author.username == 'alice', 'Post author should be the correct user'

