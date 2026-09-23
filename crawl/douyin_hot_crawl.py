import requests
import time
import asyncio
import random
import sys
import os
from datetime import datetime
from typing import List, Dict, Optional

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.douyin_db import DouyinDB

# 最大重试次数
MAX_RETRIES = 3
# 初始重试延迟（秒）
INITIAL_RETRY_DELAY = 5

class DouyinHotCrawler:
    """抖音热搜爬虫类"""
    
    def __init__(self):
        """初始化爬虫"""
        self.url = 'https://www.douyin.com/aweme/v1/web/hot/search/list/'
        self.params = {
            'device_platform': 'webapp',
            'aid': '6383',
            'channel': 'channel_pc_web',
            'detail_list': '1',
            'source': '6',
            'main_billboard_count': '5',
            'version_code': '170400',
            'version_name': '17.4.0',
            'cookie_enabled': 'true',
            'platform': 'PC',
            'downlink': '10'
        }
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'www.douyin.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Referer': 'https://www.douyin.com/hot',
            'Connection': 'keep-alive'
        }
        self.db = DouyinDB()

    @staticmethod
    def trans_date(v_timestamp):
        """10位时间戳转换为时间字符串"""
        try:
            v_timestamp = int(v_timestamp)
            timeArray = time.localtime(v_timestamp)
            return time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        except:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def _make_request(self, retry_count: int = 0) -> Optional[dict]:
        """发送请求并处理响应"""
        try:
            r = requests.get(self.url, headers=self.headers, params=self.params)
            print(f"请求状态码: {r.status_code}")

            if r.status_code == 200:
                return r.json()
            elif retry_count < MAX_RETRIES:
                delay = INITIAL_RETRY_DELAY * (2 ** retry_count) + random.uniform(0, 1)
                print(f"请求失败，{delay:.2f}秒后重试（第{retry_count + 1}次）...")
                await asyncio.sleep(delay)
                return await self._make_request(retry_count + 1)
            else:
                print(f"达到最大重试次数，请求失败")
                return None

        except Exception as e:
            print(f"请求过程中出错: {e}")
            if retry_count < MAX_RETRIES:
                delay = INITIAL_RETRY_DELAY * (2 ** retry_count) + random.uniform(0, 1)
                print(f"将在{delay:.2f}秒后重试（第{retry_count + 1}次）...")
                await asyncio.sleep(delay)
                return await self._make_request(retry_count + 1)
            return None

    def _process_hot_search_data(self, data: dict) -> List[Dict]:
        """处理热搜数据"""
        hot_searches = []
        word_list = data.get('data', {}).get('word_list', [])
        
        for item in word_list:
            try:
                event_time = self.trans_date(item.get('event_time', ''))
            except:
                event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            hot_search = {
                'word': item.get('word', ''),
                'hot_value': item.get('hot_value', 0),
                'position': item.get('position', 0),
                'sentence_id': item.get('sentence_id', ''),
                'event_time': event_time,
                'tag': item.get('label', ''),
                'video_count': item.get('video_count', 0),
                'view_count': item.get('view_count', 0),
                'discussion_count': item.get('discussion_count', 0),
                'link': f"https://www.douyin.com/hot/{item.get('sentence_id', '')}",
                'created_at': datetime.now()
            }
            hot_searches.append(hot_search)
        
        return hot_searches

    async def save_to_database(self, hot_searches: List[Dict]) -> bool:
        """保存热搜数据到数据库"""
        try:
            if not hot_searches:
                print("没有数据可保存")
                return False

            # 批量添加热搜数据
            for hot_search in hot_searches:
                result = self.db.add_hot_search(
                    title=hot_search['word'],  # 字段名称变更
                    hot_value=hot_search['hot_value'],
                    position=hot_search['position'],
                    sentence_id=hot_search['sentence_id'],
                    tag=hot_search['tag'],
                    video_count=hot_search['video_count'],
                    view_count=hot_search['view_count'],
                    discussion_count=hot_search['discussion_count'],
                    link=hot_search['link'],
                    created_at=hot_search['created_at']
                )
                
                if not result:
                    print(f"保存热搜 '{hot_search['word']}' 失败")
                    return False

            print(f"成功保存 {len(hot_searches)} 条热搜数据到数据库")
            return True

        except Exception as e:
            print(f"保存到数据库时出错: {e}")
            return False

    async def crawl(self) -> bool:
        """执行爬虫任务"""
        try:
            # 获取热搜数据
            data = await self._make_request()
            if not data:
                return False

            # 处理数据
            hot_searches = self._process_hot_search_data(data)
            if not hot_searches:
                print("未获取到热搜数据")
                return False

            # 保存到数据库
            return await self.save_to_database(hot_searches)

        except Exception as e:
            print(f"爬虫执行过程中出错: {e}")
            return False

async def main():
    """主函数"""
    crawler = DouyinHotCrawler()
    
    try:
        while True:
            print("\n开始新一轮热搜数据爬取...")
            success = await crawler.crawl()
            
            if success:
                print("本轮热搜数据爬取和保存完成！")
            else:
                print("本轮热搜数据爬取或保存失败")
            
            # 随机等待5-10分钟
            wait_time = random.randint(300, 600)
            print(f"等待 {wait_time} 秒后开始下一轮爬取...")
            await asyncio.sleep(wait_time)

    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"程序执行出错: {e}")
    finally:
        # 关闭数据库连接
        crawler.db.close()

if __name__ == "__main__":
    asyncio.run(main())