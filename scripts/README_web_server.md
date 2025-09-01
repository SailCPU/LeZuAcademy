# 乐族学园 Web服务启动脚本使用说明

## 概述

本项目提供了多个脚本来快速启动本地web服务，方便开发和测试。

## 可用的启动脚本

### 1. 快速启动脚本 (推荐)
```bash
# 在项目根目录运行
./start_web.sh
```

### 2. 基础启动脚本
```bash
# 使用Python内置服务器
./scripts/start_web_server.sh
```

### 3. 高级启动脚本
```bash
# 支持多种服务器类型
./scripts/start_web_server_advanced.sh
```

## 使用方法

### 基本使用
```bash
# 使用默认设置启动 (Python服务器，端口8000)
./start_web.sh

# 指定端口
./start_web.sh -p 8080

# 指定服务器类型
./start_web.sh -s node

# 同时指定端口和服务器类型
./start_web.sh -s node -p 3000
```

### 查看帮助
```bash
./start_web.sh --help
```

## 支持的服务器类型

| 服务器类型 | 说明 | 要求 |
|-----------|------|------|
| `python` | Python内置HTTP服务器 | 需要Python3 |
| `node` | Node.js http-server | 需要Node.js |
| `php` | PHP内置服务器 | 需要PHP |
| `nginx` | Nginx服务器 | 需要Nginx |

## 端口管理

- 默认端口：8000
- 自动端口检测：如果指定端口被占用，会自动寻找下一个可用端口
- 端口范围：8000-8010

## 项目结构显示

启动脚本会自动显示：
- 项目根目录
- 使用的端口
- 服务器类型
- 可用的项目列表
- 主页面状态

## 访问地址

启动成功后，可以通过以下地址访问：
- 主页面：`http://localhost:端口号/index.html`
- 项目页面：`http://localhost:端口号/projects/项目名/`

## 停止服务器

按 `Ctrl+C` 即可停止web服务器。

## 故障排除

### 端口被占用
脚本会自动寻找可用端口，如果8000-8010都被占用，会提示错误。

### 依赖缺失
- **Python3**: `sudo apt update && sudo apt install python3`
- **Node.js**: 脚本会自动尝试安装
- **PHP**: `sudo apt update && sudo apt install php`
- **Nginx**: `sudo apt update && sudo apt install nginx`

### 权限问题
确保脚本有执行权限：
```bash
chmod +x start_web.sh
chmod +x scripts/*.sh
```

## 示例输出

```
================================
  乐族学园 高级Web服务启动脚本
================================

项目根目录: /home/ubuntu/EduProject/LeZuAcademy
使用端口: 8000
服务器类型: python

可用的项目:
  - 柯南侦探英语冒险-杨乐北的单词探案记
  - 彭畅越的假面骑士冒险
  - 杨乐北的三国演义冒险
  - 杨乐北的奇妙冒险：数学王国历险记
  - 杨乐达的三国演义冒险
  - 范以文的三国演义冒险

找到主页面: index.html

按 Ctrl+C 停止服务器

正在启动 python 服务器...
访问地址: http://localhost:8000
主页面: http://localhost:8000/index.html
```

## 注意事项

1. 这些脚本仅用于本地开发和测试
2. 生产环境请使用专业的web服务器
3. 确保防火墙允许指定端口访问
4. 如果使用Nginx，需要sudo权限
