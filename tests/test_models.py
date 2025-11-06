import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Post


@pytest.fixture()
def session():
    # In-memory SQLite database is lightweight and reproducible.
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    sess = Session()
    yield sess
    sess.close()


def test_post_timestamp_autofilled(session):
    user = User(username='alice')
    session.add(user)
    session.commit()

    # Create a post without timestamp; timestamp should be auto-populated to UTC now
    post = Post(title='Hello', content='World', user_id=user.id)
    session.add(post)
    session.commit()

    assert post.timestamp is not None, "timestamp must be auto-populated"
    assert isinstance(post.timestamp, datetime)

    # Also verify that author is resolvable via the backref when only user_id is set
    assert post.author is user

    # timestamp should be very recent (within a small delta)
    now = datetime.utcnow()
    assert now - post.timestamp < timedelta(seconds=10)


def test_post_relationship_resolves_author(session):
    user = User(username='bob')
    session.add(user)
    session.commit()

    # Create with relationship set directly
    post = Post(title='Rel', content='Test')
    post.author = user
    session.add(post)
    session.commit()

    # Validate that the backref worked
    assert post.author is user

    # Since relationship is lazy='dynamic', it's a query object for posts
    # But we can still call .filter on it; convert to list for assertion
    posts = list(user.posts)
    assert len(posts) == 1 and posts[0] is post


def test_foreign_key_enforced(session):
    # Creating a post without an associated user should fail due to NOT NULL FK
    post = Post(title='NoUser', content='xyz', user_id=None)
    session.add(post)
    from sqlalchemy.exc import IntegrityError
    with pytest.raises(IntegrityError):
        session.commit()

