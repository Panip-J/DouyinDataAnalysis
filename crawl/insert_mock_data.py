#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
将模拟的抖音达人数据存入数据库
"""

import sys
import time
from datetime import datetime
from typing import Dict, List

# 尝试导入数据库模块
try:
    from backend.douyin_db import DouyinDB
except ImportError:
    try:
        import os
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from backend.douyin_db import DouyinDB
    except ImportError:
        print("错误: 无法导入DouyinDB")
        print("请确保backend/douyin_db.py文件存在并且可以访问")
        sys.exit(1)

def insert_mock_users():
    """插入模拟用户数据到数据库"""
    # 创建数据库连接
    db = DouyinDB()
    
    # 模拟数据
    users = [
        {
            "user_id": "MS4wLjABAAAA-QW2Yq5QMIYimn9uh_UPQbUOQRXfYHAIvImp4LL1h5A",
            "nickname": "陈赫",
            "signature": "演员，综艺咖",
            "avatar_url": "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_9d3a6e2b8c0b7c1b77e5a2eb5c8e8b37.jpeg",
            "fans_count": 66555000,
            "following_count": 326,
            "likes_count": 790000000,
            "video_count": 215,
            "verified": True,
            "category": "演员",
            "tags": ["演员", "综艺", "明星"]
        },
        {
            "user_id": "MS4wLjABAAAAlpnJ4cYwAZ1sGIZXxuNqgI1wkzXeU-2XfnPj5dU6SLs",
            "nickname": "听泉赏宝",
            "signature": "古董收藏爱好者",
            "avatar_url": "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_4d1d4c3e0b1eb9c2a7120a0189c12a0e.jpeg",
            "fans_count": 36872000,
            "following_count": 8909,
            "likes_count": 140000000,
            "video_count": 782,
            "verified": True,
            "category": "收藏家",
            "tags": ["收藏", "古董", "文玩"]
        },
        {
            "user_id": "MS4wLjABAAAA9Lz0CuKYoLZz9iNSdvHRIoiBzqJ8BcTJ0xoZ7YE9QcA",
            "nickname": "刘德华",
            "signature": "演员，歌手",
            "avatar_url": "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_0a6c7f7b5c87d78c0d313c3c8c7b9e52.jpeg",
            "fans_count": 71251000,
            "following_count": 0,
            "likes_count": 480000000,
            "video_count": 128,
            "verified": True,
            "category": "演员",
            "tags": ["演员", "歌手", "明星"]
        },
        {
            "user_id": "MS4wLjABAAAA9OTYi3rWG_tI2xPgpgGpSk1jUIWbvOIY5rY06FzYjMQ",
            "nickname": "陈翔六点半",
            "signature": "搞笑短剧",
            "avatar_url": "https://p3-pc.douyinpic.com/aweme/100x100/aweme-avatar/tos-cn-avt-0015_a7e24c0d72e342c387c1400e9fb5a97c.jpeg",
            "fans_count": 73805000,
            "following_count": 606,
            "likes_count": 1130000000,
            "video_count": 1024,
            "verified": True,
            "category": "搞笑",
            "tags": ["搞笑", "短剧", "创作者"]
        }
    ]
    
    # 插入数据到数据库
    success_count = 0
    for user in users:
        try:
            # 添加用户到数据库
            if db.add_user(
                user_id=user["user_id"],
                nickname=user["nickname"],
                signature=user["signature"],
                avatar_url=user["avatar_url"],
                fans_count=user["fans_count"],
                following_count=user["following_count"],
                likes_count=user["likes_count"],
                video_count=user["video_count"],
                verified=user["verified"],
                category=user["category"],
                tags=user["tags"]
            ):
                print(f"✅ 用户 {user['nickname']} 数据已成功存入数据库")
                success_count += 1
            else:
                print(f"❌ 用户 {user['nickname']} 数据存入数据库失败")
        except Exception as e:
            print(f"❌ 处理用户 {user['nickname']} 时出错: {e}")
    
    # 关闭数据库连接
    db.close()
    
    print(f"\n数据导入完成! 成功导入 {success_count}/{len(users)} 条记录")
    return success_count

if __name__ == "__main__":
    print("开始导入模拟抖音达人数据...")
    insert_mock_users() 