import os
import re
import json
import random
import logging
import asyncio
import sys
from typing import Dict, List, Optional, Union, Any
from datetime import datetime
import requests

# 检查必要的依赖库
try:
    import aiohttp
except ImportError:
    print("错误: 缺少必要的依赖库 'aiohttp'")
    print("请使用以下命令安装: pip install aiohttp")
    sys.exit(1)

try:
    # 尝试直接导入
    from backend.douyin_db import DouyinDB
except ImportError:
    try:
        # 尝试添加父目录到路径
        import os
        import sys
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        from backend.douyin_db import DouyinDB
    except ImportError:
        print("错误: 无法导入 'DouyinDB'")
        print("请确保 backend/douyin_db.py 文件存在并且可以访问")
        print("当前Python路径:", sys.path)
        sys.exit(1)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('douyin_crawler.log')
    ]
)
logger = logging.getLogger('DouyinUserCrawler')

# 定义重试次数和延迟
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

class DouyinUserCrawler:
    """抖音用户爬虫类"""
    
    def __init__(self, cookie: str = None):
        """
        初始化爬虫
        
        Args:
            cookie: 可选的Cookie字符串
        """
        # 初始化数据库连接
        self.db = DouyinDB()
        
        # 设置请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
        }
        
        # 如果提供了cookie，添加到请求头中
        if cookie:
            self.headers['Cookie'] = cookie
        else:
            env_cookie = os.getenv('DOUYIN_COOKIE', '')
            if env_cookie:
                self.headers['Cookie'] = env_cookie
        # 初始化代理池
        self.proxy_pool = [None]  # 默认包含一个不使用代理的选项
        
    def _get_random_proxy(self) -> Optional[str]:
        """获取随机代理IP"""
        if not self.proxy_pool or len(self.proxy_pool) <= 1:
            return None  # 这里需要返回一个值，原代码缺少返回语句
        return random.choice(self.proxy_pool)
        
    def _validate_user_id(self, user_id: str) -> bool:
        """验证用户ID格式，允许任意非空字符串（支持sec_uid和纯数字）"""
        return bool(user_id and isinstance(user_id, str))
        
    def add_proxy(self, proxy: str) -> None:
        """添加代理到代理池"""
        if proxy and proxy not in self.proxy_pool:
            self.proxy_pool.append(proxy)
            logger.info(f"代理已添加到代理池: {proxy}")
            
    async def _make_request(self, url: str, retry_count: int = 0) -> Optional[str]:
        """
        发送HTTP请求并获取响应
        
        Args:
            url: 请求URL
            retry_count: 当前重试次数
            
        Returns:
            Optional[str]: 响应内容或None
        """
        try:
            proxy = self._get_random_proxy()
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, proxy=proxy, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        logger.error(f"请求失败，状态码: {response.status}")
                        
                        # 如果还有重试机会，等待后重试
                        if retry_count < MAX_RETRIES:
                            await asyncio.sleep(RETRY_DELAY)
                            return await self._make_request(url, retry_count + 1)
                        return None
                        
        except Exception as e:
            logger.error(f"请求出错: {e}", exc_info=True)
            
            # 如果还有重试机会，等待后重试
            if retry_count < MAX_RETRIES:
                await asyncio.sleep(RETRY_DELAY)
                return await self._make_request(url, retry_count + 1)
            return None
    
    def _extract_render_data(self, html: str) -> Optional[Dict]:
        """从HTML中提取RENDER_DATA"""
        try:
            # 查找RENDER_DATA
            match = re.search(r'<script id="RENDER_DATA" type="application/json">(.*?)</script>', html)
            if not match:
                logger.error("未找到RENDER_DATA")
                return None
            
            # 解码并解析JSON
            encoded_data = match.group(1)
            decoded_data = encoded_data.encode('utf-8').decode('unicode_escape')
            render_data = json.loads(decoded_data)
            
            return render_data
            
        except Exception as e:
            logger.error(f"提取RENDER_DATA时出错: {e}", exc_info=True)
            return None
    
    def _process_user_data(self, render_data: Dict, user_id: str) -> Optional[Dict]:
        """从RENDER_DATA中提取用户信息"""
        try:
            logger.debug(f"处理RENDER_DATA: {list(render_data.keys())}")
            
            # 查找用户数据
            user_info = None
            
            # 尝试从不同路径查找用户信息
            # 1. 尝试从userModule路径查找
            if 'userModule' in render_data:
                user_module = render_data['userModule']
                if 'users' in user_module and user_id in user_module['users']:
                    user_info = user_module['users'][user_id]
                    logger.info("从userModule.users路径找到用户信息")
                elif 'userInfo' in user_module:
                    user_info = user_module['userInfo']
                    logger.info("从userModule.userInfo路径找到用户信息")
            
            # 2. 尝试从C_user路径查找
            if not user_info and 'C_user' in render_data:
                user_data = render_data['C_user']
                if 'user' in user_data:
                    user_info = user_data['user']
                    logger.info("从C_user.user路径找到用户信息")
            
            # 3. 尝试从app.initialState路径查找
            if not user_info and 'app' in render_data and 'initialState' in render_data['app']:
                initial_state = render_data['app']['initialState']
                if 'userDetail' in initial_state and 'userInfo' in initial_state['userDetail']:
                    user_info = initial_state['userDetail']['userInfo']
                    logger.info("从app.initialState.userDetail.userInfo路径找到用户信息")
            
            # 4. 遍历所有可能包含用户信息的键
            if not user_info:
                for key, value in render_data.items():
                    if isinstance(value, dict):
                        # 检查是否包含用户信息的常见字段
                        if 'user' in value and isinstance(value['user'], dict):
                            user_info = value['user']
                            logger.info(f"从{key}.user路径找到用户信息")
                            break
                        elif 'userInfo' in value and isinstance(value['userInfo'], dict):
                            user_info = value['userInfo']
                            logger.info(f"从{key}.userInfo路径找到用户信息")
                            break
            
            if not user_info:
                logger.error("在RENDER_DATA中未找到用户信息")
                logger.debug(f"RENDER_DATA顶级键: {list(render_data.keys())}")
                return None
            
            # 打印找到的用户信息结构，帮助调试
            logger.debug(f"找到的用户信息结构: {list(user_info.keys())}")
            
            # 提取用户数据，处理不同的命名约定（驼峰命名和下划线命名）
            avatar_url = user_info.get('avatar_thumb', '')
            if isinstance(avatar_url, dict):
                avatar_url = avatar_url.get('url_list', [''])[0]
            user_data = {
                'user_id': user_id,
                'nickname': user_info.get('nickname', ''),
                'signature': user_info.get('signature', ''),
                'avatar_url': avatar_url,
                'follower_count': user_info.get('mplatform_followers_count', 0),
                'following_count': user_info.get('following_count', 0),
                'likes_count': user_info.get('total_favorited', 0),
                'video_count': user_info.get('aweme_count', 0),
                'verified': user_info.get('custom_verify', '') != '',
                'category': user_info.get('custom_verify', '') or '普通用户',
                'updated_at': datetime.now()
            }
            
            # 提取更多可能的字段
            if 'uid' in user_info:
                user_data['uid'] = user_info.get('uid', '')
            elif 'id' in user_info:
                user_data['uid'] = user_info.get('id', '')
                
            if 'secUid' in user_info:
                user_data['sec_uid'] = user_info.get('secUid', '')
            elif 'sec_uid' in user_info:
                user_data['sec_uid'] = user_info.get('sec_uid', '')
                
            if 'shortId' in user_info:
                user_data['short_id'] = user_info.get('shortId', '')
            elif 'short_id' in user_info:
                user_data['short_id'] = user_info.get('short_id', '')
                
            if 'uniqueId' in user_info:
                user_data['unique_id'] = user_info.get('uniqueId', '')
            elif 'unique_id' in user_info:
                user_data['unique_id'] = user_info.get('unique_id', '')
            
            # 提取认证信息
            user_data['category'] = user_info.get('customVerify', '') or user_info.get('custom_verify', '') or '普通用户'
            
            # 提取头像URL
            avatar_url = ''
            
            # 尝试从不同的字段获取头像URL
            avatar_fields = ['avatarThumb', 'avatar_thumb', 'avatarLarger', 'avatar_larger', 'avatarMedium', 'avatar_medium', 'avatar']
            
            for field in avatar_fields:
                if field in user_info:
                    avatar_data = user_info[field]
                    if isinstance(avatar_data, dict) and 'url_list' in avatar_data:
                        url_list = avatar_data['url_list']
                        if url_list and len(url_list) > 0:
                            avatar_url = url_list[0]
                            break
                    elif isinstance(avatar_data, dict) and 'urlList' in avatar_data:
                        url_list = avatar_data['urlList']
                        if url_list and len(url_list) > 0:
                            avatar_url = url_list[0]
                            break
                    elif isinstance(avatar_data, str):
                        avatar_url = avatar_data
                        break
            
            # 如果还是没有找到头像URL，尝试从avatarUrl字段获取
            if not avatar_url and 'avatarUrl' in user_info:
                avatar_url = user_info['avatarUrl']
            
            # 设置头像URL
            user_data['avatar_url'] = avatar_url
            
            logger.info(f"成功提取用户 {user_data['nickname']} 的信息")
            return user_data
            
        except Exception as e:
            logger.error(f"处理用户数据时出错: {e}", exc_info=True)
            return None
            
    async def crawl_user(self, user_id: str) -> Optional[Dict]:
        """
        爬取用户信息的主入口方法
        
        Args:
            user_id: 用户ID
            
        Returns:
            Optional[Dict]: 用户信息或None
        """
        try:
            url = f'https://www.douyin.com/web/api/v2/user/info/?sec_uid={user_id}'
            headers = self.headers.copy()
            # requests不支持aiohttp的headers对象，需转为dict
            r = requests.get(url, headers=headers)
            if r.status_code != 200:
                logger.error(f"请求失败，状态码: {r.status_code}")
                return None
            json_data = r.json()
            user_info = json_data.get('user_info', {})
            if not user_info:
                logger.error(f"未获取到用户信息: {user_id}")
                return None
            avatar_url = user_info.get('avatar_thumb', '')
            if isinstance(avatar_url, dict):
                avatar_url = avatar_url.get('url_list', [''])[0]
            user_data = {
                'user_id': user_id,
                'nickname': user_info.get('nickname', ''),
                'signature': user_info.get('signature', ''),
                'avatar_url': avatar_url,
                'follower_count': user_info.get('mplatform_followers_count', 0),
                'following_count': user_info.get('following_count', 0),
                'likes_count': user_info.get('total_favorited', 0),
                'video_count': user_info.get('aweme_count', 0),
                'verified': user_info.get('custom_verify', '') != '',
                'category': user_info.get('custom_verify', '') or '普通用户',
                'updated_at': datetime.now()
            }
            # 存储到数据库
            if self.db.add_user(
                user_id=user_data['user_id'],
                nickname=user_data['nickname'],
                signature=user_data['signature'],
                avatar_url=user_data['avatar_url'],
                fans_count=user_data['follower_count'],
                following_count=user_data['following_count'],
                likes_count=user_data['likes_count'],
                video_count=user_data['video_count'],
                verified=user_data['verified'],
                category=user_data.get('category', ''),
                location=user_data.get('location', ''),
                tags=[]
            ):
                logger.info(f"用户数据已成功存储到数据库: {user_data['nickname']} ({user_id})")
            else:
                logger.error(f"存储用户数据到数据库失败: {user_id}")
            return user_data
        except Exception as e:
            logger.error(f"爬取用户信息时出错: {e}", exc_info=True)
            return None
        
    def close(self):
        """关闭爬虫，清理资源"""
        if hasattr(self, 'db'):
            self.db.close()
            logger.info("数据库连接已关闭")

if __name__ == "__main__":
    import argparse
    import asyncio
    
    parser = argparse.ArgumentParser(description="抖音用户信息爬取")
    parser.add_argument("user_id", type=str, help="抖音用户sec_uid")
    args = parser.parse_args()
    
    crawler = DouyinUserCrawler()
    user_id = args.user_id
    print(f"开始爬取用户 {user_id} 的信息...")
    user_data = asyncio.run(crawler.crawl_user(user_id))
    if user_data:
        print("爬取成功!")
        print(f"用户昵称: {user_data['nickname']}")
        print(f"签名: {user_data['signature']}")
        print(f"粉丝数: {user_data['follower_count']}")
        print(f"关注数: {user_data['following_count']}")
        print(f"获赞数: {user_data['likes_count']}")
        print(f"视频数: {user_data['video_count']}")
        print(f"头像URL: {user_data['avatar_url']}")
    else:
        print("爬取失败!")
    crawler.close()