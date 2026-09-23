# 爬虫模块

`crawl` 目录负责采集抖音热搜、用户资料和视频数据，完成响应解析与字段标准化，并通过项目的 MongoDB 数据访问层持久化结果。

## 模块职责

```text
第三方数据接口
      ↓
请求、重试与响应解析
      ↓
标准化爬虫数据
      ↓
通过 backend.douyin_db 写入 MongoDB
```

采集模块与后端 API、前端页面相互独立，可以单独运行采集任务。

| 模块 | 说明 |
|---|---|
| `douyin_hot_crawl.py` | 周期性采集热搜数据，处理失败重试、退避等待、时间转换和 MongoDB 持久化。 |
| `douyin_user_crawl.py` | 采集用户资料、粉丝数、关注数、获赞数和作品数等统计信息。 |
| `douyin_video_crawl.py` | 采集视频详情及互动数据，并将标准化结果写入 MongoDB。 |
| `run_multiple_users.py` | 批量执行多个用户的采集任务。 |
| `insert_mock_data.py` | 向本地数据库写入开发测试数据。 |
| `douyin_video_crawl_legacy.py` | 历史单视频 CSV 导出脚本，仅用于兼容和参考；MongoDB 流程请使用 `douyin_video_crawl.py`。 |

## 环境配置

从项目根目录复制环境变量模板：

```powershell
Copy-Item .env.example .env
```

需要使用认证请求时，在本地 `.env` 中配置：

```dotenv
DOUYIN_COOKIE=your-local-cookie
```

凭据和会话 Cookie 只能保存在本地环境文件中，不要提交到仓库、Issue 或 Pull Request。

## 运行方式

请从项目根目录执行：

```bash
# 采集热搜数据；程序会持续运行，使用 Ctrl+C 停止
python -m crawl.douyin_hot_crawl

# 采集单个用户资料
python crawl/douyin_user_crawl.py <sec_uid>

# 批量采集用户资料
python -m crawl.run_multiple_users <sec_uid_1> <sec_uid_2>

# 采集单个视频数据并写入 MongoDB
python crawl/douyin_video_crawl.py

# 写入本地开发测试数据
python crawl/insert_mock_data.py
```

运行爬虫前，需要先启动 MongoDB。具体环境配置请参考项目根目录的 README。

## 数据处理

- 将外部接口响应视为不可信输入，在写入数据库前进行字段解析和标准化；
- 通过 MongoDB 数据访问模块统一处理集合、索引和持久化逻辑；
- 采集失败时记录错误并返回失败状态，避免将请求凭据写入日志或数据记录；
- 采集结果按照用户、热搜和视频等数据域分别保存。

## 合规使用

请仅采集有权访问的数据和接口，并遵守目标平台的服务条款、访问频率限制及适用法律法规。本目录用于本地开发和课程项目演示，不用于绕过访问控制或运行不受限制的生产级爬虫。