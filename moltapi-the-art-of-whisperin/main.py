#!/usr/bin/env python3
"""
moltapi-the-art-of-whisperin - API Server
自動生成的項目，基於 Moltbook 熱門討論: The Art of Whispering to Agents
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="moltapi-the-art-of-whisperin",
    description="自動生成的項目，基於 Moltbook 熱門討論: The Art of Whispering to Agents"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "name": "moltapi-the-art-of-whisperin",
        "status": "running",
        "message": "API is working!"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/api/info")
async def info():
    return {
        "features": ['REST API', '錯誤處理', 'API 文檔'],
        "type": "api"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
