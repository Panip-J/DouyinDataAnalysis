import pymongo
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 连接信息
MONGODB_URL = os.getenv("MONGODB_URL")
if not MONGODB_URL:
    print("警告: 未找到 MONGODB_URL 环境变量，使用默认值")
    MONGODB_URL = "mongodb://localhost:27017/douyin_analysis"

print(f"使用的连接URL: {MONGODB_URL}")
DB_NAME = os.getenv("DATABASE_NAME", "douyin_analysis")

def test_connection():
    """测试MongoDB连接"""
    try:
        # 创建客户端连接
        client = pymongo.MongoClient(MONGODB_URL)
        
        # 测试连接
        client.admin.command('ping')
        
        print("✓ MongoDB连接成功!")
        print(f"服务器信息: {client.server_info()['version']}")
        
        # 获取数据库列表
        dbs = client.list_database_names()
        print(f"现有数据库: {', '.join(dbs)}")
        
        return client
    except Exception as e:
        print(f"✗ MongoDB连接失败: {e}")
        return None

def create_sample_data(client):
    """创建示例数据"""
    if not client:
        return False
    
    try:
        # 获取数据库
        db = client[DB_NAME]
        
        # 创建集合并插入示例数据
        
        # 1. 热搜词集合
        hot_words = db.hot_words
        hot_word_data = {
            "word": "测试热词",
            "search_count": 10000,
            "category": "娱乐",
            "date": datetime.now(),
            "trend": "up",
            "related_words": ["测试", "示例", "热搜"]
        }
        hot_words.insert_one(hot_word_data)
        print(f"✓ 已插入热搜词示例数据")
        
        # 2. 达人榜集合
        daren_rank = db.daren_rank
        daren_data = {
            "user_id": "test_user_123",
            "nickname": "测试达人",
            "rank": 1,
            "category": "美食",
            "follower_count": 1000000,
            "video_count": 500,
            "total_likes": 5000000,
            "date": datetime.now()
        }
        daren_rank.insert_one(daren_data)
        print(f"✓ 已插入达人榜示例数据")
        
        # 3. 热门视频集合
        hot_videos = db.hot_videos
        video_data = {
            "video_id": "test_video_456",
            "title": "测试视频标题",
            "author_id": "test_user_123",
            "play_count": 500000,
            "like_count": 50000,
            "comment_count": 2000,
            "share_count": 1000,
            "date": datetime.now(),
            "tags": ["测试", "示例视频"],
            "duration": 60
        }
        hot_videos.insert_one(video_data)
        print(f"✓ 已插入热门视频示例数据")
        
        # 4. 用户统计集合
        user_stats = db.user_stats
        stats_data = {
            "user_id": "test_user_123",
            "date": datetime.now(),
            "follower_growth": 1000,
            "video_count": 5,
            "total_likes": 50000,
            "total_comments": 2000,
            "total_shares": 1000,
            "engagement_rate": 0.05
        }
        user_stats.insert_one(stats_data)
        print(f"✓ 已插入用户统计示例数据")
        
        # 5. 粉丝画像集合
        fan_profile = db.fan_profile
        profile_data = {
            "user_id": "test_user_123",
            "date": datetime.now(),
            "age_distribution": {
                "18-24": 0.3,
                "25-34": 0.4,
                "35-44": 0.2,
                "45+": 0.1
            },
            "gender_ratio": {
                "male": 0.45,
                "female": 0.55
            },
            "active_time": {
                "morning": 0.2,
                "afternoon": 0.3,
                "evening": 0.5
            },
            "interests": ["美食", "旅游", "时尚"]
        }
        fan_profile.insert_one(profile_data)
        print(f"✓ 已插入粉丝画像示例数据")
        
        # 查询并显示所有集合
        collections = db.list_collection_names()
        print(f"\n数据库 {DB_NAME} 中的集合: {', '.join(collections)}")
        
        # 显示每个集合的文档数量
        for collection in collections:
            count = db[collection].count_documents({})
            print(f"集合 {collection} 中有 {count} 个文档")
        
        return True
    except Exception as e:
        print(f"✗ 创建示例数据失败: {e}")
        return False

def query_sample_data(client):
    """查询示例数据"""
    if not client:
        return
    
    try:
        # 获取数据库
        db = client[DB_NAME]
        
        print("\n===== 示例查询结果 =====")
        
        # 1. 查询热搜词
        hot_word = db.hot_words.find_one({})
        print("\n热搜词示例:")
        print(json.dumps(
            {k: str(v) if isinstance(v, datetime) else v for k, v in hot_word.items() if k != '_id'}, 
            ensure_ascii=False, indent=2
        ))
        
        # 2. 查询达人信息
        daren = db.daren_rank.find_one({})
        print("\n达人榜示例:")
        print(json.dumps(
            {k: str(v) if isinstance(v, datetime) else v for k, v in daren.items() if k != '_id'}, 
            ensure_ascii=False, indent=2
        ))
        
        # 3. 查询用户统计信息
        user = db.user_stats.find_one({})
        print("\n用户统计示例:")
        print(json.dumps(
            {k: str(v) if isinstance(v, datetime) else v for k, v in user.items() if k != '_id'}, 
            ensure_ascii=False, indent=2
        ))
        
    except Exception as e:
        print(f"✗ 查询示例数据失败: {e}")

def main():
    """主函数"""
    print("===== MongoDB 连接测试 =====\n")
    
    # 测试连接
    client = test_connection()
    if not client:
        print("\n请检查以下可能的问题:")
        print("1. MongoDB 服务是否正在运行")
        print("2. 连接字符串是否正确 (当前: {})".format(MONGODB_URL))
        print("3. 用户名和密码是否正确")
        print("4. 防火墙设置是否允许连接")
        return
    
    # 询问是否创建示例数据
    try:
        choice = input("\n是否创建示例数据? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            if create_sample_data(client):
                # 查询示例数据
                query_sample_data(client)
    except Exception:
        pass
    
    print("\n测试完成!")

if __name__ == "__main__":
    main()