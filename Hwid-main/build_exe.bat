@echo off
echo Instalando dependencias (si no lo estan)...
pip install -r requirements.txt

echo.
echo Compilando a .exe...
pyinstaller --onefile --noconsole --icon=icon.ico --name Hwid main.py

echo.
echo ============================================================
echo Compilacion completada.
echo El ejecutable se encuentra en: dist\Hwid.exe
echo ============================================================
pause
