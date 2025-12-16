"""
Base de datos simulada en memoria para el proyecto.
En el futuro, esto será reemplazado por Firebase.
"""
from typing import Dict, List
from app.models.schemas import Note, Comment


# ==================== BASE DE DATOS DE USUARIOS ====================
# Lista de usuarios registrados (simulación)
users_db: List[Dict] = []


# ==================== BASE DE DATOS DE NOTAS ====================
# Estructura: { "categoria": [lista de notas] }
notes_db: Dict[str, List[Note]] = {
    "Algoritmos": [
        Note(
            id=1,
            title="Apuntes de Algoritmos",
            author="Carlos Ruiz",
            rating=5.0,
            downloads=120,
            preview="Introducción a estructuras de control y funciones..."
        ),
        Note(
            id=2,
            title="Ejercicios básicos",
            author="Ana López",
            rating=4.0,
            downloads=85,
            preview="Listas, bucles y diagramas de flujo..."
        ),
    ],
    "Bases de datos": [
        Note(
            id=3,
            title="Apuntes de SQL",
            author="Pedro Torres",
            rating=5.0,
            downloads=200,
            preview="Normalización, consultas básicas y avanzadas..."
        ),
        Note(
            id=4,
            title="Diseño de BD",
            author="María González",
            rating=4.0,
            downloads=150,
            preview="Modelado relacional y ER diagrams..."
        ),
    ],
    "Redes": [
        Note(
            id=5,
            title="Fundamentos de redes",
            author="Luis Gómez",
            rating=5.0,
            downloads=90,
            preview="Topologías, protocolos y direccionamiento IP..."
        ),
        Note(
            id=6,
            title="Configuraciones Cisco",
            author="Laura Pérez",
            rating=4.0,
            downloads=60,
            preview="Configuración básica de routers y switches..."
        ),
        Note(
            id=7,
            title="Configuraciones GNS3",
            author="Laura Pérez",
            rating=3.0,
            downloads=30,
            preview="Configuración básica de gns3 y..."
        ),
    ],
}


# ==================== BASE DE DATOS DE COMENTARIOS ====================
# Estructura: { note_id: [lista de comentarios] }
comments_db: Dict[int, List[Comment]] = {
    1: [
        Comment(
            id=1,
            author="Lucía Pérez",
            date="2024-10-10",
            text="Muy buenos apuntes, me sirvieron mucho!"
        ),
        Comment(
            id=2,
            author="David Rojas",
            date="2024-10-12",
            text="Podrías agregar ejemplos de recursividad?"
        ),
    ],
    2: [
        Comment(
            id=3,
            author="Laura Torres",
            date="2024-10-15",
            text="Excelente guía para estudiar antes del parcial!"
        ),
    ],
    3: [
        Comment(
            id=4,
            author="Juan Gómez",
            date="2024-10-17",
            text="El apartado de consultas JOIN está muy claro 👏"
        ),
    ],
    4: [],
}


# ==================== BASE DE DATOS DE FAVORITOS ====================
# Estructura: { user_id: [lista de note_ids favoritos] }
favorites_db: Dict[str, List[int]] = {}


# ==================== FUNCIONES AUXILIARES ====================

def get_next_note_id() -> int:
    """Obtiene el siguiente ID disponible para una nota"""
    max_id = 0
    for notes_list in notes_db.values():
        for note in notes_list:
            if note.id > max_id:
                max_id = note.id
    return max_id + 1


def get_next_comment_id() -> int:
    """Obtiene el siguiente ID disponible para un comentario"""
    max_id = 0
    for comments_list in comments_db.values():
        for comment in comments_list:
            if comment.id > max_id:
                max_id = comment.id
    return max_id + 1


def get_all_notes() -> List[Note]:
    """Obtiene todas las notas de todas las categorías"""
    all_notes = []
    for notes_list in notes_db.values():
        all_notes.extend(notes_list)
    return all_notes


def get_note_by_id(note_id: int) -> Note | None:
    """Busca una nota por su ID"""
    for notes_list in notes_db.values():
        for note in notes_list:
            if note.id == note_id:
                return note
    return None
