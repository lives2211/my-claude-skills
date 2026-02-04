#!/usr/bin/env python3
"""
Website Builder - 自动网站构建器
根据创意自动生成完整的网站项目
"""

import os
import json
from pathlib import Path
from datetime import datetime, timezone
import hashlib
from typing import Dict, List

class WebsiteBuilder:
    """网站自动构建器"""
    
    OUTPUT_DIR = Path('output/projects')
    
    TEMPLATE_TYPES = {
        'ai_assistant': {
            'name': 'AI助手',
            'description': '基于AI的智能助手网站',
            'features': ['AI对话', '上下文理解', '个性化响应'],
            'tech_stack': ['React', 'FastAPI', 'OpenAI API', 'PostgreSQL'],
        },
        'dashboard': {
            'name': '数据分析仪表板',
            'description': '实时监控和可视化平台',
            'features': ['实时图表', '数据可视化', '告警通知'],
            'tech_stack': ['Next.js', 'Recharts', 'Python', 'InfluxDB'],
        },
        'generator': {
            'name': '自动化生成器',
            'description': '一键生成内容或项目',
            'features': ['实时预览', '批量生成', '模板系统'],
            'tech_stack': ['Next.js', 'Vercel AI SDK', 'Supabase'],
        },
        'blog': {
            'name': '博客/内容网站',
            'description': '内容展示和分享平台',
            'features': ['博客文章', '分类系统', 'SEO优化'],
            'tech_stack': ['Next.js', 'Tailwind CSS', 'MDX'],
        },
        'saas_platform': {
            'name': 'SaaS平台',
            'description': '可扩展的在线服务平台',
            'features': ['用户系统', '订阅管理', 'API接口'],
            'tech_stack': ['Next.js', 'Prisma', 'PostgreSQL', 'Stripe'],
        },
        'tool_website': {
            'name': '在线工具网站',
            'description': '提供在线功能的工具集合',
            'features': ['多工具集成', '批量处理', '数据导出'],
            'tech_stack': ['Vue.js', 'Node.js', 'Redis'],
        }
    }
    
    def __init__(self):
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
    def build(self, idea: Dict, direction: Dict = None) -> Dict:
        """根据创意构建网站项目"""
        project_type = self._determine_type(idea, direction)
        template = self.TEMPLATE_TYPES.get(project_type, self.TEMPLATE_TYPES['tool_website'])
        
        project_id = hashlib.md5(
            f"{idea['id']}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12]
        
        project_name = self._generate_project_name(idea)
        project_dir = self.OUTPUT_DIR / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        
        files = self._generate_files(idea, template, project_type, project_name)
        
        for filename, content in files.items():
            filepath = project_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
        metadata = {
            'id': project_id,
            'name': project_name,
            'type': project_type,
            'description': template['description'],
            'source_idea': {
                'id': idea['id'],
                'title': idea['title'],
                'score': idea.get('creativity_score', 0)
            },
            'direction': direction,
            'tech_stack': template['tech_stack'],
            'features': template['features'],
            'monetization': idea.get('monetization', []),
            'created_at': datetime.now(timezone.utc).isoformat(),
            'files': list(files.keys()),
            'status': 'built'
        }
        
        with open(project_dir / 'project.json', 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
            
        return {
            'success': True,
            'project_id': project_id,
            'project_name': project_name,
            'project_path': str(project_dir),
            'project_type': project_type,
            'files_created': len(files),
            'tech_stack': template['tech_stack']
        }
        
    def _determine_type(self, idea: Dict, direction: Dict = None) -> str:
        if direction:
            dtype = direction.get('type', '').lower()
            if '助手' in dtype or 'assistant' in dtype: return 'ai_assistant'
            if '仪表板' in dtype or 'dashboard' in dtype: return 'dashboard'
            if '生成器' in dtype or 'generator' in dtype: return 'generator'
            if '博客' in dtype or 'blog' in dtype: return 'blog'
            if '平台' in dtype or 'platform' in dtype: return 'saas_platform'
            if '工具' in dtype or 'tool' in dtype: return 'tool_website'
        return 'tool_website'
        
    def _generate_project_name(self, idea: Dict) -> str:
        title = idea.get('title', 'Project')
        keywords = [w for w in title.split() if len(w) > 2][:3]
        return ''.join(w.capitalize() for w in keywords)
        
    def _generate_files(self, idea: Dict, template: Dict, project_type: str, project_name: str) -> Dict[str, str]:
        files = {}
        title = idea.get('title', 'Untitled')
        description = idea.get('content', '')[:200]
        
        files['package.json'] = self._generate_package_json(project_name, template['tech_stack'])
        files['README.md'] = self._generate_readme(project_name, title, description, template, idea)
        files['.env.example'] = self._generate_env_example()
        files['.gitignore'] = self._generate_gitignore()
        
        if project_type == 'ai_assistant':
            files['app/page.tsx'] = self._generate_ai_page()
            files['app/api/chat/route.ts'] = self._generate_chat_api()
        elif project_type == 'dashboard':
            files['app/page.tsx'] = self._generate_dashboard_page()
            files['components/Dashboard.tsx'] = self._generate_dashboard_component()
        elif project_type == 'generator':
            files['app/page.tsx'] = self._generate_generator_page()
        elif project_type == 'blog':
            files['app/page.tsx'] = self._generate_blog_page()
            files['content/hello-world.md'] = self._generate_sample_post(title)
        elif project_type == 'saas_platform':
            files['app/page.tsx'] = self._generate_saas_page()
        else:
            files['index.html'] = self._generate_tool_html(project_name, template)
            
        return files
        
    def _generate_package_json(self, name: str, tech_stack: List[str]) -> str:
        deps = {
            'react': '^18.2.0',
            'react-dom': '^18.2.0',
            'next': '^14.0.0',
            'react-icons': '^4.12.0'
        }
        if 'Tailwind CSS' in tech_stack:
            deps['tailwindcss'] = '^3.4.0'
        package = {
            'name': name.lower().replace(' ', '-'),
            'version': '0.1.0',
            'description': f'基于 {name} 创意的网站项目',
            'scripts': {'dev': 'next dev', 'build': 'next build', 'start': 'next start'},
            'dependencies': deps
        }
        return json.dumps(package, indent=2)
        
    def _generate_readme(self, project_name: str, source_title: str, description: str, template: Dict, idea: Dict) -> str:
        return f'''# {project_name}

{description}

## 🎯 灵感来源

基于 Moltbook 创意: **{source_title}**

评分: {idea.get('creativity_score', 0)}/100

## ✨ 功能特性

'''
        + '\n'.join([f'- {f}' for f in template['features']]) + f'''

## 🛠️ 技术栈

'''
        + '\n'.join([f'- {t}' for t in template['tech_stack']]) + f'''

## 💰 变现方式

'''
        + '\n'.join([f'- {m}' for m in idea.get('monetization', [])]) + f'''

## 🚀 快速开始

```bash
npm install
npm run dev
```

## 📝 许可证

MIT
'''
        
    def _generate_ai_page(self) -> str:
        return '''import { useState } from 'react'

export default function Home() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return
    setLoading(true)
    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    // 模拟AI响应
    setTimeout(() => {
      setMessages([...messages, userMessage, { role: 'assistant', content: '这是AI的回复' }])
      setLoading(false)
    }, 1000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-900 text-white p-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center py-8">
          <h1 className="text-4xl font-bold mb-2">🤖 AI 助手</h1>
        </header>
        <div className="bg-white/10 rounded-xl p-4 h-96 overflow-y-auto mb-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-400 mt-32">开始发送消息</div>
          ) : (
            messages.map((msg, i) => (
              <div key={i} className={`mb-2 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
                <span className={`inline-block p-2 rounded-lg ${msg.role === 'user' ? 'bg-purple-600' : 'bg-white/20'}`}>
                  {msg.content}
                </span>
              </div>
            ))
          )}
        </div>
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入消息..."
            className="flex-1 px-4 py-2 rounded-lg bg-white/10 border border-white/20"
          />
          <button onClick={sendMessage} disabled={loading} className="px-6 py-2 bg-purple-600 rounded-lg">
            {loading ? '发送中...' : '发送'}
          </button>
        </div>
      </div>
    </div>
  )
}
'''
        
    def _generate_chat_api(self) -> str:
        return '''import { NextResponse } from 'next/server'

export async function POST(request) {
  const { message } = await request.json()
  // TODO: 调用 OpenAI API
  return NextResponse.json({ response: `收到消息: ${message}` })
}
'''
        
    def _generate_dashboard_page(self) -> str:
        return '''export default function Home() {
  const metrics = [
    { name: '用户', value: 1234 },
    { name: '收入', value: 56780 },
    { name: '订单', value: 892 }
  ]
  
  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">📊 数据仪表板</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {metrics.map((m, i) => (
            <div key={i} className="bg-white/5 rounded-xl p-6">
              <p className="text-gray-400">{m.name}</p>
              <p className="text-3xl font-bold mt-2">{m.value}</p>
            </div>
          ))}
        </div>
        <div className="bg-white/5 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">📈 趋势图</h2>
          <div className="h-64 bg-white/5 rounded flex items-center justify-center">
            图表区域
          </div>
        </div>
      </div>
    </div>
  )
}
'''
        
    def _generate_dashboard_component(self) -> str:
        return '''export default function Dashboard() {
  return (
    <div className="bg-white/5 rounded-xl p-6">
      <h2 className="text-xl font-semibold mb-4">📈 趋势图</h2>
      <div className="h-64 bg-white/5 rounded flex items-center justify-center">
        Recharts 图表区域
      </div>
    </div>
  )
}
'''
        
    def _generate_generator_page(self) -> str:
        return '''import { useState } from 'react'

export default function Home() {
  const [input, setInput] = useState('')
  const [result, setResult] = useState('')
  const [loading, setLoading] = useState(false)

  const generate = () => {
    if (!input.trim()) return
    setLoading(true)
    setTimeout(() => {
      setResult(`基于 "${input}" 生成的内容...`)
      setLoading(false)
    }, 2000)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-900 to-emerald-900 text-white p-4">
      <div className="max-w-4xl mx-auto">
        <header className="text-center py-8">
          <h1 className="text-4xl font-bold mb-2">⚡ 内容生成器</h1>
        </header>
        <div className="bg-white/10 rounded-xl p-6 mb-6">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="输入你的想法..."
            className="w-full h-32 px-4 py-3 rounded-lg bg-white/5 border border-white/20 resize-none"
          />
          <button onClick={generate} disabled={loading} className="mt-4 w-full py-3 bg-green-600 rounded-lg">
            {loading ? '生成中...' : '🚀 一键生成'}
          </button>
        </div>
        {result && (
          <div className="bg-white/10 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4">生成结果</h2>
            <p>{result}</p>
          </div>
        )}
      </div>
    </div>
  )
}
'''
        
    def _generate_blog_page(self) -> str:
        return '''import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-white/5 border-b border-white/10">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold">📝 我的博客</h1>
        </div>
      </header>
      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="grid gap-6">
          <Link href="/blog/hello-world" className="block bg-white/5 hover:bg-white/10 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-2">欢迎来到新博客</h2>
            <p className="text-gray-400">这是第一篇博客文章</p>
          </Link>
        </div>
      </main>
    </div>
  )
}
'''
        
    def _generate_sample_post(self, title: str) -> str:
        return f'''---
title: "{title}"
date: 2026-02-04
description: "基于 Moltbook 创意的文章"
---

# {title}

这是基于 Moltbook 创意自动生成的第一篇博客文章。

## 背景

{Markdown}

## 结论

这是一个示例博客文章。
'''
        
    def _generate_saas_page(self) -> str:
        return '''export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 to-indigo-900 text-white">
      <nav className="container mx-auto px-4 py-6 flex justify-between">
        <h1 className="text-2xl font-bold">🚀 SaaS 平台</h1>
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-white/10 rounded-lg">登录</button>
          <button className="px-4 py-2 bg-purple-600 rounded-lg">免费试用</button>
        </div>
      </nav>
      <main className="container mx-auto px-4 py-20 text-center">
        <h1 className="text-5xl font-bold mb-6">企业级解决方案</h1>
        <p className="text-xl text-gray-300 mb-8">专业的 SaaS 平台，帮助您提升业务效率</p>
        <button className="px-8 py-4 bg-purple-600 rounded-lg font-semibold text-lg">开始免费试用</button>
      </main>
    </div>
  )
}
'''
        
    def _generate_tool_html(self, name: str, template: Dict) -> str:
        features = '\n'.join([f'          <li>✅ {f}</li>' for f in template['features']])
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{name}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
  <div class="container mx-auto px-4 py-12">
    <header class="text-center mb-12">
      <h1 class="text-4xl font-bold mb-4">{name}</h1>
      <p class="text-gray-400">{template['description']}</p>
    </header>
    <main class="max-w-4xl mx-auto">
      <div class="bg-white/5 rounded-xl p-8 border border-white/10">
        <h2 class="text-2xl font-semibold mb-6">✨ 功能</h2>
        <ul class="space-y-3">
{features}
        </ul>
      </div>
      <div class="mt-8 text-center">
        <button class="px-8 py-4 bg-purple-600 hover:bg-purple-700 rounded-lg font-semibold text-lg">开始使用</button>
      </div>
    </main>
  </div>
</body>
</html>
'''
        
    def _generate_env_example(self) -> str:
        return '''# API Keys
OPENAI_API_KEY=your_openai_key_here
STRIPE_SECRET_KEY=sk_test_xxx

# 数据库
DATABASE_URL=postgresql://user:password@localhost:5432/db

# 应用配置
NEXT_PUBLIC_APP_URL=http://localhost:3000
'''
        
    def _generate_gitignore(self) -> str:
        return '''node_modules/
.next/
.env
.env.local
.idea/
.vscode/
*.swp
.DS_Store
*.log
'''
        
    def get_built_projects(self) -> List[Dict]:
        projects = []
        if self.OUTPUT_DIR.exists():
            for project_dir in self.OUTPUT_DIR.iterdir():
                if project_dir.is_dir():
                    metadata_file = project_dir / 'project.json'
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            projects.append(json.load(f))
        return sorted(projects, key=lambda x: x.get('created_at', ''), reverse=True)
