#!/bin/bash
# 缓存清理脚本 - BeiTianDa项目

echo "🧹 BeiTianDa 缓存清理工具"
echo "=========================="

# 获取脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_DIR="$PROJECT_DIR/output"

# 检查缓存目录是否存在
if [ ! -d "$OUTPUT_DIR" ]; then
    echo "❌ 缓存目录不存在: $OUTPUT_DIR"
    exit 1
fi

echo "📁 缓存目录: $OUTPUT_DIR"
echo

# 显示当前缓存大小
echo "📊 当前缓存使用情况："
du -sh "$OUTPUT_DIR"/* 2>/dev/null || echo "缓存目录为空"
echo

# 询问用户操作
echo "请选择操作："
echo "1) 清理临时文件 (7天前)"
echo "2) 清理日志文件 (30天前)"
echo "3) 清理所有临时文件和日志"
echo "4) 仅显示缓存状态"
echo "5) 退出"
echo

read -p "请输入选择 (1-5): " choice

case $choice in
    1)
        echo "🗑️ 清理7天前的临时文件..."
        find "$OUTPUT_DIR/temp" -type f -mtime +7 -delete 2>/dev/null
        echo "✅ 临时文件清理完成"
        ;;
    2)
        echo "🗑️ 清理30天前的日志文件..."
        find "$OUTPUT_DIR/logs" -type f -name "*.log" -mtime +30 -delete 2>/dev/null
        echo "✅ 日志文件清理完成"
        ;;
    3)
        echo "🗑️ 清理所有临时文件和旧日志..."
        find "$OUTPUT_DIR/temp" -type f -mtime +7 -delete 2>/dev/null
        find "$OUTPUT_DIR/logs" -type f -name "*.log" -mtime +30 -delete 2>/dev/null
        echo "✅ 缓存清理完成"
        ;;
    4)
        echo "📊 缓存状态："
        echo "PDF文件数量: $(find "$OUTPUT_DIR/pdf" -name "*.pdf" -type f 2>/dev/null | wc -l)"
        echo "临时文件数量: $(find "$OUTPUT_DIR/temp" -type f 2>/dev/null | wc -l)"
        echo "日志文件数量: $(find "$OUTPUT_DIR/logs" -name "*.log" -type f 2>/dev/null | wc -l)"
        ;;
    5)
        echo "👋 退出清理工具"
        exit 0
        ;;
    *)
        echo "❌ 无效选择"
        exit 1
        ;;
esac

echo
echo "📊 清理后缓存使用情况："
du -sh "$OUTPUT_DIR"/* 2>/dev/null || echo "缓存目录为空"

echo
echo "✨ 操作完成！"