from flask import Blueprint, request, jsonify
from .models import Prestamo, Libro, Usuario
from .database import db
from datetime import datetime

prestamo_bp = Blueprint('prestamos', __name__, url_prefix='/prestamos')

# Crear un nuevo préstamo
@prestamo_bp.route('', methods=['POST'])
def crear_prestamo():
    data = request.get_json()

    usuario = Usuario.query.get(data['usuario_id'])
    libro = Libro.query.get(data['libro_id'])

    if not usuario or not libro:
        return jsonify({'error': 'Usuario o libro no encontrado'}), 404

    if libro.estado != 'disponible':
        return jsonify({'error': 'El libro no está disponible'}), 400

    nuevo_prestamo = Prestamo(
        usuario_id=data['usuario_id'],
        libro_id=data['libro_id']
    )

    libro.estado = 'prestado'

    db.session.add(nuevo_prestamo)
    db.session.commit()

    return jsonify({'message': 'Préstamo creado exitosamente'}), 201

# Devolver un libro
@prestamo_bp.route('/<int:id>/devolver', methods=['PUT'])
def devolver_libro(id):
    prestamo = Prestamo.query.get_or_404(id)
    prestamo.fecha_devolucion = datetime.utcnow()

    libro = Libro.query.get(prestamo.libro_id)
    libro.estado = 'disponible'

    db.session.commit()

    return jsonify({'message': 'Libro devuelto exitosamente'})

# Obtener todos los préstamos
@prestamo_bp.route('/', methods=['GET'])
def obtener_prestamos():
    prestamos = Prestamo.query.all()
    prestamos_data = [
        {
            'id': p.id,
            'usuario_id': p.usuario_id,
            'libro_id': p.libro_id,
            'fecha_prestamo': p.fecha_prestamo,
            'fecha_devolucion': p.fecha_devolucion
        } for p in prestamos
    ]
    return jsonify(prestamos_data)
