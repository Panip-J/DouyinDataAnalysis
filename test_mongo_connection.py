import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient


def test_mongo_connection() -> bool:
    """Test the configured MongoDB connection without embedding credentials."""
    load_dotenv()
    mongo_uri = os.getenv("MONGODB_URL", "mongodb://localhost:27017/douyin_analysis")
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        print("✅ 成功连接到 MongoDB")
        print(f"当前数据库: {client.get_database().name}")
        return True
    except Exception as exc:
        print(f"❌ 连接失败: {exc}")
        return False


if __name__ == "__main__":
    sys.exit(0 if test_mongo_connection() else 1)