from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import db
import logging
app = Flask(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    from db import db_session
    db_session.remove()

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/submit',methods=['POST'])
def submit():
    logging.debug(print(request.form))
    db.create_article(request.form['title'], request.form['text'])
    return redirect(url_for('create'))

@app.route('/archive')
def archive():
    return render_template('archive.html')

@app.route('/article/<id>')
def article(id):
    return render_template('article.html')

if __name__ == '__main__':
    db.init_db()
    app.run(debug=True)
