#!/usr/bin/env python3
"""
moltapi-shipyard-is-live-on- - API Server
自動生成的項目，基於 Moltbook 熱門討論: $SHIPYARD is live on Solana. No VCs. No presale. No permission.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="moltapi-shipyard-is-live-on-",
    description="自動生成的項目，基於 Moltbook 熱門討論: $SHIPYARD is live on Solana. No VCs. No presale. No permission."
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
        "name": "moltapi-shipyard-is-live-on-",
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
