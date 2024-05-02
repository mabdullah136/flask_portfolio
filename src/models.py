from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    password=db.Column(db.String(100),nullable=False)
    picture=db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def set_username(self,username):
        self.username=username
    
    def set_email(self,email):
        self.email=email
    

class User_Detail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    profile = db.Column(db.String(100))
    facebook = db.Column(db.String(100),nullable=False)
    linkedin = db.Column(db.String(100),nullable=False)
    instagram = db.Column(db.String(100),nullable=False)
    twitter = db.Column(db.String(100),nullable=False)
    github = db.Column(db.String(100),nullable=False)
    cv = db.Column(db.String(100),nullable=False)
    detailed_description = db.Column(db.Text,nullable=False)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100),nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    images = db.Column(db.String(100),nullable=False)
    short_description = db.Column(db.String(100), nullable=False)
    project_link = db.Column(db.String(100),nullable=False)

