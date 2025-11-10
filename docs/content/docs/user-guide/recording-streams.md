+++
title = "直播录制功能"
description = "深入了解 biliup 的直播录制功能，掌握各种录制配置和技巧"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 20
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "biliup 支持 20+ 个直播平台的录制，提供丰富的配置选项满足各种录制需求。"
toc = true
top = false
+++

## 支持的直播平台

biliup 支持以下主流直播平台：

### 国内平台

- **B 站直播** - `https://live.bilibili.com/房间号`
- **斗鱼** - `https://www.douyu.com/房间号`
- **虎牙** - `https://www.huya.com/房间号`
- **抖音** - `https://live.douyin.com/房间号`
- **快手** - `https://live.kuaishou.com/u/用户ID`
- **CC 直播** - `https://cc.163.com/房间号`
- **企鹅电竞** - `https://egame.qq.com/房间号`
- **YY 直播** - `https://www.yy.com/房间号`
- **花椒** - `https://www.huajiao.com/l/房间号`
- **一直播** - `https://www.yizhibo.com/l/房间号`

### 国际平台

- **Twitch** - `https://www.twitch.tv/username`
- **YouTube Live** - `https://www.youtube.com/watch?v=视频ID`
- **Afreeca TV** - `https://play.afreecatv.com/username`
- **Twitch** - `https://www.twitch.tv/username`
- **Niconico** - `https://live.nicovideo.jp/watch/lv房间号`

更多平台持续添加中，完整列表请查看[平台支持文档](./platform-support.md)。

## 基本录制配置

### 通过 WebUI 配置

1. 打开 WebUI 界面
2. 进入"直播管理"页面
3. 点击"新建"按钮
4. 填写基本信息：

**必填项**：
- **备注名称**：为录制任务设置一个易识别的名称
- **直播地址**：输入直播间 URL

**可选项**：
- **录制格式**：选择视频格式（flv、ts、mp4）
- **画质选择**：选择录制画质
- **自动上传**：是否录制完成后自动上传

### 通过配置文件配置

创建或编辑 `config.yaml` 文件：

```yaml
streamers:
  主播名称:
    url:
      - "https://www.twitch.tv/username"
    format: "flv"
    quality: "best"
```

## 录制格式选择

biliup 支持多种录制格式，各有优缺点：

### FLV 格式（推荐）

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
```

**优点**：
- 稳定性最好，不易损坏
- 文件体积较小
- 兼容性好，B 站原生支持
- 断流恢复能力强

**缺点**：
- 不支持某些高级编码

**适用场景**：
- 长时间录制
- 网络不稳定环境
- 需要高稳定性的场景

### TS 格式

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "ts"
```

**优点**：
- 支持更多编码格式
- 分段录制更灵活
- 容错性好

**缺点**：
- 文件体积较大
- 需要转封装才能上传

**适用场景**：
- 需要后期处理
- 对画质要求高
- 需要精确分段

### MP4 格式

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "mp4"
```

**优点**：
- 通用性最好
- 可直接播放
- 文件结构清晰

**缺点**：
- 录制中断容易损坏
- 不适合长时间录制

**适用场景**：
- 短时间录制
- 网络稳定环境
- 需要直接播放


## 画质选择

### 画质配置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    quality: "best"  # 可选: best, 1080p, 720p, 480p, worst
```

### 画质选项说明

- **best**：最高画质（默认推荐）
- **1080p**：1080P 画质
- **720p**：720P 画质
- **480p**：480P 画质
- **worst**：最低画质（节省带宽）

### 画质选择建议

**选择最高画质（best）**：
- 网络带宽充足
- 存储空间充足
- 追求最佳观看体验

**选择固定画质（如 720p）**：
- 网络带宽有限
- 需要控制文件大小
- 平衡质量和存储

**选择最低画质（worst）**：
- 仅需要音频或低质量存档
- 网络环境很差
- 存储空间极其有限

## 文件分段设置

长时间录制建议启用文件分段，避免单个文件过大。

### 按大小分段

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    segment_size: "2G"  # 每 2GB 分一个文件
```

支持的单位：
- `K` - KB（千字节）
- `M` - MB（兆字节）
- `G` - GB（吉字节）

示例：
- `500M` - 500 MB
- `1G` - 1 GB
- `2.5G` - 2.5 GB

### 按时间分段

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    segment_time: "1h"  # 每 1 小时分一个文件
```

支持的单位：
- `s` - 秒
- `m` - 分钟
- `h` - 小时

示例：
- `30m` - 30 分钟
- `1h` - 1 小时
- `2h30m` - 2 小时 30 分钟

### 分段建议

**按大小分段（推荐）**：
- 更可预测的文件大小
- 便于存储管理
- 适合大多数场景

**按时间分段**：
- 便于按时间查找
- 适合定时直播
- 方便制作精华集锦

**不分段**：
- 短时间录制（< 1 小时）
- 需要完整文件
- 后期处理需求

## 多主播同时录制

biliup 支持同时录制多个直播间。

### 配置多个主播

```yaml
streamers:
  主播A:
    url: ["https://www.twitch.tv/userA"]
    format: "flv"
    
  主播B:
    url: ["https://www.douyu.com/123456"]
    format: "flv"
    
  主播C:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
```

### 并发限制

默认情况下，biliup 会同时录制所有开播的主播。如果需要限制并发数：

```yaml
global:
  max_concurrent_downloads: 3  # 最多同时录制 3 个
```

### 资源分配建议

根据你的硬件配置合理设置并发数：

**低配置（2 核 4GB 内存）**：
- 并发数：1-2
- 画质：720p 或更低

**中等配置（4 核 8GB 内存）**：
- 并发数：3-5
- 画质：1080p

**高配置（8 核 16GB+ 内存）**：
- 并发数：10+
- 画质：best

## 录制文件命名

### 默认命名规则

默认文件名格式：

```
{streamer}_{title}_{date}_{time}.{ext}
```

示例：
```
主播名称_直播标题_2025-01-10_14-30-00.flv
```

### 自定义命名模板

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    filename_template: "{streamer}/{date}/{time}_{title}.{ext}"
```

**可用变量**：
- `{streamer}` - 主播名称
- `{title}` - 直播标题
- `{date}` - 日期（YYYY-MM-DD）
- `{time}` - 时间（HH-MM-SS）
- `{timestamp}` - Unix 时间戳
- `{ext}` - 文件扩展名

**命名示例**：

```yaml
# 按日期分类
filename_template: "{streamer}/{date}/{time}.{ext}"
# 结果: 主播名称/2025-01-10/14-30-00.flv

# 包含标题
filename_template: "{date}_{streamer}_{title}.{ext}"
# 结果: 2025-01-10_主播名称_直播标题.flv

# 简洁命名
filename_template: "{timestamp}.{ext}"
# 结果: 1704891000.flv
```

## 存储位置配置

### 默认存储位置

录制文件默认保存在：

```
downloads/主播名称/视频文件.flv
```

### 自定义存储路径

```yaml
global:
  download_dir: "/path/to/recordings"
```

或为每个主播单独设置：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    output_dir: "/path/to/custom/dir"
```

### 路径配置建议

**使用绝对路径**：
```yaml
download_dir: "/home/user/recordings"  # Linux/macOS
download_dir: "D:/recordings"          # Windows
```

**使用相对路径**：
```yaml
download_dir: "./recordings"  # 相对于运行目录
```

**按主播分类**：
```yaml
streamers:
  主播A:
    output_dir: "/recordings/主播A"
  主播B:
    output_dir: "/recordings/主播B"
```


## 边录边传功能

边录边传可以在录制的同时上传到 B 站，节省本地存储空间。

### 启用边录边传

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    upload_while_recording: true
```

### 工作原理

1. 开始录制直播
2. 录制到一定大小后（如 100MB）
3. 开始上传已录制部分
4. 继续录制并上传
5. 录制结束后完成上传
6. 可选择删除本地文件

### 配置选项

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    upload_while_recording: true
    upload_chunk_size: "100M"  # 每 100MB 上传一次
    delete_after_upload: true  # 上传后删除本地文件
```

### 使用建议

**适合场景**：
- 本地存储空间有限
- 网络上传带宽充足
- 不需要本地备份

**不适合场景**：
- 网络不稳定
- 需要本地备份
- 需要后期处理

### 注意事项

⚠️ **重要提示**：
- 确保上传带宽足够，否则可能影响录制
- 建议先测试小文件上传速度
- 上传失败时本地文件会保留
- 启用 `delete_after_upload` 前请确认上传成功

## 录制过滤器

使用过滤器可以控制何时录制。

### 时间过滤

只在特定时间段录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    time_filter:
      start: "20:00"  # 晚上 8 点开始
      end: "02:00"    # 凌晨 2 点结束
```

### 星期过滤

只在特定星期录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    weekday_filter: [1, 2, 3, 4, 5]  # 周一到周五
    # 0=周日, 1=周一, ..., 6=周六
```

### 标题过滤

根据直播标题决定是否录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    title_include: ["游戏", "实况"]  # 标题包含这些关键词才录制
    title_exclude: ["聊天", "闲聊"]  # 标题包含这些关键词不录制
```

### 组合过滤

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    time_filter:
      start: "18:00"
      end: "23:00"
    weekday_filter: [1, 2, 3, 4, 5]
    title_include: ["游戏"]
```

这个配置表示：只在工作日晚上 6 点到 11 点，且标题包含"游戏"时录制。

## 高级录制选项

### 代理设置

为特定主播配置代理：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    proxy: "http://127.0.0.1:7890"
```

或全局代理：

```yaml
global:
  proxy: "http://127.0.0.1:7890"
```

### Cookie 配置

某些平台需要登录才能录制高画质或会员专属直播：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    cookies: "cookie_file.txt"
```

Cookie 文件格式（Netscape 格式）：

```
# Netscape HTTP Cookie File
.twitch.tv	TRUE	/	FALSE	1735689600	auth-token	your_token_here
```

### 重试配置

录制失败时的重试策略：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    retry_times: 3        # 重试次数
    retry_interval: 60    # 重试间隔（秒）
```

### 超时设置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    timeout: 30           # 连接超时（秒）
    read_timeout: 60      # 读取超时（秒）
```

## 录制场景示例

### 场景 1：24/7 全天候录制

适合：重要主播，不想错过任何内容

```yaml
streamers:
  重要主播:
    url: ["直播间URL"]
    format: "flv"
    quality: "best"
    segment_size: "2G"
    upload_while_recording: false  # 保留本地备份
```

### 场景 2：节省空间的边录边传

适合：存储空间有限，网络良好

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
    quality: "720p"
    upload_while_recording: true
    delete_after_upload: true
    segment_size: "1G"
```

### 场景 3：多主播同时录制

适合：关注多个主播

```yaml
global:
  max_concurrent_downloads: 5
  download_dir: "/recordings"

streamers:
  主播A:
    url: ["https://www.twitch.tv/userA"]
    format: "flv"
    quality: "1080p"
    
  主播B:
    url: ["https://www.douyu.com/123456"]
    format: "flv"
    quality: "720p"
    
  主播C:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
    quality: "best"
```

### 场景 4：定时录制特定内容

适合：只关注特定时段或特定内容

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
    quality: "best"
    time_filter:
      start: "20:00"
      end: "23:00"
    weekday_filter: [1, 2, 3, 4, 5]  # 工作日
    title_include: ["游戏", "实况"]
```

### 场景 5：高质量存档

适合：需要最高质量，后期处理

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "ts"
    quality: "best"
    segment_time: "30m"
    upload_while_recording: false
    output_dir: "/archive/{streamer}/{date}"
```

## 常见问题

### 录制文件损坏怎么办？

**原因**：
- 网络中断
- 磁盘空间不足
- 使用了不稳定的格式（如 MP4）

**解决方案**：
1. 使用 FLV 格式（最稳定）
2. 启用文件分段
3. 检查网络稳定性
4. 确保磁盘空间充足

### 录制画质不是最高？

**原因**：
- 主播未开启高画质
- 平台限制
- 需要登录/会员

**解决方案**：
1. 检查主播是否开启高画质
2. 配置平台 Cookie
3. 使用 `quality: "best"` 配置

### 录制延迟很大？

**原因**：
- 平台本身延迟
- 网络延迟
- 使用了缓冲较大的格式

**解决方案**：
- 这是正常现象，直播本身有延迟
- 录制的是直播流，会有 10-30 秒延迟
- 无法完全消除，但不影响录制质量

### 多个主播同时开播，只录制了一个？

**原因**：
- 并发限制设置过低
- 系统资源不足

**解决方案**：
```yaml
global:
  max_concurrent_downloads: 10  # 增加并发数
```

### 录制文件名乱码？

**原因**：
- 直播标题包含特殊字符
- 文件系统不支持某些字符

**解决方案**：
```yaml
streamers:
  主播名称:
    filename_template: "{streamer}_{timestamp}.{ext}"  # 使用简单命名
```

## 性能优化建议

### 硬件要求

**最低配置**：
- CPU：2 核
- 内存：2GB
- 硬盘：100GB
- 网络：10Mbps 下载

**推荐配置**：
- CPU：4 核+
- 内存：8GB+
- 硬盘：500GB+ SSD
- 网络：50Mbps+ 下载

### 优化建议

1. **使用 SSD**：提高文件写入速度
2. **有线网络**：比 WiFi 更稳定
3. **关闭不必要的程序**：释放系统资源
4. **定期清理磁盘**：避免空间不足
5. **使用 FLV 格式**：最稳定的选择

## 下一步

- [视频上传功能](./uploading-videos.md) - 了解如何配置上传参数
- [任务管理](./managing-tasks.md) - 了解如何管理录制任务
- [弹幕录制](./danmaku-recording.md) - 了解如何录制弹幕
- [平台支持](./platform-support.md) - 查看所有支持的平台
- [故障排查](./troubleshooting.md) - 解决常见问题
