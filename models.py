from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)

    # Reciprocal relationship so Post.author resolves to this user.
    # 'lazy="dynamic"' returns a query object instead of a plain list (optional).
    posts = relationship('Post', backref='author', lazy='dynamic')

class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True)

    # Ensure foreign key is declared correctly and enforces referential integrity
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)

    title = Column(String(200), nullable=False)
    content = Column(String(2000), nullable=True)

    # Correctly pass the function 'datetime.utcnow' (no parentheses). This ensures
    # the timestamp is generated at insert time rather than once at module import.
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
