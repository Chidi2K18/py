from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Influencer, Business
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

# Create a Blueprint for the 'auth' module to handle user authentication related routes
auth = Blueprint('auth', __name__)

# Route to handle login for Influencers
@auth.route('/loginI', methods=['GET', 'POST'])
def login_i():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Get the input values from the login form
        email = request.form.get('email')
        password = request.form.get('password')

        # Attempt to find an Influencer with the provided email in the database
        user = Influencer.query.filter_by(email=email).first()
        if user:
            # Check if the provided password matches the hashed password stored in the database
            if check_password_hash(user.password, password):
                # If the password is correct, log the user in, display a success message, and redirect to the home page
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                # If the password is incorrect, display an error message
                flash('Incorrect password, try again.', category='error')
        else:
            # If no Influencer with the provided email exists, display an error message
            flash('Email does not exist.', category='error')

    # Render the login template, passing the current_user object (used for handling user sessions)
    return render_template("login.html", user=current_user)

# Route to handle login for Businesses
@auth.route('/loginB', methods=['GET', 'POST'])
def login_b():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Business.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)

# Route to handle user logout (authentication required)
@auth.route('/logout')
@login_required
def logout():
    # Log the user out, remove their session, and redirect to the home page
    logout_user()
    return redirect(url_for('views.home'))

# Route to handle sign up for Influencers
@auth.route('/signupi', methods=['GET', 'POST'])
def sign_up_i():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Get the input values from the signup form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password')
        password2 = request.form.get('passwordC')

        # Attempt to find an Influencer with the provided email in the database
        user = Influencer.query.filter_by(email=email).first()
        if user:
            # If an Influencer with the provided email already exists, display an error message
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            # If the email is too short, display an error message
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            # If the first name is too short, display an error message
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            # If the provided passwords don't match, display an error message
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            # If the password is too short, display an error message
            flash('Password must be at least 7 characters.', category='error')
        else:
            # If all validation checks pass, create a new Influencer, add it to the database, log them in,
            # display a success message, and redirect to the home page
            new_user = Influencer(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    # Render the signup template, passing the current_user object (used for handling user sessions)
    return render_template("signupi.html", user=current_user)

# Route to handle sign up for Businesses
@auth.route('/signupb', methods=['GET', 'POST'])
def sign_up_b():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password')
        password2 = request.form.get('passwordC')

        user = Business.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = Business(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signupb.html", user=current_user)
