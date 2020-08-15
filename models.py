from sqlalchemy import *
from db import Base

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    text = Column(String)

    def __repr__(self):
        return f'<Article "{self.title}">'
