#!/bin/bash
# 分章节PDF导出工具 - Linux/Mac脚本

echo "========================================"
echo "柯南侦探英语冒险 - 分章节PDF导出工具"
echo "========================================"
echo

# 切换到脚本所在目录
cd "$(dirname "$0")"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.6+"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "macOS: brew install python3"
    exit 1
fi

echo "✅ Python版本: $(python3 --version)"
echo "📁 当前目录: $(pwd)"
echo

# 检查是否已安装依赖
echo "🔍 检查依赖..."
if python3 -c "import weasyprint" 2>/dev/null; then
    echo "✅ WeasyPrint已安装，开始完整导出..."
    python3 export_chapters_separately.py
else
    echo
    echo "⚠️  警告: WeasyPrint未安装，将只创建浏览器打印版本"
    echo "如需自动PDF导出，请运行:"
    echo "  pip3 install weasyprint"
    echo "  或者: sudo apt install python3-weasyprint (Ubuntu/Debian)"
    echo
    echo "继续创建浏览器打印版本..."
    python3 -c "
import sys
sys.argv = ['export_chapters_separately.py']
exec(open('export_chapters_separately.py').read())
"
fi

echo
echo "🎉 导出完成！"
echo "按任意键退出..."
read -n 1