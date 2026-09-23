# 抖音数据采集与 MongoDB 分析平台

MongoDB 课程小组项目，形成“数据采集 → MongoDB 存储 → FastAPI 查询 → Vue/ECharts 可视化”的完整链路。

## 项目结构

```text
.
├── backend/                 # FastAPI 服务、MongoDB 数据访问与配置
├── crawl/                   # 抖音热搜、用户、视频采集模块
├── src/                     # Vue 前端与数据可视化页面
├── public/                  # 前端静态资源
├── nosql-work/              # 早期实验页面，保留作历史参考
├── init-mongo.js            # MongoDB 集合校验规则和索引初始化
├── docker-compose.yml       # MongoDB 开发环境
├── .env.example             # 环境变量模板
├── requirements.txt         # Python 依赖
└── package.json             # 前端依赖与脚本
```

## 主要能力

- 抖音热搜、用户和视频数据采集；
- 请求失败重试、退避等待、字段清洗和时间转换；
- MongoDB 集合设计、文档校验、唯一索引和时间/排序索引；
- FastAPI + Motor 异步查询接口，支持分页、排序和聚合统计；
- Vue + ECharts/词云展示热搜、达人、热门视频和用户分析数据；
- Docker Compose 启动 MongoDB 开发环境。

## MongoDB 数据域

项目使用按分析主题拆分的文档集合，避免将不同业务数据强行放在同一张表中：

| 数据域 | 集合 | 用途 |
|---|---|---|
| 热搜 | `hot_words`、`hot_categories` | 热搜词、热度、排名、分类榜单及历史记录 |
| 达人 | `daren_rank`、`user_data`、`user_stats` | 达人基础资料、排行和历史统计 |
| 视频 | `hot_videos` | 热门视频、作者及互动指标 |
| 粉丝画像 | `fan_profiles` | 性别、年龄和地域分布等画像数据 |
| 内容建议 | `content_suggestions`、`word_cloud` | 热点选题、发布时间建议、推荐音乐和热词云 |

集合初始化脚本同时配置文档校验规则、唯一索引、时间索引和排序索引，便于按主题查询和保存历史快照。
## 环境配置

```bash
copy .env.example .env
```

`.env` 中的 `MONGO_ROOT_PASSWORD` 和 `MONGODB_URL` 必须使用同一个密码。`DOUYIN_COOKIE` 仅用于本地爬虫调试，不能提交到版本库。

## 启动 MongoDB

```bash
docker compose up -d
```

## 启动后端

```bash
pip install -r requirements.txt
python -m uvicorn backend.app:app --host 0.0.0.0 --port 5000 --reload
```

API 文档：`http://localhost:5000/docs`

## 运行爬虫

从项目根目录执行：

```bash
python -m crawl.douyin_hot_crawl
python crawl/douyin_user_crawl.py <sec_uid>
python -m crawl.run_multiple_users <sec_uid_1> <sec_uid_2>
python crawl/douyin_video_crawl.py
```

各爬虫的职责和早期版本差异见 [`crawl/README.md`](crawl/README.md)。

## 启动前端

```bash
npm install
npm run serve
```

## API 说明

- `backend/app.py` 是当前主要 FastAPI 服务；
- `api_example.py` 是扩展接口示例，包含更完整的统计、粉丝画像、内容建议和热词云查询；
- `nosql-work/` 是早期实验页面，不属于当前主运行链路。

## 安全说明

- 不要提交 `.env`、Cookie、API Key 或其他访问凭据；
- 公开仓库前应轮换历史上曾写入代码或配置文件的凭据；
- 当前工作树已移除本地凭据和生成的 Python 缓存；Git 历史仍可能包含旧配置，需要单独重写历史才能彻底清除。