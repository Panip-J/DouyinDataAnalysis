import pymongo
import sys
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_mongodb_connection():
    """测试MongoDB连接的简单脚本"""
    # 获取连接字符串
    mongodb_url = os.getenv("MONGODB_URL")
    if not mongodb_url:
        print("警告: 未找到 MONGODB_URL 环境变量，使用默认值")
        mongodb_url = "mongodb://localhost:27017/douyin_analysis"
    
    print(f"使用的连接URL: {mongodb_url}")
    
    try:
        # 设置连接超时
        client = pymongo.MongoClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # 测试连接
        print("尝试连接到MongoDB...")
        client.admin.command('ping')
        
        print("\n✓ MongoDB连接成功!")
        server_info = client.server_info()
        print(f"服务器版本: {server_info['version']}")
        
        # 获取数据库列表
        dbs = client.list_database_names()
        print(f"可用数据库: {', '.join(dbs)}")
        
        return True
    except pymongo.errors.ServerSelectionTimeoutError as e:
        print(f"\n✗ 连接超时: {e}")
        print("\n可能的原因:")
        print("1. MongoDB服务未运行")
        print("2. 连接字符串中的主机名或端口不正确")
        print("3. 防火墙阻止了连接")
    except pymongo.errors.OperationFailure as e:
        print(f"\n✗ 认证失败: {e}")
        print("\n可能的原因:")
        print("1. 用户名或密码不正确")
        print("2. 用户没有访问权限")
    except Exception as e:
        print(f"\n✗ 连接失败: {e}")
        print(f"错误类型: {type(e).__name__}")
    
    return False

if __name__ == "__main__":
    print("===== MongoDB 简单连接测试 =====\n")
    success = test_mongodb_connection()
    
    if not success:
        print("\n请检查以下可能的问题:")
        print("1. MongoDB 服务是否正在运行")
        print("2. 连接字符串是否正确")
        print("3. 用户名和密码是否正确")
        print("4. 防火墙设置是否允许连接")
        print("5. 尝试使用不同的连接方式，例如:")
        print("   - mongodb://用户名:密码@localhost:27017/admin")
        print("   - mongodb://用户名:密码@127.0.0.1:27017")
        sys.exit(1)
    
    print("\n测试完成!")