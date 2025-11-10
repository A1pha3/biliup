+++
title = "视频上传功能"
description = "掌握 biliup 的视频上传功能，自动或手动上传录制的视频到 B 站"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "biliup 提供强大的视频上传功能，支持自动上传、批量上传、多 P 视频等多种上传方式。"
toc = true
top = false
+++

## B 站登录

上传视频前需要先登录 B 站账号。

### 命令行登录

#### 方式一：扫码登录（推荐）

```bash
biliup login
```

选择扫码登录，使用 B 站 APP 扫描二维码即可完成登录。

#### 方式二：账号密码登录

```bash
biliup login
```

选择账号密码登录，输入手机号/邮箱和密码。

#### 方式三：使用已有 Cookie

如果你已经有 B 站的 Cookie 文件：

```bash
biliup login
```

选择使用已有 cookies，将 cookies 文件放在指定位置。

### Cookie 文件位置

登录信息默认保存在：

```
cookies.json
```

你可以通过参数指定其他位置：

```bash
biliup --user-cookie /path/to/cookies.json server
```

### 验证登录状态

```bash
biliup renew
```

这个命令会验证并刷新登录信息。

### Cookie 过期处理

Cookie 通常有效期为 30 天。过期后需要重新登录：

```bash
biliup login
```

建议定期运行 `biliup renew` 刷新登录状态。

## 基本上传配置

### 自动上传

录制完成后自动上传到 B 站：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    auto_upload: true
    upload_config:
      title: "{streamer}的直播录像 {date}"
      tid: 171  # 分区 ID
      tags: ["直播录像", "游戏"]
```

### 手动上传

使用命令行手动上传视频：

```bash
biliup upload video.mp4 --title "视频标题" --tid 171 --tag "标签1,标签2"
```

### 通过 WebUI 上传

1. 打开 WebUI 界面
2. 进入"投稿管理"页面
3. 点击"上传视频"按钮
4. 选择视频文件
5. 填写视频信息
6. 点击"开始上传"

## 上传配置详解

### 视频标题

```yaml
upload_config:
  title: "{streamer}的直播录像 {date}"
```

**可用变量**：
- `{streamer}` - 主播名称
- `{title}` - 直播标题
- `{date}` - 日期（YYYY-MM-DD）
- `{time}` - 时间（HH:MM:SS）

**示例**：

```yaml
# 示例 1：简单标题
title: "{streamer}直播录像"
# 结果：主播名称直播录像

# 示例 2：包含日期
title: "{streamer} {date} 直播录像"
# 结果：主播名称 2025-01-10 直播录像

# 示例 3：包含原标题
title: "【{streamer}】{title}"
# 结果：【主播名称】原直播标题
```

### 视频简介

```yaml
upload_config:
  desc: |
    这是一段直播录像
    主播：{streamer}
    录制时间：{date}
```

支持多行文本和变量替换。

### 分区选择

B 站要求每个视频必须选择一个分区。常用分区 ID：

```yaml
upload_config:
  tid: 171  # 分区 ID
```

**常用分区列表**：

| 分区 ID | 分区名称 | 说明 |
|---------|----------|------|
| 17 | 单机游戏 | 单机游戏内容 |
| 171 | 电子竞技 | 电竞比赛、职业选手 |
| 172 | 手机游戏 | 手游内容 |
| 65 | 网络游戏 | 网游内容 |
| 136 | 音乐综合 | 音乐相关 |
| 21 | 日常 | 生活日常 |
| 76 | 美食圈 | 美食制作 |
| 138 | 搞笑 | 搞笑内容 |
| 122 | 野生技术协会 | 技术教程 |
| 124 | 社科·法律·心理 | 知识科普 |

完整分区列表请查看 [B 站分区 Wiki](https://github.com/ForgQi/biliup/wiki)。

### 标签设置

```yaml
upload_config:
  tags: ["直播录像", "游戏", "主播名"]
```

**标签规则**：
- 最多 12 个标签
- 每个标签最长 20 字符
- 用逗号分隔
- 建议 5-8 个标签

**标签建议**：
- 包含主播名称
- 包含游戏/内容类型
- 包含"直播录像"等说明性标签
- 使用热门标签提高曝光

### 版权声明

```yaml
upload_config:
  copyright: 2  # 1=自制, 2=转载
```

- **1 - 自制**：原创内容
- **2 - 转载**：转载内容（直播录像通常选择此项）

如果选择转载，建议添加转载来源：

```yaml
upload_config:
  copyright: 2
  source: "https://www.twitch.tv/username"  # 原视频地址
```


### 封面设置

```yaml
upload_config:
  cover_path: "/path/to/cover.jpg"
```

**封面要求**：
- 格式：JPG、PNG
- 尺寸：建议 1920x1080 或 16:9 比例
- 大小：不超过 5MB

**自动封面**：

如果不指定封面，B 站会自动从视频中截取封面。

### 定时发布

```yaml
upload_config:
  dtime: "2025-01-10 20:00:00"  # 定时发布时间
```

视频会在指定时间自动发布。

**注意事项**：
- 时间格式：`YYYY-MM-DD HH:MM:SS`
- 必须是未来时间
- 最多可设置 15 天后

## 上传线路选择

biliup 支持多种上传线路，不同线路速度可能不同。

### 线路配置

```bash
# 命令行指定线路
biliup upload video.mp4 --line upos

# 或
biliup upload video.mp4 --line bupfetch
```

配置文件中指定：

```yaml
upload_config:
  line: "upos"  # 可选: upos, bupfetch, ws
```

### 线路说明

**upos（推荐）**：
- B 站官方上传线路
- 稳定性好
- 速度较快
- 适合大多数情况

**bupfetch**：
- 备用上传线路
- 某些地区可能更快
- 可作为 upos 失败时的备选

**ws**：
- WebSocket 上传
- 适合特殊网络环境

### 自动选择最快线路

```yaml
upload_config:
  line: "auto"  # 自动测速选择最快线路
```

### 线路选择建议

1. 首选 `upos`（默认）
2. 如果 upos 慢，尝试 `bupfetch`
3. 可以使用 `auto` 自动选择
4. 不同时间段线路速度可能不同

## 并发上传

### 单文件并发

控制单个视频文件的上传并发数：

```bash
biliup upload video.mp4 --limit 3
```

或在配置中：

```yaml
upload_config:
  limit: 3  # 单文件最大并发数
```

**并发数建议**：
- 家庭宽带：3-5
- 企业宽带：5-10
- 服务器：10-20

### 多文件并发

同时上传多个视频：

```yaml
global:
  max_concurrent_uploads: 2  # 最多同时上传 2 个视频
```

**注意事项**：
- 并发数过高可能导致上传失败
- 根据带宽合理设置
- 建议先测试单文件上传速度

## 多 P 上传

将多个视频文件作为一个稿件的多个分 P 上传。

### 命令行多 P 上传

```bash
biliup upload video1.mp4 video2.mp4 video3.mp4 \
  --title "合集标题" \
  --tid 171
```

### 配置文件多 P 上传

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    multi_part: true  # 启用多 P 上传
    upload_config:
      title: "{streamer}直播合集"
```

启用后，同一场直播的所有分段会作为多个分 P 上传到同一个稿件。

### 多 P 命名

每个分 P 可以有独立的标题：

```yaml
upload_config:
  part_title: "P{index} {time}"
```

**可用变量**：
- `{index}` - 分 P 序号
- `{time}` - 录制时间
- `{duration}` - 视频时长

## 追加视频

向已发布的稿件追加新的分 P。

### 命令行追加

```bash
biliup append --vid BV1xx411c7mD video.mp4
```

或使用 AV 号：

```bash
biliup append --vid av123456 video.mp4
```

### 配置文件追加

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    append_mode: true
    append_vid: "BV1xx411c7mD"  # 要追加到的稿件
```

### 追加场景

**适用场景**：
- 连载直播录像
- 系列视频
- 持续更新的内容

**注意事项**：
- 只能追加到自己的稿件
- 稿件必须已发布
- 追加的视频会成为新的分 P

## 上传失败重试

### 自动重试

```yaml
upload_config:
  retry_times: 3        # 失败后重试 3 次
  retry_interval: 300   # 重试间隔 300 秒（5 分钟）
```

### 手动重试

在 WebUI 的"投稿管理"页面，点击失败任务的"重试"按钮。

### 常见失败原因

1. **网络问题**：检查网络连接
2. **Cookie 过期**：重新登录
3. **视频格式问题**：转换为 MP4 格式
4. **文件损坏**：检查视频文件完整性
5. **B 站限制**：等待一段时间后重试

## 上传场景示例

### 场景 1：自动上传录像

录制完成后自动上传，无需人工干预：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
    auto_upload: true
    upload_config:
      title: "{streamer} {date} 直播录像"
      desc: "直播录像，仅供学习交流"
      tid: 171
      tags: ["直播录像", "游戏", "{streamer}"]
      copyright: 2
      source: "{url}"
```

### 场景 2：多 P 合集上传

将一场直播的所有分段作为多 P 上传：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
    segment_time: "30m"  # 每 30 分钟一段
    multi_part: true
    upload_config:
      title: "{streamer} {date} 直播录像"
      part_title: "Part {index}"
      tid: 171
      tags: ["直播录像"]
```

### 场景 3：定时发布

录制后定时发布，避开高峰期：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    auto_upload: true
    upload_config:
      title: "{streamer}直播录像"
      tid: 171
      dtime: "2025-01-11 08:00:00"  # 次日早上 8 点发布
```

### 场景 4：追加到系列稿件

持续追加到同一个稿件：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    append_mode: true
    append_vid: "BV1xx411c7mD"
    upload_config:
      part_title: "{date} 直播录像"
```

### 场景 5：边录边传

录制的同时上传，节省空间：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    upload_while_recording: true
    delete_after_upload: true
    upload_config:
      title: "{streamer}直播录像"
      tid: 171
      line: "upos"
      limit: 5
```


## 批量上传

### 上传目录中的所有视频

```bash
biliup upload /path/to/videos/*.mp4 --title "批量上传" --tid 171
```

### 使用配置文件批量上传

```yaml
batch_upload:
  enabled: true
  directory: "/path/to/videos"
  pattern: "*.mp4"  # 文件匹配模式
  upload_config:
    title: "{filename}"
    tid: 171
    tags: ["批量上传"]
```

### 批量上传策略

**按顺序上传**：

```yaml
batch_upload:
  mode: "sequential"  # 顺序上传
  interval: 600       # 每个视频间隔 10 分钟
```

**并发上传**：

```yaml
batch_upload:
  mode: "concurrent"  # 并发上传
  max_concurrent: 2   # 最多同时上传 2 个
```

## 上传进度监控

### 命令行查看进度

上传时会实时显示进度：

```
上传中: video.mp4
进度: 45.2% (1.2GB / 2.6GB)
速度: 5.3 MB/s
剩余时间: 约 4 分钟
```

### WebUI 查看进度

在"投稿管理"页面可以看到：

- 上传进度百分比
- 已上传大小 / 总大小
- 实时上传速度
- 预计剩余时间
- 上传状态（排队、上传中、处理中、完成）

### 上传日志

查看详细上传日志：

```bash
# 查看实时日志
tail -f biliup.log

# 查看上传相关日志
grep "upload" biliup.log
```

## 上传后处理

### 自动删除本地文件

上传成功后自动删除本地文件：

```yaml
upload_config:
  delete_after_upload: true
```

⚠️ **警告**：启用此选项前请确保上传成功，删除后无法恢复。

### 移动到归档目录

上传成功后移动文件而不是删除：

```yaml
upload_config:
  move_after_upload: true
  archive_dir: "/path/to/archive"
```

### 上传成功通知

配置上传成功后的通知：

```yaml
notification:
  enabled: true
  on_upload_success: true
  webhook: "https://your-webhook-url"
```

## 视频处理

### 视频转码

某些格式需要转码后才能上传：

```yaml
upload_config:
  transcode: true
  transcode_format: "mp4"
  transcode_codec: "h264"
```

### 视频压缩

压缩视频以加快上传速度：

```yaml
upload_config:
  compress: true
  compress_quality: "medium"  # low, medium, high
```

**注意**：压缩会降低视频质量，建议仅在必要时使用。

### 视频剪辑

自动剪辑视频（去除开头结尾）：

```yaml
upload_config:
  trim_start: 10   # 去除开头 10 秒
  trim_end: 5      # 去除结尾 5 秒
```

## 常见问题

### 上传速度很慢？

**可能原因**：
- 网络带宽限制
- 上传线路不佳
- 并发数设置不当

**解决方案**：

1. 测试上传带宽：
```bash
# 上传小文件测试速度
biliup upload test.mp4 --line upos
```

2. 尝试不同线路：
```bash
biliup upload video.mp4 --line bupfetch
```

3. 调整并发数：
```bash
biliup upload video.mp4 --limit 5
```

### 上传失败：Cookie 过期？

**解决方案**：

```bash
# 重新登录
biliup login

# 验证登录状态
biliup renew
```

### 上传失败：视频格式不支持？

**支持的格式**：
- MP4（推荐）
- FLV
- AVI
- MOV
- WMV

**解决方案**：

转换为 MP4 格式：

```bash
ffmpeg -i input.flv -c copy output.mp4
```

或启用自动转码：

```yaml
upload_config:
  transcode: true
  transcode_format: "mp4"
```

### 上传后视频审核不通过？

**常见原因**：
- 标题、标签违规
- 内容违规
- 版权问题
- 分区选择错误

**解决方案**：
1. 检查标题和标签是否合规
2. 确认内容符合 B 站规范
3. 转载内容标注来源
4. 选择正确的分区

### 多 P 上传顺序错乱？

**解决方案**：

确保文件名按顺序排列：

```bash
# 重命名文件
mv video1.mp4 01_video.mp4
mv video2.mp4 02_video.mp4
mv video3.mp4 03_video.mp4

# 上传
biliup upload 0*.mp4
```

### 上传后找不到视频？

**可能原因**：
- 视频在审核中
- 设置了定时发布
- 视频被设为私密

**解决方案**：
1. 登录 B 站查看投稿管理
2. 检查视频状态
3. 等待审核完成（通常几分钟到几小时）

## 性能优化

### 上传速度优化

1. **使用有线网络**：比 WiFi 更稳定快速
2. **选择合适的上传线路**：测试不同线路
3. **调整并发数**：根据带宽调整
4. **避开高峰期**：深夜上传通常更快
5. **使用服务器上传**：服务器带宽通常更好

### 资源占用优化

1. **限制并发上传数**：避免占用过多资源
2. **使用边录边传**：节省磁盘空间
3. **及时清理已上传文件**：释放存储空间

### 稳定性优化

1. **启用自动重试**：网络波动时自动重试
2. **使用稳定的网络**：避免频繁断线
3. **监控上传日志**：及时发现问题

## 最佳实践

### 标题规范

- 简洁明了，突出重点
- 包含关键信息（主播、日期、内容）
- 避免标题党和违规词汇
- 长度控制在 80 字符以内

### 标签策略

- 使用相关性高的标签
- 包含热门标签提高曝光
- 标签数量 5-8 个为宜
- 避免无关标签

### 简介编写

- 说明视频来源
- 添加时间戳（如果是长视频）
- 包含相关链接
- 感谢观看和关注提示

### 分区选择

- 选择最相关的分区
- 不确定时查看类似视频的分区
- 避免选择不相关的分区（可能被移除）

### 上传时间

- 避开高峰期（晚上 8-11 点）
- 深夜上传速度通常更快
- 使用定时发布在最佳时间发布

## 下一步

- [任务管理](./managing-tasks.md) - 了解如何管理上传任务
- [平台支持](./platform-support.md) - 查看支持的平台
- [故障排查](./troubleshooting.md) - 解决上传问题
- [高级配置](../configuration/advanced.md) - 深入配置选项
