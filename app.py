from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from data import Articles
from wtforms import Form, StringField,TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'myflaskapp'
app.config['MYSQL_DATABASE_PORT'] = 8889
app.config['MYSQL_DATABASE_CURSORCLASS'] = 'DictCursor'

mysql = MySQL()
mysql.init_app(app)

Articles = Articles()

@app.route('/')
def index():
  return render_template('home.html')

@app.route('/about')
def about():
  return render_template('about.html')

@app.route('/articles')
def articles():
  return render_template('articles.html', articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
  return render_template('article.html', id = id)

class RegisterForm(Form):
  name = StringField('Name', [validators.length(min=2, max=50)])
  username = StringField('Username', [validators.length(min=4, max=25)])
  email = StringField('Email', [validators.length(min=6, max=50)])
  password = PasswordField('Password', [
    validators.length(min=4, max=25),
    validators.EqualTo('confirm', message='Passwords do not match')
    ])
  confirm = PasswordField('Confirm Pasword')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegisterForm(request.form)
  if request.method == 'POST' and form.validate():
    name = form.name.data
    email = form.email.data
    username = form.username.data
    password = sha256_crypt.encrypt(str(form.password.data))

    connection = mysql.connect()
    cur = connection.cursor()

    cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

    connection.commit()

    cur.close()
    connection.close()

    flash('You are now registered and can log in', 'success')
    return redirect(url_for('index'))
    # return render_template('register.html')
  return render_template('register.html', form=form)


if __name__ == '__main__':
  app.secret_key='secrect123'
  app.run(debug=True)