from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user,login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in ', category='success')
                #return redirect(url_for('views.loggedin')) this was to create a separate page for ppl logged in instead of restricting the home page
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect passowrd try again', category='error')
        else:
            flash('email does not exist', category='error')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fname = request.form.get('firstName')
        password1 = request.form.get('password')
        password2 = request.form.get('passwordC')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('email already exists', category='error')
        elif len(email) < 2:
            flash('email must be greater than 2 characters', category='error')
        elif len(fname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 6:
            flash('Password must be greater than 6 characters', category='error')
        elif password2 != password1:
            flash('Passwords do not match!', category='error')
        else:
            new_user = User(email=email, first_name=fname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Sign up is successful', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home')) #this makes it redirect you to the home page even if the route to the homepage changes
    return render_template("signup.html", user=current_user)