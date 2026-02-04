#!/usr/bin/env python3
"""
Analyzer - 创意分析和评分系统
"""

import re
from collections import Counter
from datetime import datetime, timezone
from typing import Dict, List, Tuple
import hashlib

class IdeaAnalyzer:
    """创意分析和评分器"""
    
    # 技术创新关键词
    TECH_KEYWORDS = [
        'ai', 'agent', 'llm', 'gpt', '机器学习', '深度学习',
        'automation', 'workflow', '自动化', '工作流',
        'api', 'integration', '集成', '插件',
        'blockchain', 'web3', 'crypto',
        'cloud', 'serverless', '云原生',
        'iot', 'edge', '边缘计算'
    ]
    
    # 商业潜力关键词
    BUSINESS_KEYWORDS = [
        'saas', 'platform', '平台', 'marketplace', '市场',
        'subscription', '订阅', '付费', '商业化',
        'enterprise', '企业级', 'b2b',
        'startup', '创业', 'launch', '发布'
    ]
    
    # 实用工具关键词
    UTILITY_KEYWORDS = [
        'tool', '工具', 'library', '库', 'framework', '框架',
        'template', '模板', 'generator', '生成器',
        'dashboard', '仪表板', 'analytics', '分析',
        'monitoring', '监控', 'cli', '命令行'
    ]
    
    # 高潜力类别
    CATEGORIES = {
        'ai_application': {
            'keywords': ['ai', 'agent', 'llm', 'gpt', 'chatbot', 'assistant'],
            'weight': 1.3,
            'description': 'AI应用'
        },
        'automation': {
            'keywords': ['automation', 'workflow', '自动化', '工作流', 'pipeline'],
            'weight': 1.2,
            'description': '自动化工具'
        },
        'developer_tools': {
            'keywords': ['tool', 'cli', 'library', 'framework', 'sdk', 'api'],
            'weight': 1.1,
            'description': '开发者工具'
        },
        'platform': {
            'keywords': ['platform', 'marketplace', 'saas', 'platform'],
            'weight': 1.25,
            'description': '平台产品'
        },
        'content': {
            'keywords': ['content', 'blog', 'generator', 'writing', '文章'],
            'weight': 1.0,
            'description': '内容相关'
        }
    }
    
    def __init__(self):
        pass
        
    def analyze(self, post: Dict) -> Dict:
        """
        分析帖子并返回创意评估
        
        Args:
            post: 帖子数据
            
        Returns:
            包含评分和建议的字典
        """
        title = post.get('title', '').lower()
        content = post.get('content', '').lower()
        tags = [t.lower() for t in post.get('tags', [])]
        combined = f"{title} {content} {' '.join(tags)}"
        
        # 基础评分
        tech_score = self._calc_tech_score(combined, tags)
        business_score = self._calc_business_score(combined)
        utility_score = self._calc_utility_score(combined, tags)
        engagement_score = self._calc_engagement_score(post)
        category_score = self._calc_category_score(combined)
        
        # 综合评分
        total_score = (
            tech_score * 0.35 +
            business_score * 0.25 +
            utility_score * 0.20 +
            engagement_score * 0.10 +
            category_score * 0.10
        )
        
        # 提取项目方向
        project_directions = self._extract_project_directions(post)
        
        # 提取技术栈建议
        tech_stack = self._suggest_tech_stack(post)
        
        # 提取商业模式
        monetization = self._suggest_monetization(post)
        
        return {
            'id': post.get('id', hashlib.md5(str(post).encode()).hexdigest()[:12]),
            'title': post.get('title'),
            'content': post.get('content'),
            'tags': tags,
            'author': post.get('author', {}).get('name', 'unknown') if isinstance(post.get('author'), dict) else post.get('author'),
            'upvotes': post.get('upvotes', 0),
            'source': 'moltbook',
            'category': self._detect_category(combined),
            'creativity_score': min(100, round(total_score, 1)),
            'analysis': {
                'tech_score': tech_score,
                'business_score': business_score,
                'utility_score': utility_score,
                'engagement_score': engagement_score,
                'category_score': category_score
            },
            'reasons': self._get_reasons(combined, tags, post.get('upvotes', 0)),
            'project_directions': project_directions,
            'tech_stack': tech_stack,
            'monetization': monetization,
            'collectible': total_score >= 25,
            'high_quality': total_score >= 50,
            'analyzed_at': datetime.now(timezone.utc).isoformat()
        }
        
    def _calc_tech_score(self, text: str, tags: List[str]) -> float:
        """计算技术创新评分"""
        score = 0
        text_lower = text.lower()
        
        # 检查技术关键词
        for kw in self.TECH_KEYWORDS:
            if kw in text_lower:
                score += 5
        for kw in tags:
            if kw.lower() in self.TECH_KEYWORDS:
                score += 8
                
        return min(40, score)
        
    def _calc_business_score(self, text: str) -> float:
        """计算商业潜力评分"""
        score = 0
        text_lower = text.lower()
        
        for kw in self.BUSINESS_KEYWORDS:
            if kw in text_lower:
                score += 8
                
        return min(30, score)
        
    def _calc_utility_score(self, text: str, tags: List[str]) -> float:
        """计算实用价值评分"""
        score = 0
        text_lower = text.lower()
        
        for kw in self.UTILITY_KEYWORDS:
            if kw in text_lower:
                score += 6
        for kw in tags:
            if kw.lower() in self.UTILITY_KEYWORDS:
                score += 5
                
        return min(25, score)
        
    def _calc_engagement_score(self, post: Dict) -> float:
        """计算社区参与度评分"""
        upvotes = post.get('upvotes', 0)
        comments = post.get('comment_count', 0)
        
        score = min(15, upvotes * 0.1)
        score += min(5, comments * 0.1)
        
        return score
        
    def _calc_category_score(self, text: str) -> float:
        """计算类别加成评分"""
        max_score = 0
        text_lower = text.lower()
        
        for category, info in self.CATEGORIES.items():
            matches = sum(1 for kw in info['keywords'] if kw in text_lower)
            if matches > 0:
                score = matches * 5 * info['weight']
                max_score = max(max_score, min(20, score))
                
        return max_score
        
    def _detect_category(self, text: str) -> str:
        """检测主要类别"""
        text_lower = text.lower()
        
        for category, info in self.CATEGORIES.items():
            matches = sum(1 for kw in info['keywords'] if kw in text_lower)
            if matches >= 2:
                return info['description']
                
        return '通用'
        
    def _extract_project_directions(self, post: Dict) -> List[Dict]:
        """提取可能的项目方向"""
        directions = []
        title = post.get('title', '').lower()
        content = post.get('content', '').lower()
        
        # 基于内容分析项目类型
        if any(kw in content for kw in ['dashboard', 'monitor', 'analytics', '监控']):
            directions.append({
                'type': '数据分析仪表板',
                'description': '实时监控和可视化平台',
                'priority': 'high'
            })
            
        if any(kw in content for kw in ['generator', 'create', 'build', '生成']):
            directions.append({
                'type': '自动化生成器',
                'description': '一键生成内容或项目结构',
                'priority': 'high'
            })
            
        if any(kw in content for kw in ['agent', 'ai', '智能']):
            directions.append({
                'type': 'AI Agent 应用',
                'description': '基于AI的智能助手或Agent',
                'priority': 'high'
            })
            
        if any(kw in content for kw in ['platform', 'marketplace', '平台']):
            directions.append({
                'type': 'SaaS 平台',
                'description': '可扩展的在线服务平台',
                'priority': 'medium'
            })
            
        if any(kw in content for kw in ['tool', '工具']):
            directions.append({
                'type': '在线工具网站',
                'description': '提供在线功能的小工具',
                'priority': 'medium'
            })
            
        if any(kw in content for kw in ['blog', '内容', 'article']):
            directions.append({
                'type': '博客/内容网站',
                'description': '内容展示和分享平台',
                'priority': 'medium'
            })
            
        # 默认方向
        if not directions:
            directions.append({
                'type': '创意项目原型',
                'description': '基于想法构建的演示项目',
                'priority': 'low'
            })
            
        return directions
        
    def _suggest_tech_stack(self, post: Dict) -> Dict:
        """建议技术栈"""
        title = post.get('title', '').lower()
        content = post.get('content', '').lower()
        combined = f"{title} {content}"
        
        suggestions = {
            'frontend': [],
            'backend': [],
            'database': [],
            'deployment': []
        }
        
        # 分析前端
        if any(kw in combined for kw in ['dashboard', 'ui', 'frontend', 'web']):
            suggestions['frontend'] = ['React', 'Vue.js', 'Next.js']
        else:
            suggestions['frontend'] = ['React', 'Vue.js']
            
        # 分析后端
        if any(kw in combined for kw in ['api', 'ai', 'ml', '智能']):
            suggestions['backend'] = ['FastAPI', 'Python', 'Node.js']
        elif any(kw in combined for kw in ['real-time', '实时', 'socket']):
            suggestions['backend'] = ['Node.js', 'FastAPI']
        else:
            suggestions['backend'] = ['FastAPI', 'Express']
            
        # 分析数据库
        if any(kw in combined for kw in ['analytics', 'data', '分析']):
            suggestions['database'] = ['PostgreSQL', 'TimescaleDB', 'InfluxDB']
        else:
            suggestions['database'] = ['PostgreSQL', 'SQLite']
            
        # 部署建议
        suggestions['deployment'] = ['Vercel', 'Railway', 'Docker']
        
        return suggestions
        
    def _suggest_monetization(self, post: Dict) -> List[str]:
        """建议商业模式"""
        monetization = []
        content = f"{post.get('title', '')} {post.get('content', '')}".lower()
        
        if any(kw in content for kw in ['saas', 'platform', 'enterprise', '企业']):
            monetization = ['订阅制', '企业版', '私有化部署']
        elif any(kw in content for kw in ['tool', '工具', '免费']):
            monetization = ['免费增值', '广告收入', '赞助']
        elif any(kw in content for kw in ['api', 'service', '服务']):
            monetization = ['API调用计费', '按量付费']
        else:
            monetization = ['广告', '赞助', '联盟营销']
            
        return monetization
        
    def _get_reasons(self, text: str, tags: List[str], upvotes: int) -> List[str]:
        """获取评分原因"""
        reasons = []
        
        if upvotes >= 100:
            reasons.append(f'高人气({upvotes}赞)')
        elif upvotes >= 50:
            reasons.append(f'中等人气({upvotes}赞)')
            
        if any(kw in text for kw in ['ai', 'agent', 'llm']):
            reasons.append('AI/Agent相关')
        if any(kw in text for kw in ['automation', 'workflow']):
            reasons.append('自动化相关')
        if any(kw in text for kw in ['platform', 'saas']):
            reasons.append('平台潜力')
        if any(kw in text for kw in ['tool', 'generator']):
            reasons.append('实用工具')
        if any(kw in tags for kw in ['trending', 'popular']):
            reasons.append('热门标签')
            
        return reasons
        
    def batch_analyze(self, posts: List[Dict]) -> List[Dict]:
        """批量分析帖子"""
        results = []
        for post in posts:
            analysis = self.analyze(post)
            if analysis['collectible']:
                results.append(analysis)
        # 按评分排序
        results.sort(key=lambda x: x['creativity_score'], reverse=True)
        return results
        
    def get_top_ideas(self, analyzed_posts: List[Dict], min_score: int = 40) -> List[Dict]:
        """获取高分创意"""
        return [
            p for p in analyzed_posts 
            if p.get('creativity_score', 0) >= min_score
        ]
