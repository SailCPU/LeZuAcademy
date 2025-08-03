#!/bin/bash
# 封面PDF导出脚本 - Linux/Mac版本

echo "📚 柯南侦探英语冒险 - 封面PDF导出工具"
echo "=================================================="

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装Python"
    exit 1
fi

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "📂 项目目录: $PROJECT_DIR"

# 进入项目目录
cd "$PROJECT_DIR"

# 检查封面文件是否存在
if [ ! -f "book_cover.html" ]; then
    echo "❌ 封面文件不存在: book_cover.html"
    exit 1
fi

if [ ! -f "book_back_cover.html" ]; then
    echo "❌ 后封面文件不存在: book_back_cover.html"
    exit 1
fi

echo "✅ 封面文件检查通过"

# 检查Python依赖
echo "🔍 检查Python依赖..."
python3 -c "import weasyprint" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ weasyprint未安装"
    echo "📦 正在安装依赖..."
    
    # 检查requirements文件
    if [ -f "tools/requirements_pdf.txt" ]; then
        python3 -m pip install -r tools/requirements_pdf.txt
    else
        python3 -m pip install weasyprint
    fi
    
    # 再次检查
    python3 -c "import weasyprint" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "❌ 依赖安装失败，请手动安装:"
        echo "   pip install weasyprint"
        exit 1
    fi
fi

echo "✅ 依赖检查通过"

# 运行导出脚本
echo "🚀 开始导出封面..."

# 如果没有参数，默认使用A4模式（适合家庭打印）
if [ $# -eq 0 ]; then
    echo "💡 使用A4打印模式（家庭打印机友好）"
    python3 tools/export_cover.py a4
else
    python3 tools/export_cover.py "$@"
fi

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 封面导出完成！"
    echo ""
    echo "📁 查看导出文件:"
    ls -la output/*.pdf 2>/dev/null | grep -E "(封面|后封面)" || echo "   未找到封面PDF文件"
    
    echo ""
    echo "💡 使用建议:"
    echo "   📋 A4版本："
    echo "      1. 直接A4纸打印，16开本内容居中显示"
    echo "      2. 打印后可裁剪到16开本尺寸 (185×260mm)"
    echo "      3. 建议使用厚纸（如卡纸）作为封面"
    echo "   📋 专业版本："
    echo "      1. 发送给印刷厂制作16开本"
    echo "      2. 要求250g铜版纸，可覆膜"
    echo ""
    echo "🎯 其他导出选项:"
    echo "   ./tools/export_cover.sh a4           # 仅A4版本"
    echo "   ./tools/export_cover.sh professional # 仅专业版本"
    echo "   ./tools/export_cover.sh both         # 导出所有版本"
    echo "   ./tools/export_cover.sh help         # 查看完整帮助"
else
    echo "❌ 导出失败，请检查错误信息"
    exit 1
fi