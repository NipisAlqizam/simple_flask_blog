from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, abort, session
import db
import logging
app = Flask(__name__)
app.secret_key = 'dev'


@app.teardown_appcontext
def shutdown_session(exception=None):
    from db import db_session
    db_session.remove()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html', error_text='404. Nothing here.'), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('error.html', error_text='403. Looks like you\'re not allowed to do this'), 403


@app.route('/')
def index():
    articles = db.get_articles_preview()
    no_articles = len(articles) == 0
    return render_template('main.html', articles=articles, no_articles=no_articles)


@app.route('/create')
def create():
    if 'is_author' not in session or not session['is_author']:
        abort(403)
    return render_template('create.html')


@app.route('/submit', methods=['POST'])
def submit():
    if 'is_author' not in session or not session['is_author']:
        abort(403)
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
        login = request.form['login']
        password = request.form['password']
        if db.check_user(login, password):
            user = db.get_user(login)
            session['username'] = login
            session['is_author'] = user.is_author
            session['is_admin'] = user.is_admin
            return redirect(url_for('index'))
        else:
            return render_template('login.html', failed=True)
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        abort(404)
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    session.pop('is_author', None)
    return redirect(url_for('index'))


@app.route('/article/<id>')
def article(id):
    article = db.get_article_by_id(id)
    if article == None:
        abort(404)
    return render_template('article.html', title=article.title, text=article.text)


if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
