from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from .routes import libro_bp  
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Asegúrate de esta línea
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar SQLAlchemy
    db.init_app(app)
    # Registrar el blueprint
    app.register_blueprint(libro_bp)

    # Definir el modelo Libro
    class Libro(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        titulo = db.Column(db.String(120))
        autor = db.Column(db.String(120))
        isbn = db.Column(db.String(13))
        categoria = db.Column(db.String(50))
        estado = db.Column(db.String(20))
        fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Crear todas las tablas si no existen
    with app.app_context():
        db.create_all()  # Esto creará la base de datos y las tablas si no existen

    return app
