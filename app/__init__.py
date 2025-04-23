# app/__init__.py
from flask import Flask
from .database import db
from .routes import libro_bp

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///biblioteca.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la base de datos
    db.init_app(app)

    # Registrar los blueprints (rutas)
    app.register_blueprint(libro_bp)

    return app
