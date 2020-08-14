from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/submit',methods=['POST'])
def submit():
    print(request.form['text'])
    return redirect('/create')

@app.route('/archive')
def archive():
    return render_template('archive.html')

@app.route('/article/<id_>')
def article(id_=-1):
    return render_template('article.html')

if __name__ == '__main__':
    app.run(debug=True)
