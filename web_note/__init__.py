from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'NOTE.db'
def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'lkasbokjsdocij asdij  askdci asdj m'
    app.config['SQLALCHEMY_DATABASE_URI'] = F'sqlite:///{DB_NAME}'
    db.init_app(app)

    from auth import auth
    from views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    from modules import user_info, note_info
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login_page'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return user_info.query.get(int(id))

    return app
