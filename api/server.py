#!/usr/bin/env python3
"""
FastAPI Server - Web API 服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import asyncio
import json
from pathlib import Path

from config.config import Config
from.client import Molt apibookClient
from database.connection import Database, get_database
from analyzer.idea_analyzer import IdeaAnalyzer
from builder.website_builder import WebsiteBuilder

app = FastAPI(
    title="Moltbook Observatory API",
    description="Moltbook 被动监控和分析 API",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
db = None
client = None
analyzer = Analyzer = WebsiteBuilder = None

@app.on_event("startup")
async def startup():
    global db, client, analyzer, builder
    db = await get_database()
    client = MoltbookClient()
    analyzer = IdeaAnalyzer()
    builder = WebsiteBuilder()
    
@app.on_event("shutdown")
async def shutdown():
    if client:
        await client.close()
    if db:
        await db.disconnect()

# ============== 数据模型 ==============

class PostInput(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    author: str = "unknown"
    upvotes: int = 0

class IdeaResponse(BaseModel):
    id: str
    title: str
    content: str
    creativity_score: float
    category: str
    project_directions: List[dict]
    tech_stack: dict
    monetization: List[str]

class ProjectResponse(BaseModel):
    id: str
    name: str
    type: str
    project_path: str
    files_created: int
    tech_stack: List[str]

# ============== API 端点 ==============

@app.get("/")
async def root():
    """API 根路径"""
    return {
        "name": "Moltbook Observatory API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "feed": "/api/feed",
            "stats": "/api/stats",
            "ideas": "/api/ideas",
            "projects": "/api/projects",
            "build": "/api/build"
        }
    }

@app.get("/api/feed")
async def get_feed(limit: int = 50):
    """获取最新帖子"""
    if not client.api_key:
        posts = client.demo_data()['posts']
    else:
        posts = await client.get_posts(limit)
    return {"data": posts, "count": len(posts)}

@app.get("/api/stats")
async def get_stats():
    """获取统计信息"""
    if db:
        return await db.get_stats()
    return {"error": "数据库未连接"}

@app.get("/api/ideas")
async def get_ideas(limit: int = 10, min_score: int = 0):
    """获取高分创意"""
    if db:
        ideas = await db.get_top_ideas(100)
        if min_score > 0:
            ideas = [i for i in ideas if i.get('creativity_score', 0) >= min_score]
        return {"data": ideas[:limit], "count": len(ideas)}
    return {"error": "数据库未连接"}

@app.post("/api/analyze")
async def analyze_post(post: PostInput):
    """分析单个帖子"""
    post_data = post.dict()
    post_data['id'] = f"manual_{hash(post.title) % 10000}"
    
    analysis = analyzer.analyze(post_data)
    return analysis

@app.post("/api/build")
async def build_project(idea_id: str, direction_index: int = 0):
    """构建项目"""
    if not db:
        return {"error": "数据库未连接"}
        
    ideas = await db.get_top_ideas(100)
    idea = next((i for i in ideas if i['id'] == idea_id), None)
    
    if not idea:
        return {"error": "创意不存在"}
        
    directions = idea.get('project_directions', [])
    direction = directions[direction_index] if direction_index < len(directions) else None
    
    result = builder.build(idea, direction)
    return result

@app.get("/api/projects")
async def get_projects():
    """获取已构建项目"""
    projects = builder.get_built_projects()
    return {"data": projects, "count": len(projects)}

@app.get("/api/export")
async def export_ideas():
    """导出创意报告"""
    ideas = await db.get_top_ideas(100) if db else []
    
    report = f"""# Moltbook 创意报告

生成时间: {datetime.now().isoformat()}

## 创意列表

"""
    for i, idea in enumerate(ideas[:20], 1):
        report += f"""### {i}. {idea.get('title', 'Unknown')}
评分: {idea.get('creativity_score', 0)}/100
类别: {idea.get('category', 'N/A')}
"""
        
    return {"report": report}

# ============== 静态文件 ==============

WEB_DIR = Path('web/dist')

@app.get("/dashboard")
async def dashboard():
    """仪表板页面"""
    if WEB_DIR.exists():
        return FileResponse(str(WEB_DIR / 'index.html'))
    return {"message": "Web UI 未构建", "api_docs": "/docs"}

def run_server():
    """运行服务器"""
    import uvicorn
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)

if __name__ == '__main__':
    run_server()
