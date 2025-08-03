@echo off
chcp 65001 >nul
echo ================================================================
echo               柯南侦探英语冒险 - 创建浏览器打印版
echo ================================================================
echo.

echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    python3 --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ 未找到Python，请先安装Python 3.7+
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo 开始创建打印版本...
%PYTHON_CMD% create_print_version.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ 打印版本创建成功！
    echo 📂 正在打开输出目录...
    start "" "../output"
) else (
    echo ❌ 创建失败
)

echo.
echo 按任意键退出...
pause >nul