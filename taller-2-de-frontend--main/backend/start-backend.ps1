# Script para iniciar el backend FastAPI
# Uso: .\start-backend.ps1

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🚀 Iniciando Backend FastAPI                             ║" -ForegroundColor Cyan
Write-Host "║  Sistema de Gestión de Apuntes Académicos                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en la carpeta correcta
if (-Not (Test-Path "app\main.py")) {
    Write-Host "❌ Error: No se encuentra app\main.py" -ForegroundColor Red
    Write-Host "   Asegúrate de ejecutar este script desde la carpeta 'backend'" -ForegroundColor Yellow
    exit 1
}

# Verificar si existe el entorno virtual
if (-Not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "⚠️  No se encontró el entorno virtual. Creando..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✅ Entorno virtual creado" -ForegroundColor Green
}

# Activar entorno virtual
Write-Host "📦 Activando entorno virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Verificar si están instaladas las dependencias
$pipList = pip list
if ($pipList -notmatch "fastapi") {
    Write-Host "⚠️  Instalando dependencias..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Iniciando servidor...                                 ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  📖 Swagger UI: http://localhost:8000/docs                ║" -ForegroundColor Green
Write-Host "║  📚 ReDoc: http://localhost:8000/redoc                    ║" -ForegroundColor Green
Write-Host "║  🔌 API: http://localhost:8000                            ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  Presiona Ctrl+C para detener el servidor                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Iniciar el servidor
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
