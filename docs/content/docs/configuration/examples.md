+++
title = "配置示例集"
description = "各种使用场景的完整配置示例，帮助你快速上手"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 60
template = "docs/page.html"

[extra]
lead = "本文档提供各种常见场景的完整配置示例，你可以直接复制使用或根据需要修改。"
toc = true
top = false
+++

## 概述

本文档包含以下场景的配置示例：
- 单主播录制
- 多主播录制
- 边录边传
- 分段录制
- 自定义上传参数
- Docker 环境配置

## 示例 1：单主播录制（最简配置）

最简单的配置，录制一个主播并自动上传到 B 站。

### TOML 格式

```toml
# 单主播录制配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300

# 主播配置
[streamers."我的主播"]
url = ["https://www.twitch.tv/username"]
tags = ["直播录像", "游戏"]
tid = 171

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### YAML 格式

```yaml
# 单主播录制配置

# 全局设置
file_size: 2621440000
filtering_threshold: 20
delay: 300

# 主播配置
streamers:
  我的主播:
    url:
      - https://www.twitch.tv/username
    tags:
      - 直播录像
      - 游戏
    tid: 171

# 认证配置
user:
  bili_cookie_file: cookies.json
```

### 说明

- 使用默认下载器和上传器
- 文件大小超过 2.5GB 自动分段
- 过滤小于 20MB 的文件
- 下播后延迟 5 分钟再上传

## 示例 2：多主播录制

同时录制多个主播，每个主播使用不同的配置。

### TOML 格式

```toml
# 多主播录制配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300
lines = "AUTO"
threads = 3

# 游戏主播1
[streamers."游戏主播A"]
url = ["https://www.twitch.tv/gamerA"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["星际争霸2", "电竞", "直播录像"]
description = """
视频简介: {title}
录制时间: %Y-%m-%d %H:%M:%S
主播直播间：{url}
"""
dynamic = "#星际争霸2# #电子竞技#"

# 游戏主播2
[streamers."游戏主播B"]
url = ["https://www.youtube.com/@gamerB/live"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["英雄联盟", "电竞", "直播录像"]
description = """
视频简介: {title}
录制时间: %Y-%m-%d %H:%M:%S
主播直播间：{url}
"""

# 音乐主播
[streamers."音乐主播"]
url = ["https://live.bilibili.com/123456"]
title = "{title}%Y-%m-%d{streamer}"
tid = 130
tags = ["音乐", "唱见", "直播录像"]
use_live_cover = true

# 绘画主播
[streamers."绘画主播"]
url = ["https://www.twitch.tv/artist"]
title = "{title}%Y-%m-%d{streamer}"
tid = 163
tags = ["绘画", "创作", "直播录像"]

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### YAML 格式

```yaml
# 多主播录制配置

# 全局设置
file_size: 2621440000
filtering_threshold: 20
delay: 300
lines: AUTO
threads: 3

# 主播配置
streamers:
  游戏主播A:
    url:
      - https://www.twitch.tv/gamerA
    title: "{title}%Y-%m-%d{streamer}"
    tid: 171
    tags:
      - 星际争霸2
      - 电竞
      - 直播录像
    description: |-
      视频简介: {title}
      录制时间: %Y-%m-%d %H:%M:%S
      主播直播间：{url}
    dynamic: "#星际争霸2# #电子竞技#"
  
  游戏主播B:
    url:
      - https://www.youtube.com/@gamerB/live
    title: "{title}%Y-%m-%d{streamer}"
    tid: 171
    tags:
      - 英雄联盟
      - 电竞
      - 直播录像
    description: |-
      视频简介: {title}
      录制时间: %Y-%m-%d %H:%M:%S
      主播直播间：{url}
  
  音乐主播:
    url:
      - https://live.bilibili.com/123456
    title: "{title}%Y-%m-%d{streamer}"
    tid: 130
    tags:
      - 音乐
      - 唱见
      - 直播录像
    use_live_cover: true
  
  绘画主播:
    url:
      - https://www.twitch.tv/artist
    title: "{title}%Y-%m-%d{streamer}"
    tid: 163
    tags:
      - 绘画
      - 创作
      - 直播录像

# 认证配置
user:
  bili_cookie_file: cookies.json
```

### 说明

- 同时录制 4 个主播
- 每个主播使用不同的分区和标签
- 音乐主播使用直播间封面
- 所有主播使用相同的认证信息


## 示例 3：边录边传

录制的同时自动上传，适合追求时效性的场景。

### TOML 格式

```toml
# 边录边传配置

# 全局设置
file_size = 1073741824  # 1GB，减小分段大小
filtering_threshold = 20
delay = 0  # 立即上传
lines = "bda2"  # 选择快速线路
threads = 5  # 增加并发

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]
description = """
视频简介: {title}
录制时间: %Y-%m-%d %H:%M:%S
"""

# 上传完成后删除文件
postprocessor = [
    {rm}
]

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### YAML 格式

```yaml
# 边录边传配置

# 全局设置
file_size: 1073741824  # 1GB
filtering_threshold: 20
delay: 0  # 立即上传
lines: bda2
threads: 5

# 主播配置
streamers:
  主播:
    url:
      - https://www.twitch.tv/username
    title: "{title}%Y-%m-%d{streamer}"
    tid: 171
    tags:
      - 直播录像
      - 游戏
    description: |-
      视频简介: {title}
      录制时间: %Y-%m-%d %H:%M:%S
    postprocessor:
      - rm

# 认证配置
user:
  bili_cookie_file: cookies.json
```

### 说明

- 文件大小 1GB 自动分段并上传
- 下播后立即开始上传
- 使用快速上传线路
- 上传完成后自动删除文件

## 示例 4：分段录制

按时间或大小分段录制，适合长时间直播。

### 按时间分段（TOML）

```toml
# 按时间分段配置

# 全局设置
filtering_threshold = 20
delay = 300

# 主播配置
[streamers."长时间直播主播"]
url = ["https://www.twitch.tv/username"]
title = "{title}第{index}部分%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]
segment_time = "01:00:00"  # 每小时分段

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### 按大小分段（TOML）

```toml
# 按大小分段配置

# 全局设置
file_size = 1073741824  # 1GB
filtering_threshold = 20
delay = 300

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
title = "{title}第{index}部分%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### 说明

- 按时间分段：每小时自动分段
- 按大小分段：每 1GB 自动分段
- 分段文件会自动编号上传

## 示例 5：自定义上传参数

完整的上传参数配置，包括封面、简介、动态等。

### TOML 格式

```toml
# 自定义上传参数配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300
lines = "AUTO"
threads = 3

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]

# 标题模板
title = "{title}%Y-%m-%d{streamer}"

# 分区
tid = 171

# 版权
copyright = 2

# 标签
tags = ["星际争霸2", "电竞", "直播录像", "INnoVation"]

# 简介
description = """
🎮 视频简介
━━━━━━━━━━━━━━━━━━━━
📺 直播标题: {title}
📅 录制时间: %Y-%m-%d %H:%M:%S
🔗 主播直播间：{url}
━━━━━━━━━━━━━━━━━━━━
⚡ Powered By biliup
📦 Github: https://github.com/ForgQi/biliup
"""

# 动态
dynamic = "#星际争霸2# #电子竞技# #INnoVation#"

# 来源
source = "转载自 Twitch"

# 封面
cover_path = "/covers/sc2.jpg"

# 视频属性
dolby = 0
hires = 0
no_reprint = 0
charging_pay = 0
is_only_self = 0

# 自定义文件名
filename_prefix = "[{streamer}]%Y%m%d_%H%M%S_{title}"

# 后处理
postprocessor = [
    {mv = "backup/"},
    {run = "python3 notify.py"}
]

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### YAML 格式

```yaml
# 自定义上传参数配置

# 全局设置
file_size: 2621440000
filtering_threshold: 20
delay: 300
lines: AUTO
threads: 3

# 主播配置
streamers:
  主播:
    url:
      - https://www.twitch.tv/username
    title: "{title}%Y-%m-%d{streamer}"
    tid: 171
    copyright: 2
    tags:
      - 星际争霸2
      - 电竞
      - 直播录像
      - INnoVation
    description: |-
      🎮 视频简介
      ━━━━━━━━━━━━━━━━━━━━
      📺 直播标题: {title}
      📅 录制时间: %Y-%m-%d %H:%M:%S
      🔗 主播直播间：{url}
      ━━━━━━━━━━━━━━━━━━━━
      ⚡ Powered By biliup
      📦 Github: https://github.com/ForgQi/biliup
    dynamic: "#星际争霸2# #电子竞技# #INnoVation#"
    source: 转载自 Twitch
    cover_path: /covers/sc2.jpg
    dolby: 0
    hires: 0
    no_reprint: 0
    charging_pay: 0
    is_only_self: 0
    filename_prefix: "[{streamer}]%Y%m%d_%H%M%S_{title}"
    postprocessor:
      - mv: backup/
      - run: python3 notify.py

# 认证配置
user:
  bili_cookie_file: cookies.json
```

### 说明

- 完整的视频元信息配置
- 自定义封面和文件名
- 上传后移动到备份目录并发送通知


## 示例 6：Docker 环境配置

适用于 Docker 容器环境的配置。

### docker-compose.yml

```yaml
version: '3'

services:
  biliup:
    image: ghcr.io/biliup/biliup:latest
    container_name: biliup
    restart: unless-stopped
    volumes:
      - ./config.toml:/app/config.toml
      - ./cookies.json:/app/cookies.json
      - ./videos:/app/videos
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
    command: start
```

### config.toml

```toml
# Docker 环境配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300
lines = "AUTO"
threads = 3

# 日志配置
[LOGGING.handlers.file]
level = "INFO"
class = "biliup.common.log.SafeRotatingFileHandler"
when = "D"
interval = 1
backupCount = 7
filename = "/app/logs/biliup.log"
formatter = "verbose"
encoding = "utf-8"

[LOGGING.formatters.verbose]
format = "%(asctime)s %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[LOGGING.root]
handlers = ["console"]
level = "INFO"

[LOGGING.loggers.biliup]
handlers = ["file"]
level = "INFO"

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]
filename_prefix = "/app/videos/{streamer}%Y-%m-%d_%H%M%S_{title}"

# 上传后删除
postprocessor = [
    {rm}
]

# 认证配置
[user]
bili_cookie_file = "/app/cookies.json"
```

### 使用方法

```bash
# 创建目录
mkdir -p videos logs

# 复制配置文件
cp config.toml ./
cp cookies.json ./

# 启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止容器
docker-compose down
```

### 说明

- 配置文件和 Cookie 挂载到容器
- 视频保存到宿主机 `videos` 目录
- 日志保存到宿主机 `logs` 目录
- 使用上海时区

## 示例 7：高画质录制

录制 B 站高画质直播。

### TOML 格式

```toml
# 高画质录制配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300

# B 站配置
bili_protocol = "hls_fmp4"  # fmp4流
bili_qn = 10000  # 原画
bili_cdn = ["cn-gotcha208"]  # 优选CDN
downloader = "streamlink"  # 多线程下载

# 主播配置
[streamers."B站主播"]
url = ["https://live.bilibili.com/123456"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]
use_live_cover = true

# 覆盖全局配置
[streamers."B站主播".override]
bili_qn = 10000
bili_protocol = "hls_fmp4"
downloader = "streamlink"

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### 说明

- 使用 fmp4 流获取最高画质
- 使用 streamlink 多线程下载
- 优选 cn-gotcha208 CDN
- 需要配置 Cookie

## 示例 8：多账号上传

使用多个 B 站账号上传不同内容。

### TOML 格式

```toml
# 多账号上传配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300

# 游戏主播 - 使用游戏账号
[streamers."游戏主播1"]
url = ["https://www.twitch.tv/gamer1"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["游戏", "电竞"]
user_cookie = "game_account.json"

[streamers."游戏主播2"]
url = ["https://www.twitch.tv/gamer2"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["游戏", "电竞"]
user_cookie = "game_account.json"

# 音乐主播 - 使用音乐账号
[streamers."音乐主播"]
url = ["https://www.youtube.com/@musician/live"]
title = "{title}%Y-%m-%d{streamer}"
tid = 130
tags = ["音乐", "唱见"]
user_cookie = "music_account.json"

# 其他主播 - 使用默认账号
[streamers."其他主播"]
url = ["https://example.com"]
title = "{title}%Y-%m-%d{streamer}"
tid = 21
tags = ["日常", "生活"]
# 使用全局默认账号

# 全局默认账号
[user]
bili_cookie_file = "main_account.json"
```

### 说明

- 游戏内容使用游戏账号
- 音乐内容使用音乐账号
- 其他内容使用默认账号
- 避免单账号内容过于杂乱

## 示例 9：仅录制不上传

只录制直播，不自动上传。

### TOML 格式

```toml
# 仅录制配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300
uploader = "Noop"  # 不上传

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
filename_prefix = "recordings/{streamer}%Y-%m-%d_%H%M%S_{title}"

# 保存到本地
postprocessor = [
    {mv = "recordings/"}
]
```

### 说明

- 设置 `uploader = "Noop"` 禁用上传
- 录制的视频保存到 `recordings` 目录
- 适合手动上传或本地存档

## 示例 10：延时发布

录制后延时发布视频。

### TOML 格式

```toml
# 延时发布配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["直播录像", "游戏"]
dtime = 1710086400  # 2024-03-10 16:00:00 UTC

# 认证配置
[user]
bili_cookie_file = "cookies.json"
```

### 说明

- 使用 `dtime` 设置发布时间
- 时间戳必须距离提交时间大于 2 小时
- 适合定时发布或避开高峰期

## 示例 11：完整生产环境配置

适合生产环境的完整配置。

### TOML 格式

```toml
# 生产环境配置

# 全局设置
file_size = 2621440000
filtering_threshold = 20
delay = 300
lines = "AUTO"
threads = 3
downloader = "streamlink"

# 任务调度
event_loop_interval = 30
checker_sleep = 10
check_sourcecode = 0  # 禁用自动重启

# 线程池
pool1_size = 10
pool2_size = 10

# 日志配置
[LOGGING.formatters.verbose]
format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[LOGGING.handlers.console]
level = "INFO"
class = "logging.StreamHandler"
formatter = "verbose"
stream = "ext://sys.stdout"

[LOGGING.handlers.file]
level = "DEBUG"
class = "biliup.common.log.SafeRotatingFileHandler"
when = "D"
interval = 1
backupCount = 30
filename = "logs/biliup.log"
formatter = "verbose"
encoding = "utf-8"

[LOGGING.root]
handlers = ["console"]
level = "INFO"

[LOGGING.loggers.biliup]
handlers = ["file"]
level = "INFO"

# 主播配置
[streamers."主播1"]
url = ["https://www.twitch.tv/streamer1"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["游戏", "电竞", "直播录像"]
description = """
视频简介: {title}
录制时间: %Y-%m-%d %H:%M:%S
主播直播间：{url}
"""
use_live_cover = true
user_cookie = "account1.json"

postprocessor = [
    {mv = "backup/"},
    {run = "python3 scripts/notify.py"}
]

[streamers."主播2"]
url = ["https://www.youtube.com/@streamer2/live"]
title = "{title}%Y-%m-%d{streamer}"
tid = 130
tags = ["音乐", "唱见", "直播录像"]
user_cookie = "account2.json"

postprocessor = [
    {mv = "backup/"},
    {run = "python3 scripts/notify.py"}
]

# 认证配置
[user]
bili_cookie_file = "main_account.json"
```

### 说明

- 完整的日志配置，保留 30 天
- 禁用自动重启，避免生产环境意外重启
- 多主播、多账号配置
- 上传后备份并发送通知
- 适合长期稳定运行

## 相关链接

- [配置文件格式](./config-file-format.md)
- [主播配置详解](./streamer-config.md)
- [上传配置详解](./upload-config.md)
- [高级配置选项](./advanced-config.md)
- [认证配置](./authentication.md)
