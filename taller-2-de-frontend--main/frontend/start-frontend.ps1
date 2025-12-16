# Script para iniciar el frontend React
# Uso: .\start-frontend.ps1

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🎨 Iniciando Frontend React                              ║" -ForegroundColor Cyan
Write-Host "║  Sistema de Gestión de Apuntes Académicos                ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar si estamos en la carpeta correcta
if (-Not (Test-Path "package.json")) {
    Write-Host "❌ Error: No se encuentra package.json" -ForegroundColor Red
    Write-Host "   Asegúrate de ejecutar este script desde la carpeta 'frontend'" -ForegroundColor Yellow
    exit 1
}

# Verificar si están instaladas las dependencias
if (-Not (Test-Path "node_modules")) {
    Write-Host "⚠️  No se encontró node_modules. Instalando dependencias..." -ForegroundColor Yellow
    npm install
    Write-Host "✅ Dependencias instaladas" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  ✅ Iniciando servidor de desarrollo...                   ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  🌐 Aplicación: http://localhost:5173                     ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║  Presiona Ctrl+C para detener el servidor                ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Iniciar el servidor
npm run dev
