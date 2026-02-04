#!/usr/bin/env python3
"""
Moltbook Observatory Dashboard
被动监控和分析仪表板
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """配置管理"""
    
    # API 配置
    MOLTBOOK_API_KEY = os.getenv('MOLTBOOK_API_KEY', '')
    BASE_URL = 'https://moltbook.com/api/v1'
    
    # 数据库
    DATABASE_PATH = os.getenv('DATABASE_PATH', './data/observatory.db')
    
    # 监控频率
    POLL_POSTS_INTERVAL = int(os.getenv('POLL_POSTS_INTERVAL', 120))
    POLL_AGENTS_INTERVAL = int(os.getenv('POLL_AGENTS_INTERVAL', 900))
    POLL_SUBMOLTS_INTERVAL = int(os.getenv('POLL_SUBMOLTS_INTERVAL', 3600))
    POLL_TRENDS_INTERVAL = int(os.getenv('POLL_TRENDS_INTERVAL', 600))
    POLL_SNAPSHOTS_INTERVAL = int(os.getenv('POLL_SNAPSHOTS_INTERVAL', 3600))
    
    # 服务器
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 8000))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # 分析
    SENTIMENT_ENABLED = os.getenv('SENTIMENT_ENABLED', 'true').lower() == 'true'
    TREND_WORD_MIN_LENGTH = int(os.getenv('TREND_WORD_MIN_LENGTH', 3))
    TREND_TOP_WORDS = int(os.getenv('TREND_TOP_WORDS', 50))
    
    # 导出
    EXPORT_DIR = os.getenv('EXPORT_DIR', './exports')
    
    @classmethod
    def get_headers(cls):
        """获取 API 请求头"""
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Moltbook-Observatory-Dashboard/1.0'
        }
        if cls.MOLTBOOK_API_KEY:
            headers['Authorization'] = f'Bearer {cls.MOLTBOOK_API_KEY}'
        return headers
        
    @classmethod
    def get_database_path(cls):
        """获取数据库路径"""
        path = Path(cls.DATABASE_PATH)
        path.parent.mkdir(parents=True, exist_ok=True)
        return str(path)
        
    @classmethod
    def get_export_dir(cls):
        """获取导出目录"""
        path = Path(cls.EXPORT_DIR)
        path.mkdir(parents=True, exist_ok=True)
        return str(path)
