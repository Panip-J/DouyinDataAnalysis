import os
import requests
import pandas as pd
import time

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

r = requests.get(url, headers=headers)  # 发送请求
print(r.status_code)  # 查看响应码
json_data = r.json()  # 用json接收请求数据

def trans_date(v_timestamp):
	"""10位时间戳转换为时间字符串"""
	v_timestamp = int(v_timestamp)
	timeArray = time.localtime(v_timestamp)
	otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
	return otherStyleTime

# 标题
caption = json_data['data']['aweme_detail']['caption']
# 作者
autor = json_data['data']['aweme_detail']['author']['nickname']
# 链接
href = 'https://www.douyin.com/video/' + video_id
# 时间
try:
    time1 = trans_date(json_data['data']['aweme_detail']['create_time'])
except:
    time1 = ''
time = time1
# 点赞量
like_cnt = json_data['data']['aweme_detail']['statistics']['digg_count']
# 评论数
comment_cnt = json_data['data']['aweme_detail']['statistics']['comment_count']
# 收藏量
collect_cnt = json_data['data']['aweme_detail']['statistics']['collect_count']
# 转发量
share_cnt = json_data['data']['aweme_detail']['statistics']['share_count']

df = pd.DataFrame(
    {
		'标题': [caption],
        '作者': [autor],
        '链接': [href],
        '时间': [time],
        '点赞量': [like_cnt],
        '评论数': [comment_cnt],
        '收藏量': [collect_cnt],
        '转发量': [share_cnt],
	}
)
df.to_csv('抖音视频.csv', index=False, encoding='utf_8_sig')  # 保存结果到csv文件
print('目标视频：' + caption)
print('爬取结束！')