"""
抖音数据库操作模块
提供与MongoDB数据库交互的功能，用于存储和检索抖音数据
"""

import logging
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Any

# 检查必要的依赖库
try:
    import pymongo
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure, ServerSelectionTimeoutError
except ImportError:
    print("错误: 缺少必要的依赖库 'pymongo'")
    print("请使用以下命令安装: pip install pymongo")
    sys.exit(1)

# 导入配置
try:
    from backend.config import (
        MONGODB_URL, 
        DATABASE_NAME, 
        COLLECTIONS, 
        CONNECT_TIMEOUT, 
        SOCKET_TIMEOUT,
        MAX_RETRIES,
        RETRY_DELAY
    )
except ImportError:
    # 默认配置
    MONGODB_URL = "mongodb://localhost:27017/douyin_analysis"
    DATABASE_NAME = "douyin_analysis"
    COLLECTIONS = {
        "users": "user_data",           # 用户基础数据
        "videos": "hot_videos",         # 热门视频数据
        "comments": "comments",         # 评论数据
        "hot_searches": "hot_words",    # 热搜榜数据
        "user_stats": "user_stats",     # 用户统计数据
        "fan_profiles": "fan_profiles", # 粉丝画像数据
        "daren_rank": "daren_rank",     # 达人排行榜数据
        "hot_categories": "hot_categories", # 热搜分类数据
        "content_suggestions": "content_suggestions", # 创作建议数据
        "word_cloud": "word_cloud"      # 热词云数据
    }
    CONNECT_TIMEOUT = 5
    SOCKET_TIMEOUT = 5
    MAX_RETRIES = 3
    RETRY_DELAY = 1
    print("警告: 未找到配置文件，使用默认配置")

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('douyin_db.log')
    ]
)
logger = logging.getLogger('DouyinDB')

class DouyinDB:
    """抖音数据库操作类"""
    
    def __init__(self):
        """初始化数据库连接"""
        self.client = None
        self.db = None
        self._connect()
        self._setup_collections()
        
    def _connect(self, retry_count: int = 0) -> bool:
        """
        连接到MongoDB数据库
        
        Args:
            retry_count: 当前重试次数
            
        Returns:
            bool: 连接是否成功
        """
        try:
            # 创建MongoDB客户端
            self.client = MongoClient(
                MONGODB_URL,
                connectTimeoutMS=CONNECT_TIMEOUT * 1000,
                socketTimeoutMS=SOCKET_TIMEOUT * 1000,
                serverSelectionTimeoutMS=CONNECT_TIMEOUT * 1000
            )
            
            # 测试连接
            self.client.admin.command('ping')
            
            # 获取数据库
            self.db = self.client[DATABASE_NAME]
            
            logger.info(f"成功连接到MongoDB数据库: {DATABASE_NAME}")
            return True
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"连接MongoDB失败: {e}")
            
            # 如果还有重试机会，等待后重试
            if retry_count < MAX_RETRIES:
                logger.info(f"将在{RETRY_DELAY}秒后重试连接（第{retry_count + 1}次）...")
                time.sleep(RETRY_DELAY)
                return self._connect(retry_count + 1)
            
            logger.error("达到最大重试次数，连接失败")
            return False
            
        except Exception as e:
            logger.error(f"连接MongoDB时发生未知错误: {e}", exc_info=True)
            return False
    
    def _setup_collections(self):
        """设置集合和索引"""
        if self.db is None:
            logger.error("数据库未连接，无法设置集合")
            return
            
        try:
            # 1. 用户基础数据集合
            self.users = self.db[COLLECTIONS.get("users", "user_data")]
            self.users.create_index([("user_id", pymongo.ASCENDING)], unique=True)
            self.users.create_index([("nickname", pymongo.ASCENDING)])
            self.users.create_index([("fans_count", pymongo.DESCENDING)])
            self.users.create_index([("created_at", pymongo.DESCENDING)])
            
            # 2. 热门视频集合
            self.videos = self.db[COLLECTIONS.get("videos", "hot_videos")]
            self.videos.create_index([("video_id", pymongo.ASCENDING), ("date", pymongo.ASCENDING)], unique=True)
            self.videos.create_index([("user_id", pymongo.ASCENDING)])
            self.videos.create_index([("likes", pymongo.DESCENDING)])
            self.videos.create_index([("date", pymongo.DESCENDING)])
            
            # 3. 热搜词集合
            self.hot_searches = self.db[COLLECTIONS.get("hot_searches", "hot_words")]
            self.hot_searches.create_index([("position", pymongo.ASCENDING), ("created_at", pymongo.ASCENDING)], unique=True)
            self.hot_searches.create_index([("title", pymongo.ASCENDING)])
            self.hot_searches.create_index([("hot_value", pymongo.DESCENDING)])
            self.hot_searches.create_index([("created_at", pymongo.DESCENDING)])
            
            # 4. 用户统计数据集合
            self.user_stats = self.db[COLLECTIONS.get("user_stats", "user_stats")]
            self.user_stats.create_index([("user_id", pymongo.ASCENDING), ("date", pymongo.ASCENDING)], unique=True)
            self.user_stats.create_index([("date", pymongo.DESCENDING)])
            self.user_stats.create_index([("fans_increase", pymongo.DESCENDING)])
            
            # 5. 达人排行榜集合
            self.daren_rank = self.db[COLLECTIONS.get("daren_rank", "daren_rank")]
            self.daren_rank.create_index([("user_id", pymongo.ASCENDING), ("date", pymongo.ASCENDING)], unique=True)
            self.daren_rank.create_index([("nickname", pymongo.ASCENDING)])
            self.daren_rank.create_index([("fans", pymongo.DESCENDING)])
            self.daren_rank.create_index([("sales", pymongo.DESCENDING)])
            self.daren_rank.create_index([("date", pymongo.DESCENDING)])
            
            # 6. 热搜分类集合
            self.hot_categories = self.db[COLLECTIONS.get("hot_categories", "hot_categories")]
            self.hot_categories.create_index([("category", pymongo.ASCENDING), ("created_at", pymongo.ASCENDING)], unique=True)
            self.hot_categories.create_index([("created_at", pymongo.DESCENDING)])
            
            # 7. 粉丝画像集合
            self.fan_profiles = self.db[COLLECTIONS.get("fan_profiles", "fan_profiles")]
            self.fan_profiles.create_index([("user_id", pymongo.ASCENDING), ("date", pymongo.ASCENDING)], unique=True)
            self.fan_profiles.create_index([("date", pymongo.DESCENDING)])
            
            # 8. 创作建议集合
            self.content_suggestions = self.db[COLLECTIONS.get("content_suggestions", "content_suggestions")]
            self.content_suggestions.create_index([("date", pymongo.ASCENDING)], unique=True)
            self.content_suggestions.create_index([("created_at", pymongo.DESCENDING)])
            
            # 9. 热词云集合
            self.word_cloud = self.db[COLLECTIONS.get("word_cloud", "word_cloud")]
            self.word_cloud.create_index([("date", pymongo.ASCENDING)], unique=True)
            self.word_cloud.create_index([("created_at", pymongo.DESCENDING)])
            self.word_cloud.create_index([("value", pymongo.DESCENDING)])
            
            logger.info("成功设置集合和索引")
            
        except Exception as e:
            logger.error(f"设置集合和索引时出错: {e}", exc_info=True)
    
    def add_user(self, user_id: str, nickname: str, signature: str = "", 
                avatar_url: str = "", fans_count: int = 0, 
                following_count: int = 0, likes_count: int = 0, 
                video_count: int = 0, verified: bool = False,
                category: str = "", location: str = "",
                age: int = None, gender: str = "",
                tags: List[str] = None) -> bool:
        """
        添加或更新用户基础数据
        
        Args:
            user_id: 用户ID
            nickname: 用户昵称
            signature: 用户签名
            avatar_url: 头像URL
            fans_count: 粉丝数
            following_count: 关注数
            likes_count: 获赞数
            video_count: 视频数
            verified: 是否认证
            category: 用户分类
            location: 用户地区
            age: 用户年龄
            gender: 用户性别
            tags: 用户标签列表
            
        Returns:
            bool: 操作是否成功
        """
        if self.db is None:
            logger.error("数据库未连接，无法添加用户")
            return False
            
        try:
            # 准备用户数据
            user_data = {
                "user_id": user_id,
                "nickname": nickname,
                "signature": signature,
                "avatar_url": avatar_url,
                "fans_count": fans_count,
                "following_count": following_count,
                "likes_count": likes_count,
                "video_count": video_count,
                "verified": verified,
                "category": category,
                "location": location,
                "tags": tags or [],
                "updated_at": datetime.now()
            }
            
            # 添加可选字段
            if age is not None:
                user_data["age"] = age
            if gender:
                user_data["gender"] = gender
            
            # 使用upsert=True，如果用户存在则更新，不存在则插入
            result = self.users.update_one(
                {"user_id": user_id},
                {
                    "$set": user_data,
                    "$setOnInsert": {"created_at": datetime.now()}
                },
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"成功添加新用户: {nickname} ({user_id})")
                
                # 初始化用户统计数据
                self.add_user_stats(
                    user_id=user_id,
                    fans_count=fans_count,
                    following_count=following_count,
                    likes_count=likes_count,
                    video_count=video_count
                )
            else:
                logger.info(f"成功更新用户: {nickname} ({user_id})")
                
            return True
            
        except Exception as e:
            logger.error(f"添加/更新用户时出错: {e}", exc_info=True)
            return False
    
    def add_hot_video(self, video_id: str, title: str, author: str, 
                     user_id: str, url: str, create_time: Union[str, datetime], 
                     likes: int = 0, comments: int = 0, 
                     shares: int = 0, collects: int = 0,
                     play_count: int = 0, forward_count: int = 0,
                     description: str = "", music_id: str = "",
                     music_title: str = "", tags: List[str] = None,
                     date: Union[str, datetime] = None) -> bool:
        """
        添加或更新热门视频
        
        Args:
            video_id: 视频ID
            title: 视频标题
            author: 作者昵称
            user_id: 作者ID
            url: 视频URL
            create_time: 创建时间
            likes: 点赞数
            comments: 评论数
            shares: 分享数
            collects: 收藏数
            play_count: 播放次数
            forward_count: 转发数
            description: 视频描述
            music_id: 音乐ID
            music_title: 音乐标题
            tags: 视频标签列表
            date: 数据统计日期，如果不提供则使用当前日期
            
        Returns:
            bool: 操作是否成功
        """
        if self.db is None:
            logger.error("数据库未连接，无法添加视频")
            return False
            
        try:
            # 处理日期
            if isinstance(create_time, str):
                create_time = datetime.fromisoformat(create_time.replace('Z', '+00:00'))
            
            current_date = None
            if date:
                if isinstance(date, str):
                    current_date = date
                else:
                    current_date = date.strftime("%Y-%m-%d")
            else:
                current_date = datetime.now().strftime("%Y-%m-%d")
            
            # 准备视频数据
            video_data = {
                "video_id": video_id,
                "title": title,
                "author": author,
                "user_id": user_id,
                "url": url,
                "create_time": create_time,
                "likes": likes,
                "comments": comments,
                "shares": shares,
                "collects": collects,
                "play_count": play_count,
                "forward_count": forward_count,
                "description": description,
                "music_id": music_id,
                "music_title": music_title,
                "tags": tags or [],
                "date": current_date,
                "updated_at": datetime.now()
            }
            
            # 使用video_id和date作为唯一标识，如果存在则更新，不存在则插入
            result = self.videos.update_one(
                {
                    "video_id": video_id,
                    "date": current_date
                },
                {"$set": video_data},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"成功添加新视频: {title} ({video_id}) - 日期: {current_date}")
            else:
                logger.info(f"成功更新视频: {title} ({video_id}) - 日期: {current_date}")
                
            return True
            
        except Exception as e:
            logger.error(f"添加/更新视频时出错: {e}", exc_info=True)
            return False
    
    def add_user_stats(self, user_id: str, fans_count: int = 0, 
                      following_count: int = 0, likes_count: int = 0, 
                      video_count: int = 0, date: Union[str, datetime] = None) -> bool:
        """
        添加或更新用户统计数据
        
        Args:
            user_id: 用户ID
            fans_count: 粉丝数
            following_count: 关注数
            likes_count: 获赞数
            video_count: 视频数
            date: 统计日期，如果不提供则使用当前日期
            
        Returns:
            bool: 操作是否成功
        """
        if self.db is None:
            logger.error("数据库未连接，无法添加用户统计数据")
            return False
            
        try:
            # 处理日期
            current_date = None
            if date:
                if isinstance(date, str):
                    current_date = date
                else:
                    current_date = date.strftime("%Y-%m-%d")
            else:
                current_date = datetime.now().strftime("%Y-%m-%d")
            
            # 获取前一天的统计数据
            yesterday = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
            previous_stats = self.user_stats.find_one({
                "user_id": user_id,
                "date": yesterday
            })
            
            # 计算增长数据
            fans_increase = 0
            following_increase = 0
            likes_increase = 0
            video_increase = 0
            
            if previous_stats:
                fans_increase = fans_count - previous_stats.get("fans_count", 0)
                following_increase = following_count - previous_stats.get("following_count", 0)
                likes_increase = likes_count - previous_stats.get("likes_count", 0)
                video_increase = video_count - previous_stats.get("video_count", 0)
            
            # 准备统计数据
            stats_data = {
                "user_id": user_id,
                "date": current_date,
                "fans_count": fans_count,
                "following_count": following_count,
                "likes_count": likes_count,
                "video_count": video_count,
                "fans_increase": fans_increase,
                "following_increase": following_increase,
                "likes_increase": likes_increase,
                "video_increase": video_increase,
                "updated_at": datetime.now()
            }
            
            # 使用user_id和date作为唯一标识，如果存在则更新，不存在则插入
            result = self.user_stats.update_one(
                {
                    "user_id": user_id,
                    "date": current_date
                },
                {"$set": stats_data},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"成功添加用户统计数据: {user_id} - 日期: {current_date}")
            else:
                logger.info(f"成功更新用户统计数据: {user_id} - 日期: {current_date}")
                
            return True
            
        except Exception as e:
            logger.error(f"添加/更新用户统计数据时出错: {e}", exc_info=True)
            return False
            
    def update_user_stats(self, user_id: str, total_likes: int = 0, 
                         total_comments: int = 0, total_shares: int = 0) -> bool:
        """
        更新用户统计信息
        
        Args:
            user_id: 用户ID
            total_likes: 总点赞数
            total_comments: 总评论数
            total_shares: 总分享数
            
        Returns:
            bool: 操作是否成功
        """
        if self.db is None:
            logger.error("数据库未连接，无法更新用户统计")
            return False
            
        try:
            # 检查用户是否存在
            user = self.users.find_one({"user_id": user_id})
            if not user:
                logger.warning(f"用户不存在，无法更新统计: {user_id}")
                return False
                
            # 更新用户统计信息
            result = self.users.update_one(
                {"user_id": user_id},
                {
                    "$inc": {
                        "total_likes": total_likes,
                        "total_comments": total_comments,
                        "total_shares": total_shares
                    },
                    "$set": {"stats_updated_at": datetime.now()}
                }
            )
            
            if result.modified_count > 0:
                logger.info(f"成功更新用户统计: {user_id}")
                return True
            else:
                logger.warning(f"用户统计未更新: {user_id}")
                return False
                
        except Exception as e:
            logger.error(f"更新用户统计时出错: {e}", exc_info=True)
            return False
    
    def add_hot_search(self, title: str, hot_value: int, position: int, 
                      sentence_id: str = None, tag: str = "", 
                      video_count: int = 0, view_count: int = 0, 
                      discussion_count: int = 0, link: str = "", 
                      created_at: datetime = None) -> bool:
        """
        添加热搜词数据
        
        Args:
            title: 热搜词标题
            hot_value: 热度值
            position: 排名位置
            sentence_id: 热搜ID（可选）
            tag: 标签
            video_count: 视频数
            view_count: 浏览数
            discussion_count: 讨论数
            link: 链接
            created_at: 创建时间
            
        Returns:
            bool: 操作是否成功
        """
        if self.db is None:
            logger.error("数据库未连接，无法添加热搜词")
            return False
            
        try:
            # 准备热搜词数据
            current_time = created_at or datetime.now()
            hot_search_data = {
                "title": title,
                "word": title,
                "hot_value": hot_value,
                "position": position,
                "tag": tag,
                "video_count": video_count,
                "view_count": view_count,
                "discussion_count": discussion_count,
                "link": link,
                "created_at": current_time,
                "date": current_time
            }
            
            # 如果提供了sentence_id，添加到数据中
            if sentence_id:
                hot_search_data["sentence_id"] = sentence_id
                
            # 使用upsert=True，如果相同位置和创建时间的热搜词已存在则更新，不存在则插入
            result = self.hot_searches.update_one(
                {
                    "position": position,
                    "created_at": current_time
                },
                {"$set": hot_search_data},
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"成功添加热搜词: {title} (位置: {position})")
                return True
            elif result.modified_count > 0:
                logger.info(f"成功更新热搜词: {title} (位置: {position})")
                return True
            else:
                logger.warning(f"热搜词添加/更新失败: {title}")
                return False
                
        except Exception as e:
            logger.error(f"添加热搜词时出错: {e}", exc_info=True)
            return False
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        """
        获取用户信息
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[Dict]: 用户信息或None
        """
        if self.db is None:
            logger.error("数据库未连接，无法获取用户")
            return None
            
        try:
            user = self.users.find_one({"user_id": user_id})
            return user
            
        except Exception as e:
            logger.error(f"获取用户时出错: {e}", exc_info=True)
            return None
    
    def get_video(self, video_id: str) -> Optional[Dict]:
        """
        获取视频信息
        
        Args:
            video_id: 视频ID
            
        Returns:
            Optional[Dict]: 视频信息或None
        """
        if self.db is None:
            logger.error("数据库未连接，无法获取视频")
            return None
            
        try:
            video = self.videos.find_one({"video_id": video_id})
            return video
            
        except Exception as e:
            logger.error(f"获取视频时出错: {e}", exc_info=True)
            return None
    
    def get_user_videos(self, user_id: str, limit: int = 10) -> List[Dict]:
        """
        获取用户的视频列表
        
        Args:
            user_id: 用户ID
            limit: 返回的最大视频数量
            
        Returns:
            List[Dict]: 视频列表
        """
        if self.db is None:
            logger.error("数据库未连接，无法获取用户视频")
            return []
            
        try:
            videos = list(self.videos.find(
                {"author_id": user_id}
            ).sort("create_time", pymongo.DESCENDING).limit(limit))
            
            return videos
            
        except Exception as e:
            logger.error(f"获取用户视频时出错: {e}", exc_info=True)
            return []
    
    def get_hot_searches(self, date: str = None, start_time: datetime = None, 
                        end_time: datetime = None, limit: int = 50) -> List[Dict]:
        """
        获取热搜词列表
        
        Args:
            date: 指定日期，格式为'YYYY-MM-DD'，如果不指定则获取最新数据
            start_time: 开始时间，如果指定则获取该时间之后的数据
            end_time: 结束时间，如果指定则获取该时间之前的数据
            limit: 返回的最大热搜词数量
            
        Returns:
            List[Dict]: 热搜词列表
        """
        if self.db is None:
            logger.error("数据库未连接，无法获取热搜词")
            return []
            
        try:
            # 构建查询条件
            query = {}
            
            if date:
                query["date"] = date
            elif start_time or end_time:
                time_query = {}
                if start_time:
                    time_query["$gte"] = start_time
                if end_time:
                    time_query["$lte"] = end_time
                if time_query:
                    query["created_at"] = time_query
            else:
                # 如果没有指定时间范围，获取最新的记录
                latest = self.hot_searches.find_one(
                    sort=[("created_at", pymongo.DESCENDING)]
                )
                if not latest:
                    return []
                query["created_at"] = latest["created_at"]
            
            # 获取热搜词列表
            hot_searches = list(self.hot_searches.find(query)
                              .sort([("created_at", pymongo.DESCENDING),
                                   ("position", pymongo.ASCENDING)])
                              .limit(limit))
            
            # 添加排名变化信息（如果有历史数据）
            if hot_searches and not date and not start_time and not end_time:
                latest_time = hot_searches[0]["created_at"]
                # 获取上一个时间点的数据
                previous_time = self.hot_searches.find_one(
                    {"created_at": {"$lt": latest_time}},
                    sort=[("created_at", pymongo.DESCENDING)]
                )
                
                if previous_time:
                    previous_time = previous_time["created_at"]
                    previous_searches = {
                        item["title"]: item["position"]
                        for item in self.hot_searches.find({"created_at": previous_time})
                    }
                    
                    # 计算排名变化
                    for item in hot_searches:
                        title = item["title"]
                        current_position = item["position"]
                        previous_position = previous_searches.get(title)
                        
                        if previous_position is not None:
                            item["rank_change"] = previous_position - current_position
                        else:
                            item["rank_change"] = "new"
            
            return hot_searches
            
        except Exception as e:
            logger.error(f"获取热搜词列表时出错: {e}", exc_info=True)
            return []
    
    def close(self):
        """关闭数据库连接"""
        if self.client:
            try:
                self.client.close()
                logger.info("数据库连接已关闭")
            except Exception as e:
                logger.error(f"关闭数据库连接时出错: {e}", exc_info=True)


# 测试代码
if __name__ == "__main__":
    try:
        # 创建数据库实例
        db = DouyinDB()
        
        # 测试连接
        print("数据库连接测试...")
        
        # 添加测试用户
        test_user_id = "test_user_123"
        result = db.add_user(
            user_id=test_user_id,
            nickname="测试用户",
            signature="这是一个测试用户",
            follower_count=1000,
            following_count=500,
            likes_count=5000,
            video_count=20
        )
        print(f"添加测试用户: {'成功' if result else '失败'}")
        
        # 获取测试用户
        user = db.get_user(test_user_id)
        if user:
            print(f"获取测试用户成功: {user['nickname']}")
        else:
            print("获取测试用户失败")
        
        # 关闭连接
        db.close()
        
    except Exception as e:
        print(f"测试过程中出错: {e}")