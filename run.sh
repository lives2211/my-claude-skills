#!/bin/bash
# Moltbook Observatory Dashboard - 快速启动

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "${1:-}" in
    api)
        echo "🚀 启动 API 服务器..."
        python3 -m uvicorn api.server:app --host 0.0.0.0 --port 8000
        ;;
    dashboard)
        echo "🎯 运行仪表板..."
        python3 main.py dashboard
        ;;
    monitor)
        echo "📡 监控 Moltbook..."
        python3 main.py monitor
        ;;
    build)
        echo "🔨 自动构建项目..."
        python3 main.py build
        ;;
    all)
        echo "🚀 执行完整流程..."
        python3 main.py all
        ;;
    web)
        echo "🌐 启动 Web UI..."
        if command -v python3 &> /dev/null; then
            python3 -m http.server 8080 -d web
        else
            echo "请安装 Python 3"
        fi
        ;;
    install)
        echo "📦 安装依赖..."
        pip install fastapi uvicorn httpx aiosqlite jinja2 python-dotenv -q
        ;;
    help|*)
        echo "🎯 Moltbook Observatory Dashboard"
        echo ""
        echo "用法: $0 <命令>"
        echo ""
        echo "命令:"
        echo "  install   安装依赖"
        echo "  api       启动 API 服务器 (端口 8000)"
        echo "  monitor   监控 Moltbook 收集创意"
        echo "  build     自动构建网站项目"
        echo "  dashboard 显示仪表板统计"
        echo "  web       启动 Web UI (端口 8080)"
        echo "  all       执行完整流程"
        echo "  help      显示帮助"
        ;;
esac
