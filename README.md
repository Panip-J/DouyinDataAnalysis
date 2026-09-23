# 抖音数据采集与 MongoDB 分析平台

一个面向抖音公开数据采集、MongoDB 存储、FastAPI 查询和可视化展示的全栈数据分析项目。

## 项目架构

```text
数据采集（crawl）
        ↓
MongoDB 文档存储与索引（backend / init-mongo.js）
        ↓
FastAPI 查询接口（backend/app.py）
        ↓
Vue + ECharts 数据展示（src/）
```

## 项目结构

```text
.
├── backend/                 # FastAPI 服务、MongoDB 数据访问与配置
├── crawl/                   # 热搜、用户和视频数据采集
├── src/                     # Vue 前端与数据可视化页面
├── public/                  # 前端静态资源
├── nosql-work/              # 早期实验页面，不属于当前主运行链路
├── init-mongo.js            # MongoDB 集合校验规则和索引初始化
├── docker-compose.yml       # MongoDB 开发环境
├── .env.example             # 环境变量模板
├── requirements.txt         # Python 依赖
└── package.json             # 前端依赖和脚本
```

## 主要能力

- 采集抖音热搜、用户和视频数据；
- 对外部响应进行解析、字段标准化、时间转换和异常重试；
- 使用 MongoDB 进行文档建模、校验、索引和历史数据存储；
- 使用 FastAPI + Motor 提供异步查询接口，支持分页、排序和聚合统计；
- 使用 Vue、ECharts 和词云组件展示热搜、达人、热门视频及用户分析数据；
- 使用 Docker Compose 管理本地 MongoDB 开发环境。

## 数据采集模块

`crawl/` 目录中的脚本按数据类型拆分：

| 模块 | 说明 |
|---|---|
| `douyin_hot_crawl.py` | 周期性采集热搜，包含失败重试、退避等待、字段清洗和 MongoDB 持久化。 |
| `douyin_user_crawl.py` | 采集用户资料及粉丝、获赞、作品等统计信息。 |
| `douyin_video_crawl.py` | 采集视频详情和互动指标，并写入 MongoDB。 |
| `run_multiple_users.py` | 批量执行用户采集任务。 |
| `insert_mock_data.py` | 写入本地开发测试数据。 |
| `douyin_video_crawl_legacy.py` | 历史单视频 CSV 导出脚本，仅用于兼容和参考。 |

更多采集模块说明和命令见 [`crawl/README.md`](crawl/README.md)。

## MongoDB 数据域

项目按分析主题拆分 MongoDB 集合，保持数据域边界清晰：

| 数据域 | 集合 | 用途 |
|---|---|---|
| 热搜 | `hot_words`、`hot_categories` | 热搜词、热度、排名、分类榜单及历史记录 |
| 达人 | `daren_rank`、`user_data`、`user_stats` | 达人基础资料、排行和历史统计 |
| 视频 | `hot_videos` | 热门视频、作者及互动指标 |
| 粉丝画像 | `fan_profiles` | 性别、年龄和地域分布等画像数据 |
| 内容建议 | `content_suggestions`、`word_cloud` | 热点选题、发布时间建议、推荐音乐和热词云 |

`init-mongo.js` 负责创建集合、配置文档校验规则，并建立唯一索引、时间索引和排序索引。

## 环境配置

复制环境变量模板：

```bash
cp .env.example .env
```

Windows PowerShell 也可以执行：

```powershell
Copy-Item .env.example .env
```

配置时保持以下两项中的密码一致：

- `MONGO_ROOT_PASSWORD`
- `MONGODB_URL` 中的密码部分

`DOUYIN_COOKIE` 仅用于本地采集任务的请求配置，不应写入源代码。

## 启动 MongoDB

```bash
docker compose up -d
```

## 启动后端

```bash
pip install -r requirements.txt
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000 --reload
```

启动后可访问 FastAPI 文档：

```text
http://localhost:5000/docs
```

## 启动前端

```bash
npm install
npm run serve
```

前端默认通过 `src/utils/api.js` 访问本地后端服务。

## 运行采集任务

从项目根目录运行：

```bash
# 热搜采集
python -m crawl.douyin_hot_crawl

# 单个用户采集
python crawl/douyin_user_crawl.py <sec_uid>

# 批量用户采集
python -m crawl.run_multiple_users <sec_uid_1> <sec_uid_2>

# 单个视频采集
python crawl/douyin_video_crawl.py
```

也可以使用批处理入口：

```bat
run_crawler.bat <sec_uid_1> <sec_uid_2>
```

## API

### 主服务：`backend/app.py`

- `GET /`：服务状态；
- `GET /api/hot-words`：获取最新热搜；
- `GET /api/hot-videos`：获取热门视频；
- `GET /api/users`：获取用户列表；
- `GET /api/user/{user_id}`：获取用户信息；
- `GET /api/user/{user_id}/videos`：获取用户视频；
- `GET /api/crawled-users`：获取已采集用户。

### 扩展接口示例：`api_example.py`

`api_example.py` 保留了更完整的接口示例，包括：

- 热搜统计和时间范围筛选；
- 热搜分类；
- 达人排行；
- 用户历史统计；
- 粉丝画像；
- 内容创作建议；
- 热词云数据。

它用于展示扩展查询方式，不是当前前端的唯一后端入口。

## 开发说明

- 当前主链路为 `crawl → MongoDB → backend/app.py → src/`；
- `nosql-work/` 为早期实验页面，仅作历史参考；
- 课程设计中规划的 Service/DAO/Model 分层和部分分析模块，只有在实际代码中落地的部分才纳入当前运行说明。