"""
Endpoints de autenticación: Registro e Inicio de sesión de usuarios
"""
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserRegister, UserLogin, AuthResponse, UserResponse, MessageResponse
from app.database import users_db
from datetime import datetime

router = APIRouter(
    prefix="/auth",
    tags=["Autenticación"],
    responses={404: {"description": "Not found"}}
)


@router.post(
    "/register",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Registra un nuevo usuario en el sistema. El email debe ser único."
)
async def register_user(user: UserRegister):
    """
    Registra un nuevo usuario con los siguientes datos:
    - **name**: Nombre completo del usuario
    - **email**: Correo electrónico único
    - **password**: Contraseña (mínimo 6 caracteres)
    
    Retorna un mensaje de éxito o error.
    """
    # Validar si el email ya existe
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado."
        )
    
    # Crear nuevo usuario
    new_user = {
        "id": str(int(datetime.now().timestamp() * 1000)),  # Timestamp como ID
        "name": user.name,
        "email": user.email,
        "password": user.password  # En producción, usar hash
    }
    
    users_db.append(new_user)
    
    return MessageResponse(
        success=True,
        message="Registro exitoso. Ahora puedes iniciar sesión."
    )


@router.post(
    "/login",
    response_model=AuthResponse,
    summary="Iniciar sesión",
    description="Inicia sesión con email y contraseña. Retorna un token de autenticación."
)
async def login_user(credentials: UserLogin):
    """
    Inicia sesión con:
    - **email**: Correo electrónico registrado
    - **password**: Contraseña del usuario
    
    Retorna un token de autenticación y los datos del usuario.
    """
    # Buscar usuario
    user = next((u for u in users_db if u["email"] == credentials.email), None)
    
    # Validar credenciales
    if not user or user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas."
        )
    
    # Generar token simulado
    token = f"simulated-token-{user['id']}-{int(datetime.now().timestamp() * 1000)}"
    
    # Preparar respuesta
    user_response = UserResponse(
        id=user["id"],
        name=user["name"],
        email=user["email"]
    )
    
    return AuthResponse(
        success=True,
        message="Inicio de sesión exitoso.",
        token=token,
        user=user_response
    )


@router.get(
    "/users",
    response_model=list[UserResponse],
    summary="Listar todos los usuarios (Desarrollo)",
    description="Endpoint para visualizar todos los usuarios registrados. Solo para desarrollo."
)
async def list_users():
    """
    Lista todos los usuarios registrados (sin contraseñas).
    Útil para desarrollo y debugging.
    """
    return [
        UserResponse(id=u["id"], name=u["name"], email=u["email"])
        for u in users_db
    ]
