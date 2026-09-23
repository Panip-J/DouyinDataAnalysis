from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

app = FastAPI(title="抖音数据分析平台API示例")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB连接
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017/douyin_analysis")
DATABASE_NAME = os.getenv("DATABASE_NAME", "douyin_analysis")

# 数据模型
class HotWord(BaseModel):
    position: Optional[int]
    title: str
    link: str
    time: Optional[str]
    hot_value: int
    created_at: datetime

class HotWordStats(BaseModel):
    total_words: int
    avg_hot_value: float
    max_hot_value: int
    min_hot_value: int
    top_words: List[HotWord]

class HotCategory(BaseModel):
    category: str
    date: str
    hot_list: List[Dict[str, Any]]
    created_at: datetime

class DarenRank(BaseModel):
    user_id: str
    nickname: str
    fans: int
    sales: float
    change: float
    date: str
    created_at: datetime

class HotVideo(BaseModel):
    video_id: str
    user_id: str
    title: str
    user: str
    date: str
    likes: str
    shares: str
    comments: str
    created_at: datetime

class UserData(BaseModel):
    user_id: str
    nickname: str
    fans_count: int
    video_count: int
    created_at: datetime

class UserStats(BaseModel):
    user_id: str
    date: str
    fans_count: int
    fans_increase: int
    video_count: int
    avg_play: int
    created_at: datetime

class FanProfile(BaseModel):
    user_id: str
    date: str
    gender_ratio: Dict[str, float]
    age_distribution: Dict[str, float]
    location_distribution: Dict[str, float]
    created_at: datetime

class ContentSuggestion(BaseModel):
    date: str
    hot_topics: List[Dict[str, Any]]
    best_time: List[Dict[str, Any]]
    recommended_music: List[Dict[str, Any]]
    created_at: datetime

class WordCloud(BaseModel):
    date: str
    words: List[Dict[str, Any]]
    created_at: datetime

# MongoDB客户端
client = AsyncIOMotorClient(MONGODB_URL)
db = client[DATABASE_NAME]

@app.on_event("startup")
async def startup_db_client():
    try:
        # 测试数据库连接
        await db.command("ping")
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# API路由
@app.get("/")
async def root():
    return {"message": "抖音数据分析平台API示例"}

@app.get("/api/hot-words", response_model=List[HotWord])
async def get_hot_words(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=100),
    hours: int = Query(default=24, ge=1, le=168),  # 1小时到7天
    sort_by: str = Query(default="position", regex="^(position|hot_value|created_at)$"),
    order: int = Query(default=1, ge=-1, le=1)
):
    try:
        # 计算时间范围
        time_threshold = datetime.now() - timedelta(hours=hours)
        
        # 构建查询条件
        query = {"created_at": {"$gte": time_threshold}}
        
        # 获取热搜词数据
        cursor = db.hot_words.find(query)
        
        # 添加排序
        if sort_by == "position":
            cursor = cursor.sort("position", order)
        elif sort_by == "hot_value":
            cursor = cursor.sort("hot_value", -1 if order == -1 else 1)
        else:  # created_at
            cursor = cursor.sort("created_at", -1 if order == -1 else 1)
        
        # 应用分页
        cursor = cursor.skip(skip).limit(limit)
        
        # 获取数据
        hot_words = await cursor.to_list(length=limit)
        
        # 格式化结果
        formatted_hot_words = []
        for word in hot_words:
            word["_id"] = str(word["_id"])  # 转换ObjectId为字符串
            formatted_hot_words.append(word)
            
        return formatted_hot_words
    except Exception as e:
        print(f"获取热搜数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hot-words/stats", response_model=HotWordStats)
async def get_hot_words_stats():
    try:
        # 获取最近24小时的数据统计
        yesterday = datetime.now() - timedelta(days=1)
        
        # 获取基础统计信息
        pipeline = [
            {"$match": {"created_at": {"$gte": yesterday}}},
            {"$group": {
                "_id": None,
                "total_words": {"$sum": 1},
                "avg_hot_value": {"$avg": "$hot_value"},
                "max_hot_value": {"$max": "$hot_value"},
                "min_hot_value": {"$min": "$hot_value"}
            }}
        ]
        stats = await db.hot_words.aggregate(pipeline).to_list(length=1)
        
        # 获取热度最高的词汇（去重，只保留最新的记录）
        pipeline_top_words = [
            {"$match": {"created_at": {"$gte": yesterday}}},
            {"$sort": {"hot_value": -1, "created_at": -1}},
            {"$group": {
                "_id": "$title",
                "doc": {"$first": "$$ROOT"}
            }},
            {"$replaceRoot": {"newRoot": "$doc"}},
            {"$limit": 10}
        ]
        top_words = await db.hot_words.aggregate(pipeline_top_words).to_list(length=10)
        
        # 格式化结果
        for word in top_words:
            word["_id"] = str(word["_id"])  # 转换ObjectId为字符串
            
        result = {
            "total_words": stats[0].get("total_words", 0) if stats else 0,
            "avg_hot_value": float(stats[0].get("avg_hot_value", 0)) if stats else 0,
            "max_hot_value": int(stats[0].get("max_hot_value", 0)) if stats else 0,
            "min_hot_value": int(stats[0].get("min_hot_value", 0)) if stats else 0,
            "top_words": top_words
        }
        
        return result
    except Exception as e:
        print(f"获取统计数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hot-categories", response_model=List[HotCategory])
async def get_hot_categories(
    category: Optional[str] = None,
    days: int = Query(default=7, ge=1, le=30)
):
    try:
        # 计算时间范围
        time_threshold = datetime.now() - timedelta(days=days)
        
        # 构建查询条件
        query = {"created_at": {"$gte": time_threshold}}
        if category:
            query["category"] = category
            
        # 获取数据
        cursor = db.hot_categories.find(query).sort("created_at", -1)
        categories = await cursor.to_list(length=100)
        
        # 格式化结果
        formatted_categories = []
        for cat in categories:
            cat["_id"] = str(cat["_id"])  # 转换ObjectId为字符串
            formatted_categories.append(cat)
            
        return formatted_categories
    except Exception as e:
        print(f"获取热搜分类数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/daren-rank", response_model=List[DarenRank])
async def get_daren_rank(
    date: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="fans", regex="^(fans|sales|change)$"),
    order: int = Query(default=-1, ge=-1, le=1)
):
    try:
        # 构建查询条件
        query = {}
        if date:
            query["date"] = date
            
        # 获取数据
        cursor = db.daren_rank.find(query)
        
        # 添加排序
        cursor = cursor.sort(sort_by, order).limit(limit)
        
        # 获取数据
        daren_list = await cursor.to_list(length=limit)
        
        # 格式化结果
        formatted_daren = []
        for daren in daren_list:
            daren["_id"] = str(daren["_id"])  # 转换ObjectId为字符串
            formatted_daren.append(daren)
            
        return formatted_daren
    except Exception as e:
        print(f"获取达人榜数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/hot-videos", response_model=List[HotVideo])
async def get_hot_videos(
    user_id: Optional[str] = None,
    limit: int = Query(default=20, ge=1, le=100)
):
    try:
        # 构建查询条件
        query = {}
        if user_id:
            query["user_id"] = user_id
            
        # 获取数据
        cursor = db.hot_videos.find(query).sort("created_at", -1).limit(limit)
        videos = await cursor.to_list(length=limit)
        
        # 格式化结果
        formatted_videos = []
        for video in videos:
            video["_id"] = str(video["_id"])  # 转换ObjectId为字符串
            formatted_videos.append(video)
            
        return formatted_videos
    except Exception as e:
        print(f"获取热门视频数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}", response_model=UserData)
async def get_user_data(user_id: str):
    try:
        # 获取用户数据
        user = await db.user_data.find_one({"user_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail=f"用户 {user_id} 不存在")
            
        # 格式化结果
        user["_id"] = str(user["_id"])  # 转换ObjectId为字符串
        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/stats", response_model=List[UserStats])
async def get_user_stats(
    user_id: str,
    days: int = Query(default=30, ge=1, le=90)
):
    try:
        # 计算时间范围
        time_threshold = datetime.now() - timedelta(days=days)
        
        # 获取用户统计数据
        cursor = db.user_stats.find({
            "user_id": user_id,
            "created_at": {"$gte": time_threshold}
        }).sort("date", 1)
        
        stats = await cursor.to_list(length=100)
        if not stats:
            raise HTTPException(status_code=404, detail=f"用户 {user_id} 的统计数据不存在")
            
        # 格式化结果
        formatted_stats = []
        for stat in stats:
            stat["_id"] = str(stat["_id"])  # 转换ObjectId为字符串
            formatted_stats.append(stat)
            
        return formatted_stats
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取用户统计数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/user/{user_id}/fan-profile", response_model=FanProfile)
async def get_fan_profile(user_id: str):
    try:
        # 获取最新的粉丝画像数据
        profile = await db.fan_profiles.find_one(
            {"user_id": user_id},
            sort=[("created_at", -1)]
        )
        
        if not profile:
            raise HTTPException(status_code=404, detail=f"用户 {user_id} 的粉丝画像数据不存在")
            
        # 格式化结果
        profile["_id"] = str(profile["_id"])  # 转换ObjectId为字符串
        return profile
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取粉丝画像数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/content-suggestions", response_model=ContentSuggestion)
async def get_content_suggestions(date: Optional[str] = None):
    try:
        # 构建查询条件
        query = {}
        if date:
            query["date"] = date
            
        # 获取最新的创作建议数据
        suggestion = await db.content_suggestions.find_one(
            query,
            sort=[("created_at", -1)]
        )
        
        if not suggestion:
            raise HTTPException(status_code=404, detail="创作建议数据不存在")
            
        # 格式化结果
        suggestion["_id"] = str(suggestion["_id"])  # 转换ObjectId为字符串
        return suggestion
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取创作建议数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/word-cloud", response_model=WordCloud)
async def get_word_cloud(date: Optional[str] = None):
    try:
        # 构建查询条件
        query = {}
        if date:
            query["date"] = date
            
        # 获取最新的热词云数据
        word_cloud = await db.word_cloud.find_one(
            query,
            sort=[("created_at", -1)]
        )
        
        if not word_cloud:
            raise HTTPException(status_code=404, detail="热词云数据不存在")
            
        # 格式化结果
        word_cloud["_id"] = str(word_cloud["_id"])  # 转换ObjectId为字符串
        return word_cloud
    except HTTPException:
        raise
    except Exception as e:
        print(f"获取热词云数据出错: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)