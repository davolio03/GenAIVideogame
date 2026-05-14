$ErrorActionPreference = "Stop"

$RequiredPython = "3.10"
$VenvPath = ".\.venv"
$PythonExe = "$VenvPath\Scripts\python.exe"

Write-Host "Verificando Python..."
$PythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"

if ($PythonVersion -ne $RequiredPython) {
    Write-Host "ADVERTENCIA: este proyecto espera Python $RequiredPython, pero encontre Python $PythonVersion."
    Write-Host "Si algo falla, instala Python $RequiredPython y volve a ejecutar este script."
}

if (-not (Test-Path $VenvPath)) {
    Write-Host "Creando entorno virtual en $VenvPath..."
    python -m venv $VenvPath
} else {
    Write-Host "El entorno virtual ya existe en $VenvPath."
}

Write-Host "Actualizando pip..."
try {
    & $PythonExe -m pip install --upgrade pip
} catch {
    Write-Host "No se pudo actualizar pip con SSL normal. Reintentando con hosts confiables..."
    & $PythonExe -m pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org
}

Write-Host "Instalando requirements.txt..."
try {
    & $PythonExe -m pip install -r .\requirements.txt
} catch {
    Write-Host "No se pudo instalar con SSL normal. Reintentando con hosts confiables..."
    & $PythonExe -m pip install -r .\requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
}

Write-Host ""
Write-Host "Entorno listo."
Write-Host "Para generar contenido del juego real:"
Write-Host ".\.venv\Scripts\python.exe .\S16Game\build_prompt.py"
Write-Host ""
Write-Host "Para probar el cliente Mercury manualmente:"
Write-Host ".\.venv\Scripts\python.exe .\api.py"
