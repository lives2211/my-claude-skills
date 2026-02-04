#!/bin/bash
# Moltbook Idea Factory - 一键运行所有功能

echo "🎯 Moltbook 创意工厂"
echo "===================="
echo ""

# 检查并安装依赖
echo "📦 检查依赖..."
python3 -c "import flask" 2>/dev/null || pip install flask -q

# 运行创意分析
echo "🔍 运行创意分析..."
python3 scripts/factory.py

echo ""
echo "📄 生成的项目:"
ls -la output/ 2>/dev/null | head -10

echo ""
echo "🎉 完成!"
