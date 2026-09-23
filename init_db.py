import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# MongoDB连接配置
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/douyin_analysis")
DATABASE_NAME = os.getenv("DATABASE_NAME", "douyin_analysis")

async def init_database():
    try:
        # 连接MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # 1. 热搜词集合 (hot_words) - 已有数据
        # 存储抖音热搜榜数据
        await db.hot_words.create_index([("position", 1), ("created_at", 1)], unique=True)
        await db.hot_words.create_index([("title", 1)])
        await db.hot_words.create_index([("hot_value", -1)])
        await db.hot_words.create_index([("created_at", -1)])
        
        # 2. 热搜分类集合 (hot_categories)
        # 存储热搜分类数据（种草热点、平台热点）
        await db.hot_categories.create_index([("category", 1), ("created_at", 1)], unique=True)
        await db.hot_categories.create_index([("created_at", -1)])
        
        # 3. 达人榜集合 (daren_rank)
        # 存储达人排行榜数据
        await db.daren_rank.create_index([("user_id", 1), ("date", 1)], unique=True)
        await db.daren_rank.create_index([("nickname", 1)])
        await db.daren_rank.create_index([("fans", -1)])
        await db.daren_rank.create_index([("sales", -1)])
        await db.daren_rank.create_index([("date", -1)])
        
        # 4. 热门视频集合 (hot_videos)
        # 存储热门视频数据
        await db.hot_videos.create_index([("video_id", 1), ("date", 1)], unique=True)
        await db.hot_videos.create_index([("user_id", 1)])
        await db.hot_videos.create_index([("likes", -1)])
        await db.hot_videos.create_index([("date", -1)])
        
        # 5. 用户数据集合 (user_data)
        # 存储用户基础数据
        await db.user_data.create_index([("user_id", 1)], unique=True)
        await db.user_data.create_index([("nickname", 1)])
        await db.user_data.create_index([("fans_count", -1)])
        await db.user_data.create_index([("created_at", -1)])
        
        # 6. 用户统计数据集合 (user_stats)
        # 存储用户每日统计数据
        await db.user_stats.create_index([("user_id", 1), ("date", 1)], unique=True)
        await db.user_stats.create_index([("date", -1)])
        await db.user_stats.create_index([("fans_increase", -1)])
        
        # 7. 粉丝画像集合 (fan_profiles)
        # 存储用户粉丝画像数据
        await db.fan_profiles.create_index([("user_id", 1), ("date", 1)], unique=True)
        await db.fan_profiles.create_index([("date", -1)])
        
        # 8. 创作建议集合 (content_suggestions)
        # 存储内容创作建议数据
        await db.content_suggestions.create_index([("date", 1)], unique=True)
        await db.content_suggestions.create_index([("created_at", -1)])
        
        # 9. 热词云集合 (word_cloud)
        # 存储热词云数据
        await db.word_cloud.create_index([("date", 1)], unique=True)
        await db.word_cloud.create_index([("created_at", -1)])
        await db.word_cloud.create_index([("value", -1)])
        
        print("数据库集合和索引创建成功！")
        
        # 关闭连接
        client.close()
        
    except Exception as e:
        print(f"创建数据库集合失败: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(init_database())