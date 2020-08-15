from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime

engine = create_engine('sqlite:///test.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_article(title: str, text: str):
    from models import Article
    new_article = Article(title=title, text=text, created=datetime.now())
    db_session.add(new_article)
    db_session.commit()


def get_preview(text: str):
    line_break = text.find('\n')
    if line_break == -1:
        line_break = len(text)
    first_paragraph = text[:line_break]
    return first_paragraph


def get_articles_preview():
    from models import Article
    articles = Article.query.all()
    res = []
    for article in articles:
        id = article.id
        title = article.title
        text = get_preview(article.text)
        date = article.created.strftime('%d-%m-%y')
        res.append({'id': id, 'title': title, 'text': text, 'created': date})
    return res[::-1]


def get_articles_archive():
    from models import Article
    articles = Article.query.all()
    res = {}
    for article in articles:
        if article.created.year not in res:
            res[article.created.year] = {article.created.month:[(article.id, article.title)]}
        else:
            res[article.created.year][article.created.month].append((article.id, article.title))
    return res


def get_article_by_id(id):
    from models import Article
    return Article.query.filter(Article.id == id).first()


def init_db():
    import models
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
