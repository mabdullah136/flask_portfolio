from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# from flask_session import Session
from flask import Flask
from flask_cors import CORS
from flask_mail import Mail

db = SQLAlchemy()
def create_app():

    app=Flask(__name__,static_url_path='/static')
    cors = CORS(app, resources={r"*": {"origins": "*"}})

    app.config['MAIL_SERVER'] = 'smtp.gmail.com' 
    app.config['MAIL_PORT'] = 587 
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'sabir99918@gmail.com'  
    app.config['MAIL_PASSWORD'] = 'cumc cclk zclh wrms' 
    mail = Mail(app)
    app.config['SECRET_KEY']='secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/portfolio'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = False
    app.config['UPLOAD_FOLDER'] = 'src/static/images'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    db.init_app(app)

    login_manager= LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)

    app.register_blueprint(auth_blueprint)
    
    with app.app_context():
        db.create_all()

    return app
