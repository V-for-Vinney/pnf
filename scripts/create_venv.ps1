if(!(Test-Path -Path "./main.py")){
    cd ..
}

Write-Host "Installing python..." -ForegroundColor Yellow
deactivate
pyenv uninstall 3.4.4-win32
pyenv install 3.4.4-win32

Write-Host "Creating venv..." -ForegroundColor Yellow
Remove-Item -Recurse venv
pyenv exec python -m venv venv
.\venv\Scripts\activate

Write-Host "Installing requirements..." -ForegroundColor Yellow
python -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt
