#!/bin/bash
# 批量安装 OpenClaw Skills

SKILLS=(
    # Git & GitHub
    "github"
    "git-essentials"
    "git-sync"
    "github-pr"
    "gitlab-cli-skills"
    
    # Moltbook
    "moltbook-interact"
    "moltbook-curator"
    "moltbook-registry"
    "moltchan"
    
    # Web & Frontend
    "frontend-design"
    "ui-ux-pro-max"
    "nextjs-expert"
    "react-email-skills"
    "remotion-best-practices"
    
    # Coding Agents
    "coding-agent"
    "skill-creator"
    "tdd-guide"
    "test-runner"
    "debug-pro"
    
    # DevOps & Cloud
    "kubernetes"
    "docker-essentials"
    "aws-infra"
    "azure-infra"
    "cloudflare"
    
    # Browser & Automation
    "computer-use"
    "webapp-testing"
    
    # AI & LLMs
    "claude-optimised"
    "model-usage"
    
    # Marketing
    "social-content"
    "email-sequence"
    "page-cro"
    
    # Productivity
    "notion"
    "tg"
    "slack"
    
    # Finance
    "binance"
    "hyperliquid-trading"
    "solana-trader"
)

echo "🚀 开始安装 Skills..."
echo "========================"

for skill in "${SKILLS[@]}"; do
    echo "📦 安装: $skill"
    clawdhub install "$skill" --path . 2>&1 | grep -v "^🔍\|^✅\|^⚠️" || true
    sleep 1
done

echo ""
echo "✅ 安装完成!"
echo "========================"
