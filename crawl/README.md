# crawl

抖音数据采集模块，负责将热搜、用户和视频数据清洗后写入 MongoDB。

## 文件

- `douyin_hot_crawl.py`：热搜采集、重试/退避和周期执行；
- `douyin_user_crawl.py`：用户资料解析和 MongoDB 持久化；
- `douyin_video_crawl.py`：视频详情解析和 MongoDB 持久化；
- `douyin_video_crawl_legacy.py`：旧版单视频 CSV 导出脚本，仅保留作历史参考；
- `run_multiple_users.py`：批量用户采集入口；
- `insert_mock_data.py`：开发测试数据填充脚本。

## 运行示例

从项目根目录执行：

```bash
python -m crawl.douyin_hot_crawl
python crawl/douyin_user_crawl.py <sec_uid>
python -m crawl.run_multiple_users <sec_uid_1> <sec_uid_2>
python crawl/douyin_video_crawl.py
```

爬虫从根目录 `.env` 读取 `DOUYIN_COOKIE`，源码不保存平台 Cookie。

## 与本地早期 Crawl 副本的关系

- 早期热搜脚本主要输出 CSV；当前版本封装为数据库采集流程，并增加重试/退避；
- 早期用户脚本是交互式 CSV 导出；当前版本增加结构化解析、日志、数据库写入和批量入口；
- 早期视频脚本与当前 `douyin_video_crawl_legacy.py` 内容一致；当前主版本额外写入 MongoDB；
- 早期目录中的 B 站爬虫和历史 CSV 未并入本项目。