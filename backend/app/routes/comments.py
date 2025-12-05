"""
Endpoints de gestión de comentarios
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from app.models.schemas import Comment, CommentCreate, MessageResponse
from app.database import comments_db, get_next_comment_id, get_note_by_id

router = APIRouter(
    prefix="/comments",
    tags=["Comentarios"],
    responses={404: {"description": "Not found"}}
)


@router.get(
    "/note/{note_id}",
    response_model=List[Comment],
    summary="Obtener comentarios de una nota",
    description="Retorna todos los comentarios asociados a una nota específica."
)
async def get_comments_by_note(note_id: int):
    """
    Obtiene todos los comentarios de una nota específica.
    
    - **note_id**: ID de la nota
    
    Retorna una lista de comentarios con autor, fecha y texto.
    """
    # Verificar que la nota existe
    note = get_note_by_id(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {note_id} no encontrada."
        )
    
    # Retornar comentarios (lista vacía si no hay comentarios)
    return comments_db.get(note_id, [])


@router.post(
    "/create",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo comentario",
    description="Añade un nuevo comentario a una nota específica."
)
async def create_comment(comment_data: CommentCreate):
    """
    Crea un nuevo comentario con:
    - **note_id**: ID de la nota a comentar
    - **author**: Nombre del autor del comentario
    - **text**: Texto del comentario (máximo 500 caracteres)
    """
    # Verificar que la nota existe
    note = get_note_by_id(comment_data.note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nota con ID {comment_data.note_id} no encontrada."
        )
    
    # Crear el nuevo comentario
    new_comment = Comment(
        id=get_next_comment_id(),
        author=comment_data.author,
        date=datetime.now().strftime("%Y-%m-%d"),
        text=comment_data.text
    )
    
    # Inicializar lista de comentarios si no existe
    if comment_data.note_id not in comments_db:
        comments_db[comment_data.note_id] = []
    
    # Añadir comentario
    comments_db[comment_data.note_id].append(new_comment)
    
    return MessageResponse(
        success=True,
        message=f"Comentario añadido exitosamente a la nota '{note.title}'."
    )


@router.get(
    "/all",
    response_model=dict,
    summary="Obtener todos los comentarios (Desarrollo)",
    description="Retorna todos los comentarios del sistema. Solo para desarrollo."
)
async def get_all_comments():
    """
    Obtiene todos los comentarios del sistema organizados por nota.
    Útil para desarrollo y debugging.
    """
    return {
        "success": True,
        "comments": comments_db,
        "total_notes_with_comments": len(comments_db)
    }


@router.delete(
    "/{comment_id}",
    response_model=MessageResponse,
    summary="Eliminar comentario",
    description="Elimina un comentario específico por su ID."
)
async def delete_comment(comment_id: int):
    """
    Elimina un comentario específico:
    - **comment_id**: ID del comentario a eliminar
    """
    # Buscar y eliminar el comentario
    for note_id, comments_list in comments_db.items():
        for idx, comment in enumerate(comments_list):
            if comment.id == comment_id:
                deleted_comment = comments_list.pop(idx)
                return MessageResponse(
                    success=True,
                    message=f"Comentario de '{deleted_comment.author}' eliminado exitosamente."
                )
    
    # Si no se encontró
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Comentario con ID {comment_id} no encontrado."
    )
