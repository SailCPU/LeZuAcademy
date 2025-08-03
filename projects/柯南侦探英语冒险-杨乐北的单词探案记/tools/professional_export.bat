@echo off
chcp 65001 >nul
echo ================================================================
echo               柯南侦探英语冒险 - 专业印刷级PDF导出
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

echo 检查依赖包...
pip show weasyprint >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 安装专业PDF导出依赖包...
    pip install weasyprint beautifulsoup4 lxml
    if %errorlevel% neq 0 (
        echo ❌ 依赖包安装失败，请手动运行：pip install weasyprint beautifulsoup4 lxml
        pause
        exit /b 1
    )
)

echo 开始专业PDF导出...
echo 输出位置：../output/professional/
%PYTHON_CMD% professional_pdf_export.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ 专业PDF导出成功！
    echo 📂 正在打开输出目录...
    start "" "../output/professional"
) else (
    echo ❌ 导出失败
)

echo.
echo 按任意键退出...
pause >nul