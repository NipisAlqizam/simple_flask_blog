from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, abort
import db
import logging
app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    from db import db_session
    db_session.remove()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('notfound.html'), 404


@app.route('/')
def index():
    articles = db.get_articles_preview()
    no_articles = len(articles) == 0
    return render_template('main.html', articles=articles, no_articles=no_articles)


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/submit', methods=['POST'])
def submit():
    db.create_article(request.form['title'], request.form['text'])
    return redirect(url_for('create'))


@app.route('/edit/<id>')
def edit(id):
    article = db.get_article_by_id(id)
    if article == None:
        abort(404)
    return render_template('edit.html', id=article.id, title=article.title, text=article.text)


@app.route('/update/<id>', methods=['POST'])
def update(id):
    db.update_article(id, request.form['title'], request.form['text'])
    return redirect(url_for('article', id=id))


@app.route('/archive')
def archive():
    archive = db.get_articles_archive()
    print(archive)
    no_articles = len(archive) == 0
    return render_template('archive.html', archive=archive, no_articles=no_articles)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        abort(404)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        abort(404)
    return render_template('register.html')


@app.route('/article/<id>')
def article(id):
    article = db.get_article_by_id(id)
    if article == None:
        abort(404)
    return render_template('article.html', title=article.title, text=article.text)


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
