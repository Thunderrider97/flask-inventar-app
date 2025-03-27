from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

#Erstellt die App
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    # Blueprints importieren
    from .routes import auth, inventory, profile, api, main
    app.register_blueprint(auth.bp)
    app.register_blueprint(inventory.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(main.bp)

    # Modelle importieren (nach db.init_app)
    from app.models import User

    # user_loader DEFINITION – HIER!
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    

    # Zeit auslesen!
    from datetime import datetime
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}

    return app
