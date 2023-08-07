from . import auth
from flask import render_template, session, Markup
from .forms import RegisterForm, LoginForm
from .. import db
from flask import flash, url_for, redirect, request
from ..models import User
from flask_login import login_user, login_required, logout_user


@auth.route('/register', methods=['GET', 'POST'])
def register():
    link = '<a href="auth/login">Login</a>'
    form = RegisterForm()
    if form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        username = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            flash('This email is already registered.')
            return render_template('register.html', form=form, link=link)
        if username is not None:
            flash('This username is already in use')
            return render_template('register.html', form=form)
        user = User(username=form.username.data, email=form.email.data.lower(), password=form.password.data,
                    name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('You have register.')
    return render_template('register.html', form=form, link=link)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate:
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.hello')
            return redirect(next)
        flash('Invalid email or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    print(session.items())
    return redirect(url_for('auth.login'))
