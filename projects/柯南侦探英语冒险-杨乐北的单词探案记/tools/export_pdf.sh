#!/bin/bash
# PDF导出脚本 - Linux/macOS版本

echo "================================================================"
echo "               柯南侦探英语冒险 - PDF导出工具"
echo "================================================================"
echo

# 检测Python命令
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ 未找到Python，请先安装Python 3.7+"
    exit 1
fi

echo "✅ 找到Python: $($PYTHON_CMD --version)"

# 检查pip命令
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "❌ 未找到pip，请先安装pip"
    exit 1
fi

# 检查依赖包
echo "检查依赖包..."
if ! $PIP_CMD show weasyprint &> /dev/null; then
    echo "📦 安装依赖包..."
    $PIP_CMD install -r requirements_pdf.txt
    if [ $? -ne 0 ]; then
        echo "❌ 依赖包安装失败，请手动运行：$PIP_CMD install weasyprint beautifulsoup4 lxml"
        exit 1
    fi
fi

echo "开始导出PDF..."
echo "输出位置：../../output/pdf/"
cd .. && $PYTHON_CMD tools/export_to_pdf.py

echo
echo "导出完成！"