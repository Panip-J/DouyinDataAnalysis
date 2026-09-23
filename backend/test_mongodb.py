import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime

# MongoDB连接配置
MONGODB_URL = "mongodb://localhost:27017/douyin_analysis"
DATABASE_NAME = "douyin_analysis"

async def test_connection():
    try:
        # 连接MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        # 测试连接
        await client.admin.command('ping')
        print("成功连接到MongoDB")
        return client
    except Exception as e:
        print(f"MongoDB连接失败: {e}")
        raise

async def get_hot_words():
    try:
        client = await test_connection()
        db = client[DATABASE_NAME]
        
        # 获取最新的热搜数据
        cursor = db.hot_words.find().sort("created_at", -1).limit(10)
        hot_words = await cursor.to_list(length=10)
        
        # 打印数据
        if hot_words:
            print(f"\n获取到 {len(hot_words)} 条热搜数据:")
            for word in hot_words:
                print(f"排名: {word.get('position')}, 标题: {word.get('title')}, 热度: {word.get('hot_value')}")
        else:
            print("未获取到热搜数据")
        
        # 关闭连接
        client.close()
        
    except Exception as e:
        print(f"获取热搜数据失败: {e}")
        raise

async def main():
    await get_hot_words()

if __name__ == "__main__":
    asyncio.run(main()) 