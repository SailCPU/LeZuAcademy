#!/bin/bash

# 乐族学园 快速启动脚本
# 在项目根目录运行此脚本即可启动web服务

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 运行高级启动脚本
"$SCRIPT_DIR/scripts/start_web_server_advanced.sh" "$@"
