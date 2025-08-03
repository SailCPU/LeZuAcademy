@echo off
REM 分章节PDF导出工具 - Windows批处理脚本
echo ========================================
echo 柯南侦探英语冒险 - 分章节PDF导出工具
echo ========================================
echo.

REM 切换到工具目录
cd /d "%~dp0"

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.6+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 显示当前目录
echo 当前目录: %CD%
echo.

REM 检查是否已安装依赖
echo 检查依赖...
python -c "import weasyprint" >nul 2>&1
if errorlevel 1 (
    echo.
    echo 警告: WeasyPrint未安装，将只创建浏览器打印版本
    echo 如需自动PDF导出，请运行: pip install weasyprint
    echo.
    echo 继续创建浏览器打印版本...
    python export_chapters_separately.py --browser-only
) else (
    echo 依赖检查完成，开始导出...
    echo.
    python export_chapters_separately.py
)

echo.
echo 导出完成！
pause