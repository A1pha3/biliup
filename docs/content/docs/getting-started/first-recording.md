+++
title = "第一次使用教程"
description = "从零开始，完成你的第一次直播录制和上传。"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 40
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "跟随本教程，一步步完成从登录到录制的完整流程。"
toc = true
top = false
+++

## 前提条件

在开始之前，请确保：

- ✅ 已经[安装 biliup](../installation/)
- ✅ biliup 服务正在运行
- ✅ 可以访问 WebUI 界面（`http://localhost:19159`）
- ✅ 有一个 B 站账号（用于上传视频）

## 第一步：登录 B 站账号

要将录制的视频自动上传到 B 站，首先需要登录你的 B 站账号。

### 使用命令行登录

打开终端或命令提示符，运行：

```bash
biliup login
```

你会看到以下提示：

```
请选择登录方式:
1. 扫码登录（推荐）
2. 账号密码登录
3. 使用已有的 cookies
请输入选项 (1-3):
```

### 方式一：扫码登录（推荐）

1. 输入 `1` 选择扫码登录
2. 终端会显示一个二维码
3. 使用 B 站 APP 扫描二维码
4. 在手机上确认登录
5. 看到"登录成功"提示后，登录信息会自动保存

```bash
请输入选项 (1-3): 1
请使用 B 站 APP 扫描以下二维码：

█████████████████████████████
█████████████████████████████
████ ▄▄▄▄▄ █▀█ █▄▄█ ▄▄▄▄▄ ████
████ █   █ █▀▀▀█ ▄█ █   █ ████
████ █▄▄▄█ █▀ █▀▀ █ █▄▄▄█ ████
...

✓ 登录成功！
登录信息已保存到: cookies.json
```

### 方式二：账号密码登录

1. 输入 `2` 选择账号密码登录
2. 输入你的 B 站账号（手机号或邮箱）
3. 输入密码
4. 如果需要，完成验证码验证
5. 登录信息会自动保存

### 方式三：使用已有的 cookies

如果你已经有 B 站的 cookies 文件：

1. 输入 `3`
2. 将 cookies 文件放在当前目录，命名为 `cookies.json`
3. 或者指定 cookies 文件路径

### 验证登录状态

登录成功后，可以验证登录状态：

```bash
biliup show
```

如果登录成功，会显示你的账号信息。

## 第二步：创建配置文件

配置文件用于定义要录制的直播间和上传参数。

### 使用 WebUI 创建（推荐）

1. 在浏览器中打开 `http://localhost:19159`
2. 点击左侧菜单的"主播管理"
3. 点击右上角的"添加主播"按钮
4. 填写以下信息：
   - **主播名称**: 给这个录制任务起个名字（例如："某某的直播录像"）
   - **直播间 URL**: 输入直播间地址（例如：`https://www.twitch.tv/username`）
   - **视频标签**: 添加标签，用逗号分隔（例如："游戏,直播录像"）
5. 点击"保存"

### 手动创建配置文件

在 biliup 运行目录创建 `config.toml` 文件：

```toml
# 基本配置示例
[streamers."主播名称"]
url = ["https://www.twitch.tv/username"]
tags = ["游戏", "直播录像"]
```

#### 配置说明

- `streamers."主播名称"`: 为这个录制任务命名
- `url`: 直播间地址，支持多个地址
- `tags`: 视频标签，上传到 B 站时使用

#### 支持的平台

biliup 支持 20+ 直播平台，包括：

- **Twitch**: `https://www.twitch.tv/username`
- **斗鱼**: `https://www.douyu.com/房间号`
- **虎牙**: `https://www.huya.com/房间号`
- **B 站**: `https://live.bilibili.com/房间号`
- **抖音**: `https://live.douyin.com/房间号`
- **YouTube**: `https://www.youtube.com/watch?v=视频ID`

更多平台支持请查看[平台列表](../../user-guide/supported-platforms/)。

### 配置文件示例

#### 示例 1：录制单个主播

```toml
[streamers."游戏主播"]
url = ["https://www.twitch.tv/shroud"]
tags = ["FPS", "游戏", "直播录像"]
```

#### 示例 2：录制多个主播

```toml
[streamers."主播A"]
url = ["https://www.twitch.tv/userA"]
tags = ["游戏"]

[streamers."主播B"]
url = ["https://www.douyu.com/123456"]
tags = ["娱乐"]
```

#### 示例 3：高级配置

```toml
[streamers."专业主播"]
url = ["https://www.twitch.tv/username"]
tags = ["电竞", "直播"]
format = "flv"  # 录制格式
quality = "best"  # 画质选择

# 上传配置
title = "【{streamer}】{title}"  # 视频标题模板
desc = "直播录像"  # 视频简介
tid = 171  # 分区 ID（171 = 电子竞技）
```

## 第三步：添加第一个直播间

让我们以录制 Twitch 直播为例。

### 通过 WebUI 添加

1. 打开 WebUI（`http://localhost:19159`）
2. 进入"主播管理"页面
3. 点击"添加主播"
4. 填写信息：
   ```
   主播名称: Shroud的直播
   直播间URL: https://www.twitch.tv/shroud
   标签: FPS,游戏,直播录像
   ```
5. 点击"保存"

### 通过配置文件添加

编辑 `config.toml`，添加：

```toml
[streamers."Shroud的直播"]
url = ["https://www.twitch.tv/shroud"]
tags = ["FPS", "游戏", "直播录像"]
```

保存文件后，biliup 会自动重新加载配置。

## 第四步：启动服务

如果服务尚未启动，运行：

```bash
biliup server --auth
```

你会看到类似的输出：

```
2025-01-10T12:00:00.000Z  INFO biliup_cli::server: Starting server on 0.0.0.0:19159
2025-01-10T12:00:00.000Z  INFO biliup_cli::server: Authentication enabled
2025-01-10T12:00:00.000Z  INFO biliup: Loaded 1 streamer(s) from config
2025-01-10T12:00:00.000Z  INFO biliup: Monitoring: Shroud的直播
```

## 第五步：访问 WebUI

在浏览器中打开：

```
http://localhost:19159
```

如果启用了认证（`--auth` 参数），首次访问需要设置密码。

### WebUI 界面说明

- **仪表板**: 显示录制任务概览和统计信息
- **主播管理**: 添加、编辑、删除录制任务
- **任务列表**: 查看当前和历史录制任务
- **日志查看**: 实时查看系统日志
- **设置**: 配置全局参数

## 第六步：开始录制

biliup 会自动监控配置的直播间：

### 自动录制

- **主播开播时**: 自动开始录制
- **主播下播时**: 自动停止录制并保存文件
- **录制完成后**: 如果配置了上传，会自动上传到 B 站

### 手动控制

在 WebUI 的"主播管理"页面，你可以：

- **启用/禁用**: 控制是否监控该直播间
- **立即录制**: 手动开始录制（即使未开播）
- **停止录制**: 手动停止当前录制

### 查看录制状态

在"任务列表"页面，你可以看到：

- **录制状态**: 等待开播、录制中、已完成
- **录制时长**: 当前录制的时长
- **文件大小**: 已录制的文件大小
- **实时日志**: 录制过程的详细日志

## 第七步：查看录制结果

### 查看录制文件

录制完成的视频默认保存在：

```
downloads/主播名称/视频文件.flv
```

例如：

```
downloads/Shroud的直播/2025-01-10_12-00-00.flv
```

### 查看上传状态

如果配置了自动上传，在"任务列表"中可以看到：

- **上传进度**: 实时显示上传百分比
- **上传速度**: 当前上传速度
- **稿件信息**: 上传成功后的 B 站稿件链接

### 在 B 站查看视频

1. 上传成功后，点击稿件链接
2. 或者访问你的 B 站投稿管理页面
3. 找到刚刚上传的视频

## 预期结果

完成以上步骤后，你应该能看到：

### 1. 服务正常运行

终端显示：

```
✓ 服务已启动
✓ 配置已加载
✓ 正在监控 1 个直播间
```

### 2. WebUI 正常访问

浏览器中可以看到：

- 主播列表显示你添加的直播间
- 状态显示"等待开播"或"录制中"
- 日志实时更新

### 3. 录制成功

当主播开播时：

- 自动开始录制
- 日志显示录制进度
- 文件保存到 downloads 目录

### 4. 上传成功（如果配置）

录制完成后：

- 自动开始上传
- 上传进度实时显示
- 上传成功后显示稿件链接

## 常见问题

### 无法检测到开播？

**可能原因**:
- 直播间 URL 不正确
- 网络连接问题
- 平台 API 变化

**解决方案**:
```bash
# 查看详细日志
biliup server --rust-log=debug

# 手动测试直播间
biliup download "直播间URL" --output test.flv
```

### 录制文件损坏？

**可能原因**:
- 网络不稳定导致录制中断
- 磁盘空间不足

**解决方案**:
- 检查网络连接
- 确保有足够的磁盘空间
- 使用更稳定的录制格式（flv）

### 上传失败？

**可能原因**:
- 登录信息过期
- 视频格式不支持
- 网络问题

**解决方案**:
```bash
# 重新登录
biliup login

# 手动上传测试
biliup upload "视频文件路径" --title "测试视频"
```

### 视频标题乱码？

**可能原因**:
- 配置文件编码问题

**解决方案**:
- 确保配置文件使用 UTF-8 编码
- 使用 WebUI 配置避免编码问题

## 下一步

恭喜！你已经完成了第一次录制。接下来你可以：

### 学习更多功能

- [配置高级选项](../../configuration/advanced/)：自定义录制参数
- [管理多个主播](../../user-guide/multi-streamer/)：同时录制多个直播间
- [自定义上传模板](../../configuration/upload-template/)：个性化视频信息
- [使用弹幕录制](../../user-guide/danmaku/)：保存直播弹幕

### 优化你的配置

- [选择最佳画质](../../user-guide/quality-selection/)：平衡质量和文件大小
- [配置存储策略](../../user-guide/storage/)：管理磁盘空间
- [设置通知提醒](../../user-guide/notifications/)：开播提醒和录制通知

### 自动化运行

- [配置开机自启](../installation/#配置后台运行)：无人值守运行
- [使用 Docker 部署](../installation/#docker-安装)：容器化部署
- [远程访问配置](../../user-guide/remote-access/)：从任何地方管理

## 获取帮助

如果遇到问题：

- 查看[故障排查指南](../../user-guide/troubleshooting/)
- 阅读[常见问题](../../help/faq/)
- 在 [GitHub Issues](https://github.com/biliup/biliup/issues) 提问
- 加入 [Telegram 群组](https://t.me/+IkpIABHqy6U0ZTQ5)
- 访问[论坛](https://bbs.biliup.rs)

## 小贴士

💡 **提示**: 
- 首次录制建议选择一个正在直播的主播进行测试
- 录制前确保有足够的磁盘空间（建议至少 10GB）
- 使用 `--auth` 参数保护你的 WebUI 访问
- 定期备份 `cookies.json` 文件，避免重复登录
- 查看日志可以帮助你了解录制状态和排查问题

🎉 **恭喜**: 你已经掌握了 biliup 的基本使用！现在可以开始录制你喜欢的直播内容了。
