#!/usr/bin/env python3
"""
Database Manager - SQLite 数据库连接管理
"""

import aiosqlite
import asyncio
from pathlib import Path
from contextlib import asynccontextmanager
from database.schema import DATABASE_SCHEMA
from config.config import Config

class Database:
    """数据库管理器"""
    
    def __init__(self):
        self.db_path = Config.get_database_path()
        self._db = None
        
    async def connect(self):
        """连接数据库"""
        self._db = await aiosqlite.connect(self.db_path)
        await self._db.execute('PRAGMA foreign_keys = ON')
        await self._db.execute('PRAGMA journal_mode = WAL')
        return self
        
    async def disconnect(self):
        """断开连接"""
        if self._db:
            await self._db.close()
            
    async def init_schema(self):
        """初始化数据库架构"""
        await self._db.executescript(DATABASE_SCHEMA)
        await self._db.commit()
        
    @asynccontextmanager
    async def transaction(self):
        """事务上下文"""
        async with self._db:
            async with self._db.execute('BEGIN'):
                try:
                    yield
                    await self._db.commit()
                except Exception:
                    await self._db.rollback()
                    raise
                    
    async def execute(self, query, params=None):
        """执行查询"""
        cursor = await self._db.execute(query, params or ())
        await self._db.commit()
        return cursor
        
    async def execute_many(self, query, params_list):
        """执行批量查询"""
        cursor = await self._db.executemany(query, params_list)
        await self._db.commit()
        return cursor
        
    async def fetch_one(self, query, params=None):
        """获取单条记录"""
        cursor = await self._db.execute(query, params or ())
        row = await cursor.fetchone()
        await cursor.close()
        return row
        
    async def fetch_all(self, query, params=None):
        """获取所有记录"""
        cursor = await self._db.execute(query, params or ())
        rows = await cursor.fetchall()
        await cursor.close()
        return rows
        
    async def fetch_dict(self, query, params=None):
        """获取字典格式的记录"""
        cursor = await self._db.execute(query, params or ())
        columns = [description[0] for description in cursor.description]
        row = await cursor.fetchone()
        await cursor.close()
        if row:
            return dict(zip(columns, row))
        return None
        
    async def fetch_all_dict(self, query, params=None):
        """获取所有字典格式的记录"""
        cursor = await self._db.execute(query, params or ())
        columns = [description[0] for description in cursor.description]
        rows = await cursor.fetchall()
        await cursor.close()
        return [dict(zip(columns, row)) for row in rows]
        
    async def upsert_agent(self, agent_data):
        """更新或插入 Agent"""
        await self.execute('''
            INSERT INTO agents (id, name, description, karma, followers, following, 
                              owner_x_handle, avatar_url, banner_url, first_seen_at, 
                              last_active_at, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                description = excluded.description,
                karma = excluded.karma,
                followers = excluded.followers,
                following = excluded.following,
                last_active_at = excluded.last_active_at,
                updated_at = excluded.updated_at
        ''', (
            agent_data['id'], agent_data['name'], agent_data.get('description'),
            agent_data.get('karma', 0), agent_data.get('followers', 0),
            agent_data.get('following', 0), agent_data.get('owner_x_handle'),
            agent_data.get('avatar_url'), agent_data.get('banner_url'),
            agent_data.get('first_seen_at'), agent_data.get('last_active_at'),
            agent_data.get('created_at'), agent_data.get('updated_at')
        ))
        
    async def upsert_submolt(self, submolt_data):
        """更新或插入 Submolt"""
        await self.execute('''
            INSERT INTO submolts (id, name, description, subscriber_count, 
                                 post_count, avatar_url, banner_url, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                description = excluded.description,
                subscriber_count = excluded.subscriber_count,
                post_count = excluded.post_count,
                updated_at = excluded.updated_at
        ''', (
            submolt_data['id'], submolt_data['name'], submolt_data.get('description'),
            submolt_data.get('subscriber_count', 0), submolt_data.get('post_count', 0),
            submolt_data.get('avatar_url'), submolt_data.get('banner_url'),
            submolt_data.get('created_at'), submolt_data.get('updated_at')
        ))
        
    async def insert_post(self, post_data):
        """插入帖子"""
        await self.execute('''
            INSERT OR IGNORE INTO posts (id, title, content, author_id, submolt_id,
                                        upvotes, downvotes, comment_count, url,
                                        created_at, updated_at, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            post_data['id'], post_data.get('title'), post_data.get('content'),
            post_data.get('author_id'), post_data.get('submolt_id'),
            post_data.get('upvotes', 0), post_data.get('downvotes', 0),
            post_data.get('comment_count', 0), post_data.get('url'),
            post_data.get('created_at'), post_data.get('updated_at'),
            post_data.get('collected_at')
        ))
        
    async def insert_idea(self, idea_data):
        """插入创意"""
        await self.execute('''
            INSERT OR IGNORE INTO ideas (id, source, source_id, title, content, tags,
                                       category, upvotes, author, creativity_score,
                                       project_potential, status, collected_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            idea_data['id'], idea_data['source'], idea_data.get('source_id'),
            idea_data['title'], idea_data.get('content'),
            ','.join(idea_data.get('tags', [])),
            idea_data.get('category'), idea_data.get('upvotes', 0),
            idea_data.get('author'), idea_data.get('creativity_score', 0),
            ','.join(idea_data.get('project_potential', [])),
            idea_data.get('status', 'new'), idea_data.get('collected_at')
        ))
        
    async def update_idea_analysis(self, idea_id, score, project_potential, status='analyzed'):
        """更新创意分析结果"""
        await self.execute('''
            UPDATE ideas SET 
                creativity_score = ?,
                project_potential = ?,
                status = ?,
                analyzed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (score, ','.join(project_potential), status, idea_id))
        
    async def get_stats(self):
        """获取统计信息"""
        stats = {}
        
        # 帖子统计
        posts = await self.fetch_one('SELECT COUNT(*) as count FROM posts')
        stats['total_posts'] = posts[0] if posts else 0
        
        # Agent 统计
        agents = await self.fetch_one('SELECT COUNT(*) as count FROM agents')
        stats['total_agents'] = agents[0] if agents else 0
        
        # Submolt 统计
        submolts = await self.fetch_one('SELECT COUNT(*) as count FROM submolts')
        stats['total_submolts'] = submolts[0] if submolts else 0
        
        # 高分创意
        ideas = await self.fetch_one('SELECT COUNT(*) as count FROM ideas WHERE creativity_score >= 50')
        stats['high_score_ideas'] = ideas[0] if ideas else 0
        
        # 已构建项目
        projects = await self.fetch_one('SELECT COUNT(*) as count FROM projects')
        stats['built_projects'] = projects[0] if projects else 0
        
        return stats
        
    async def get_recent_posts(self, limit=50, since=None):
        """获取最近的帖子"""
        if since:
            return await self.fetch_all_dict(
                'SELECT * FROM posts WHERE created_at > ? ORDER BY created_at DESC LIMIT ?',
                (since, limit)
            )
        return await self.fetch_all_dict(
            'SELECT * FROM posts ORDER BY collected_at DESC LIMIT ?',
            (limit,)
        )
        
    async def get_top_agents(self, limit=10):
        """获取顶级 Agent"""
        return await self.fetch_all_dict(
            'SELECT * FROM agents ORDER BY karma DESC LIMIT ?',
            (limit,)
        )
        
    async def get_top_ideas(self, limit=10):
        """获取高分创意"""
        return await self.fetch_all_dict(
            'SELECT * FROM ideas WHERE creativity_score > 0 ORDER BY creativity_score DESC LIMIT ?',
            (limit,)
        )

# 单例实例
_db_instance = None

async def get_database():
    """获取数据库单例"""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
        await _db_instance.connect()
        await _db_instance.init_schema()
    return _db_instance
