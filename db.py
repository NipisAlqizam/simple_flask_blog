from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
from hashlib import sha256
import markdown
from markupsafe import Markup
import re

engine = create_engine('sqlite:///test.db', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def create_article(title: str, text: str, authorname: str):
    """
        Добавить статью в базу данных.

        Параметры:
        title - заголовок статьи
        text - текст статьи
        authorname - ник автора статьи

        Функция ничего не возвращает.
    """
    from models import Article, User
    author = User.query.filter_by(username=authorname).first()
    new_article = Article(title=title, text=text,
                          created=datetime.now(), author=author)
    db_session.add(new_article)
    db_session.commit()


def create_user(name: str, password: str, is_author: bool = False, is_admin: bool = False):
    """
        Создать пользователя.

        Параметры:
        name - имя нового пользователя (для адекватной работы, его не должно существовать в базе данных)
        password - пароль в виде строки (хешируется внутри функции)
        is_author - может ли пользователь создавать статьи. (по умолчанию False)
        is_admin - является ли пользователь админом. (по умолчанию False)
    """
    from models import User
    user = User(username=name, password=get_password_hash(
        password), is_author=is_author, is_admin=is_admin)
    db_session.add(user)
    db_session.commit()


def create_comment(username: str, article_id: int, text: str):
    from models import Comment, User, Article
    user = User.query.filter_by(username=username).first()
    article = Article.query.filter_by(id=article_id).first()
    new_comment = Comment(article=article, user=user, text=text)
    db_session.add(new_comment)
    db_session.commit()


def get_comments(article_id: int) -> list:
    from models import Comment
    comments = Comment.query.filter_by(article_id=article_id).all()
    return comments


def get_preview(text: str) -> str:
    """
        Обрезать первый абзац текста.

        Параметры:
        text - текст для обрезки

        Возвращает:
        первый абзац текста.
    """
    line_break = text.find('\n')
    if line_break == -1:
        line_break = len(text)
    first_paragraph = text[:line_break]
    first_paragraph = markdown_to_html(first_paragraph)
    first_paragraph = remove_html(str(first_paragraph))
    return first_paragraph


def get_articles_preview():
    """
        Получить список статей с метаданными и их первыми абзацами.

        Возвращает:
        Список, состоящий из словарей. В каждом словаре есть ключи:
        id - номер статьи
        title - заголовок статьи
        text - первый абзац статьи
        created - дата создания статьи
        author - ник автора статьи
    """
    from models import Article
    articles = Article.query.filter(Article.id != -1).all()
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
    """
        Получить пользователя по его нику.

        Параметры:
        username - ник пользователя

        Возвращает:
        Объект класса User с соответствующим ником.
    """
    from models import User
    return User.query.filter_by(username=username).first()


def get_user_list() -> list:
    """
        Получить список всех пользователей
    """
    from models import User
    users = User.query.order_by(User.id).all()
    res = []
    for user in users:
        if user.username == 'admin':
            continue
        d = {}
        d['username'] = user.username
        d['is_author'] = user.is_author
        d['is_admin'] = user.is_admin
        res.append(d)
    return res


def get_users():
    from models import User
    users = User.query.all()
    return users


def check_user(username: str, password: str) -> bool:
    """
        Проверяет корректность пары логин/пароль.

        Параметры:
        username - ник пользователя
        password - пароль пользователя (хешируется внутри)

        Возвращает:
        True, если существует пользователь с таким ником
        и его пароль задан корректно
        False, если пользователя не существует или пароль
        не верен
    """
    from models import User
    user = User.query.filter_by(username=username).first()
    if user == None:
        return False
    if get_password_hash(password) != user.password:
        return False
    return True


def user_exists(username: str) -> bool:
    from models import User
    user = User.query.filter_by(username=username).first()
    return user != None


def update_article(id: int, new_title: str, new_text: str):
    """
        Меняет заголовок и текст статьи с указаным номером.

        Параметры:
        id - номер статьи
        new_title - новый заголовок
        new_text - новый текст
    """
    from models import Article
    article = Article.query.filter_by(id=id).first()
    article.title = new_title
    article.text = new_text
    db_session.commit()


def update_user_password(username: str, new_password: str):
    """
        Меняет пароль пользователя с указанным ником.

        Параметры:
        username - ник пользователя
        new_password - новый пароль
    """
    from models import User
    user = get_user(username)
    user.password = get_password_hash(new_password)
    db_session.commit()


def update_user(id: int, is_author: bool, is_admin: bool):
    from models import User
    user = User.query.filter_by(id=id).first()
    print(user)
    if is_author != None:
        user.is_author = is_author
    if is_admin != None:
        user.is_admin = is_admin
    print(is_author, is_admin, user)
    db_session.commit()


def update_desc(text: str):
    from models import Article
    desc = Article.query.filter_by(id=-1).first()
    if desc == None:
        desc = Article(id=-1, title='О блоге')
        db_session.add(desc)
    desc.text = text
    db_session.commit()


def get_desc():
    from models import Article
    desc = Article.query.filter_by(id=-1).first()
    if desc == None:
        return
    return desc


def get_articles_archive():
    """
        Возвращает словарь, где ключами являются года написания статей, а
        значениями - другие словари, в них ключами являются номера месяцев, а
        значениями - кортежи из номера статьи и её заголовка
    """
    from models import Article
    articles = Article.query.filter(Article.id != -1).all()
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


def markdown_to_html(md: str) -> str:
    """
        Возвращает объект Markup с html, соответствующим html разметке 
        данной статьи в формате markdown.
    """
    print(repr(md))
    print()
    md = str(Markup.escape(md))
    md = re.sub('^#', '##', md, flags=re.M)
    html = markdown.markdown(md)
    return Markup(html)


def remove_html(html: str) -> str:
    clean_re = re.compile('<.*?>')
    clean_text = re.sub(clean_re, '', html)
    return clean_text


def get_article_by_id(id):
    """
        Возвращает объект статьи с указаным номером.
    """
    from models import Article
    return Article.query.filter(Article.id == id).first()


def get_password_hash(password: str) -> str:
    """
        Хеширует пароль.
    """
    hash = sha256(password.encode('utf-8')).hexdigest()
    return hash


def direct_sql(sql: str):
    from sqlalchemy import text
    s = text(sql)
    conn = engine.connect()
    alchemy_res = conn.execute(s).fetchall()
    res = []
    for row in alchemy_res:
        res.append([col for col in row])
    return res


def init_db():
    """
        Инициализирует базу данных и создаёт администратора admin:admin, если
        его не существует.
    """
    import models
    Base.metadata.create_all(engine)
    if models.User.query.first() == None:
        create_user('admin', 'admin', True, True)


if __name__ == '__main__':
    print(markdown_to_html('<h1>\n# adfq\n - abc\n - abc\n\nabc\nabc'))
