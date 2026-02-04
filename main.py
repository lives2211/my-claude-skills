#!/bin/bash
# Moltbook Idea Factory - 主入口

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CMD="${1:-}"

if [ "$CMD" = "monitor" ]; then
    echo "🔍 监控 Moltbook 收集创意..."
    python3 scripts/monitor.py
    
elif [ "$CMD" = "factory" ]; then
    echo "🎯 运行创意工厂..."
    python3 scripts/factory.py
    
elif [ "$CMD" = "all" ]; then
    echo "🚀 执行完整流程..."
    echo ""
    echo "=== 步骤1: 监控 Moltbook ==="
    python3 scripts/monitor.py
    echo ""
    echo "=== 步骤2: 创意分析 ==="
    python3 scripts/factory.py
    echo ""
    echo "✅ 完成!"
    
elif [ "$CMD" = "report" ]; then
    echo "📄 生成创意报告..."
    python3 << 'PYEOF'
from scripts.factory import IdeaFactory
f = IdeaFactory()
print(f.generate_report())
PYEOF
    
elif [ "$CMD" = "status" ]; then
    echo "📊 系统状态..."
    python3 << 'PYEOF'
from scripts.factory import IdeaFactory
f = IdeaFactory()
s = f.get_status()
print(f'收集的想法: {s["total_ideas"]}')
print(f'已分析: {s["analyzed"]}')
print(f'已扩展: {s["expanded"]}')
print(f'已构建: {s["built"]}')
print(f'输出项目: {s["output_projects"]}')
PYEOF

else
    echo "🎯 Moltbook Idea Factory"
    echo ""
    echo "用法: $0 <命令>"
    echo ""
    echo "命令:"
    echo "  monitor    监控 Moltbook 收集创意"
    echo "  factory    运行创意工厂分析"
    echo "  all       执行完整流程 (监控+分析)"
    echo "  report    生成创意报告"
    echo "  status    查看系统状态"
    echo "  help      显示帮助"
fi
