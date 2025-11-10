+++
title = "高级配置"
description = "了解 biliup 的高级配置选项，包括代理、日志、数据库、事件钩子和性能优化"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 40
template = "docs/page.html"

[extra]
lead = "本文档介绍 biliup 的高级配置选项，适合需要深度定制和优化的用户。"
toc = true
top = false
+++

## 概述

高级配置包括代理设置、日志配置、数据库配置、事件钩子和性能优化等选项，可以帮助你更好地控制 biliup 的行为。

## 代理配置

### 全局代理

为所有网络请求设置代理。

**TOML 示例：**
```toml
[proxy]
http = "http://127.0.0.1:7890"
https = "http://127.0.0.1:7890"
```

**YAML 示例：**
```yaml
proxy:
  http: http://127.0.0.1:7890
  https: http://127.0.0.1:7890
```

**说明：**
- 支持 HTTP、HTTPS、SOCKS5 代理
- 适用于需要代理访问的网络环境
- 海外服务器访问国内平台时可能需要

### SOCKS5 代理

```toml
[proxy]
http = "socks5://127.0.0.1:1080"
https = "socks5://127.0.0.1:1080"
```

### 环境变量代理

也可以通过环境变量设置代理：

```bash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
biliup start
```

## 日志配置

biliup 使用 Python logging 模块进行日志管理。

### 基本日志配置

**TOML 示例：**
```toml
[LOGGING.root]
handlers = ["console"]
level = "INFO"

[LOGGING.loggers.biliup]
handlers = ["file"]
level = "INFO"
```

**YAML 示例：**
```yaml
LOGGING:
  root:
    handlers: [console]
    level: INFO
  loggers:
    biliup:
      handlers: [file]
      level: INFO
```

### 日志级别

**可选级别：**
- `DEBUG`：调试信息（最详细）
- `INFO`：一般信息
- `WARNING`：警告信息
- `ERROR`：错误信息
- `CRITICAL`：严重错误

**示例：**
```toml
[LOGGING.root]
level = "DEBUG"  # 输出所有日志
```

### 日志格式化

**TOML 示例：**
```toml
[LOGGING.formatters.verbose]
format = "%(asctime)s %(filename)s[line:%(lineno)d](Pid:%(process)d Tname:%(threadName)s) %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[LOGGING.formatters.simple]
format = "%(filename)s%(lineno)d[%(levelname)s]Tname:%(threadName)s %(message)s"
```

**YAML 示例：**
```yaml
LOGGING:
  formatters:
    verbose:
      format: '%(asctime)s %(filename)s[line:%(lineno)d](Pid:%(process)d Tname:%(threadName)s) %(levelname)s %(message)s'
      datefmt: '%Y-%m-%d %H:%M:%S'
    simple:
      format: '%(filename)s%(lineno)d[%(levelname)s]Tname:%(threadName)s %(message)s'
```

### 日志处理器

#### 控制台输出

```toml
[LOGGING.handlers.console]
level = "DEBUG"
class = "logging.StreamHandler"
formatter = "simple"
stream = "ext://sys.stdout"
```

#### 文件输出

```toml
[LOGGING.handlers.file]
level = "DEBUG"
class = "biliup.common.log.SafeRotatingFileHandler"
when = "W0"  # 每周一轮换
interval = 1
backupCount = 1  # 保留1个备份
filename = "ds_update.log"
formatter = "verbose"
encoding = "utf-8"
```

**参数说明：**
- `when`：轮换时机
  - `S`：秒
  - `M`：分钟
  - `H`：小时
  - `D`：天
  - `W0`-`W6`：星期（0=星期一）
- `interval`：轮换间隔
- `backupCount`：保留备份数量

### 完整日志配置示例

```toml
[LOGGING.formatters.verbose]
format = "%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"
datefmt = "%Y-%m-%d %H:%M:%S"

[LOGGING.formatters.simple]
format = "%(levelname)s %(message)s"

[LOGGING.handlers.console]
level = "INFO"
class = "logging.StreamHandler"
formatter = "simple"
stream = "ext://sys.stdout"

[LOGGING.handlers.file]
level = "DEBUG"
class = "biliup.common.log.SafeRotatingFileHandler"
when = "D"  # 每天轮换
interval = 1
backupCount = 7  # 保留7天
filename = "biliup.log"
formatter = "verbose"
encoding = "utf-8"

[LOGGING.root]
handlers = ["console"]
level = "INFO"

[LOGGING.loggers.biliup]
handlers = ["file"]
level = "DEBUG"
```


## 任务调度配置

### delay

检测到主播下播后的延迟时间。

**类型**：整数（秒）  
**必需**：否  
**默认值**：0

**示例：**
```toml
delay = 300  # 5分钟
```

**说明：**
- 避免特殊情况提早启动上传导致漏录
- 推荐设置 300 秒（5分钟）
- 超过 60 秒会启用分段检测机制（每 60 秒检测一次）

### event_loop_interval

平台检测间隔时间。

**类型**：整数（秒）  
**必需**：否  
**默认值**：30

**示例：**
```toml
event_loop_interval = 30
```

**说明：**
- 所有主播检测完后等待的时间
- 例如：虎牙所有主播检测完后等待 30 秒再重新检测

### checker_sleep

单个主播检测间隔时间。

**类型**：整数（秒）  
**必需**：否  
**默认值**：10

**示例：**
```toml
checker_sleep = 10
```

**说明：**
- 每个主播之间的检测间隔
- 例如：10 个主播，每个主播间隔 10 秒检测

### check_sourcecode

检测源码文件变化间隔。

**类型**：整数（秒）  
**必需**：否  
**默认值**：15

**示例：**
```toml
check_sourcecode = 15
```

**说明：**
- 检测到源码变化后，程序会在空闲时自动重启
- 设置为 0 禁用自动重启
- 适用于开发和调试

## 线程池配置

### pool1_size

线程池1大小，负责下载事件。

**类型**：整数  
**必需**：否  
**默认值**：3

**示例：**
```toml
pool1_size = 5
```

**说明：**
- 每个下载占用 1 个线程
- 应设置为比主播数量略大
- 如不确定，可设置为 999

### pool2_size

线程池2大小，负责上传事件。

**类型**：整数  
**必需**：否  
**默认值**：3

**示例：**
```toml
pool2_size = 5
```

**说明：**
- 每个上传占用 1 个线程
- 应设置为比主播数量略大
- 如开启 `uploading_record` 需要设置更多

## 录制配置

### downloader

全局默认下载插件。

**类型**：字符串  
**必需**：否  
**默认值**：`stream-gears`

**可选值：**
- `stream-gears`：默认下载器
- `streamlink`：Streamlink + FFmpeg 混合模式
- `ffmpeg`：纯 FFmpeg 下载

**示例：**
```toml
downloader = "ffmpeg"
```

**说明：**
- `streamlink`：适合 HLS_FMP4 和 HLS_TS 流，支持多线程
- `ffmpeg`：纯 FFmpeg 下载
- `stream-gears`：默认推荐

### file_size

录像单文件大小限制。

**类型**：整数（字节）  
**必需**：否  
**默认值**：2621440000（2.5GB）

**示例：**
```toml
file_size = 2621440000  # 2.5GB
```

**说明：**
- 超过此大小自动分段
- 下载回放时无法使用

### segment_time

录像单文件时间限制。

**类型**：字符串（HH:MM:SS）  
**必需**：否  
**默认值**：无

**示例：**
```toml
segment_time = "01:00:00"  # 1小时
```

**说明：**
- 超过此时间自动分段
- 与 `file_size` 互斥，优先使用 `segment_time`
- 如需使用大小分段，请注释此字段

### filtering_threshold

文件过滤阈值。

**类型**：整数（MB）  
**必需**：否  
**默认值**：20

**示例：**
```toml
filtering_threshold = 20
```

**说明：**
- 小于此大小的视频文件会被过滤删除
- 用于过滤测试或异常的短视频

### filename_prefix

自定义录播文件名模板。

**类型**：字符串  
**必需**：否  
**默认值**：`{streamer}%Y-%m-%d %H_%M_%S{title}`

**示例：**
```toml
filename_prefix = "{streamer}%Y-%m-%d %H_%M_%S{title}"
```

**说明：**
- 支持占位符：`{streamer}`、`{title}`
- 支持时间格式化
- 必须包含时间，避免分段文件覆盖

### segment_processor_parallel

视频分段后处理并行。

**类型**：布尔值  
**必需**：否  
**默认值**：false

**示例：**
```toml
segment_processor_parallel = true
```

**说明：**
- 开启后无法保证分段后处理的先后顺序
- 可提高处理速度

## 事件钩子配置

事件钩子允许在特定时机执行自定义操作。详细说明请参考[主播配置](./streamer-config.md)中的事件钩子部分。

### preprocessor

开始下载时触发。

```toml
[streamers."主播"]
preprocessor = [
    {run = "sh ./notify_start.sh"}
]
```

### segment_processor

视频分段时触发。

```toml
[streamers."主播"]
segment_processor = [
    {run = "sh ./process_segment.sh"}
]
```

### downloaded_processor

准备上传时触发。

```toml
[streamers."主播"]
downloaded_processor = [
    {run = "sh ./pre_upload.sh"}
]
```

### postprocessor

上传完成后触发。

```toml
[streamers."主播"]
postprocessor = [
    {mv = "backup/"},
    {run = "python3 notify.py"}
]
```

## 性能优化配置

### 优化下载性能

1. **选择合适的下载器**
   ```toml
   downloader = "streamlink"  # 多线程下载
   ```

2. **调整线程池大小**
   ```toml
   pool1_size = 10  # 根据主播数量调整
   ```

3. **合理设置分段**
   ```toml
   file_size = 1073741824  # 1GB，减小单文件大小
   ```

### 优化上传性能

1. **选择最优线路**
   ```toml
   lines = "AUTO"  # 或手动测试选择
   ```

2. **增加并发数**
   ```toml
   threads = 5  # 根据带宽调整
   ```

3. **调整线程池**
   ```toml
   pool2_size = 10  # 支持更多并发上传
   ```

### 优化内存使用

1. **减小文件分段**
   ```toml
   file_size = 1073741824  # 1GB
   ```

2. **限制并发任务**
   ```toml
   pool1_size = 3
   pool2_size = 3
   ```

### 优化磁盘使用

1. **及时清理文件**
   ```toml
   [streamers."主播"]
   postprocessor = [
       {rm}  # 上传后删除
   ]
   ```

2. **设置过滤阈值**
   ```toml
   filtering_threshold = 50  # 过滤小于50MB的文件
   ```


## 平台特定配置

### Bilibili 配置

详细的 Bilibili 配置请参考[平台支持文档](../user-guide/platform-support.md)。

**基本配置：**
```toml
bili_protocol = "stream"  # 或 hls_ts, hls_fmp4
bili_qn = 10000  # 原画
bili_cdn = ["cn-gotcha208"]
```

### Twitch 配置

```toml
twitch_danmaku = false  # 录制弹幕
twitch_disable_ads = true  # 去除广告
```

### YouTube 配置

```toml
youtube_prefer_vcodec = "av01|vp9|avc"
youtube_prefer_acodec = "opus|mp4a"
youtube_max_resolution = "1080"
youtube_enable_download_live = true
youtube_enable_download_playback = true
```

### 斗鱼配置

```toml
douyu_cdn = "tct-h5"
douyu_danmaku = false
douyu_rate = 0  # 原画
```

### 虎牙配置

```toml
huya_cdn = "AL"
huya_danmaku = false
huya_max_ratio = 10000  # 蓝光10M
```

### 抖音配置

```toml
douyin_danmaku = false
douyin_quality = "origin"  # 原画
```

## 完整高级配置示例

```toml
# 代理配置
[proxy]
http = "http://127.0.0.1:7890"
https = "http://127.0.0.1:7890"

# 任务调度
delay = 300
event_loop_interval = 30
checker_sleep = 10
check_sourcecode = 15

# 线程池
pool1_size = 10
pool2_size = 10

# 录制配置
downloader = "streamlink"
file_size = 1073741824  # 1GB
filtering_threshold = 20
filename_prefix = "{streamer}%Y-%m-%d %H_%M_%S{title}"
segment_processor_parallel = false

# 上传配置
uploader = "biliup-rs"
lines = "AUTO"
threads = 5

# 平台配置
bili_protocol = "hls_fmp4"
bili_qn = 10000
bili_cdn = ["cn-gotcha208"]
use_live_cover = true

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
backupCount = 7
filename = "biliup.log"
formatter = "verbose"
encoding = "utf-8"

[LOGGING.root]
handlers = ["console"]
level = "INFO"

[LOGGING.loggers.biliup]
handlers = ["file"]
level = "DEBUG"

# 主播配置
[streamers."主播"]
url = ["https://www.twitch.tv/username"]
tags = ["游戏", "直播"]
tid = 171

[streamers."主播".override]
downloader = "ffmpeg"
bili_qn = 10000
```

## 环境变量

部分配置可通过环境变量设置：

```bash
# 日志级别
export RUST_LOG=debug

# 代理
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 配置文件路径
export BILIUP_CONFIG=/path/to/config.toml

# 启动
biliup start
```

## 调试技巧

### 启用详细日志

```toml
[LOGGING.root]
level = "DEBUG"

[LOGGING.loggers.biliup]
level = "DEBUG"
```

### 查看实时日志

```bash
tail -f biliup.log
```

### 测试配置

```bash
# 验证配置文件
biliup --config config.toml start --dry-run

# 查看配置
biliup --config config.toml config show
```

### 性能监控

```bash
# 监控进程
top -p $(pgrep -f biliup)

# 监控磁盘
df -h

# 监控网络
iftop
```

## 常见问题

### 代理不生效

**问题**：设置代理后仍无法访问

**解决方案：**
1. 确认代理服务正常运行
2. 检查代理地址和端口
3. 尝试使用环境变量设置
4. 查看日志确认代理是否被使用

### 日志文件过大

**问题**：日志文件占用大量磁盘空间

**解决方案：**
1. 调整日志级别为 INFO 或 WARNING
   ```toml
   [LOGGING.root]
   level = "INFO"
   ```

2. 减少备份数量
   ```toml
   [LOGGING.handlers.file]
   backupCount = 3
   ```

3. 缩短轮换周期
   ```toml
   [LOGGING.handlers.file]
   when = "D"  # 每天轮换
   ```

### 性能问题

**问题**：CPU 或内存占用过高

**解决方案：**
1. 减少并发任务
   ```toml
   pool1_size = 3
   pool2_size = 3
   ```

2. 减小文件分段
   ```toml
   file_size = 1073741824  # 1GB
   ```

3. 关闭不必要的功能
   ```toml
   check_sourcecode = 0  # 禁用自动重启
   ```

4. 优化下载器选择
   ```toml
   downloader = "stream-gears"  # 使用默认下载器
   ```

### 自动重启失效

**问题**：修改配置后未自动重启

**解决方案：**
1. 确认 `check_sourcecode` 不为 0
   ```toml
   check_sourcecode = 15
   ```

2. 手动重启服务
   ```bash
   biliup restart
   ```

3. 检查日志查看错误信息

## 相关链接

- [配置文件格式](./config-file-format.md)
- [主播配置详解](./streamer-config.md)
- [上传配置详解](./upload-config.md)
- [认证配置](./authentication.md)
- [平台支持](../user-guide/platform-support.md)
- [配置示例集](./examples.md)
