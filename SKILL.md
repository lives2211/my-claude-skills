# Moltbook Observatory Dashboard

被动监控 + 分析 + 自动构建完整系统

## 🎯 功能概述

| 模块 | 功能 | 说明 |
|------|------|------|
| **Monitor** | 被动监控 | 自动收集 Moltbook 帖子 |
| **Analyzer** | 创意分析 | 评分算法，评估商业潜力 |
| **Builder** | 自动构建 | 根据创意生成网站项目 |
| **Dashboard** | 可视化面板 | Web UI 展示统计和创意 |
| **API** | REST API | 程序化访问接口 |

## 🚀 快速开始

### 1. 安装依赖

```bash
bash run.sh install
```

### 2. 运行完整流程

```bash
bash run.sh all
```

### 3. 启动 Web 界面

```bash
# 终端1: 启动 API
bash run.sh api

# 终端2: 启动 Web
bash run.sh web
```

访问 http://localhost:8080 查看仪表板。

## 📁 项目结构

```
moltbook-observatory-dashboard/
├── main.py              # 主程序
├── run.sh               # 快速启动脚本
├── api/
│   ├── server.py        # FastAPI 服务器
│   └── client.py        # Moltbook API 客户端
├── config/
│   └── config.py        # 配置管理
├── database/
│   ├── connection.py    # SQLite 数据库
│   └── schema.py        # 数据库架构
├── analyzer/
│   └── idea_analyzer.py # 创意评分系统
├── builder/
│   └── website_builder.py # 自动构建器
├── web/
│   └── index.html       # Web UI
├── data/                # SQLite 数据库
├── output/
│   └── projects/       # 构建的项目
└── reports/            # 报告
```

## 💡 评分标准

| 维度 | 权重 | 说明 |
|------|------|------|
| 技术创新 | 35% | AI、自动化、新技术 |
| 商业潜力 | 25% | SaaS、平台、变现 |
| 实用价值 | 20% | 工具、模板、生成器 |
| 参与度 | 10% | 点赞、评论 |
| 类别加成 | 10% | AI应用、自动化等 |

## 🛠️ 自动生成的项目类型

| 类型 | 技术栈 | 特点 |
|------|--------|------|
| **AI助手** | React + FastAPI | 对话式AI |
| **仪表板** | Next.js + Recharts | 数据可视化 |
| **生成器** | Next.js | 一键生成 |
| **博客** | Next.js + MDX | 内容系统 |
| **SaaS平台** | Next.js + Stripe | 订阅变现 |
| **工具网站** | Vue.js | 在线工具 |

## 🔧 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/feed` | GET | 获取帖子 |
| `/api/stats` | GET | 统计信息 |
| `/api/ideas` | GET | 高分创意 |
| `/api/projects` | GET | 已构建项目 |
| `/api/analyze` | POST | 分析创意 |
| `/api/build` | POST | 构建项目 |

## 📊 示例输出

```
📊 Moltbook 观测仪表板
========================

📈 统计:
  • 总帖子数: 1,234
  • 高分创意: 45
  • 已构建项目: 12

🏆 Top 创意:
  1. AI Agent 协作平台
     评分: 85 | 方向: AI应用
  2. 自动化内容生成器
     评分: 78 | 方向: 工具
```

## 🔒 合规保证

- ✅ 仅收集公开信息
- ✅ 不侵犯版权
- ✅ 不涉及隐私
- ✅ 灵感启发，原创创新

## 📝 配置

编辑 `.env` 文件：

```env
MOLTBOOK_API_KEY=your_api_key
DATABASE_PATH=./data/observatory.db
PORT=8000
```
