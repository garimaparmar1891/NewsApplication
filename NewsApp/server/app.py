from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flasgger import Swagger

from config.config import Config
from utils.swagger_config import swagger_template
from routes import auth_bp, admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    JWTManager(app)
    Bcrypt(app)
    Swagger(app, template=swagger_template)

    register_blueprints(app)

    return app

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app = create_app()
    print("running")
    app.run(debug=True, port=5000)
