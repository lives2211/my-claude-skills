#!/usr/bin/env python3
"""
Moltbook Idea Factory - 自动化创意发现和网站构建系统
基于 Moltbook 监控，自动发现优秀想法并构建创意项目
"""

import os
import sys
import json
import time
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/factory.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class IdeaFactory:
    """创意工厂 - 自动发现、收集、分析优秀想法"""
    
    def __init__(self):
        self.data_dir = Path('data')
        self.ideas_dir = Path('ideas')
        self.output_dir = Path('output')
        self.templates_dir = Path('templates')
        
        for d in [self.data_dir, self.ideas_dir, self.output_dir, self.templates_dir]:
            d.mkdir(exist_ok=True)
            
        self.ideas_file = self.data_dir / 'collected_ideas.json'
        self.ideas = self._load_ideas()
        
    def _load_ideas(self):
        """加载已收集的想法"""
        if self.ideas_file.exists():
            with open(self.ideas_file, 'r') as f:
                return json.load(f)
        return {'ideas': [], 'projects': []}
        
    def _save_ideas(self):
        """保存想法"""
        with open(self.ideas_file, 'w') as f:
            json.dump(self.ideas, f, indent=2, ensure_ascii=False)
            
    def add_idea(self, source, title, content, tags, category='general'):
        """添加新想法"""
        idea = {
            'id': hashlib.md5(f"{source}{title}".encode()).hexdigest()[:12],
            'source': source,
            'title': title,
            'content': content,
            'tags': tags,
            'category': category,
            'collected_at': datetime.now(timezone.utc).isoformat(),
            'status': 'new',
            'creativity_score': 0,
            'project_potential': [],
            'expanded_ideas': []
        }
        
        # 检查是否已存在
        existing_ids = [i['id'] for i in self.ideas['ideas']]
        if idea['id'] not in existing_ids:
            self.ideas['ideas'].append(idea)
            self._save_ideas()
            logger.info(f"✅ 新想法已添加: {title}")
            return True
        return False
        
    def analyze_idea(self, idea_id):
        """分析单个想法的创意潜力"""
        idea = next((i for i in self.ideas['ideas'] if i['id'] == idea_id), None)
        if not idea:
            return None
            
        content = idea['content'].lower()
        title = idea['title'].lower()
        
        # 评分标准
        score = 0
        project_potentials = []
        
        # 技术创新性
        if any(kw in content for kw in ['ai', 'agent', 'automation', '生成']):
            score += 20
            project_potentials.append('AI Agent 应用')
        if any(kw in content for kw in ['api', 'integration', 'plugin']):
            score += 15
            project_potentials.append('API 集成工具')
        if any(kw in content for kw in ['dashboard', 'analytics', '监控']):
            score += 15
            project_potentials.append('监控仪表板')
        if any(kw in content for kw in ['workflow', '自动化']):
            score += 15
            project_potentials.append('工作流自动化')
            
        # 商业潜力
        if any(kw in content for kw in ['saas', 'platform', '服务']):
            score += 20
            project_potentials.append('SaaS 平台')
        if any(kw in content for kw in ['open source', '开源']):
            score += 10
            project_potentials.append('开源项目')
        if any(kw in content for kw in ['free', '免费']):
            score += 5
            project_potentials.append('免费工具')
            
        # 实用性
        if any(kw in content for kw in ['tool', '工具', 'library']):
            score += 15
            project_potentials.append('开发者工具')
        if any(kw in content for kw in ['template', '模板']):
            score += 10
            project_potentials.append('模板/脚手架')
        if any(kw in content for kw in ['generator', '生成器']):
            score += 15
            project_potentials.append('代码生成器')
            
        # 社区热度
        if any(kw in content for kw in ['trending', 'popular', '热门']):
            score += 10
            project_potentials.append('趋势应用')
            
        idea['creativity_score'] = min(100, score)
        idea['project_potential'] = project_potentials
        idea['status'] = 'analyzed'
        self._save_ideas()
        
        return idea
        
    def generate_website_ideas(self, idea_id):
        """基于想法生成网站创意"""
        idea = next((i for i in self.ideas['ideas'] if i['id'] == idea_id), None)
        if not idea:
            return []
            
        expanded = []
        
        # 根据类别生成创意
        category = idea['category']
        tags = [t.lower() for t in idea['tags']]
        
        if 'ai' in tags or 'agent' in tags or '人工智能' in idea['content'].lower():
            expanded.append({
                'name': f"{idea['title']} AI助手",
                'type': 'Web应用',
                'description': f"基于 {idea['title']} 构建的AI助手网站，提供智能问答和服务",
                'tech_stack': ['React', 'FastAPI', 'OpenAI API', 'PostgreSQL'],
                'features': ['AI对话', '个性化推荐', '数据分析'],
                'monetization': ['订阅制', 'API调用计费']
            })
            
        if 'tool' in tags or '工具' in idea['content'].lower():
            expanded.append({
                'name': f"{idea['title']}工具箱",
                'type': '工具网站',
                'description': f"在线 {idea['title']} 工具集合，提供便捷的在线服务",
                'tech_stack': ['Vue.js', 'Node.js', 'Redis'],
                'features': ['在线使用', '批量处理', '数据导出'],
                'monetization': ['广告', '高级功能付费']
            })
            
        if 'dashboard' in tags or '监控' in idea['content'].lower():
            expanded.append({
                'name': f"{idea['title']}仪表板",
                'type': '数据分析平台',
                'description': f"实时监控和数据分析仪表板，可视化展示关键指标",
                'tech_stack': ['React', 'D3.js', 'Python', 'InfluxDB'],
                'features': ['实时图表', '告警通知', '自定义报告'],
                'monetization': ['企业版', '私有化部署']
            })
            
        if 'automation' in tags or 'workflow' in tags:
            expanded.append({
                'name': f"{idea['title']}自动化平台",
                'type': '自动化服务',
                'description': f"无代码自动化平台，帮助用户快速构建工作流",
                'tech_stack': ['React Flow', 'Node.js', 'n8n'],
                'features': ['可视化编排', '模板市场', '定时触发'],
                'monetization': ['订阅制', '企业定制']
            })
            
        if 'template' in tags or 'generator' in tags:
            expanded.append({
                'name': f"{idea['title']}生成器",
                'type': '在线生成器',
                'description': f"一键生成 {idea['title']}，支持自定义配置",
                'tech_stack': ['Next.js', 'Vercel', 'Supabase'],
                'features': ['实时预览', '一键部署', '配置保存'],
                'monetization': ['免费增值', '模板市场']
            })
            
        # 默认创意
        if not expanded:
            expanded.append({
                'name': f"基于{idea['title']}的创意网站",
                'type': '内容网站',
                'description': idea['content'][:200],
                'tech_stack': ['Next.js', 'Tailwind CSS'],
                'features': ['响应式设计', 'SEO优化'],
                'monetization': ['广告', '赞助']
            })
            
        idea['expanded_ideas'] = expanded
        idea['status'] = 'expanded'
        self._save_ideas()
        
        return expanded
        
    def build_website(self, idea_id, website_index=0):
        """基于创意生成网站"""
        idea = next((i for i in self.ideas['ideas'] if i['id'] == idea_id), None)
        if not idea:
            return None
            
        expanded = idea.get('expanded_ideas', [])
        if website_index >= len(expanded):
            return None
            
        website = expanded[website_index]
        
        # 生成网站配置
        project_config = {
            'name': website['name'],
            'type': website['type'],
            'description': website['description'],
            'tech_stack': website['tech_stack'],
            'features': website['features'],
            'monetization': website['monetization'],
            'source_idea': idea['title'],
            'created_at': datetime.now(timezone.utc).isoformat(),
            'files': {}
        }
        
        # 生成基础文件
        project_config['files'] = self._generate_base_files(website)
        
        # 保存项目
        project_id = hashlib.md5(f"{website['name']}{datetime.now().isoformat()}".encode()).hexdigest()[:12]
        project_dir = self.output_dir / project_id
        project_dir.mkdir(exist_ok=True)
        
        # 写入文件
        for filename, content in project_config['files'].items():
            filepath = project_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
                
        # 保存项目配置
        with open(project_dir / 'project.json', 'w') as f:
            json.dump(project_config, f, indent=2, ensure_ascii=False)
            
        # 更新想法状态
        idea['status'] = 'built'
        self._save_ideas()
        
        return {
            'project_id': project_id,
            'project_dir': str(project_dir),
            'name': website['name'],
            'files': list(project_config['files'].keys())
        }
        
    def _generate_base_files(self, website):
        """生成基础项目文件"""
        files = {}
        
        # package.json
        tech_stack = website['tech_stack']
        deps = {}
        if 'React' in tech_stack or 'Next.js' in tech_stack:
            deps = {
                'react': '^18.2.0',
                'react-dom': '^18.2.0',
                'next': '^14.0.0',
                'react-icons': '^4.12.0'
            }
        elif 'Vue.js' in tech_stack:
            deps = {
                'vue': '^3.3.0',
                'vite': '^5.0.0',
                'vue-router': '^4.2.0'
            }
        else:
            deps = {
                'express': '^4.18.0',
                'cors': '^2.8.5'
            }
            
        package_json = {
            'name': website['name'].lower().replace(' ', '-'),
            'version': '0.1.0',
            'description': website['description'],
            'scripts': {
                'dev': 'next dev' if 'Next.js' in tech_stack else 'vite',
                'build': 'next build' if 'Next.js' in tech_stack else 'vite build',
                'preview': 'next preview' if 'Next.js' in tech_stack else 'vite preview'
            },
            'dependencies': deps
        }
        files['package.json'] = json.dumps(package_json, indent=2)
        
        # README.md
        readme = f"""# {website['name']}

{website['description']}

## 🎯 灵感来源
基于 Moltbook 创意: {website['source_idea']}

## ✨ 功能特性
"""
        for feature in website['features']:
            readme += f"- {feature}\n"
            
        readme += f"""
## 🛠️ 技术栈
"""
        for tech in website['tech_stack']:
            readme += f"- {tech}\n"
            
        readme += f"""
## 💰 变现方式
"""
        for mono in website['monetization']:
            readme += f"- {mono}\n"
            
        readme += """
## 🚀 快速开始

```bash
npm install
npm run dev
```

## 📝 许可证
MIT
"""
        files['README.md'] = readme
        
        # index.html (基础模板)
        if 'Next.js' in tech_stack:
            files['app/page.js'] = f"""export default function Home() {{
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <h1 className="text-5xl font-bold mb-4">{{{{website['name']}}}}</h1>
        <p className="text-xl text-gray-300 mb-8">{{{{website['description']}}}}</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {{{{website['features'][:3].map((f, i) => `(
            <div key={{{{i}}}} className="bg-white/10 backdrop-blur rounded-lg p-6">
              <h3 className="text-xl font-semibold mb-2">{{{{f}}}}</h3>
            </div>
          )`).join('\\n')}}}}
        </div>
        
        <div className="mt-12 flex gap-4">
          <button className="bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold">
            开始使用
          </button>
        </div>
      </div>
    </div>
  )
}}
"""
            files['app/layout.js'] = """export default function Layout({ children }) {
  return (
    <html lang="zh">
      <body className="bg-gray-900 text-white">{children}</body>
    </html>
  )
}
"""
            files['next.config.js'] = """/** @type {import('next').NextConfig} */
const nextConfig = {}
module.exports = nextConfig
"""
            files['tailwind.config.js'] = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        else:
            files['index.html'] = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{website['name']}</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 text-white min-h-screen">
  <div class="container mx-auto px-4 py-16">
    <h1 class="text-5xl font-bold mb-4">{website['name']}</h1>
    <p class="text-xl text-gray-300 mb-8">{website['description']}</p>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      {' '.join([f'<div class="bg-white/10 backdrop-blur rounded-lg p-6"><h3 class="text-xl font-semibold">{f}</h3></div>' for f in website['features'][:3]])}
    </div>
  </div>
</body>
</html>
"""
            
        return files
        
    def get_top_ideas(self, limit=10):
        """获取评分最高的创意"""
        sorted_ideas = sorted(
            self.ideas['ideas'],
            key=lambda x: x.get('creativity_score', 0),
            reverse=True
        )
        return sorted_ideas[:limit]
        
    def get_status(self):
        """获取系统状态"""
        return {
            'total_ideas': len(self.ideas['ideas']),
            'analyzed': len([i for i in self.ideas['ideas'] if i['status'] in ['analyzed', 'expanded', 'built']]),
            'expanded': len([i for i in self.ideas['ideas'] if i['status'] in ['expanded', 'built']]),
            'built': len([i for i in self.ideas['ideas'] if i['status'] == 'built']),
            'output_projects': len(list(self.output_dir.iterdir()))
        }
        
    def generate_report(self):
        """生成创意报告"""
        total_ideas = len(self.ideas['ideas'])
        analyzed = len([i for i in self.ideas['ideas'] if i['status'] in ['analyzed', 'expanded', 'built']])
        expanded = len([i for i in self.ideas['ideas'] if i['status'] in ['expanded', 'built']])
        built = len([i for i in self.ideas['ideas'] if i['status'] == 'built'])
        
        report = f"""# 🎯 Moltbook 创意工厂报告

**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}

---

## 📊 系统状态

| 指标 | 数量 |
|------|------|
| 收集的想法 | {total_ideas} |
| 已分析 | {analyzed} |
| 已扩展 | {expanded} |
| 已构建 | {built} |

---

## 🏆 Top 5 优秀创意

"""
        top_ideas = self.get_top_ideas(5)
        for i, idea in enumerate(top_ideas, 1):
            report += f"""### {i}. {idea['title']}

**来源**: {idea['source']}
**评分**: {idea.get('creativity_score', 0)}/100
**标签**: {', '.join(idea['tags'])}
**类别**: {idea['category']}

**项目方向**:
"""
            for p in idea.get('project_potential', []):
                report += f"- {p}\n"
                
            if idea.get('expanded_ideas'):
                report += "\n**网站创意**:\n"
                for j, w in enumerate(idea['expanded_ideas'][:2], 1):
                    report += f"- **{w['name']}** ({w['type']}): {w['description'][:100]}...\n"
                    
            report += "\n---\n\n"
            
        report += """
## 💡 创意洞察

### 热门技术方向
"""
        # 统计标签
        all_tags = []
        for idea in self.ideas['ideas']:
            all_tags.extend(idea.get('tags', []))
            
        from collections import Counter
        tag_counts = Counter(all_tags).most_common(10)
        for tag, count in tag_counts:
            report += f"- {tag}: {count} 个创意\n"
            
        report += """
### 建议关注的项目类型
"""
        potentials = []
        for idea in self.ideas['ideas']:
            potentials.extend(idea.get('project_potential', []))
            
        potential_counts = Counter(potentials).most_common(5)
        for p, count in potential_counts:
            report += f"- {p}: {count} 个创意相关\n"
            
        return report
        
def demo():
    """演示"""
    factory = IdeaFactory()
    
    # 添加一些示例创意
    demo_ideas = [
        ('moltbook', 'AI Agent 社交网络监控', '构建一个被动监控系统，收集AI agent的社交行为数据', ['ai', 'monitoring', 'analytics'], 'monitoring'),
        ('moltbook', '自动化博客生成器', '基于主题自动生成完整的静态网站和博客', ['generator', 'blog', 'static-site'], 'generator'),
        ('moltbook', '多平台内容聚合', '聚合多个平台的内容，自动分类和推荐', ['aggregation', 'content', 'recommendation'], 'platform'),
        ('github', '开发者工具市场', '为开发者提供一站式工具发现和集成平台', ['developer-tools', 'marketplace', 'saas'], 'platform'),
        ('github', 'AI项目模板库', '收集和分享AI项目的最佳实践和模板', ['ai', 'template', 'boilerplate'], 'library'),
    ]
    
    for source, title, content, tags, category in demo_ideas:
        factory.add_idea(source, title, content, tags, category)
        
    # 分析创意
    for idea in factory.ideas['ideas']:
        factory.analyze_idea(idea['id'])
        factory.generate_website_ideas(idea['id'])
        
    # 输出状态
    status = factory.get_status()
    print(f"\n🎯 创意工厂状态:")
    print(f"  - 收集的想法: {status['total_ideas']}")
    print(f"  - 已分析: {status['analyzed']}")
    print(f"  - 已扩展: {status['expanded']}")
    print(f"  - 已构建: {status['built']}")
    
    # 显示 Top 创意
    print(f"\n🏆 Top 创意:")
    for idea in factory.get_top_ideas(3):
        print(f"  - {idea['title']}: {idea.get('creativity_score', 0)}分")
        for w in idea.get('expanded_ideas', [])[:2]:
            print(f"    → {w['name']} ({w['type']})")
            
    # 生成报告
    report = factory.generate_report()
    with open('reports/idea-factory-report.md', 'w') as f:
        f.write(report)
    print(f"\n📄 报告已生成: reports/idea-factory-report.md")
    
    return factory

if __name__ == '__main__':
    demo()
