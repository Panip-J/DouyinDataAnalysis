from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager

# 加载环境变量
load_dotenv()

# MongoDB连接配置
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/douyin_analysis")
DATABASE_NAME = os.getenv("DATABASE_NAME", "douyin_analysis")

# 数据库连接
client = None
db = None

# 使用新的生命周期管理方式
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    # 测试连接
    try:
        await client.admin.command('ping')
        print("成功连接到MongoDB")
    except Exception as e:
        print(f"MongoDB连接失败: {e}")
        raise
    
    yield  # 应用运行期间
    
    # 关闭时执行
    if client:
        client.close()
        print("MongoDB连接已关闭")

# 创建FastAPI应用
app = FastAPI(
    title="抖音数据分析API", 
    description="提供抖音数据分析平台的后端API服务",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模型定义
class HotWord(BaseModel):
    keyword: str
    hot_value: int
    position: int
    tag: Optional[str] = None
    created_at: datetime

class User(BaseModel):
    user_id: str
    nickname: str
    follower_count: int
    following_count: int
    video_count: int
    likes_count: int
    avatar_url: Optional[str] = None

class Video(BaseModel):
    video_id: str
    title: str
    author: str
    author_id: str
    url: str
    create_time: str
    likes: int
    comments: int
    shares: int

# API路由
@app.get("/")
async def root():
    return {"message": "欢迎使用抖音数据分析API"}

@app.get("/api/hot-words", response_model=List[dict])
async def get_hot_words():
    try:
        # 获取最新的热搜记录时间
        latest = await db.hot_searches.find_one(
            sort=[("created_at", -1)]
        )
        
        if not latest:
            return []
            
        latest_time = latest["created_at"]
        
        # 获取该时间点的所有热搜，按位置排序
        cursor = db.hot_searches.find(
            {"created_at": latest_time}
        ).sort("position", 1).limit(50)
        
        hot_words = await cursor.to_list(length=50)
        
        # 转换ObjectId为字符串
        for word in hot_words:
            if "_id" in word:
                word["_id"] = str(word["_id"])
            if "created_at" in word:
                word["created_at"] = word["created_at"].isoformat()
        
        return hot_words
    except Exception as e:
        print(f"获取热搜数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取热搜数据失败: {str(e)}")

@app.get("/api/hot-videos", response_model=List[dict])
async def get_hot_videos(limit: int = 20, skip: int = 0):
    try:
        cursor = db.hot_videos.find().sort(
            "hot_score", -1
        ).skip(skip).limit(limit)
        
        videos = await cursor.to_list(length=limit)
        
        # 转换ObjectId为字符串
        for video in videos:
            if "_id" in video:
                video["_id"] = str(video["_id"])
            if "updated_at" in video:
                video["updated_at"] = video["updated_at"].isoformat()
        
        return videos
    except Exception as e:
        print(f"获取热门视频失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取热门视频失败: {str(e)}")

@app.get("/api/users", response_model=List[dict])
async def get_users(limit: int = 10, skip: int = 0):
    try:
        cursor = db.users.find().sort(
            "follower_count", -1
        ).skip(skip).limit(limit)
        
        users = await cursor.to_list(length=limit)
        
        # 转换ObjectId为字符串
        for user in users:
            if "_id" in user:
                user["_id"] = str(user["_id"])
            if "updated_at" in user:
                user["updated_at"] = user["updated_at"].isoformat()
        
        return users
    except Exception as e:
        print(f"获取用户数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取用户数据失败: {str(e)}")

@app.get("/api/user/{user_id}", response_model=dict)
async def get_user(user_id: str):
    try:
        user = await db.users.find_one({"user_id": user_id})
        
        if not user:
            raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
        
        # 转换ObjectId为字符串
        if "_id" in user:
            user["_id"] = str(user["_id"])
        if "updated_at" in user:
            user["updated_at"] = user["updated_at"].isoformat()
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取用户数据失败: {str(e)}")

@app.get("/api/user/{user_id}/videos", response_model=List[dict])
async def get_user_videos(user_id: str, limit: int = 20, skip: int = 0):
    try:
        cursor = db.videos.find(
            {"author_id": user_id}
        ).sort("create_time", -1).skip(skip).limit(limit)
        
        videos = await cursor.to_list(length=limit)
        
        # 转换ObjectId为字符串
        for video in videos:
            if "_id" in video:
                video["_id"] = str(video["_id"])
            if "updated_at" in video:
                video["updated_at"] = video["updated_at"].isoformat()
        
        return videos
    except Exception as e:
        print(f"获取用户视频失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取用户视频失败: {str(e)}")

@app.get("/api/crawled-users", response_model=List[dict])
async def get_crawled_users(limit: int = 10, skip: int = 0):
    """
    获取由 crawl/douyin_user_crawl.py 爬取的用户数据
    """
    try:
        # 从users集合中获取数据，按粉丝数降序排列
        cursor = db.users.find().sort(
            "fans_count", -1
        ).skip(skip).limit(limit)
        
        users = await cursor.to_list(length=limit)
        
        # 如果没有找到数据，尝试从user_data集合获取
        if not users:
            cursor = db.user_data.find().sort(
                "follower_count", -1
            ).skip(skip).limit(limit)
            users = await cursor.to_list(length=limit)
        
        # 转换ObjectId为字符串
        for user in users:
            if "_id" in user:
                user["_id"] = str(user["_id"])
            if "updated_at" in user:
                user["updated_at"] = user["updated_at"].isoformat()
            if "created_at" in user:
                user["created_at"] = user["created_at"].isoformat()
                
            # 计算平均点赞数
            if "likes_count" in user and "video_count" in user and user["video_count"] > 0:
                user["avg_likes"] = user["likes_count"] // user["video_count"]
            elif "total_favorited" in user and "aweme_count" in user and user["aweme_count"] > 0:
                user["avg_likes"] = user["total_favorited"] // user["aweme_count"]
            else:
                user["avg_likes"] = 0
                
            # 确保字段命名一致
            if "follower_count" in user and "fans_count" not in user:
                user["fans_count"] = user["follower_count"]
            if "mplatform_followers_count" in user and "fans_count" not in user:
                user["fans_count"] = user["mplatform_followers_count"]
        
        return users
    except Exception as e:
        print(f"获取爬虫用户数据失败: {e}")
        raise HTTPException(status_code=500, detail=f"获取爬虫用户数据失败: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)