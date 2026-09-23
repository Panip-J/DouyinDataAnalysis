"""
抖音数据分析系统配置文件
包含数据库连接和其他系统配置
"""

# MongoDB连接配置
MONGODB_URL = "mongodb://localhost:27017/douyin_analysis/douyin_analysis?authSource=admin"
DATABASE_NAME = "douyin_analysis"

# 集合名称配置
COLLECTIONS = {
    "users": "user_data",           # 用户基础数据
    "videos": "hot_videos",         # 热门视频数据
    "comments": "comments",         # 评论数据
    "hot_searches": "hot_words",    # 热搜榜数据
    "user_stats": "user_stats",     # 用户统计数据
    "fan_profiles": "fan_profiles", # 粉丝画像数据
    "daren_rank": "daren_rank",     # 达人排行榜数据
    "hot_categories": "hot_categories", # 热搜分类数据
    "content_suggestions": "content_suggestions", # 创作建议数据
    "word_cloud": "word_cloud"      # 热词云数据
}

# 数据库连接超时设置（秒）
CONNECT_TIMEOUT = 5
SOCKET_TIMEOUT = 5

# 重试设置
MAX_RETRIES = 3
RETRY_DELAY = 1

# 爬虫配置
CRAWL_DELAY = 2  # 爬虫请求间隔（秒）
MAX_CRAWL_RETRIES = 3  # 爬虫最大重试次数

# API限制
API_RATE_LIMIT = 100  # 每分钟最大请求次数
API_TIMEOUT = 30  # API请求超时时间（秒）

# 日志配置
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "douyin_analysis.log"

# 缓存配置
CACHE_ENABLED = True
CACHE_TIMEOUT = 300  # 缓存过期时间（秒）

# 安全配置
MAX_CONNECTIONS = 100  # 最大同时连接数