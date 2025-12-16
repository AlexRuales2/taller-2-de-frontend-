"""
Aplicación principal FastAPI - Sistema de Gestión de Apuntes Académicos
Backend API RESTful para el proyecto del corte 3

Autor: Alexander Ruales
Fecha: Noviembre 2025
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, notes, comments

# ==================== CONFIGURACIÓN DE LA API ====================

app = FastAPI(
    title="API Sistema de Gestión de Apuntes Académicos",
    description="""
    ## 📚 Sistema de Gestión de Apuntes Académicos
    
    API RESTful desarrollada con FastAPI para la gestión de apuntes y materiales académicos.
    
    ### Funcionalidades principales:
    
    * **Autenticación de Usuarios**: Registro e inicio de sesión
    * **Gestión de Notas**: Crear, listar y buscar apuntes por categoría
    * **Sistema de Favoritos**: Marcar notas como favoritas
    * **Comentarios**: Añadir y gestionar comentarios en las notas
    * **Categorías**: Organización de notas por materias
    
    ### Arquitectura:
    
    - **Backend**: FastAPI + Pydantic (Validación de datos)
    - **Frontend Futuro**: React 19 + Axios + Zustand
    - **Persistencia Futura**: Firebase (actualmente simulada en memoria)
    
    ### Documentación:
    
    - **Swagger UI**: `/docs` (esta página)
    - **ReDoc**: `/redoc`
    
    ---
    
    **Nota**: Esta API utiliza datos simulados en memoria. En el proyecto final se integrará 
    con Firebase para persistencia real de datos.
    """,
    version="1.0.0",
    contact={
        "name": "Alexander Ruales",
        "email": "alexander.ruales@example.com",
    },
    license_info={
        "name": "MIT",
    },
    docs_url="/docs",
    redoc_url="/redoc"
)


# ==================== CONFIGURACIÓN DE CORS ====================
# Permite que el frontend React pueda consumir la API

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # React default
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los headers
)


# ==================== REGISTRO DE ROUTERS ====================

# Router de autenticación
app.include_router(auth.router)

# Router de notas
app.include_router(notes.router)

# Router de comentarios
app.include_router(comments.router)


# ==================== ENDPOINTS RAÍZ ====================

@app.get(
    "/",
    tags=["Root"],
    summary="Endpoint raíz",
    description="Información básica de la API"
)
async def root():
    """
    Endpoint raíz que retorna información básica de la API.
    """
    return {
        "message": "API Sistema de Gestión de Apuntes Académicos",
        "version": "1.0.0",
        "status": "active",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints": {
            "auth": "/auth",
            "notes": "/notes",
            "comments": "/comments"
        }
    }


@app.get(
    "/health",
    tags=["Root"],
    summary="Health check",
    description="Verifica el estado de la API"
)
async def health_check():
    """
    Endpoint de health check para verificar que la API está funcionando.
    """
    return {
        "status": "healthy",
        "message": "API funcionando correctamente"
    }


# ==================== PUNTO DE ENTRADA ====================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  🚀 API Sistema de Gestión de Apuntes Académicos          ║
    ║                                                            ║
    ║  📖 Documentación: http://localhost:8000/docs             ║
    ║  🔄 ReDoc: http://localhost:8000/redoc                    ║
    ║                                                            ║
    ║  Presiona Ctrl+C para detener el servidor                ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Hot reload para desarrollo
        log_level="info"
    )
