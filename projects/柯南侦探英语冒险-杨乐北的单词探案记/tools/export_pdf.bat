@echo off
chcp 65001 >nul
echo ================================================================
echo               柯南侦探英语冒险 - PDF导出工具
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
    echo 📦 安装依赖包...
    pip install -r requirements_pdf.txt
    if %errorlevel% neq 0 (
        echo ❌ 依赖包安装失败，请手动运行：pip install weasyprint beautifulsoup4 lxml
        pause
        exit /b 1
    )
)

echo 开始导出PDF...
echo 输出位置：../../output/pdf/
cd .. && %PYTHON_CMD% tools/export_to_pdf.py

echo.
echo 按任意键退出...
pause >nul