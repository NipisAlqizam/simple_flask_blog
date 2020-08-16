from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from hashlib import sha256

engine = create_engine('sqlite:///test.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_article(title: str, text: str, authorname: str):
    from models import Article, User
    author = User.query.filter_by(username=authorname).first()
    new_article = Article(title=title, text=text,
                          created=datetime.now(), author=author)
    db_session.add(new_article)
    db_session.commit()


def create_user(name: str, password: str, is_author: bool = False, is_admin: bool = False):
    from models import User
    user = User(username=name, password=get_password_hash(
        password), is_author=is_author, is_admin=is_admin)
    db_session.add(user)
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
        author = article.author.username
        res.append({'id': id, 'title': title, 'text': text,
                    'created': date, 'author': author})
    return res[::-1]


def get_user(username: str):
    from models import User
    return User.query.filter_by(username=username).first()


def check_user(username: str, password: str) -> bool:
    from models import User
    user = User.query.filter_by(username=username).first()
    if user == None:
        return False
    if get_password_hash(password) != user.password:
        return False
    return True


def update_article(id: int, new_title: str, new_text: str):
    from models import Article
    article = Article.query.filter_by(id=id).first()
    article.title = new_title
    article.text = new_text
    db_session.commit()


def update_user_password(username: str, new_password: str):
    from models import User
    user = get_user(username)
    user.password = get_password_hash(new_password)
    db_session.commit()


def get_articles_archive():
    from models import Article
    articles = Article.query.all()
    res = {}
    for article in articles:
        if article.created.year not in res:
            res[article.created.year] = {
                article.created.month: [(article.id, article.title)]
            }
        else:
            res[article.created.year][article.created.month].append(
                (article.id, article.title)
            )
    return res


def get_article_by_id(id):
    from models import Article
    return Article.query.filter(Article.id == id).first()


def get_password_hash(password: str) -> str:
    hash = sha256(password.encode('utf-8')).hexdigest()
    return hash


def init_db():
    import models
    Base.metadata.create_all(engine)
    if models.User.query.first() == None:
        create_user('admin', 'admin', True, True)


if __name__ == '__main__':
    init_db()
