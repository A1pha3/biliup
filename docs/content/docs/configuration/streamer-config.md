+++
title = "主播配置"
description = "详细了解如何配置主播录制参数、上传设置和自定义选项"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 20
template = "docs/page.html"

[extra]
lead = "主播配置是 biliup 的核心部分，本文档详细说明 streamers 配置段的所有选项，包括 URL、标签、分区、文件命名等。"
toc = true
top = false
+++

## 概述

主播配置用于指定要录制的直播间和上传参数。每个主播可以有独立的配置，支持多个直播间 URL、自定义标题模板、分区设置等。

## 基本配置

### 最小配置

最简单的主播配置只需要指定直播间 URL：

**TOML 格式：**
```toml
[streamers."主播名称"]
url = ["https://www.twitch.tv/username"]
```

**YAML 格式：**
```yaml
streamers:
  主播名称:
    url:
      - https://www.twitch.tv/username
```

### 完整配置示例

**TOML 格式：**
```toml
[streamers."主播名称"]
url = ["https://www.twitch.tv/username"]
title = "{title}%Y-%m-%d{streamer}"
tid = 171
tags = ["游戏", "娱乐"]
description = "视频简介"
dynamic = "#直播录像#"
user_cookie = "cookies.json"
```

**YAML 格式：**
```yaml
streamers:
  主播名称:
    url:
      - https://www.twitch.tv/username
    title: "{title}%Y-%m-%d{streamer}"
    tid: 171
    tags:
      - 游戏
      - 娱乐
    description: 视频简介
    dynamic: "#直播录像#"
    user_cookie: cookies.json
```

## 配置项详解

### url（必需）

指定要录制的直播间 URL，支持多个平台。

**类型**：字符串数组  
**必需**：是  
**默认值**：无

**示例：**
```toml
# 单个 URL
url = ["https://www.twitch.tv/username"]

# 多个 URL（只会同时录制一个）
url = [
    "https://www.twitch.tv/username",
    "https://www.youtube.com/@channel/live"
]
```

**说明：**
- 填写多个 URL 时，只能同时录制一个直播间
- 如需同时录制多个直播间，请为每个直播间单独配置
- 支持的平台包括：Bilibili、Twitch、YouTube、斗鱼、虎牙、抖音等

### title

自定义投稿标题模板，支持占位符和时间格式化。

**类型**：字符串  
**必需**：否  
**默认值**：`{title}`

**占位符：**
- `{title}`：直播间标题
- `{streamer}`：配置中的主播名称
- `{url}`：直播间 URL（第一个）
- 时间格式：支持 strftime 格式，如 `%Y-%m-%d`、`%H:%M:%S`

**示例：**
```toml
# 基本模板
title = "{title}"

# 包含日期和主播名
title = "{title}%Y-%m-%d{streamer}"

# 完整模板
title = "{title}第一视角%Y-%m-%d %H:%M{streamer}{url}"
```

**常用时间格式：**
- `%Y`：四位年份（2025）
- `%m`：月份（01-12）
- `%d`：日期（01-31）
- `%H`：小时（00-23）
- `%M`：分钟（00-59）
- `%S`：秒（00-59）

### tid

B 站投稿分区 ID。

**类型**：整数  
**必需**：否  
**默认值**：无（需要手动选择）

**常用分区 ID：**
- `171`：电子竞技
- `172`：网络游戏
- `65`：网络游戏（旧）
- `136`：搞笑
- `138`：搞笑（旧）
- `21`：日常
- `76`：美食圈
- `160`：生活
- `138`：搞笑
- `27`：综合

**示例：**
```toml
tid = 171  # 电子竞技分区
```

**说明：**
- 完整分区列表请参考 [B 站分区对照表](https://github.com/ForgQi/biliup/wiki/Bilibili-分区对照表)
- 选择正确的分区有助于视频获得更好的推荐


### tags

视频标签，用于分类和搜索。

**类型**：字符串数组  
**必需**：否  
**默认值**：空数组

**示例：**
```toml
tags = ["biliup", "直播录像", "游戏"]
```

```yaml
tags:
  - biliup
  - 直播录像
  - 游戏
```

**说明：**
- 最多可以添加 12 个标签
- 每个标签最长 20 个字符
- 标签有助于视频被搜索和推荐

### description

视频简介，支持占位符和多行文本。

**类型**：字符串  
**必需**：否  
**默认值**：空

**占位符：**
- `{title}`：直播间标题
- `{streamer}`：主播名称
- `{url}`：直播间 URL
- 时间格式：支持 strftime 格式

**TOML 示例：**
```toml
description = """
视频简介: {title} %Y-%m-%d %H:%M:%S
{streamer}主播直播间地址：{url}
---
Powered By biliup - Github: https://github.com/ForgQi/biliup"""
```

**YAML 示例：**
```yaml
description: |-
  视频简介: {title} %Y-%m-%d %H:%M:%S
  {streamer}主播直播间地址：{url}
  ---
  Powered By biliup - Github: https://github.com/ForgQi/biliup
```

**@其他用户：**

如需在简介中 @ 其他用户，使用 `credits` 配置：

```toml
credits = [
  { username = "用户名", uid = 123456 }
]
description = """
视频简介
【@credit】
"""
```

```yaml
credits:
  - username: 用户名
    uid: 123456
description: |-
  视频简介
  【@credit】
```

### dynamic

投稿时的动态文本。

**类型**：字符串  
**必需**：否  
**默认值**：空

**示例：**
```toml
dynamic = "#直播录像# #游戏#"
```

**说明：**
- 动态会显示在你的个人动态中
- 可以使用话题标签增加曝光

### copyright

版权声明。

**类型**：整数  
**必需**：否  
**默认值**：2（转载）

**可选值：**
- `1`：自制
- `2`：转载

**示例：**
```toml
copyright = 2  # 转载
```

### cover_path

自定义封面图片路径。

**类型**：字符串  
**必需**：否  
**默认值**：无

**示例：**
```toml
cover_path = "/path/to/cover.jpg"
```

**说明：**
- 支持 JPG、PNG 格式
- 推荐尺寸：1920x1080 或 16:9 比例
- 优先级高于 `use_live_cover`

### use_live_cover

使用直播间封面作为投稿封面。

**类型**：布尔值  
**必需**：否  
**默认值**：false

**示例：**
```toml
use_live_cover = true
```

**说明：**
- 目前支持 Bilibili、Twitch、YouTube
- 封面保存在 `cover/` 目录，上传后自动删除
- 优先级低于 `cover_path`

### user_cookie

指定用于上传的账号 Cookie 文件。

**类型**：字符串  
**必需**：否  
**默认值**：使用全局配置

**示例：**
```toml
user_cookie = "cookies.json"
```

**说明：**
- 用于多账号上传
- Cookie 文件格式参见[认证配置](./authentication.md)

### uploader

覆盖全局上传插件设置。

**类型**：字符串  
**必需**：否  
**默认值**：使用全局配置

**可选值：**
- `biliup-rs`：使用 Rust 上传器（推荐）
- `bili_web`：使用网页接口上传
- `Noop`：不上传，但执行后处理

**示例：**
```toml
uploader = "biliup-rs"
```

### filename_prefix

自定义录播文件命名规则。

**类型**：字符串  
**必需**：否  
**默认值**：使用全局配置

**占位符：**
- `{streamer}`：主播名称
- `{title}`：直播间标题
- 时间格式：支持 strftime 格式

**示例：**
```toml
filename_prefix = "{streamer}%Y-%m-%d %H_%M_%S{title}"
```

**说明：**
- 文件名必须包含时间，避免分段文件互相覆盖
- 如果上传文件，文件名必须符合此模板


### format

视频保存格式。

**类型**：字符串  
**必需**：否  
**默认值**：FLV（取决于平台）

**可选值：**
- `mp4`：MP4 格式
- `flv`：FLV 格式
- `mkv`：MKV 格式

**示例：**
```toml
format = "mp4"
```

**说明：**
- 使用 MP4 格式必须切换 downloader 为 `ffmpeg` 或 `streamlink`
- YouTube 不支持 MP4 格式
- B 站支持 MP4、MKV、WEBM 格式

### dtime

延时发布时间（时间戳）。

**类型**：整数  
**必需**：否  
**默认值**：立即发布

**示例：**
```toml
dtime = 14400  # 4小时后发布
```

**说明：**
- 格式为 Unix 时间戳（秒）
- 必须距离提交时间大于 2 小时
- 可用于定时发布视频

### dolby

是否开启杜比音效。

**类型**：整数  
**必需**：否  
**默认值**：0（关闭）

**可选值：**
- `0`：关闭
- `1`：开启

**示例：**
```toml
dolby = 1
```

### hires

是否开启 Hi-Res 高解析度音频。

**类型**：整数  
**必需**：否  
**默认值**：0（关闭）

**可选值：**
- `0`：关闭
- `1`：开启

**示例：**
```toml
hires = 1
```

### no_reprint

自制声明（未经允许禁止转载）。

**类型**：整数  
**必需**：否  
**默认值**：0（允许转载）

**可选值：**
- `0`：允许转载
- `1`：未经允许禁止转载

**示例：**
```toml
no_reprint = 1
```

### charging_pay

是否开启充电面板。

**类型**：整数  
**必需**：否  
**默认值**：0（关闭）

**可选值：**
- `0`：关闭
- `1`：开启

**示例：**
```toml
charging_pay = 1
```

### is_only_self

视频可见范围。

**类型**：整数  
**必需**：否  
**默认值**：0（公开）

**可选值：**
- `0`：公开
- `1`：仅自己可见

**示例：**
```toml
is_only_self = 1
```

### time_range

录制时间范围，仅在此时间段内录制。

**类型**：字符串（ISO 8601 格式的时间数组）  
**必需**：否  
**默认值**：无限制

**示例：**
```toml
time_range = "[\"2025-03-26T16:00:00.000Z\",\"2025-03-27T15:59:59.000Z\"]"
```

**说明：**
- 使用 ISO 8601 格式
- 可用于只录制特定时间段的直播

### excluded_keywords

排除关键词，如果房间名包含关键词则不录制。

**类型**：字符串数组  
**必需**：否  
**默认值**：空

**TOML 示例：**
```toml
excluded_keywords = ["测试", "休息"]
```

**YAML 示例：**
```yaml
excluded_keywords:
  - 测试
  - 休息
```

**说明：**
- 用于过滤不想录制的直播
- 匹配房间标题中的关键词

### opt_args

FFmpeg 自定义参数。

**类型**：字符串数组  
**必需**：否  
**默认值**：空

**示例：**
```toml
opt_args = ["-ss", "00:00:16"]  # 跳过开始的16秒
```

```yaml
opt_args:
  - '-ss'
  - '00:00:16'
```

## 分段录制配置

### split_time

按时间分段录制。

**类型**：字符串  
**必需**：否  
**默认值**：无（使用全局 segment_time）

**格式**：`HH:MM:SS`

**示例：**
```toml
split_time = "01:00:00"  # 每小时分段
```

**说明：**
- 超过此时间自动分段
- 下载回放时无法使用
- 与 `split_size` 互斥，优先使用 `split_time`

### split_size

按文件大小分段录制。

**类型**：整数  
**必需**：否  
**默认值**：2621440000（2.5GB）

**单位**：字节（Byte）

**示例：**
```toml
split_size = 1073741824  # 1GB
```

**说明：**
- 超过此大小自动分段
- 下载回放时无法使用

## 事件钩子配置

biliup 支持在不同阶段执行自定义操作。

### preprocessor

开始下载直播时触发。

**类型**：对象数组  
**必需**：否  
**默认值**：空

**示例：**
```toml
preprocessor = [
    {run = "sh ./notify.sh"}
]
```

```yaml
preprocessor:
  - run: sh ./notify.sh
```

**输出数据（JSON 格式）：**
- `name`：主播名称
- `url`：直播间地址
- `start_time`：开播时间（时间戳）

### segment_processor

视频分段时触发。

**类型**：对象数组  
**必需**：否  
**默认值**：空

**示例：**
```toml
segment_processor = [
    {run = "sh ./process_segment.sh"}
]
```

**说明：**
- 返回当前生成的文件路径
- 可用于实时处理分段文件


### downloaded_processor

准备上传直播时触发。

**类型**：对象数组  
**必需**：否  
**默认值**：空

**示例：**
```toml
downloaded_processor = [
    {run = "sh ./pre_upload.sh"}
]
```

```yaml
downloaded_processor:
  - run: sh ./pre_upload.sh
```

**输出数据（JSON 格式）：**
- `name`：主播名称
- `url`：直播间地址
- `room_title`：直播间标题（重启后会丢失，默认为配置名称）
- `start_time`：开播时间（时间戳，重启后会丢失）
- `end_time`：下播时间（时间戳，重启后会丢失）
- `file_list`：视频文件列表

**说明：**
- 如果对视频进行修改，需保证文件名符合 `filename_prefix` 规则
- 上传顺序按文件创建时间排序

### postprocessor

上传完成后触发。

**类型**：对象数组  
**必需**：否  
**默认值**：`[{rm}]`（删除文件）

**可用操作：**
- `run`：执行命令
- `mv`：移动文件
- `rm`：删除文件

**示例：**
```toml
postprocessor = [
    {run = "echo 上传完成!"},
    {mv = "backup/"},
    {run = "python3 path/to/mail.py"},
    {run = "sh ./upload_to_cloud.sh"}
]
```

```yaml
postprocessor:
  - run: echo 上传完成!
  - mv: backup/
  - run: python3 path/to/mail.py
  - run: sh ./upload_to_cloud.sh
```

**说明：**
- 当 `postprocessor` 不存在时，默认执行删除文件操作
- 视频文件路径作为标准输入传入
- 可用于发送通知、备份文件、上传网盘等

**常用脚本示例：**
- [发送邮件通知](https://biliup.github.io/biliup/Guide.html#上传完成后发送邮件通知)
- [自动上传网盘](https://gist.github.com/UVJkiNTQ/ae4282e8f9fe4e45b3144b57605b4178)

## 覆盖全局配置

使用 `override` 段可以为单个主播覆盖全局配置。

**TOML 示例：**
```toml
[streamers."主播名称"]
url = ["https://example.com"]

[streamers."主播名称".override]
downloader = "ffmpeg"
bili_qn = 10000
lines = "bda2"
```

**YAML 示例：**
```yaml
streamers:
  主播名称:
    url:
      - https://example.com
    override:
      downloader: ffmpeg
      bili_qn: 10000
      lines: bda2
```

**可覆盖的配置项：**
- `downloader`：下载器
- `bili_qn`：B 站画质
- `bili_protocol`：B 站协议
- `bili_cdn`：B 站 CDN
- `lines`：上传线路
- `threads`：并发数
- 其他全局配置项

## 多主播配置示例

### 示例 1：录制多个主播

**TOML：**
```toml
[streamers."主播A"]
url = ["https://www.twitch.tv/streamerA"]
tags = ["游戏", "FPS"]
tid = 171

[streamers."主播B"]
url = ["https://www.youtube.com/@streamerB/live"]
tags = ["音乐", "唱见"]
tid = 130

[streamers."主播C"]
url = ["https://live.bilibili.com/123456"]
tags = ["绘画", "创作"]
tid = 163
```

**YAML：**
```yaml
streamers:
  主播A:
    url:
      - https://www.twitch.tv/streamerA
    tags:
      - 游戏
      - FPS
    tid: 171
  
  主播B:
    url:
      - https://www.youtube.com/@streamerB/live
    tags:
      - 音乐
      - 唱见
    tid: 130
  
  主播C:
    url:
      - https://live.bilibili.com/123456
    tags:
      - 绘画
      - 创作
    tid: 163
```

### 示例 2：完整配置

```toml
[streamers."星际2INnoVation"]
url = ["https://www.twitch.tv/innovation_s2"]
title = "{title}第一视角%Y-%m-%d{streamer}"
tid = 171
copyright = 2
description = """
视频简介: {title} %Y-%m-%d %H:%M:%S
{streamer}主播直播间地址：{url}
---
Powered By biliup"""
dynamic = "#星际争霸2# #电子竞技#"
tags = ["星际争霸2", "INnoVation", "电子竞技"]
user_cookie = "cookies.json"
use_live_cover = true
filename_prefix = "{streamer}%Y-%m-%d %H_%M_%S{title}"

postprocessor = [
    {mv = "backup/"},
    {run = "python3 notify.py"}
]

[streamers."星际2INnoVation".override]
downloader = "ffmpeg"
bili_qn = 10000
```

### 示例 3：仅录制不上传

```toml
[streamers."测试主播"]
url = ["https://www.twitch.tv/test"]
uploader = "Noop"  # 不上传

postprocessor = [
    {mv = "recordings/"}  # 仅保存到本地
]
```

### 示例 4：多账号上传

```toml
[streamers."账号1的主播"]
url = ["https://example.com/1"]
user_cookie = "account1.json"

[streamers."账号2的主播"]
url = ["https://example.com/2"]
user_cookie = "account2.json"
```

## 常见场景配置

### 高画质录制

```toml
[streamers."高画质主播"]
url = ["https://live.bilibili.com/123456"]

[streamers."高画质主播".override]
bili_qn = 10000  # 原画
bili_protocol = "hls_fmp4"  # fmp4流
downloader = "streamlink"
```

### 分段录制

```toml
[streamers."长时间直播"]
url = ["https://example.com"]
split_time = "01:00:00"  # 每小时分段
```

### 自定义文件名

```toml
[streamers."主播"]
url = ["https://example.com"]
filename_prefix = "[{streamer}]%Y%m%d_%H%M%S_{title}"
```

### 延时发布

```toml
[streamers."主播"]
url = ["https://example.com"]
dtime = 1710000000  # Unix时间戳
```

## 相关链接

- [配置文件格式](./config-file-format.md)
- [上传配置详解](./upload-config.md)
- [高级配置选项](./advanced-config.md)
- [认证配置](./authentication.md)
- [配置示例集](./examples.md)
