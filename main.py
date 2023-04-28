from flask import Flask, render_template, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from data import db_session
from data import weather_api
from data.users import User
from forms.register_form import RegisterForm
from forms.login_form import LoginForm

import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'type_your_secret_key_there'

PARAMS = {}


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(days=14)


@app.route('/')
def index():
    db_sess = db_session.create_session()
    PARAMS['title'] = 'API Project'
    PARAMS['login'] = False
    for user in db_sess.query(User).all():
        if user.email in session:
            PARAMS['username'] = db_sess.query(User).filter(User.session_key == session[user.email]).first().name
            PARAMS['apikey'] = db_sess.query(User).filter(User.session_key == session[user.email]).first().apikey
            PARAMS['login'] = True
            render_template('main.html', **PARAMS)
    return render_template('main.html', **PARAMS)


@app.route('/api_info')
def api_info():
    db_sess = db_session.create_session()
    PARAMS['title'] = 'API info'
    PARAMS['login'] = False
    for user in db_sess.query(User).all():
        if user.email in session:
            PARAMS['login'] = True
    return render_template('api_info.html', **PARAMS)


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
            hashed_password=generate_password_hash(form.password.data)
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
        if not db_sess.query(User).filter(User.email == form.email.data).first() or \
                not check_password_hash(db_sess.query(User).filter(
                    User.email == form.email.data).first().hashed_password, form.password.data):
            PARAMS['message'] = 'Wrong email or password'
            return render_template('login.html', **PARAMS)
        session[db_sess.query(User).filter(User.email == form.email.data).first().email] = \
            db_sess.query(User).filter(User.email == form.email.data).first().session_key
        return redirect('/')
    return render_template('login.html', **PARAMS)


@app.route('/logout')
def logout():
    db_sess = db_session.create_session()
    for user in db_sess.query(User).all():
        if user.email in session:
            session.pop(db_sess.query(User).filter(User.session_key == session[user.email]).first().email, None)
            return redirect('/')
    return redirect('/')


def main():
    db_session.global_init('db/user_db.sql')
    app.register_blueprint(weather_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
