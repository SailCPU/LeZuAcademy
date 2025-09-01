#!/bin/bash

# 乐族学园 网络配置检查脚本
# 检查局域网访问配置

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  乐族学园 网络配置检查脚本${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# 检查网络接口
echo -e "${BLUE}1. 网络接口信息:${NC}"
if command -v ip &> /dev/null; then
    echo "网络接口列表:"
    ip addr show | grep -E "^[0-9]+:" | awk '{print $2}' | sed 's/://'
    echo ""
else
    echo -e "${YELLOW}ip命令不可用，尝试使用ifconfig${NC}"
    if command -v ifconfig &> /dev/null; then
        ifconfig | grep -E "^[a-zA-Z0-9]+" | awk '{print $1}' | sed 's/://'
        echo ""
    else
        echo -e "${RED}无法获取网络接口信息${NC}"
    fi
fi

# 获取本机IP地址
echo -e "${BLUE}2. 本机IP地址:${NC}"
get_local_ip() {
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

LOCAL_IP=$(get_local_ip)
if [ -n "$LOCAL_IP" ]; then
    echo -e "${GREEN}本机IP地址: $LOCAL_IP${NC}"
else
    echo -e "${RED}无法获取本机IP地址${NC}"
fi
echo ""

# 检查防火墙状态
echo -e "${BLUE}3. 防火墙状态:${NC}"
if command -v ufw &> /dev/null; then
    ufw_status=$(sudo ufw status 2>/dev/null | head -n1)
    if [[ "$ufw_status" == *"inactive"* ]]; then
        echo -e "${GREEN}UFW防火墙: 已禁用${NC}"
    else
        echo -e "${YELLOW}UFW防火墙: 已启用${NC}"
        echo -e "${YELLOW}注意: 防火墙可能阻止局域网访问${NC}"
    fi
elif command -v iptables &> /dev/null; then
    echo -e "${YELLOW}iptables防火墙: 已安装${NC}"
    echo -e "${YELLOW}注意: 请检查iptables规则是否允许局域网访问${NC}"
else
    echo -e "${GREEN}未检测到防火墙${NC}"
fi
echo ""

# 检查端口占用
echo -e "${BLUE}4. 常用端口占用情况:${NC}"
for port in 8000 8001 8002 8003 8004 8005; do
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}端口 $port: 已被占用${NC}"
    else
        echo -e "${GREEN}端口 $port: 可用${NC}"
    fi
done
echo ""

# 检查网络连通性
echo -e "${BLUE}5. 网络连通性测试:${NC}"
if [ -n "$LOCAL_IP" ]; then
    # 测试本地回环
    if ping -c 1 127.0.0.1 >/dev/null 2>&1; then
        echo -e "${GREEN}本地回环: 正常${NC}"
    else
        echo -e "${RED}本地回环: 异常${NC}"
    fi
    
    # 测试本机IP
    if ping -c 1 "$LOCAL_IP" >/dev/null 2>&1; then
        echo -e "${GREEN}本机IP ($LOCAL_IP): 可达${NC}"
    else
        echo -e "${RED}本机IP ($LOCAL_IP): 不可达${NC}"
    fi
    
    # 测试网关连通性
    gateway=$(ip route | grep default | awk '{print $3}' | head -n1)
    if [ -n "$gateway" ]; then
        if ping -c 1 "$gateway" >/dev/null 2>&1; then
            echo -e "${GREEN}网关 ($gateway): 可达${NC}"
        else
            echo -e "${RED}网关 ($gateway): 不可达${NC}"
        fi
    fi
else
    echo -e "${RED}无法获取本机IP，跳过连通性测试${NC}"
fi
echo ""

# 提供局域网访问建议
echo -e "${BLUE}6. 局域网访问建议:${NC}"
if [ -n "$LOCAL_IP" ]; then
    echo -e "${GREEN}局域网访问地址:${NC}"
    echo -e "${GREEN}  http://$LOCAL_IP:8000${NC}"
    echo -e "${GREEN}  http://$LOCAL_IP:8001${NC}"
    echo -e "${GREEN}  http://$LOCAL_IP:8002${NC}"
    echo ""
    echo -e "${BLUE}其他设备访问说明:${NC}"
    echo "1. 确保其他设备与当前设备在同一局域网"
    echo "2. 使用上述IP地址访问web服务"
    echo "3. 如果无法访问，请检查防火墙设置"
    echo "4. 某些路由器可能阻止局域网设备间通信"
else
    echo -e "${RED}无法获取本机IP地址，局域网访问可能受限${NC}"
fi
echo ""

# 检查系统服务
echo -e "${BLUE}7. 系统服务状态:${NC}"
if systemctl is-active --quiet networking; then
    echo -e "${GREEN}网络服务: 运行中${NC}"
else
    echo -e "${YELLOW}网络服务: 未运行${NC}"
fi

if systemctl is-active --quiet NetworkManager; then
    echo -e "${GREEN}NetworkManager: 运行中${NC}"
else
    echo -e "${YELLOW}NetworkManager: 未运行${NC}"
fi
echo ""

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}  网络检查完成${NC}"
echo -e "${BLUE}================================${NC}"
