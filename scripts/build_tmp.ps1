if(!(Test-Path -Path "./main.py")){
    cd ..
}
.\venv\Scripts\activate
pyinstaller --hiddenimport win32timezone --hiddenimport win32serviceutil --hiddenimport win32service --hiddenimport win32event --hiddenimport servicemanager --onefile --clean --name=PyPNFtmp --icon resource/pypnf.ico --log-level DEBUG simplest_win_service.py
Copy-Item .\config.ini .\dist\
Copy-Item .\scripts\service_control\* .\dist\
deactivate
