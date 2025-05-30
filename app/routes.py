from flask import Blueprint, request, jsonify
from .models import Libro
from .database import db

libro_bp = Blueprint('libros', __name__, url_prefix='/libros')

# Crear un nuevo libro
@libro_bp.route('', methods=['POST'])
def crear_libro():
    data = request.get_json()

    nuevo_libro = Libro(
        titulo=data['titulo'],
        autor=data['autor'],
        isbn=data.get('isbn', ''),             # Evitar error si no envían
        categoria=data.get('categoria', ''),
        estado=data.get('estado', 'disponible')
    )

    db.session.add(nuevo_libro)
    db.session.commit()

    return jsonify({'message': 'Libro creado exitosamente!'}), 201

# Obtener todos los libros
@libro_bp.route('/', methods=['GET'])
def obtener_libros():
    libros = Libro.query.all()
    libros_data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'isbn': libro.isbn,
            'categoria': libro.categoria,
            'estado': libro.estado,
            'fecha_creacion': libro.fecha_creacion
        } for libro in libros
    ]
    return jsonify(libros_data)

# Obtener un libro específico
@libro_bp.route('/<int:id>', methods=['GET'])
def obtener_libro(id):
    libro = Libro.query.get_or_404(id)
    libro_data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'autor': libro.autor,
        'isbn': libro.isbn,
        'categoria': libro.categoria,
        'estado': libro.estado,
        'fecha_creacion': libro.fecha_creacion
    }
    return jsonify(libro_data)

# Actualizar un libro
@libro_bp.route('/<int:id>', methods=['PUT'])
def actualizar_libro(id):
    libro = Libro.query.get_or_404(id)
    data = request.get_json()

    libro.titulo = data['titulo']
    libro.autor = data['autor']
    libro.isbn = data.get('isbn', libro.isbn)
    libro.categoria = data.get('categoria', libro.categoria)
    libro.estado = data.get('estado', libro.estado)

    db.session.commit()

    return jsonify({'message': 'Libro actualizado exitosamente!'})

# Eliminar un libro
@libro_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_libro(id):
    libro = Libro.query.get_or_404(id)
    db.session.delete(libro)
    db.session.commit()

    return jsonify({'message': 'Libro eliminado exitosamente!'})

# Buscar libros
@libro_bp.route('/buscar', methods=['GET'])
def buscar_libros():
    titulo = request.args.get('titulo')
    autor = request.args.get('autor')
    categoria = request.args.get('categoria')

    query = Libro.query

    if titulo:
        query = query.filter(Libro.titulo.ilike(f'%{titulo}%'))
    if autor:
        query = query.filter(Libro.autor.ilike(f'%{autor}%'))
    if categoria:
        query = query.filter(Libro.categoria.ilike(f'%{categoria}%'))

    libros = query.all()

    libros_data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autor': libro.autor,
            'isbn': libro.isbn,
            'categoria': libro.categoria,
            'estado': libro.estado,
            'fecha_creacion': libro.fecha_creacion
        } for libro in libros
    ]
    return jsonify(libros_data)
