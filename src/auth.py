from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required
from .models import User
from . import db

auth=Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup',methods=['POST'])
def signup_post():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    print(username, email, password)
    user = User.query.filter_by(email=email).first()
    if user:
        flash('User already exists!', 'info')
        return redirect(url_for('auth.signup'))

    new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))


from flask import jsonify, make_response

from flask import jsonify, make_response
from validate_email import validate_email
import json

@auth.route('/login', methods=['POST'])
def login_post():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = json.loads(request.data.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
    elif content_type.startswith('multipart/form-data') or content_type.startswith('application/x-www-form-urlencoded'):
        email = request.form.get('email')
        password = request.form.get('password')
    if not email or not isinstance(email, str):
        return make_response(jsonify({'message': 'Email is missing or invalid'}), 400)
    if not validate_email(email):
        flash('Email is in the wrong format', 'info')
        return make_response(jsonify({'message': 'Email is in the wrong format'}), 400)
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('User does not exist', 'info')
        return make_response(jsonify({'message': 'User does not exist'}), 401)
    if not check_password_hash(user.password, password):
        flash('Password incorrect', 'info')
        return make_response(jsonify({'message': 'Password incorrect'}), 401)
    login_user(user)
    return make_response(jsonify({'message': 'Login successful'}), 200)




@auth.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_id',None)
    return redirect(url_for('auth.login'))

