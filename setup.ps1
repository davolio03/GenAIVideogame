$ErrorActionPreference = "Stop"

$RequiredPython = "3.10"
$VenvPath = ".\.venv"
$PythonExe = "$VenvPath\Scripts\python.exe"

Write-Host "Verificando Python..."
$PythonVersion = python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"

if ($PythonVersion -ne $RequiredPython) {
    Write-Host "ADVERTENCIA: este proyecto espera Python $RequiredPython, pero encontré Python $PythonVersion."
    Write-Host "Si algo falla, instalá Python $RequiredPython y volvé a ejecutar este script."
}

if (-not (Test-Path $VenvPath)) {
    Write-Host "Creando entorno virtual en $VenvPath..."
    python -m venv $VenvPath
} else {
    Write-Host "El entorno virtual ya existe en $VenvPath."
}

Write-Host "Actualizando pip..."
& $PythonExe -m pip install --upgrade pip

Write-Host "Instalando requirements.txt..."
& $PythonExe -m pip install -r .\requirements.txt

Write-Host ""
Write-Host "Entorno listo."
Write-Host "Para ejecutar el proyecto:"
Write-Host ".\.venv\Scripts\python.exe api.py"
