# Crawler Module

The `crawl` package collects Douyin hot-search, user-profile, and video data, normalizes the responses, and persists the results through the project’s MongoDB data-access layer.

## Responsibilities

```text
External endpoints
      ↓
Request / retry / response parsing
      ↓
Normalized crawler records
      ↓
MongoDB persistence via backend.douyin_db
```

The crawlers are intentionally kept separate from the API and frontend layers so that collection jobs can be run independently from the web service.

## Modules

| Module | Responsibility |
|---|---|
| `douyin_hot_crawl.py` | Periodically collects hot-search records, applies retry/backoff handling, normalizes timestamps and fields, and stores records in MongoDB. |
| `douyin_user_crawl.py` | Collects and normalizes user profile data, including identity, profile, follower, following, likes and video statistics. |
| `douyin_video_crawl.py` | Collects video metadata and engagement statistics, then persists the normalized record to MongoDB. |
| `run_multiple_users.py` | Batch entry point for collecting multiple user profiles. |
| `insert_mock_data.py` | Inserts development fixtures for local testing. |
| `douyin_video_crawl_legacy.py` | Legacy single-video CSV exporter retained for compatibility; use `douyin_video_crawl.py` for the MongoDB pipeline. |

## Configuration

Create a local environment file from the project template:

```bash
copy .env.example .env
```

The crawlers read the following value when an authenticated request is required:

```dotenv
DOUYIN_COOKIE=your-local-cookie
```

Credentials and session cookies must remain in local environment files. Do not commit them to the repository or include them in issue reports and pull requests.

## Usage

Run commands from the repository root:

```bash
# Collect hot-search data; the process continues until interrupted.
python -m crawl.douyin_hot_crawl

# Collect one user profile.
python crawl/douyin_user_crawl.py <sec_uid>

# Collect multiple user profiles.
python -m crawl.run_multiple_users <sec_uid_1> <sec_uid_2>

# Collect one video and persist it to MongoDB.
python crawl/douyin_video_crawl.py

# Insert local fixture data for development.
python crawl/insert_mock_data.py
```

The MongoDB service must be running before starting a crawler. See the repository root README for Docker Compose and environment setup.

## Data handling

- Response payloads are treated as external input and normalized before persistence.
- MongoDB indexes and collection setup are defined by the backend data-access and initialization scripts.
- Crawler failures are logged and reported without committing response credentials or session data.

## Responsible use

Use only data and endpoints that you are authorized to access, and comply with the target platform’s terms, rate limits, and applicable laws. This repository is intended for local development and coursework demonstrations, not for bypassing access controls or operating an unrestricted production crawler.