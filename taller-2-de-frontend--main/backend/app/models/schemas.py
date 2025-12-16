"""
Modelos de datos usando Pydantic para validación y documentación automática.
Estos modelos representan las entidades principales del sistema de gestión de apuntes.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime


# ==================== MODELOS DE AUTENTICACIÓN ====================

class UserRegister(BaseModel):
    """Modelo para registro de nuevos usuarios"""
    name: str = Field(..., min_length=2, max_length=100, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Juan Pérez",
                "email": "juan.perez@example.com",
                "password": "password123"
            }]
        }
    }


class UserLogin(BaseModel):
    """Modelo para inicio de sesión"""
    email: EmailStr = Field(..., description="Correo electrónico registrado")
    password: str = Field(..., description="Contraseña del usuario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "email": "juan.perez@example.com",
                "password": "password123"
            }]
        }
    }


class UserResponse(BaseModel):
    """Modelo de respuesta de usuario (sin contraseña)"""
    id: str
    name: str
    email: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "1234567890",
                "name": "Juan Pérez",
                "email": "juan.perez@example.com"
            }]
        }
    }


class AuthResponse(BaseModel):
    """Modelo de respuesta de autenticación exitosa"""
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[UserResponse] = None
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "success": True,
                "message": "Inicio de sesión exitoso",
                "token": "simulated-token-1234567890-1234567890",
                "user": {
                    "id": "1234567890",
                    "name": "Juan Pérez",
                    "email": "juan.perez@example.com"
                }
            }]
        }
    }


# ==================== MODELOS DE NOTAS ====================

class NoteBase(BaseModel):
    """Modelo base para una nota/apunte"""
    title: str = Field(..., min_length=3, max_length=200, description="Título del apunte")
    preview: str = Field(..., min_length=10, description="Vista previa o descripción del contenido")


class NoteCreate(NoteBase):
    """Modelo para crear una nueva nota"""
    category: str = Field(..., min_length=2, description="Categoría o materia del apunte")
    author: str = Field(..., min_length=2, description="Autor del apunte")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "title": "Introducción a Python",
                "category": "Programación",
                "author": "María González",
                "preview": "Conceptos básicos de Python: variables, tipos de datos, funciones..."
            }]
        }
    }


class Note(NoteBase):
    """Modelo completo de una nota"""
    id: int
    author: str
    rating: float = Field(default=5.0, ge=0, le=5)
    downloads: int = Field(default=0, ge=0)
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "title": "Introducción a Python",
                "author": "María González",
                "rating": 4.5,
                "downloads": 150,
                "preview": "Conceptos básicos de Python: variables, tipos de datos, funciones..."
            }]
        }
    }


class Category(BaseModel):
    """Modelo para una categoría de notas"""
    id: int
    name: str
    count: int = Field(default=0, ge=0, description="Cantidad de notas en esta categoría")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "name": "Algoritmos",
                "count": 5
            }]
        }
    }


class FavoriteToggle(BaseModel):
    """Modelo para marcar/desmarcar favoritos"""
    note_id: int = Field(..., gt=0, description="ID de la nota a marcar/desmarcar como favorita")
    user_id: str = Field(..., description="ID del usuario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "note_id": 1,
                "user_id": "1234567890"
            }]
        }
    }


# ==================== MODELOS DE COMENTARIOS ====================

class CommentCreate(BaseModel):
    """Modelo para crear un nuevo comentario"""
    note_id: int = Field(..., gt=0, description="ID de la nota a comentar")
    author: str = Field(..., min_length=2, description="Nombre del autor del comentario")
    text: str = Field(..., min_length=1, max_length=500, description="Texto del comentario")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "note_id": 1,
                "author": "Carlos López",
                "text": "Excelente material, muy útil para el parcial!"
            }]
        }
    }


class Comment(BaseModel):
    """Modelo completo de un comentario"""
    id: int
    author: str
    date: str
    text: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "author": "Carlos López",
                "date": "2024-11-27",
                "text": "Excelente material, muy útil para el parcial!"
            }]
        }
    }


# ==================== MODELOS DE RESPUESTA GENÉRICOS ====================

class MessageResponse(BaseModel):
    """Modelo genérico de respuesta con mensaje"""
    success: bool
    message: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "success": True,
                "message": "Operación exitosa"
            }]
        }
    }


class NotesResponse(BaseModel):
    """Modelo de respuesta con lista de notas"""
    success: bool
    notes: List[Note]
    count: int
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "success": True,
                "notes": [
                    {
                        "id": 1,
                        "title": "Introducción a Python",
                        "author": "María González",
                        "rating": 4.5,
                        "downloads": 150,
                        "preview": "Conceptos básicos..."
                    }
                ],
                "count": 1
            }]
        }
    }
