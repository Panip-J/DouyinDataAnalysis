import subprocess
import sys
import os

def install_package(package_name):
    """使用 Python 模块方式安装包，避免路径问题"""
    print(f"正在安装 {package_name}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        print(f"✓ {package_name} 安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {package_name} 安装失败: {e}")
        return False

def main():
    """安装所有必要的依赖"""
    print("===== 安装 MongoDB 数据库所需依赖 =====\n")
    
    # 基本依赖
    packages = ["pymongo", "python-dotenv"]
    
    # API 示例依赖
    api_packages = ["fastapi", "uvicorn", "motor"]
    
    # 安装基本依赖
    print("正在安装基本依赖...")
    all_success = True
    for package in packages:
        if not install_package(package):
            all_success = False
    
    # 询问是否安装 API 示例依赖
    print("\n是否要安装 API 示例所需的依赖？")
    print("这些依赖用于运行 api_example.py (FastAPI, Uvicorn, Motor)")
    
    try:
        choice = input("安装 API 示例依赖? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            print("\n正在安装 API 示例依赖...")
            for package in api_packages:
                if not install_package(package):
                    all_success = False
    except Exception:
        print("跳过安装 API 示例依赖")
    
    # 总结
    if all_success:
        print("\n✓ 所有依赖安装成功!")
    else:
        print("\n⚠ 部分依赖安装失败，请查看上面的错误信息")
        print("你可以尝试手动安装失败的依赖:")
        print("python -m pip install <package_name>")
    
    print("\n按任意键退出...")
    try:
        input()
    except Exception:
        pass

if __name__ == "__main__":
    main()