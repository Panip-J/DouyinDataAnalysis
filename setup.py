import os
import time
import subprocess
import sys

def check_requirements():
    """检查必要的依赖是否已安装"""
    print("检查必要的依赖...")
    
    # 检查 Docker 是否已安装
    try:
        subprocess.run(["docker", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✓ Docker 已安装")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("✗ Docker 未安装或无法访问。请安装 Docker 后再继续。")
        return False
    
    # 检查 Docker Compose 是否已安装
    try:
        subprocess.run(["docker-compose", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✓ Docker Compose 已安装")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("✗ Docker Compose 未安装或无法访问。请安装 Docker Compose 后再继续。")
        return False
    
    # 检查 Python 依赖
    try:
        import pymongo
        print("✓ PyMongo 已安装")
    except ImportError:
        print("正在安装 PyMongo...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pymongo"], check=True)
            print("✓ PyMongo 安装成功")
        except subprocess.SubprocessError:
            print("✗ 安装 PyMongo 失败。请手动运行 'pip install pymongo'。")
            return False
    
    return True

def start_mongodb():
    """启动 MongoDB Docker 容器"""
    print("\n启动 MongoDB Docker 容器...")
    try:
        # 检查容器是否已经在运行
        result = subprocess.run(
            ["docker", "ps", "-q", "-f", "name=douyin_mongo"],
            check=True, stdout=subprocess.PIPE, text=True
        )
        
        if result.stdout.strip():
            print("MongoDB 容器已经在运行中")
        else:
            # 启动容器
            subprocess.run(["docker-compose", "up", "-d"], check=True)
            print("MongoDB 容器启动成功")
            
            # 等待 MongoDB 完全启动
            print("等待 MongoDB 初始化 (10秒)...")
            time.sleep(10)
    except subprocess.SubprocessError as e:
        print(f"✗ 启动 MongoDB 容器失败: {e}")
        return False
    
    return True

def run_test_script():
    """运行测试脚本"""
    print("\n运行测试脚本...")
    try:
        subprocess.run([sys.executable, "test_mongodb.py"], check=True)
        print("\n✓ 测试脚本执行成功")
    except subprocess.SubprocessError as e:
        print(f"✗ 测试脚本执行失败: {e}")
        return False
    
    return True

def main():
    """主函数"""
    print("===== 抖音数据分析平台 MongoDB 设置 =====\n")
    
    # 检查依赖
    if not check_requirements():
        print("\n✗ 依赖检查失败，请解决上述问题后重试。")
        return
    
    # 启动 MongoDB
    if not start_mongodb():
        print("\n✗ MongoDB 启动失败，请检查 Docker 是否正常运行。")
        return
    
    # 运行测试脚本
    if not run_test_script():
        print("\n✗ 测试脚本执行失败，请检查错误信息。")
        return
    
    print("\n===== 设置完成 =====")
    print("MongoDB 已成功设置并填充了示例数据。")
    print("你现在可以使用以下连接信息连接到数据库：")
    print("  - URL: configured by MONGODB_URL in .env")
    print("  - 数据库名称: douyin_analysis")
    print("\n如需更多信息，请查看 README.md 文件。")

if __name__ == "__main__":
    main()