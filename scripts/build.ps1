if(!(Test-Path -Path "./main.py")){
    cd ..
}
.\venv\Scripts\activate
pyinstaller --hiddenimport win32timezone --onefile --clean --name=PyPNF --icon resource/pypnf.ico --log-level INFO main.py
Copy-Item .\config.ini .\dist\
Copy-Item .\scripts\service_control\* .\dist\
deactivate
