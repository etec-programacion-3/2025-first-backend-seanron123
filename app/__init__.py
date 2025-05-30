from flask import Flask
from flask_cors import CORS
from app.routes import libro_bp  
from app.database import db
from app.usuarios_routes import usuario_bp
from app.prestamos_routes import prestamo_bp

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy
    db.init_app(app)

    # Activar CORS para todo el backend
    CORS(app)

    # Registrar el blueprint
    app.register_blueprint(libro_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(prestamo_bp)

    # Crear todas las tablas si no existen
    with app.app_context():
        db.create_all()

    return app
