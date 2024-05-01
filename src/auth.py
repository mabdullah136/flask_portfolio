from flask import Blueprint, render_template, redirect, url_for, request, flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required
from .models import User
from . import db
from flask import jsonify, make_response
from flask import jsonify, make_response
from validate_email import validate_email
import json

auth=Blueprint('auth',__name__)


@auth.route('/login', methods=['POST'])
def login_post():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        data = request.json
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
    if user.password != password:
        flash('Password incorrect', 'info')
        return make_response(jsonify({'message': 'Password incorrect'}), 401)
    login_user(user)
    return make_response(jsonify({'message': 'Login successful'}), 200)



