from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///test.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def create_article(title: str, text: str):
    from models import Article
    new_article = Article(title=title, text=text)
    db_session.add(new_article)
    db_session.commit()

def get_all_articles():
    from models import Article
    return Article.query.all()

def get_article_by_id(id):
    from models import Article
    return Article.query.filter(Article.id == id).first()


def init_db():
    import models
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()
