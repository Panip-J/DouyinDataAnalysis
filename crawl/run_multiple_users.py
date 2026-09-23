#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
批量爬取抖音用户信息脚本
"""

import sys
import asyncio
import argparse
from typing import List

# 尝试导入DouyinUserCrawl
try:
    from douyin_user_crawl import DouyinUserCrawler
except ImportError:
    try:
        from crawl.douyin_user_crawl import DouyinUserCrawler
    except ImportError:
        print("错误: 无法导入DouyinUserCrawler类")
        print("请确保当前目录下存在douyin_user_crawl.py文件")
        sys.exit(1)

async def crawl_multiple_users(user_ids: List[str]):
    """
    批量爬取多个用户的信息
    
    Args:
        user_ids: 用户ID列表
    """
    if not user_ids:
        print("错误: 未提供用户ID")
        return
    
    # 创建爬虫实例
    crawler = DouyinUserCrawler()
    
    print(f"开始爬取 {len(user_ids)} 个用户的信息...")
    
    # 存储成功和失败的用户ID
    success_ids = []
    failed_ids = []
    
    # 爬取每个用户的信息
    for i, user_id in enumerate(user_ids):
        print(f"\n[{i+1}/{len(user_ids)}] 正在爬取用户 {user_id} 的信息...")
        try:
            user_data = await crawler.crawl_user(user_id)
            if user_data:
                print(f"✅ 用户 {user_data['nickname']} 爬取成功!")
                print(f"  - 粉丝数: {user_data['follower_count']}")
                print(f"  - 关注数: {user_data['following_count']}")
                print(f"  - 获赞数: {user_data['likes_count']}")
                print(f"  - 视频数: {user_data['video_count']}")
                success_ids.append(user_id)
            else:
                print(f"❌ 用户 {user_id} 爬取失败!")
                failed_ids.append(user_id)
        except Exception as e:
            print(f"❌ 爬取用户 {user_id} 时出错: {e}")
            failed_ids.append(user_id)
    
    # 关闭爬虫
    crawler.close()
    
    # 打印汇总信息
    print("\n爬取完成!")
    print(f"成功: {len(success_ids)}/{len(user_ids)}")
    print(f"失败: {len(failed_ids)}/{len(user_ids)}")
    
    if failed_ids:
        print("\n失败的用户ID:")
        for user_id in failed_ids:
            print(f"  - {user_id}")

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="批量爬取抖音用户信息")
    parser.add_argument("user_ids", nargs="+", help="要爬取的抖音用户sec_uid列表")
    args = parser.parse_args()
    
    # 运行爬虫
    asyncio.run(crawl_multiple_users(args.user_ids)) 