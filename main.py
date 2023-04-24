from flask import Flask, render_template, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session
from data.users import User
from forms.register_form import RegisterForm
from forms.login_form import LoginForm

import secrets
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'type_your_secret_key_there'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=30)

PARAMS = {}


def generate_apikey():
    db_sess = db_session.create_session()
    while True:
        apikey = secrets.token_urlsafe(25)
        if db_sess.query(User).filter(User.apikey != apikey).all():
            return apikey


def generate_hashed_password(password):
    return generate_password_hash(password)


def check_hashed_password(password, hashed_password):
    return check_password_hash(hashed_password, password)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    PARAMS['title'] = 'API Project'
    PARAMS['username'] = db_sess.query(User).first().name
    PARAMS['apikey'] = db_sess.query(User).first().apikey
    return render_template('main.html', **PARAMS)


@app.route('/registration', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_sess = db_session.create_session()
    PARAMS['title'] = 'Registration'
    PARAMS['form'] = form
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            PARAMS['message'] = "Password mismatch"
            return render_template('registration.html', **PARAMS)
        if db_sess.query(User).filter(User.email == form.email.data).first():
            PARAMS['message'] = 'This username already exists'
            return render_template('registration.html', **PARAMS)
        user = User(
            email=form.email.data,
            name=form.name.data,
            hashed_password=generate_hashed_password(form.password.data),
            apikey=generate_apikey()
        )
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', **PARAMS)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    db_sess = db_session.create_session()
    PARAMS['title'] = 'Login'
    PARAMS['form'] = form
    if form.validate_on_submit():
        if db_sess.query(User).filter(User.email != form.email.data).first() or \
                not check_hashed_password(form.password.data, db_sess.query(User).filter(User.hashed_password).all()):
            PARAMS['message'] = 'Wrong email or password'
            return render_template('login.html', **PARAMS)
        return redirect('/')
    return render_template('login.html', **PARAMS)


def main():
    db_session.global_init('db/user_db.sql')
    app.run()


if __name__ == '__main__':
    main()
