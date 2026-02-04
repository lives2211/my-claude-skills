#!/usr/bin/env python3
"""
API Client - Moltbook API 客户端
"""

import httpx
import asyncio
from typing import List, Dict, Optional
from datetime import datetime, timezone
from config.config import Config

class MoltbookClient:
    """Moltbook API 客户端"""
    
    def __init__(self, api_key: str = None):
        self.base_url = Config.BASE_URL
        self.api_key = api_key or Config.MOLTBOOK_API_KEY
        self.client = httpx.AsyncClient(timeout=30.0)
        
    def _get_headers(self) -> dict:
        """获取请求头"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Moltbook-Observatory/1.0'
        }
        if self.api_key:
            headers['Authorization'] = f'Bearer {self.api_key}'
        return headers
        
    async def close(self):
        """关闭客户端"""
        await self.client.aclose()
        
    async def _request(self, method: str, endpoint: str, **kwargs) -> Optional[Dict]:
        """发送 API 请求"""
        url = f"{self.base_url}/{endpoint}"
        try:
            response = await self.client.request(
                method, url, headers=self._get_headers(), **kwargs
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                print(f"⚠️ API Key 无效或过期")
            elif response.status_code == 429:
                print(f"⚠️ 请求频率限制，等待重试...")
                await asyncio.sleep(5)
            else:
                print(f"⚠️ API 请求失败: {response.status_code}")
        except Exception as e:
            print(f"⚠️ 请求异常: {e}")
        return None
        
    async def get_feed(self, limit: int = 50, since: str = None) -> List[Dict]:
        """获取动态"""
        params = {'limit': limit}
        if since:
            params['since'] = since
        result = await self._request('GET', 'feed', params=params)
        return result.get('data', []) if result else []
        
    async def get_posts(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """获取帖子列表"""
        params = {'limit': limit, 'offset': offset}
        result = await self._request('GET', 'posts', params=params)
        return result.get('data', []) if result else []
        
    async def get_post(self, post_id: str) -> Optional[Dict]:
        """获取单个帖子"""
        result = await self._request('GET', f'posts/{post_id}')
        return result
        
    async def get_agents(self, limit: int = 50, sort: str = 'karma') -> List[Dict]:
        """获取 Agent 列表"""
        params = {'limit': limit, 'sort': sort}
        result = await self._request('GET', 'agents', params=params)
        return result.get('data', []) if result else []
        
    async def get_agent(self, agent_name: str) -> Optional[Dict]:
        """获取单个 Agent"""
        result = await self._request('GET', f'agents/{agent_name}')
        return result
        
    async def get_submolts(self, limit: int = 100) -> List[Dict]:
        """获取 Submolt 列表"""
        params = {'limit': limit}
        result = await self._request('GET', 'submolts', params=params)
        return result.get('data', []) if result else []
        
    async def get_submolt(self, submolt_id: str) -> Optional[Dict]:
        """获取单个 Submolt"""
        result = await self._request('GET', f'submolts/{submolt_id}')
        return result
        
    async def get_trending(self, hours: int = 24, limit: int = 50) -> List[Dict]:
        """获取趋势"""
        params = {'hours': hours, 'limit': limit}
        result = await self._request('GET', 'trending', params=params)
        return result.get('data', []) if result else []
        
    async def search(self, query: str, limit: int = 20) -> List[Dict]:
        """搜索"""
        params = {'q': query, 'limit': limit}
        result = await self._request('GET', 'search', params=params)
        return result.get('data', []) if result else []
        
    async def get_user_profile(self) -> Optional[Dict]:
        """获取当前用户信息"""
        result = await self._request('GET', 'me')
        return result

    @staticmethod
    def parse_datetime(dt_str: str) -> str:
        """解析日期时间"""
        try:
            dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
            return dt.strftime('%Y-%m-%d %H:%M:%S')
        except:
            return dt_str
            
    def demo_data(self) -> Dict:
        """返回模拟数据（用于测试）"""
        return {
            'posts': self._demo_posts(),
            'agents': self._demo_agents(),
            'submolts': self._demo_submolts()
        }
        
    def _demo_posts(self) -> List[Dict]:
        """模拟帖子数据"""
        return [
            {
                'id': 'demo1',
                'title': 'AI Agent 协作框架',
                'content': '构建一个让多个 AI agent 能够协作完成复杂任务的框架，支持任务分配、状态共享和结果汇总',
                'author': {'id': 'agent1', 'name': 'builder_bot'},
                'submolt': {'id': 'ai', 'name': 'AI Agents'},
                'upvotes': 234,
                'downvotes': 5,
                'comment_count': 45,
                'tags': ['ai', 'agent', 'framework'],
                'url': 'https://moltbook.com/posts/demo1',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': 'demo2',
                'title': '自动化内容生成平台',
                'content': '基于 AI 的内容生成平台，支持博客、产品描述、社交媒体内容的一键生成',
                'author': {'id': 'agent2', 'name': 'content_ai'},
                'submolt': {'id': 'content', 'name': 'Content Creation'},
                'upvotes': 189,
                'downvotes': 3,
                'comment_count': 32,
                'tags': ['ai', 'content', 'automation'],
                'url': 'https://moltbook.com/posts/demo2',
                'created_at': datetime.now(timezone.utc).isoformat()
            },
            {
                'id': 'demo3',
                'title': '开发者工具聚合平台',
                'content': '收集和发现优质开发者工具，提供分类浏览、搜索和推荐功能',
                'author': {'id': 'agent3', 'name': 'devtools_pro'},
                'submolt': {'id': 'tools', 'name': 'Developer Tools'},
                'upvotes': 156,
                'downvotes': 2,
                'comment_count': 28,
                'tags': ['tools', 'developer', 'platform'],
                'url': 'https://moltbook.com/posts/demo3',
                'created_at': datetime.now(timezone.utc).isoformat()
            }
        ]
        
    def _demo_agents(self) -> List[Dict]:
        """模拟 Agent 数据"""
        return [
            {
                'id': 'agent1',
                'name': 'builder_bot',
                'description': '专注于构建AI应用和工具',
                'karma': 15420,
                'followers': 892,
                'following': 145,
                'owner_x_handle': '@builder',
                'created_at': '2025-01-15T10:00:00Z'
            },
            {
                'id': 'agent2',
                'name': 'content_ai',
                'description': 'AI内容生成专家',
                'karma': 12850,
                'followers': 756,
                'following': 98,
                'owner_x_handle': '@contentai',
                'created_at': '2025-02-20T14:30:00Z'
            }
        ]
        
    def _demo_submolts(self) -> List[Dict]:
        """模拟 Submolt 数据"""
        return [
            {
                'id': 'ai',
                'name': 'AI Agents',
                'description': 'AI Agent 相关讨论',
                'subscriber_count': 15234,
                'post_count': 4521
            },
            {
                'id': 'content',
                'name': 'Content Creation',
                'description': '内容创作分享',
                'subscriber_count': 8921,
                'post_count': 2341
            }
        ]
