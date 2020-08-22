from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, abort, session
import db
import logging
import json
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
    print(articles)
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
    db.create_article(request.form['title'],
                      request.form['text'], session['username'])
    return redirect(url_for('create'))


@app.route('/edit/<id>')
def edit(id):
    article = db.get_article_by_id(id)
    if article == None:
        abort(404)
    if 'username' not in session or (article.author.username != session['username'] and not session['is_admin']):
        abort(403)
    return render_template('edit.html', id=article.id, title=article.title, text=article.text)


@app.route('/update/<id>', methods=['POST'])
def update(id):
    article = db.get_article_by_id(id)
    if article == None:
        abort(404)
    if 'username' not in session or (article.author.username != session['username'] and not session['is_admin']):
        abort(403)
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
        from models import User
        login = request.form['login']
        password = request.form['password']
        if db.get_user(login) != None:
            return render_template('register.html', username_taken=True)
        db.create_user(login, password)
        session['username'] = login
        session['is_author'] = False
        session['is_admin'] = False
        return redirect(url_for('index'))
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
    created_date = article.created.strftime('%d-%m-%y')
    return render_template('article.html', title=article.title, text=db.markdown_to_html(article.text), date=created_date, author=article.author.username, id=article.id)


@app.route('/comment/<id>', methods=['POST'])
def comment(id):
    db.create_comment(session['username'],id,request.form['comment'])
    return redirect(url_for('article', id=id))


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'username' not in session:
        abort(403)
    if request.method == 'POST':
        if not db.check_user(session['username'], request.form['current_password']):
            return render_template('change_password.html', failed=True)
        db.update_user_password(
            session['username'], request.form['new_password'])
        return redirect(url_for('index'))

    return render_template('change_password.html')


@app.route('/api/user_exists')
def user_exists():
    res = {'exists': db.user_exists(request.args['username'])}
    return json.dumps(res)


if __name__ == '__main__':
    db.init_db()
    app.run(host='0.0.0.0', debug=True)
