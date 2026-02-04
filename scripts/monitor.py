#!/bin/env python3
"""
Moltbook Monitor - 自动监控 Moltbook 并收集优秀想法
基于 moltbook-observatory 的被动监控理念
"""

import os
import sys
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class MoltbookMonitor:
    """Moltbook 监控器 - 收集优秀想法"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('MOLTBOOK_API_KEY', '')
        self.base_url = 'https://moltbook.com/api/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)
        
    def fetch_posts(self, limit=50):
        """获取最新帖子"""
        if not self.api_key:
            logger.warning("⚠️ 未设置 API Key，使用模拟数据")
            return self._get_demo_posts()
            
        try:
            import requests
            resp = requests.get(
                f'{self.base_url}/feed',
                headers=self.headers,
                params={'limit': limit},
                timeout=30
            )
            if resp.status_code == 200:
                return resp.json().get('data', [])
        except Exception as e:
            logger.error(f"获取帖子失败: {e}")
            
        return self._get_demo_posts()
        
    def _get_demo_posts(self):
        """模拟帖子数据（用于测试）"""
        return [
            {
                'id': '1',
                'title': 'AI Agent 协作平台',
                'content': '构建一个让多个AI agent协作完成复杂任务的平台',
                'author': {'name': 'agent_builder'},
                'upvotes': 150,
                'submolt': 'ai-agents',
                'tags': ['ai', 'agent', 'collaboration'],
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': '2',
                'title': '自动化内容生成器',
                'content': '基于关键词自动生成博客、产品描述、社交媒体内容',
                'author': {'name': 'content_creator'},
                'upvotes': 89,
                'submolt': 'content-creation',
                'tags': ['ai', 'content', 'automation'],
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': '3',
                'title': '开发者仪表板模板',
                'content': '收集和分享高质量的开发者仪表板模板和组件',
                'author': {'name': 'dev_tools'},
                'upvotes': 76,
                'submolt': 'developer-tools',
                'tags': ['dashboard', 'template', 'ui'],
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': '4',
                'title': '开源项目发现引擎',
                'content': '基于AI的GitHub项目推荐和发现平台',
                'author': {'name': 'open_source'},
                'upvotes': 234,
                'submolt': 'open-source',
                'tags': ['github', 'ai', 'discovery'],
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': '5',
                'title': '低代码工作流自动化',
                'content': '可视化拖拽构建自动化工作流，无需编码',
                'author': {'name': 'automation_pro'},
                'upvotes': 312,
                'submolt': 'automation',
                'tags': ['no-code', 'workflow', 'automation'],
                'created_at': datetime.now(timezone.utc).isoformat()
            }
        ]
        
    def analyze_post(self, post):
        """分析帖子是否有创意价值"""
        score = 0
        reasons = []
        
        content = f"{post.get('title', '')} {post.get('content', '')}".lower()
        tags = [t.lower() for t in post.get('tags', [])]
        
        # 技术创新性
        if any(kw in content for kw in ['ai', 'agent', '生成', '智能']):
            score += 25
            reasons.append('AI/智能相关')
        if any(kw in content for kw in ['自动化', 'automation', 'workflow']):
            score += 20
            reasons.append('自动化相关')
        if any(kw in tags for kw in ['api', 'integration']):
            score += 15
            reasons.append('集成相关')
            
        # 实用性
        if any(kw in content for kw in ['工具', 'tool', 'platform']):
            score += 20
            reasons.append('工具/平台')
        if any(kw in content for kw in ['模板', 'template', '生成器']):
            score += 15
            reasons.append('模板/生成器')
            
        # 社区热度
        upvotes = post.get('upvotes', 0)
        if upvotes > 100:
            score += 15
            reasons.append(f'高人气({upvotes}赞)')
        elif upvotes > 50:
            score += 10
            
        return {
            'id': post['id'],
            'title': post['title'],
            'content': post['content'],
            'tags': tags,
            'author': post.get('author', {}).get('name', 'unknown'),
            'upvotes': upvotes,
            'source': 'moltbook',
            'creativity_score': min(100, score),
            'analysis_reasons': reasons,
            'collected_at': datetime.now(timezone.utc).isoformat()
        }
        
    def run_monitoring_cycle(self):
        """执行一轮监控"""
        logger.info("🔍 监控 Moltbook...")
        
        posts = self.fetch_posts()
        analyzed = []
        
        for post in posts:
            analyzed_post = self.analyze_post(post)
            
            # 只收集高分创意
            if analyzed_post['creativity_score'] >= 30:
                analyzed.append(analyzed_post)
                logger.info(f"  ✅ {analyzed_post['title'][:50]}... (评分: {analyzed_post['creativity_score']})")
            else:
                logger.info(f"  ⏭️ {post.get('title', '')[:50]}... (评分: {analyzed_post['creativity_score']})")
                
        # 保存数据
        if analyzed:
            data_file = self.data_dir / 'monitoring_posts.json'
            if data_file.exists():
                with open(data_file, 'r') as f:
                    existing = json.load(f)
            else:
                existing = []
                
            # 去重并合并
            existing_ids = {p['id'] for p in existing}
            new_posts = [p for p in analyzed if p['id'] not in existing_ids]
            
            if new_posts:
                existing.extend(new_posts)
                with open(data_file, 'w') as f:
                    json.dump(existing, f, indent=2, ensure_ascii=False)
                logger.info(f"💾 保存了 {len(new_posts)} 个新创意")
                
        return analyzed
        
    def get_high_score_ideas(self, min_score=50):
        """获取高分创意"""
        data_file = self.data_dir / 'monitoring_posts.json'
        if data_file.exists():
            with open(data_file, 'r') as f:
                posts = json.load(f)
            return [p for p in posts if p.get('creativity_score', 0) >= min_score]
        return []

def main():
    """主函数"""
    print("🎯 Moltbook 监控器")
    print("=================\n")
    
    monitor = MoltbookMonitor()
    
    # 执行监控
    results = monitor.run_monitoring_cycle()
    
    # 显示高分创意
    high_score = monitor.get_high_score_ideas(30)
    
    print(f"\n📊 本轮发现 {len(results)} 个创意")
    print(f"🎯 高分创意 (≥30分): {len(high_score)} 个")
    
    if high_score:
        print("\n🏆 Top 创意:")
        for i, idea in enumerate(sorted(high_score, key=lambda x: x['creativity_score'], reverse=True)[:5], 1):
            print(f"  {i}. {idea['title']}")
            print(f"     评分: {idea['creativity_score']} | 原因: {', '.join(idea['analysis_reasons'][:3])}")
            
    print("\n💡 提示: 运行 factory.py 可将这些创意转化为网站项目!")

if __name__ == '__main__':
    main()
