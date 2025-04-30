from flask import Blueprint, request, jsonify
from .models import Usuario
from .database import db

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

# Crear un nuevo usuario
@usuario_bp.route('', methods=['POST'])
def crear_usuario():
    data = request.get_json()

    nuevo_usuario = Usuario(
        nombre=data['nombre'],
        email=data['email'],
        contrasena=data['contrasena']  # Nota: En producción, usa una librería de hashing para contraseñas
    )

    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario creado exitosamente!'}), 201

# Obtener todos los usuarios
@usuario_bp.route('/', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    usuarios_data = [
        {
            'id': usuario.id,
            'nombre': usuario.nombre,
            'email': usuario.email
        } for usuario in usuarios
    ]
    return jsonify(usuarios_data)

# Obtener un usuario específico
@usuario_bp.route('/<int:id>', methods=['GET'])
def obtener_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario_data = {
        'id': usuario.id,
        'nombre': usuario.nombre,
        'email': usuario.email
    }
    return jsonify(usuario_data)

# Eliminar un usuario
@usuario_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()

    return jsonify({'message': 'Usuario eliminado exitosamente!'})
