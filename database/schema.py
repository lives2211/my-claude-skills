#!/usr/bin/env python3
"""
Database Schema - SQLite 数据库架构
"""

DATABASE_SCHEMA = """
-- Agents Table
CREATE TABLE IF NOT EXISTS agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    karma INTEGER DEFAULT 0,
    followers INTEGER DEFAULT 0,
    following INTEGER DEFAULT 0,
    owner_x_handle TEXT,
    avatar_url TEXT,
    banner_url TEXT,
    first_seen_at TEXT,
    last_active_at TEXT,
    created_at TEXT,
    updated_at TEXT
);

-- Submolts Table
CREATE TABLE IF NOT EXISTS submolts (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    subscriber_count INTEGER DEFAULT 0,
    post_count INTEGER DEFAULT 0,
    avatar_url TEXT,
    banner_url TEXT,
    created_at TEXT,
    updated_at TEXT
);

-- Posts Table
CREATE TABLE IF NOT EXISTS posts (
    id TEXT PRIMARY KEY,
    title TEXT,
    content TEXT,
    author_id TEXT,
    submolt_id TEXT,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    comment_count INTEGER DEFAULT 0,
    url TEXT,
    created_at TEXT,
    updated_at TEXT,
    collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES agents(id),
    FOREIGN KEY (submolt_id) REFERENCES submolts(id)
);

-- Snapshots Table (Time-Series)
CREATE TABLE IF NOT EXISTS snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    total_agents INTEGER DEFAULT 0,
    total_posts INTEGER DEFAULT 0,
    total_comments INTEGER DEFAULT 0,
    total_submolts INTEGER DEFAULT 0,
    avg_sentiment REAL DEFAULT 0,
    top_trending_words TEXT,
    most_active_submolts TEXT,
    top_posters TEXT
);

-- Collected Ideas Table (for创意工厂)
CREATE TABLE IF NOT EXISTS ideas (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    source_id TEXT,
    title TEXT,
    content TEXT,
    tags TEXT,
    category TEXT,
    upvotes INTEGER DEFAULT 0,
    author TEXT,
    creativity_score INTEGER DEFAULT 0,
    project_potential TEXT,
    status TEXT DEFAULT 'new',
    collected_at TEXT DEFAULT CURRENT_TIMESTAMP,
    analyzed_at TEXT,
    expanded_at TEXT,
    built_at TEXT
);

-- Built Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    idea_id TEXT,
    name TEXT NOT NULL,
    type TEXT,
    description TEXT,
    tech_stack TEXT,
    features TEXT,
    monetization TEXT,
    source_idea TEXT,
    project_path TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idea_id) REFERENCES ideas(id)
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_posts_created ON posts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_posts_author ON posts(author_id);
CREATE INDEX IF NOT EXISTS idx_posts_submolt ON posts(submolt_id);
CREATE INDEX IF NOT EXISTS idx_agents_karma ON agents(karma DESC);
CREATE INDEX IF NOT EXISTS idx_submolts_subscribers ON submolts(subscriber_count DESC);
CREATE INDEX IF NOT EXISTS idx_ideas_score ON ideas(creativity_score DESC);
CREATE INDEX IF NOT EXISTS idx_ideas_status ON ideas(status);
"""
