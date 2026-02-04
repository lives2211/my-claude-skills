#!/usr/bin/env python3
"""
Moltbook Observatory Dashboard - 主程序
被动监控 + 分析 + 自动构建完整流程
"""

import asyncio
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from dotenv import load_dotenv

# 导入模块
from config.config import Config
from api.client import MoltbookClient
from database.connection import Database, get_database
from analyzer.idea_analyzer import IdeaAnalyzer
from builder.website_builder import WebsiteBuilder

load_dotenv()

class ObservatoryDashboard:
    """Moltbook 观测仪表板主程序"""
    
    def __init__(self):
        self.db = None
        self.client = None
        self.analyzer = IdeaAnalyzer()
        self.builder = WebsiteBuilder()
        
    async def initialize(self):
        """初始化"""
        print("🚀 初始化 Moltbook 观测仪表板...")
        self.db = await get_database()
        self.client = MoltbookClient()
        print("✅ 初始化完成!")
        
    async def cleanup(self):
        """清理资源"""
        if self.client:
            await self.client.close()
        if self.db:
            await self.db.disconnect()
            
    async def run_monitoring_cycle(self, save_to_db=True):
        """执行监控周期"""
        print("\n📡 监控 Moltbook...")
        
        # 获取帖子（使用模拟数据或真实API）
        posts = self.client.demo_data()['posts'] if not self.client.api_key else []
        
        if not posts:
            print("  使用模拟数据...")
            posts = self.client.demo_data()['posts']
            
        print(f"  获取到 {len(posts)} 个帖子")
        
        # 分析帖子
        analyzed = []
        for post in posts:
            analysis = self.analyzer.analyze(post)
            if analysis['collectible']:
                analyzed.append(analysis)
                
        # 按评分排序
        analyzed.sort(key=lambda x: x['creativity_score'], reverse=True)
        
        print(f"  🎯 高质量创意: {len(analyzed)} 个")
        
        # 保存到数据库
        if save_to_db and self.db:
            for idea in analyzed:
                await self.db.insert_idea(idea)
                
        return analyzed
        
    async def run_auto_build_cycle(self, min_score=40):
        """执行自动构建周期"""
        print("\n🔨 执行自动构建...")
        
        # 从数据库获取高分创意
        ideas = await self.db.get_top_ideas(20) if self.db else []
        
        # 分析新帖子
        analyzed = await self.run_monitoring_cycle(save_to_db=False)
        
        # 合并
        all_ideas = ideas + analyzed
        high_score = [i for i in all_ideas if i.get('creativity_score', 0) >= min_score]
        
        print(f"  📊 待构建项目: {len(high_score)} 个")
        
        built_projects = []
        for idea in high_score[:5]:  # 最多构建5个项目
            if idea.get('status') == 'built':
                continue
                
            # 获取最高优先级的项目方向
            directions = idea.get('project_directions', [])
            direction = directions[0] if directions else None
            
            # 构建项目
            result = self.builder.build(idea, direction)
            
            if result['success']:
                built_projects.append(result)
                print(f"  ✅ {result['project_name']}")
                print(f"     类型: {result['project_type']}")
                print(f"     技术栈: {', '.join(result['tech_stack'])}")
                
                # 更新数据库状态
                if self.db:
                    await self.db.execute(
                        'UPDATE ideas SET status = ?, built_at = ? WHERE id = ?',
                        ('built', datetime.now(timezone.utc).isoformat(), idea['id'])
                    )
                    
        return built_projects
        
    async def show_dashboard(self):
        """显示仪表板"""
        print("\n" + "="*60)
        print("📊 Moltbook 观测仪表板")
        print("="*60)
        
        # 统计
        if self.db:
            stats = await self.db.get_stats()
            print(f"\n📈 统计:")
            print(f"  • 总帖子数: {stats.get('total_posts', 0)}")
            print(f"  • 总Agent数: {stats.get('total_agents', 0)}")
            print(f"  • 总Submolt数: {stats.get('total_submolts', 0)}")
            print(f"  • 高分创意: {stats.get('high_score_ideas', 0)}")
            print(f"  • 已构建项目: {stats.get('built_projects', 0)}")
            
        # 显示高分创意
        ideas = await self.db.get_top_ideas(5) if self.db else []
        if ideas:
            print(f"\n🏆 Top 创意:")
            for i, idea in enumerate(ideas[:5], 1):
                print(f"  {i}. {idea.get('title', 'Unknown')[:50]}")
                print(f"     评分: {idea.get('creativity_score', 0)} | 方向: {idea.get('category', 'N/A')}")
                
        # 显示已构建项目
        projects = self.builder.get_built_projects()[:3]
        if projects:
            print(f"\n🔨 最近构建的项目:")
            for proj in projects:
                print(f"  • {proj.get('name', 'Unknown')}")
                print(f"    类型: {proj.get('type', 'N/A')} | 技术栈: {', '.join(proj.get('tech_stack', []))}")
                
        print("\n" + "="*60)
        
    async def export_ideas(self):
        """导出创意报告"""
        ideas = await self.db.get_top_ideas(20) if self.db else []
        
        report = f"""# 🎯 Moltbook 创意报告

**生成时间**: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}
**创意数量**: {len(ideas)}

---

## 📊 Top 创意

"""
        for i, idea in enumerate(ideas[:10], 1):
            report += f"""### {i}. {idea.get('title', 'Unknown')}

**评分**: {idea.get('creativity_score', 0)}/100
**作者**: {idea.get('author', 'Unknown')}
**类别**: {idea.get('category', 'N/A')}
**标签**: {', '.join(idea.get('tags', []))}

**简介**: {idea.get('content', 'N/A')[:200]}...

**建议方向**:
"""
            for d in idea.get('project_directions', [])[:2]:
                report += f"- {d.get('type', 'N/A')}: {d.get('description', 'N/A')}\n"
                
            monetization = idea.get('monetization', [])
            if monetization:
                report += f"\n**变现方式**: {', '.join(monetization)}\n"
                
            report += "\n---\n\n"
            
        # 保存报告
        report_file = Path('reports/ideas_report.md')
        report_file.parent.mkdir(exist_ok=True)
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
            
        print(f"📄 报告已保存: {report_file}")
        return report_file
        
    async def run(self, mode='all'):
        """运行主程序"""
        try:
            await self.initialize()
            
            if mode == 'monitor':
                await self.run_monitoring_cycle()
            elif mode == 'build':
                await self.run_auto_build_cycle()
            elif mode == 'dashboard':
                await self.show_dashboard()
            elif mode == 'export':
                await self.export_ideas()
            else:  # all
                await self.run_monitoring_cycle()
                await self.run_auto_build_cycle()
                await self.show_dashboard()
                await self.export_ideas()
                
        finally:
            await self.cleanup()
            
        return True

def main():
    """主入口"""
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    dashboard = ObservatoryDashboard()
    
    if mode == 'help':
        print("""
🎯 Moltbook Observatory Dashboard

用法: python main.py <命令>

命令:
  monitor    监控 Moltbook，收集创意
  build      自动构建网站项目
  dashboard  显示仪表板统计
  export     导出创意报告
  all        执行完整流程（默认）
  help       显示帮助
        """)
        return
        
    asyncio.run(dashboard.run(mode))

if __name__ == '__main__':
    main()
