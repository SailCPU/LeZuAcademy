#!/bin/bash

# 乐族学园 高级Web服务启动脚本
# 适用于Ubuntu系统，支持多种web服务器

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# 获取脚本所在目录的上级目录（项目根目录）
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 默认配置
DEFAULT_PORT=8000
DEFAULT_SERVER="python"

# 显示帮助信息
show_help() {
    echo -e "${BLUE}乐族学园 Web服务启动脚本 - 使用帮助${NC}"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  -p, --port PORT     指定端口号 (默认: $DEFAULT_PORT)"
    echo "  -s, --server SERVER 指定服务器类型 (默认: $DEFAULT_SERVER)"
    echo "  -h, --help         显示此帮助信息"
    echo ""
    echo "支持的服务器类型:"
    echo "  python             使用Python内置HTTP服务器"
    echo "  node               使用Node.js http-server (如果已安装)"
    echo "  php                使用PHP内置服务器 (如果已安装)"
    echo "  nginx             使用Nginx (如果已安装)"
    echo ""
    echo "示例:"
    echo "  $0                    # 使用默认设置启动"
    echo "  $0 -p 8080           # 在端口8080启动"
    echo "  $0 -s node -p 3000   # 使用Node.js在端口3000启动"
}

# 解析命令行参数
PORT=$DEFAULT_PORT
SERVER_TYPE=$DEFAULT_SERVER

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            PORT="$2"
            shift 2
            ;;
        -s|--server)
            SERVER_TYPE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}未知选项: $1${NC}"
            show_help
            exit 1
            ;;
    esac
done

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  乐族学园 高级Web服务启动脚本${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查端口是否被占用
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1
    fi
    return 0
}

# 查找可用端口
find_available_port() {
    local start_port=$1
    local port=$start_port
    
    while ! check_port $port; do
        echo -e "${YELLOW}警告: 端口 $port 已被占用${NC}"
        port=$((port + 1))
        if [ $port -gt $((start_port + 10)) ]; then
            echo -e "${RED}错误: 无法找到可用端口${NC}"
            exit 1
        fi
    done
    
    echo $port
}

# 检查并安装依赖
check_dependencies() {
    case $SERVER_TYPE in
        python)
            if ! command -v python3 &> /dev/null; then
                echo -e "${RED}错误: 未找到Python3${NC}"
                echo "请先安装Python3: sudo apt update && sudo apt install python3"
                exit 1
            fi
            ;;
        node)
            if ! command -v node &> /dev/null; then
                echo -e "${YELLOW}警告: 未找到Node.js${NC}"
                echo "正在尝试安装Node.js..."
                if command -v curl &> /dev/null; then
                    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                    sudo apt-get install -y nodejs
                else
                    echo -e "${RED}错误: 无法安装Node.js，请手动安装${NC}"
                    exit 1
                fi
            fi
            
            if ! command -v npx &> /dev/null; then
                echo -e "${YELLOW}正在安装http-server...${NC}"
                npm install -g http-server
            fi
            ;;
        php)
            if ! command -v php &> /dev/null; then
                echo -e "${RED}错误: 未找到PHP${NC}"
                echo "请先安装PHP: sudo apt update && sudo apt install php"
                exit 1
            fi
            ;;
        nginx)
            if ! command -v nginx &> /dev/null; then
                echo -e "${RED}错误: 未找到Nginx${NC}"
                echo "请先安装Nginx: sudo apt update && sudo apt install nginx"
                exit 1
            fi
            ;;
    esac
}

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

# 启动服务器
start_server() {
    local port=$1
    local server_type=$2
    
    # 获取本机IP地址
    local local_ip=$(get_local_ip)
    
    echo -e "${GREEN}正在启动 $server_type 服务器...${NC}"
    echo -e "${GREEN}本地访问地址: http://localhost:$port${NC}"
    echo -e "${GREEN}主页面: http://localhost:$port/index.html${NC}"
    
    if [ -n "$local_ip" ]; then
        echo -e "${GREEN}局域网访问地址: http://$local_ip:$port${NC}"
        echo -e "${GREEN}主页面: http://$local_ip:$port/index.html${NC}"
    fi
    echo ""
    
    case $server_type in
        python)
            python3 -m http.server $port --bind 0.0.0.0 --directory "$PROJECT_ROOT"
            ;;
        node)
            npx http-server "$PROJECT_ROOT" -p $port -o -a 0.0.0.0
            ;;
        php)
            php -S 0.0.0.0:$port -t "$PROJECT_ROOT"
            ;;
        nginx)
            # 创建临时nginx配置
            local nginx_conf="/tmp/nginx_temp_$port.conf"
            cat > "$nginx_conf" << EOF
server {
    listen $port;
    server_name _;
    root $PROJECT_ROOT;
    index index.html index.htm;
    
    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF
            sudo nginx -c "$nginx_conf" -g "daemon off;"
            ;;
    esac
}

# 显示项目信息
show_project_info() {
    echo -e "${GREEN}项目根目录: $PROJECT_ROOT${NC}"
    echo -e "${GREEN}使用端口: $PORT${NC}"
    echo -e "${GREEN}服务器类型: $SERVER_TYPE${NC}"
    
    # 获取并显示网络信息
    local local_ip=$(get_local_ip)
    if [ -n "$local_ip" ]; then
        echo -e "${GREEN}本机IP地址: $local_ip${NC}"
        echo -e "${BLUE}网络访问信息:${NC}"
        echo -e "${BLUE}  本地访问: http://localhost:$PORT${NC}"
        echo -e "${BLUE}  局域网访问: http://$local_ip:$PORT${NC}"
    else
        echo -e "${YELLOW}本机IP地址: 无法获取${NC}"
    fi
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
    
    # 检查是否有index.html文件
    if [ -f "index.html" ]; then
        echo -e "${GREEN}找到主页面: index.html${NC}"
    else
        echo -e "${YELLOW}警告: 未找到主页面index.html${NC}"
    fi
    echo ""
}

# 主程序
main() {
    # 检查依赖
    check_dependencies
    
    # 查找可用端口
    PORT=$(find_available_port $PORT)
    
    # 显示项目信息
    show_project_info
    
    echo -e "${YELLOW}按 Ctrl+C 停止服务器${NC}"
    echo ""
    
    # 启动服务器
    start_server $PORT $SERVER_TYPE
}

# 运行主程序
main
