@echo off
echo ========================================
echo    婚礼抽奖系统 - Windows打包脚本
echo ========================================
echo.

REM 检查Python环境
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 安装依赖...
pip install -r requirements.txt -q

REM 打包
echo [2/3] 打包应用程序...
pyinstaller build.spec --clean -y

echo.
echo [3/3] 打包完成！
echo 输出文件: dist\婚礼抽奖系统.exe
echo.
pause

