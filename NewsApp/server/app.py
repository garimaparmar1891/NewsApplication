from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from config.config import Config
from scheduler.news_fetcher import start_scheduled_jobs
from utils.swagger_config import swagger_template
from routes import (
    auth_bp, article_bp, user_bp, notification_bp,
    keyword_bp, admin_bp, reaction_bp, user_keyword_bp
)
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY
    app.config.from_object(Config)

    JWTManager(app)
    Bcrypt(app)
    Swagger(app, template=swagger_template)

    register_blueprints(app)

    start_scheduled_jobs()

    return app

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(article_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(keyword_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reaction_bp)
    app.register_blueprint(user_keyword_bp)

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
