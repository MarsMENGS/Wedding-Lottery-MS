@echo off
chcp 936 >nul 2>&1
echo ==============================
echo  Lottery System Build Script
echo ==============================
echo.

:: 1. Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    pause
    exit /b 1
)

:: 2. Install dependencies
echo [1/3] Install dependencies...
python -m pip install --upgrade pip
python -m pip install PySide6 pyinstaller

:: 3. Build
echo [2/3] Building...
python -m PyInstaller build.spec --clean -y

:: 4. Finish
echo [3/3] Build finished!
echo Output: dist\婚礼抽奖系统.exe
echo.
pause