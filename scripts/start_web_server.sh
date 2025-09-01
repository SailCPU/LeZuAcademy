#!/bin/bash

# 乐族学园 Web服务启动脚本
# 适用于Ubuntu系统

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录的上级目录（项目根目录）
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  乐族学园 Web服务启动脚本${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到Python3${NC}"
    echo "请先安装Python3: sudo apt update && sudo apt install python3"
    exit 1
fi

# 检查端口是否被占用
PORT=8000
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    echo -e "${YELLOW}警告: 端口 $PORT 已被占用${NC}"
    PORT=$((PORT + 1))
    if [ $PORT -gt 8010 ]; then
        echo -e "${RED}错误: 无法找到可用端口${NC}"
        exit 1
    fi
done

echo -e "${GREEN}项目根目录: $PROJECT_ROOT${NC}"
echo -e "${GREEN}使用端口: $PORT${NC}"
echo ""

# 显示可用的项目
echo -e "${BLUE}可用的项目:${NC}"
if [ -d "projects" ]; then
    for project in projects/*/; do
        if [ -d "$project" ]; then
            project_name=$(basename "$project")
            echo "  - $project_name"
        fi
    done
fi
echo ""

# 启动web服务器
echo -e "${GREEN}正在启动Web服务器...${NC}"
echo -e "${GREEN}访问地址: http://localhost:$PORT${NC}"
echo -e "${GREEN}主页面: http://localhost:$PORT/index.html${NC}"
echo ""

# 检查是否有index.html文件
if [ -f "index.html" ]; then
    echo -e "${GREEN}找到主页面: index.html${NC}"
else
    echo -e "${YELLOW}警告: 未找到主页面index.html${NC}"
fi

echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
echo ""

# 获取本机IP地址
get_local_ip() {
    # 尝试多种方式获取本机IP
    local ip=""
    
    # 方法1: 通过hostname获取
    if command -v hostname &> /dev/null; then
        ip=$(hostname -I | awk '{print $1}')
    fi
    
    # 方法2: 通过ip命令获取
    if [ -z "$ip" ] && command -v ip &> /dev/null; then
        ip=$(ip route get 1.1.1.1 | awk '{print $7}' | head -n1)
    fi
    
    # 方法3: 通过ifconfig获取
    if [ -z "$ip" ] && command -v ifconfig &> /dev/null; then
        ip=$(ifconfig | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1' | head -n1)
    fi
    
    echo "$ip"
}

# 获取本机IP地址
LOCAL_IP=$(get_local_ip)

if [ -n "$LOCAL_IP" ]; then
    echo -e "${GREEN}局域网访问地址:${NC}"
    echo -e "${GREEN}  http://$LOCAL_IP:$PORT${NC}"
    echo -e "${GREEN}  http://$LOCAL_IP:$PORT/index.html${NC}"
    echo ""
else
    echo -e "${YELLOW}警告: 无法获取本机IP地址${NC}"
    echo -e "${YELLOW}局域网访问可能受限${NC}"
    echo ""
fi

# 启动Python HTTP服务器
python3 -m http.server $PORT --bind 0.0.0.0 --directory "$PROJECT_ROOT"
