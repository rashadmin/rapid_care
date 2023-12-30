from app import db
from app.auth import bp
from flask import render_template,url_for,redirect,flash,request
from app.auth.form import Login,Register
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User,Conversation
from urllib.parse import urlsplit
from datetime import datetime
from config import Config

@bp.route('/register',methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Register()
    if form.validate_on_submit():
        user = User(firstname= form.firstname.data,lastname=form.lastname.data,username = form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Successfully logged in')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',title='login',form=form)


@bp.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid Username or Password')
            return redirect(url_for('auth.login'))
        login_user(user,remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        if current_user.bloodgroup is None or current_user.genotype is None:
            return redirect(url_for('main.EditProfile'))
        return redirect(next_page)
    return render_template('auth/login.html',title='login',form=form)
    

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))