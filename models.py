from sqlalchemy import *
from sqlalchemy.orm import relationship
from db import Base


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)
    created = Column(DateTime)
    author_id = Column(Integer, ForeignKey('users.id'))

    author = relationship('User', back_populates='articles')
    comments = relationship('Comment', back_populates='article')

    def __repr__(self):
        return f'<Article "{self.title}">'


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    is_author = Column(Boolean)
    is_admin = Column(Boolean)

    articles = relationship(
        'Article', order_by=Article.id, back_populates='author')
    comments = relationship(
        'Comment', order_by=Article.id, back_populates='user')


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(String)

    article = relationship('Article', back_populates='comments')
    user = relationship('User', back_populates='comments')
