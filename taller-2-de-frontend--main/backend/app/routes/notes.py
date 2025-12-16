"""
Endpoints de gestión de notas y categorías
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import List
from app.models.schemas import Note, NoteCreate, Category, NotesResponse, MessageResponse, FavoriteToggle
from app.database import notes_db, favorites_db, get_next_note_id, get_all_notes, get_note_by_id

router = APIRouter(
    prefix="/notes",
    tags=["Notas"],
    responses={404: {"description": "Not found"}}
)


@router.get(
    "/categories",
    response_model=List[Category],
    summary="Obtener todas las categorías",
    description="Retorna la lista de todas las categorías disponibles con el conteo de notas en cada una."
)
async def get_categories():
    """
    Obtiene todas las categorías existentes con:
    - **id**: ID único de la categoría
    - **name**: Nombre de la categoría/materia
    - **count**: Cantidad de notas en la categoría
    """
    categories = []
    for idx, (name, notes_list) in enumerate(notes_db.items(), start=1):
        categories.append(Category(
            id=idx,
            name=name,
            count=len(notes_list)
        ))
    return categories


@router.get(
    "/category/{category_name}",
    response_model=NotesResponse,
    summary="Obtener notas por categoría",
    description="Retorna todas las notas de una categoría específica."
)
async def get_notes_by_category(category_name: str):
    """
    Obtiene todas las notas de una categoría específica.
    
    - **category_name**: Nombre de la categoría (ej: "Algoritmos", "Bases de datos")
    """
    # Buscar categoría (case-insensitive)
    category_key = next(
        (key for key in notes_db.keys() if key.lower() == category_name.lower()),
        None
    )
    
    if not category_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría '{category_name}' no encontrada."
        )
    
    notes = notes_db[category_key]
    
    return NotesResponse(
        success=True,
        notes=notes,
        count=len(notes)
    )


@router.get(
    "/all",
    response_model=NotesResponse,
    summary="Obtener todas las notas",
    description="Retorna todas las notas de todas las categorías."
)
async def get_all_notes_endpoint():
    """
    Obtiene todas las notas del sistema, independientemente de su categoría.
    """
    all_notes = get_all_notes()
    
    return NotesResponse(
        success=True,
        notes=all_notes,
        count=len(all_notes)
    )


@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Obtener nota por ID",
    description="Retorna los detalles de una nota específica por su ID."
)
async def get_note_by_id_endpoint(note_id: int):
    """
    Obtiene una nota específica por su ID.
    
    - **note_id**: ID único de la nota
    """
    note = get_note_by_id(note_id)
    
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada."
        )
    
    return note


@router.post(
    "/create",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nueva nota",
    description="Crea una nueva nota en una categoría específica."
)
async def create_note(note_data: NoteCreate):
    """
    Crea una nueva nota con:
    - **title**: Título del apunte
    - **category**: Categoría/materia del apunte
    - **author**: Autor del apunte
    - **preview**: Vista previa o descripción del contenido
    """
    # Obtener el siguiente ID
    new_id = get_next_note_id()
    
    # Crear la nueva nota
    new_note = Note(
        id=new_id,
        title=note_data.title,
        author=note_data.author,
        rating=5.0,  # Rating inicial
        downloads=0,  # Sin descargas inicialmente
        preview=note_data.preview
    )
    
    # Añadir a la categoría (crear categoría si no existe)
    if note_data.category not in notes_db:
        notes_db[note_data.category] = []
    
    notes_db[note_data.category].append(new_note)
    
    return MessageResponse(
        success=True,
        message=f"Nota '{note_data.title}' creada exitosamente en la categoría '{note_data.category}'."
    )


@router.get(
    "/search/",
    response_model=NotesResponse,
    summary="Buscar notas por título",
    description="Busca notas que contengan el texto especificado en su título."
)
async def search_notes(
    query: str = Query(..., min_length=1, description="Texto a buscar en los títulos")
):
    """
    Busca notas por título:
    - **query**: Texto a buscar (case-insensitive)
    
    Retorna todas las notas que contengan el texto en su título.
    """
    all_notes = get_all_notes()
    
    # Filtrar notas que contengan el query en el título
    filtered_notes = [
        note for note in all_notes
        if query.lower() in note.title.lower()
    ]
    
    return NotesResponse(
        success=True,
        notes=filtered_notes,
        count=len(filtered_notes)
    )


@router.post(
    "/favorites/toggle",
    response_model=MessageResponse,
    summary="Marcar/Desmarcar favorito",
    description="Añade o remueve una nota de los favoritos del usuario."
)
async def toggle_favorite(favorite_data: FavoriteToggle):
    """
    Alterna el estado de favorito de una nota:
    - **note_id**: ID de la nota
    - **user_id**: ID del usuario
    """
    # Verificar que la nota existe
    note = get_note_by_id(favorite_data.note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {favorite_data.note_id} no encontrada."
        )
    
    # Inicializar lista de favoritos del usuario si no existe
    if favorite_data.user_id not in favorites_db:
        favorites_db[favorite_data.user_id] = []
    
    user_favorites = favorites_db[favorite_data.user_id]
    
    # Toggle: añadir o remover
    if favorite_data.note_id in user_favorites:
        user_favorites.remove(favorite_data.note_id)
        message = f"Nota '{note.title}' removida de favoritos."
    else:
        user_favorites.append(favorite_data.note_id)
        message = f"Nota '{note.title}' añadida a favoritos."
    
    return MessageResponse(success=True, message=message)


@router.get(
    "/favorites/{user_id}",
    response_model=NotesResponse,
    summary="Obtener notas favoritas del usuario",
    description="Retorna todas las notas marcadas como favoritas por el usuario."
)
async def get_user_favorites(user_id: str):
    """
    Obtiene las notas favoritas de un usuario:
    - **user_id**: ID del usuario
    """
    # Obtener IDs de favoritos del usuario
    favorite_ids = favorites_db.get(user_id, [])
    
    # Obtener las notas correspondientes
    favorite_notes = [
        note for note in get_all_notes()
        if note.id in favorite_ids
    ]
    
    return NotesResponse(
        success=True,
        notes=favorite_notes,
        count=len(favorite_notes)
    )
