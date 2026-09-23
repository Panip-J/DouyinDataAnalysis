@echo off
setlocal
if "%~1"=="" (
  echo Usage: run_crawler.bat ^<sec_uid_1^> [sec_uid_2 ...]
  exit /b 1
)
python -m crawl.run_multiple_users %*
endlocal