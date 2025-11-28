# 📚 API Sistema de Gestión de Apuntes Académicos

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-2.5.3-E92063?style=for-the-badge&logo=pydantic&logoColor=white)

Backend API RESTful desarrollado con **FastAPI** para la gestión de apuntes y materiales académicos. Este proyecto forma parte del corte 3 y representa el desacoplamiento de un proyecto monolítico hacia una arquitectura cliente-servidor.

---

## 🎯 Características Principales

✅ **Autenticación de Usuarios**
- Registro de nuevos usuarios
- Inicio de sesión con validación de credenciales
- Generación de tokens de autenticación simulados

✅ **Gestión de Notas**
- Crear notas/apuntes con categorías
- Listar notas por categoría
- Obtener detalles de notas específicas
- Búsqueda de notas por título

✅ **Sistema de Favoritos**
- Marcar/desmarcar notas como favoritas por usuario
- Listar notas favoritas de un usuario

✅ **Sistema de Comentarios**
- Añadir comentarios a las notas
- Listar comentarios por nota
- Eliminar comentarios

✅ **Categorías Dinámicas**
- Organización por materias académicas
- Creación automática de categorías

---

## 🏗️ Arquitectura del Proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Punto de entrada de la aplicación
│   ├── database.py          # Base de datos simulada en memoria
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py       # Modelos Pydantic para validación
│   └── routes/
│       ├── __init__.py
│       ├── auth.py          # Endpoints de autenticación
│       ├── notes.py         # Endpoints de gestión de notas
│       └── comments.py      # Endpoints de comentarios
├── screenshots/             # Capturas de Swagger UI
├── requirements.txt         # Dependencias del proyecto
├── .gitignore
└── README.md
```

---

## 🚀 Instalación y Ejecución

### Prerrequisitos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar el Repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd backend
```

### Paso 2: Crear Entorno Virtual

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar la API

**Opción 1: Usando Uvicorn directamente**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Opción 2: Ejecutando el archivo main.py**
```bash
python app/main.py
```

### Paso 5: Acceder a la Documentación

Una vez iniciado el servidor, accede a:

- **Swagger UI (Interactiva)**: http://localhost:8000/docs
- **ReDoc (Documentación)**: http://localhost:8000/redoc
- **API Root**: http://localhost:8000/

---

## 📡 Endpoints Disponibles

### 🔐 Autenticación (`/auth`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/auth/register` | Registrar nuevo usuario |
| POST | `/auth/login` | Iniciar sesión |
| GET | `/auth/users` | Listar usuarios (desarrollo) |

### 📝 Notas (`/notes`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/notes/categories` | Obtener todas las categorías |
| GET | `/notes/category/{category_name}` | Obtener notas por categoría |
| GET | `/notes/all` | Obtener todas las notas |
| GET | `/notes/{note_id}` | Obtener nota por ID |
| POST | `/notes/create` | Crear nueva nota |
| GET | `/notes/search/?query=texto` | Buscar notas por título |
| POST | `/notes/favorites/toggle` | Marcar/desmarcar favorito |
| GET | `/notes/favorites/{user_id}` | Obtener favoritos del usuario |

### 💬 Comentarios (`/comments`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/comments/note/{note_id}` | Obtener comentarios de una nota |
| POST | `/comments/create` | Crear nuevo comentario |
| GET | `/comments/all` | Obtener todos los comentarios (desarrollo) |
| DELETE | `/comments/{comment_id}` | Eliminar comentario |

---

## 📸 Capturas de Pantalla - Swagger UI

### Documentación Interactiva de la API

![Swagger UI - Endpoints](./screenshots/swagger-endpoints.png)
*Vista general de todos los endpoints disponibles en la API*

### Ejemplos de Endpoints

![Swagger UI - Auth](./screenshots/swagger-auth.png)
*Endpoints de autenticación: registro e inicio de sesión*

![Swagger UI - Notes](./screenshots/swagger-notes.png)
*Endpoints de gestión de notas y categorías*

![Swagger UI - Comments](./screenshots/swagger-comments.png)
*Endpoints del sistema de comentarios*

---

## 🧪 Ejemplos de Uso

### Registrar Usuario

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Pérez",
    "email": "juan.perez@example.com",
    "password": "password123"
  }'
```

### Iniciar Sesión

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan.perez@example.com",
    "password": "password123"
  }'
```

### Crear Nueva Nota

```bash
curl -X POST "http://localhost:8000/notes/create" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introducción a Python",
    "category": "Programación",
    "author": "Juan Pérez",
    "preview": "Conceptos básicos de Python: variables, tipos de datos..."
  }'
```

### Buscar Notas

```bash
curl -X GET "http://localhost:8000/notes/search/?query=algoritmos"
```

---

## 🔧 Tecnologías Utilizadas

- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web moderno y rápido para Python
- **[Pydantic](https://docs.pydantic.dev/)** - Validación de datos y configuración
- **[Uvicorn](https://www.uvicorn.org/)** - Servidor ASGI de alto rendimiento
- **[Python 3.11+](https://www.python.org/)** - Lenguaje de programación

---

## 🎓 Proyecto Académico

Este proyecto es parte del **Corte 3** de la asignatura de Frontend, donde se implementa:

1. ✅ **Desacoplamiento del Backend**: Separación de la lógica de negocio del frontend
2. ✅ **API RESTful**: Implementación de endpoints siguiendo buenas prácticas REST
3. ✅ **Documentación Automática**: Uso de Swagger/OpenAPI integrado en FastAPI
4. ⏳ **Integración Futura con Firebase**: Para persistencia real de datos
5. ⏳ **Consumo desde React 19**: Frontend con Axios y Zustand

---

## 🔮 Próximos Pasos (Proyecto Final)

- [ ] Integración con Firebase para persistencia real
- [ ] Implementación de autenticación JWT
- [ ] Frontend con React 19 + Axios + Zustand
- [ ] Sistema de calificaciones y ratings
- [ ] Upload de archivos (PDFs, imágenes)
- [ ] Sistema de notificaciones
- [ ] Paginación de resultados

---

## 👨‍💻 Autor

**Alexander Ruales**
- Sexto Semestre - Frontend
- Universidad: [Tu Universidad]
- Email: [tu-email@ejemplo.com]

---

## 📄 Licencia

Este proyecto es académico y está bajo la licencia MIT para fines educativos.

---

## 🤝 Contribuciones

Este es un proyecto académico individual. Las sugerencias son bienvenidas a través de issues en el repositorio.

---

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:
1. Revisa la documentación en `/docs`
2. Verifica que todas las dependencias estén instaladas
3. Asegúrate de estar usando Python 3.11 o superior

---

**¡Gracias por revisar este proyecto! 🚀**
