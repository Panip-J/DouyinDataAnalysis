import requests
import time
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.douyin_db import DouyinDB

def trans_date(v_timestamp):
    """10位时间戳转换为时间字符串"""
    v_timestamp = int(v_timestamp)
    timeArray = time.localtime(v_timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

if __name__ == "__main__":
    video_id = input("请输入视频vid：")
    url = 'https://douyin.wtf/api/douyin/web/fetch_one_video?aweme_id=' + video_id
    headers = {
        'Cookie': os.getenv('DOUYIN_COOKIE', ''),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Host': 'douyin.wtf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
        'Referer': 'https://douyin.wtf/api/douyin/web',
        'Connection': 'keep-alive'
    }
    try:
        r = requests.get(url, headers=headers)
        print(f"请求状态码: {r.status_code}")
        json_data = r.json()
        aweme_detail = json_data['data']['aweme_detail']
        caption = aweme_detail.get('caption', '')
        author = aweme_detail.get('author', {}).get('nickname', '')
        href = f'https://www.douyin.com/video/{video_id}'
        try:
            time1 = trans_date(aweme_detail['create_time'])
        except:
            time1 = ''
        like_cnt = aweme_detail.get('statistics', {}).get('digg_count', 0)
        comment_cnt = aweme_detail.get('statistics', {}).get('comment_count', 0)
        collect_cnt = aweme_detail.get('statistics', {}).get('collect_count', 0)
        share_cnt = aweme_detail.get('statistics', {}).get('share_count', 0)
        print(f'标题: {caption}')
        print(f'作者: {author}')
        print(f'链接: {href}')
        print(f'时间: {time1}')
        print(f'点赞量: {like_cnt}')
        print(f'评论数: {comment_cnt}')
        print(f'收藏量: {collect_cnt}')
        print(f'转发量: {share_cnt}')
        print('爬取结束！')

        # 保存到MongoDB
        db = DouyinDB()
        db.add_hot_video(
            video_id=video_id,
            title=caption,
            author=author,
            user_id=aweme_detail.get('author', {}).get('sec_uid', ''),
            url=href,
            create_time=time1,
            likes=like_cnt,
            comments=comment_cnt,
            shares=share_cnt,
            collects=collect_cnt,
            play_count=aweme_detail.get('statistics', {}).get('play_count', 0),
            forward_count=aweme_detail.get('statistics', {}).get('forward_count', 0),
            description=aweme_detail.get('desc', ''),
            music_id=aweme_detail.get('music', {}).get('id', ''),
            music_title=aweme_detail.get('music', {}).get('title', ''),
            tags=[],
            date=None
        )
        db.close()
    except Exception as e:
        print(f"请求或解析数据时出错: {e}")