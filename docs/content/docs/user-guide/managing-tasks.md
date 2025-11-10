+++
title = "任务管理"
description = "学习如何管理 biliup 的录制和上传任务"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 40
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "掌握任务管理技巧，轻松控制录制和上传任务的启动、停止、监控等操作。"
toc = true
top = false
+++

## 任务概述

biliup 中的任务主要分为两类：

### 录制任务

- **监控任务**：持续监控直播间状态
- **录制任务**：实际录制直播流
- **后处理任务**：录制完成后的处理（如转码）

### 上传任务

- **上传任务**：将视频上传到 B 站
- **审核任务**：等待 B 站审核
- **发布任务**：定时发布视频

## 通过 WebUI 管理任务

WebUI 提供了最直观的任务管理方式。

### 查看任务列表

1. 打开 WebUI（`http://localhost:19159`）
2. 进入"直播管理"页面
3. 查看所有录制任务的状态

### 任务状态说明

每个任务卡片会显示当前状态：

- **空闲**（绿色）：等待直播开始
- **直播中**（红色）：正在录制
- **等待下载**（灰色）：已检测到直播，准备录制
- **检测/上传中**（靛蓝色）：检测直播或上传视频
- **非录播时间**（绿色）：不在录播时间范围内
- **暂停中**（粉色）：任务已暂停

### 启动任务

**自动启动**：
- 服务启动时自动加载所有任务
- 检测到开播时自动开始录制

**手动启动**：
1. 在任务卡片上找到"启动"按钮
2. 点击启动按钮
3. 任务开始运行

### 停止任务

1. 找到正在运行的任务
2. 点击"停止"按钮
3. 确认停止操作

**注意**：
- 停止录制任务会保存已录制的内容
- 停止上传任务会暂停上传，可以稍后继续

### 暂停/恢复任务

**暂停任务**：
1. 点击任务卡片上的"暂停"按钮
2. 任务状态变为"暂停中"
3. 不再监控该直播间

**恢复任务**：
1. 点击"恢复"按钮
2. 任务恢复监控状态

**使用场景**：
- 临时不想录制某个主播
- 主播休假期间
- 调试其他任务时

### 重启任务

如果任务出现问题，可以重启：

1. 停止任务
2. 等待几秒
3. 重新启动任务

或者直接点击"重启"按钮（如果有）。

### 删除任务

1. 点击任务卡片上的"删除"按钮
2. 确认删除操作
3. 任务被永久删除

⚠️ **警告**：删除任务不会删除已录制的文件，但会删除任务配置。

## 通过 CLI 管理任务

命令行提供了更灵活的任务管理方式。

### 查看任务状态

```bash
# 查看所有任务
biliup status

# 查看特定任务
biliup status --name "主播名称"
```

### 启动服务

```bash
# 启动服务（自动加载所有任务）
biliup server

# 指定端口
biliup server --port 8080

# 启用认证
biliup server --auth
```

### 停止服务

```bash
# 使用 Ctrl+C 停止服务
# 或发送 SIGTERM 信号
kill -TERM <pid>
```

### 重新加载配置

修改配置文件后，重新加载配置：

```bash
# 方式 1：重启服务
# Ctrl+C 停止，然后重新启动

# 方式 2：发送 SIGHUP 信号（如果支持）
kill -HUP <pid>
```

### 查看任务日志

```bash
# 查看所有日志
tail -f biliup.log

# 查看特定任务的日志
grep "主播名称" biliup.log

# 查看最近的错误
grep "ERROR" biliup.log | tail -20
```

## 任务监控

### 实时监控

#### WebUI 实时监控

1. 进入"实时日志"页面
2. 查看实时日志输出
3. 可以按级别过滤（INFO、WARN、ERROR）

#### 命令行实时监控

```bash
# 实时查看日志
tail -f biliup.log

# 只看错误
tail -f biliup.log | grep ERROR

# 只看特定主播
tail -f biliup.log | grep "主播名称"
```

### 任务统计

#### 查看录制统计

在 WebUI 的"历史记录"页面可以看到：

- 总录制时长
- 总文件大小
- 录制成功/失败次数
- 平均录制时长

#### 查看上传统计

在"投稿管理"页面可以看到：

- 总上传数量
- 上传成功/失败次数
- 总上传大小
- 平均上传速度

### 性能监控

#### 系统资源监控

```bash
# 查看 CPU 和内存使用
top -p $(pgrep biliup)

# 或使用 htop
htop -p $(pgrep biliup)
```

#### 磁盘空间监控

```bash
# 查看磁盘使用情况
df -h

# 查看录制目录大小
du -sh downloads/
```

#### 网络监控

```bash
# 查看网络连接
netstat -an | grep 19159

# 查看网络流量
iftop
```


## 任务日志

### 日志级别

biliup 支持多个日志级别：

- **DEBUG**：调试信息，非常详细
- **INFO**：常规信息
- **WARN**：警告信息
- **ERROR**：错误信息

### 配置日志级别

```bash
# 启动时指定日志级别
biliup server --rust-log=debug

# 或设置环境变量
export RUST_LOG=debug
biliup server
```

配置文件中设置：

```yaml
global:
  log_level: "info"  # debug, info, warn, error
```

### 日志文件位置

默认日志文件：

```
biliup.log
```

自定义日志文件：

```yaml
global:
  log_file: "/path/to/custom.log"
```

### 日志轮转

防止日志文件过大：

```yaml
global:
  log_rotation:
    enabled: true
    max_size: "100M"  # 单个日志文件最大 100MB
    max_files: 5      # 保留最近 5 个日志文件
```

### 查看日志

**查看最新日志**：

```bash
tail -n 100 biliup.log
```

**实时查看日志**：

```bash
tail -f biliup.log
```

**搜索日志**：

```bash
# 搜索错误
grep "ERROR" biliup.log

# 搜索特定主播
grep "主播名称" biliup.log

# 搜索今天的日志
grep "2025-01-10" biliup.log
```

**导出日志**：

```bash
# 导出最近 1000 行
tail -n 1000 biliup.log > export.log

# 导出特定时间段
grep "2025-01-10" biliup.log > today.log
```

## 自动重试机制

biliup 内置了自动重试机制，提高任务成功率。

### 录制重试

录制失败时自动重试：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    retry:
      enabled: true
      max_attempts: 3      # 最多重试 3 次
      interval: 60         # 重试间隔 60 秒
      backoff: true        # 使用指数退避
```

**指数退避**：
- 第 1 次重试：等待 60 秒
- 第 2 次重试：等待 120 秒
- 第 3 次重试：等待 240 秒

### 上传重试

上传失败时自动重试：

```yaml
upload_config:
  retry:
    enabled: true
    max_attempts: 5      # 最多重试 5 次
    interval: 300        # 重试间隔 300 秒
```

### 重试策略

**立即重试**：

```yaml
retry:
  strategy: "immediate"
  max_attempts: 3
```

**延迟重试**：

```yaml
retry:
  strategy: "delayed"
  interval: 60
  max_attempts: 3
```

**指数退避**：

```yaml
retry:
  strategy: "exponential"
  initial_interval: 60
  max_attempts: 5
```

### 重试条件

可以配置在什么情况下重试：

```yaml
retry:
  on_network_error: true   # 网络错误时重试
  on_timeout: true         # 超时时重试
  on_server_error: true    # 服务器错误时重试
  on_client_error: false   # 客户端错误不重试
```

## 任务队列

### 队列管理

biliup 使用队列管理任务，避免资源过载。

#### 录制队列

```yaml
global:
  recording_queue:
    max_size: 100        # 队列最大长度
    max_concurrent: 5    # 最大并发录制数
```

#### 上传队列

```yaml
global:
  upload_queue:
    max_size: 50
    max_concurrent: 2
```

### 队列优先级

为任务设置优先级：

```yaml
streamers:
  重要主播:
    url: ["直播间URL"]
    priority: 10  # 优先级 10（高）
    
  普通主播:
    url: ["直播间URL"]
    priority: 5   # 优先级 5（中）
```

优先级越高，越先执行。

### 查看队列状态

在 WebUI 的"任务平台"页面可以看到：

- 队列中的任务数量
- 正在执行的任务
- 等待中的任务
- 已完成的任务

## 任务调度

### 定时任务

设置定时录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    schedule:
      enabled: true
      cron: "0 20 * * *"  # 每天晚上 8 点检查
```

Cron 表达式格式：

```
分 时 日 月 星期
*  *  *  *  *
```

**示例**：

```yaml
# 每天晚上 8 点
cron: "0 20 * * *"

# 每周一到周五晚上 8 点
cron: "0 20 * * 1-5"

# 每小时检查一次
cron: "0 * * * *"

# 每 30 分钟检查一次
cron: "*/30 * * * *"
```

### 时间窗口

只在特定时间段录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    time_window:
      start: "20:00"
      end: "02:00"
```

### 星期过滤

只在特定星期录制：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    weekdays: [1, 2, 3, 4, 5]  # 周一到周五
```

## 任务通知

### 配置通知

```yaml
notification:
  enabled: true
  
  # 录制开始通知
  on_recording_start: true
  
  # 录制结束通知
  on_recording_end: true
  
  # 上传成功通知
  on_upload_success: true
  
  # 任务失败通知
  on_task_failure: true
```

### 通知方式

#### Webhook 通知

```yaml
notification:
  webhook:
    url: "https://your-webhook-url"
    method: "POST"
```

#### 邮件通知

```yaml
notification:
  email:
    enabled: true
    smtp_server: "smtp.gmail.com"
    smtp_port: 587
    username: "your-email@gmail.com"
    password: "your-password"
    to: "notify@example.com"
```

#### Telegram 通知

```yaml
notification:
  telegram:
    enabled: true
    bot_token: "your-bot-token"
    chat_id: "your-chat-id"
```

### 通知内容

自定义通知内容：

```yaml
notification:
  templates:
    recording_start: "{streamer} 开始直播了！"
    recording_end: "{streamer} 直播结束，已录制 {duration}"
    upload_success: "视频上传成功：{title}"
    task_failure: "任务失败：{error}"
```

## 任务备份与恢复

### 备份任务配置

```bash
# 备份配置文件
cp config.yaml config.yaml.backup

# 备份数据库（如果使用）
cp biliup.db biliup.db.backup
```

### 恢复任务配置

```bash
# 恢复配置文件
cp config.yaml.backup config.yaml

# 重启服务
biliup server
```

### 导出任务列表

通过 WebUI 导出任务列表：

1. 进入"直播管理"页面
2. 点击"导出"按钮
3. 选择导出格式（JSON、YAML）
4. 保存文件

### 导入任务列表

1. 进入"直播管理"页面
2. 点击"导入"按钮
3. 选择配置文件
4. 确认导入

## 常见任务管理场景

### 场景 1：临时停止所有录制

```bash
# 停止服务
pkill biliup

# 或在 WebUI 中逐个暂停任务
```

### 场景 2：只录制特定主播

```yaml
streamers:
  主播A:
    url: ["直播间URL"]
    enabled: true  # 启用
    
  主播B:
    url: ["直播间URL"]
    enabled: false  # 禁用
```

### 场景 3：批量修改任务配置

```bash
# 编辑配置文件
vim config.yaml

# 重新加载配置
# 重启服务或发送 SIGHUP 信号
```

### 场景 4：清理失败的任务

在 WebUI 的"任务平台"页面：

1. 筛选失败的任务
2. 批量选择
3. 点击"清理"按钮

### 场景 5：迁移任务到新服务器

1. 备份配置文件和数据库
2. 在新服务器安装 biliup
3. 复制配置文件和数据库
4. 启动服务

```bash
# 在旧服务器
tar -czf biliup-backup.tar.gz config.yaml biliup.db downloads/

# 传输到新服务器
scp biliup-backup.tar.gz user@new-server:/path/

# 在新服务器
tar -xzf biliup-backup.tar.gz
biliup server
```

## 故障排查

### 任务无法启动

**检查项**：
1. 配置文件语法是否正确
2. 直播间 URL 是否有效
3. 网络连接是否正常
4. 日志中是否有错误信息

**解决方案**：

```bash
# 验证配置文件
biliup config validate

# 查看详细日志
biliup server --rust-log=debug
```

### 任务频繁失败

**可能原因**：
- 网络不稳定
- 直播平台限制
- 系统资源不足

**解决方案**：
1. 增加重试次数和间隔
2. 降低并发数
3. 检查系统资源使用情况

### 任务卡住不动

**解决方案**：

```bash
# 查看任务状态
biliup status

# 重启卡住的任务
# 在 WebUI 中停止并重新启动

# 或重启整个服务
pkill biliup
biliup server
```

## 最佳实践

### 任务命名

- 使用有意义的名称
- 包含主播名称或平台
- 便于识别和管理

### 任务分组

将相关任务分组管理：

```yaml
groups:
  游戏主播:
    - 主播A
    - 主播B
  
  娱乐主播:
    - 主播C
    - 主播D
```

### 定期维护

- 每周检查任务状态
- 清理失败的任务
- 更新配置文件
- 备份重要数据

### 监控告警

- 设置任务失败告警
- 监控磁盘空间
- 监控系统资源
- 定期查看日志

## 下一步

- [弹幕录制](./danmaku-recording.md) - 了解如何录制弹幕
- [平台支持](./platform-support.md) - 查看支持的平台
- [故障排查](./troubleshooting.md) - 解决常见问题
- [高级配置](../configuration/advanced.md) - 深入配置选项
