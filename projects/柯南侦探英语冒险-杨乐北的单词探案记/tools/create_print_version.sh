#!/bin/bash
# 创建浏览器打印版本脚本 - Linux/macOS版本

echo "================================================================"
echo "               柯南侦探英语冒险 - 创建浏览器打印版"
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
echo

echo "开始创建打印版本..."
$PYTHON_CMD create_print_version.py

if [ $? -eq 0 ]; then
    echo
    echo "✅ 打印版本创建成功！"
    echo "📂 输出目录：../output/"
    
    # 尝试打开输出目录
    if command -v xdg-open &> /dev/null; then
        xdg-open "../output" &> /dev/null
    elif command -v open &> /dev/null; then
        open "../output" &> /dev/null
    fi
else
    echo "❌ 创建失败"
    exit 1
fi

echo
echo "🎉 创建完成！"