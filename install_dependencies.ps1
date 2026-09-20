$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not (Test-Path ".venv")) {
    Write-Host "Criando ambiente virtual .venv..."
    py -m venv .venv
}

Write-Host "Ativando ambiente virtual..."
try {
    & ".\.venv\Scripts\Activate.ps1"
}
catch {
    Write-Host "A ativação foi bloqueada pela política de execução. Ajustando para o usuário atual..."
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
    & ".\.venv\Scripts\Activate.ps1"
}

Write-Host "Atualizando pip..."
python -m pip install --upgrade pip

Write-Host "Instalando dependências do projeto..."
python -m pip install -r requirements.txt

Write-Host ""
Write-Host "Instalação concluída."
Write-Host "Agora rode:"
Write-Host "  python manage.py migrate"
Write-Host "  python manage.py runserver"
