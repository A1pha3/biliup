+++
title = "常见问题"
description = "biliup 常见问题解答"
date = 2021-05-01T19:30:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "biliup 使用过程中的常见问题和解决方案"
toc = true
top = false
+++

## 安装问题

### 如何安装 biliup？

biliup 支持多种安装方式：

- **pip 安装**（推荐）：`pip install biliup`
- **Docker 安装**：`docker pull ghcr.io/biliup/caution:latest`
- **从源码安装**：克隆仓库后运行 `pip install -e .`

详细安装步骤请参考 [安装指南](../getting-started/installation.md)。

### 安装时提示 Python 版本不兼容怎么办？

biliup 要求 Python 3.9 或更高版本。请使用以下命令检查你的 Python 版本：

```bash
python --version
```

如果版本过低，请从 [Python 官网](https://www.python.org/downloads/) 下载并安装最新版本。

### pip 安装失败，提示网络错误？

可以尝试使用国内镜像源加速安装：

```bash
pip install biliup -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Docker 容器无法启动？

请检查以下几点：

1. 确保 Docker 服务正在运行
2. 检查端口 19159 是否被占用
3. 确保挂载的目录路径正确且有读写权限
4. 查看容器日志：`docker logs biliup`

### ARM 平台（如树莓派）安装失败？

ARM 平台用户可能需要降级 stream-gears 版本。请参考 [GitHub 讨论](https://github.com/biliup/biliup/discussions/407) 中的解决方案。

## 配置问题

### 配置文件应该放在哪里？

biliup 会按以下顺序查找配置文件：

1. 命令行指定的路径：`biliup --config /path/to/config.toml start`
2. 当前工作目录下的 `config.toml` 或 `config.yaml`
3. 用户主目录下的 `.biliup/config.toml`

### 配置文件格式是什么？

biliup 支持两种配置格式：

- **TOML 格式**（推荐）：`config.toml`
- **YAML 格式**：`config.yaml`

详细配置说明请参考 [配置文件格式](../configuration/config-file-format.md)。

### 如何配置多个主播同时录制？

在配置文件中添加多个 `streamers` 配置段：

```toml
[streamers."主播1"]
url = ["https://www.twitch.tv/streamer1"]
tags = ["游戏", "直播"]

[streamers."主播2"]
url = ["https://www.douyu.com/123456"]
tags = ["娱乐", "直播"]
```

### 如何获取 B 站 Cookie？

使用 biliup-rs 命令行工具登录：

```bash
biliup login
```

登录成功后会在当前目录生成 `cookies.json` 文件。详细步骤请参考 [认证配置](../configuration/authentication.md)。

### Cookie 过期了怎么办？

重新运行 `biliup login` 命令获取新的 Cookie。建议定期更新 Cookie 以避免上传失败。

## 录制问题

### 录制一直失败，提示连接超时？

可能的原因和解决方案：

1. **网络问题**：检查网络连接，尝试使用代理
2. **直播间地址错误**：确认 URL 格式正确
3. **平台限制**：某些平台可能需要登录或特殊配置
4. **防火墙拦截**：检查防火墙设置

### 录制的视频文件很大，如何分段？

在配置文件中设置分段参数：

```toml
[streamers."主播名"]
url = ["https://..."]
split_time = 3600  # 按时间分段，单位秒（1小时）
split_size = 2048  # 按大小分段，单位MB（2GB）
```

### 支持哪些直播平台？

biliup 支持以下平台：

- Twitch
- 斗鱼（Douyu）
- 虎牙（Huya）
- Bilibili
- 抖音（Douyin）
- YouTube
- 快手（Kuaishou）
- 等更多平台

完整列表请参考 [平台支持](../user-guide/platform-support.md)。

### 如何录制弹幕？

在配置文件中启用弹幕录制：

```toml
[streamers."主播名"]
url = ["https://..."]
danmu = true  # 启用弹幕录制
```

弹幕会保存为 XML 格式文件。详细说明请参考 [弹幕录制](../user-guide/danmaku-recording.md)。

### 录制斗鱼平台提示需要 JavaScript 解释器？

录制斗鱼需要安装 JavaScript 解释器，可选：

- **QuickJS**（Python 包）：`pip install quickjs`
- **Node.js**：从 [官网](https://nodejs.org/) 下载安装

### 录制卡死或下载超时怎么办？

biliup 会自动重试 3 次。如果仍然失败：

1. 检查网络连接
2. 尝试更换下载器（streamlink、ffmpeg）
3. 查看日志文件排查具体错误
4. 在 [GitHub Issues](https://github.com/biliup/biliup/issues) 报告问题

## 上传问题

### 上传失败，提示未登录？

确保 `cookies.json` 文件存在且有效：

1. 检查文件是否在正确的位置
2. 使用 `biliup login` 重新登录
3. 确认 Cookie 未过期

### 上传速度很慢怎么办？

可以尝试以下优化方法：

1. **选择合适的上传线路**：在配置中设置 `line = "kodo"` 或 `line = "bda2"`
2. **增加并发数**：设置 `limit = 5`（根据网络情况调整）
3. **使用国外 VPS**：国外 VPS 上传到 B 站通常更快

详细说明请参考 [上传配置](../configuration/upload-config.md)。

### 如何选择上传线路？

不同地区推荐的线路：

- **国内**：`bda2`（百度）、`qn`（七牛）
- **国外**：`ws`（网宿）、`kodo`（七牛）

可以设置为 `AUTO` 让系统自动选择最优线路。

### 上传后视频审核不通过？

请检查：

1. 视频内容是否符合 B 站社区规范
2. 标题、标签、简介是否合规
3. 分区选择是否正确
4. 是否添加了转载来源（转载视频必填）

### 如何实现边录边传？

在配置文件中启用边录边传功能：

```toml
[streamers."主播名"]
url = ["https://..."]
upload = true  # 启用自动上传
```

录制完成后会自动上传到 B 站。

### 上传时提示分区错误？

确保 `tid` 配置正确。常用分区代码：

- `171`：电子竞技
- `172`：手机游戏
- `65`：网络游戏
- `122`：野生技能协会

完整分区列表请参考 [B 站分区表](https://github.com/ForgQi/biliup/wiki)。

## 性能优化

### 如何提高录制性能？

1. **使用 SSD 存储**：提高磁盘 I/O 性能
2. **合理设置并发数**：根据 CPU 和网络情况调整
3. **选择合适的下载器**：stream-gears 性能通常最好
4. **关闭不必要的功能**：如不需要弹幕可以关闭

### 如何减少磁盘占用？

1. **启用自动上传**：上传后自动删除本地文件
2. **设置分段录制**：避免单个文件过大
3. **定期清理**：手动或脚本定期清理旧文件

### 多主播录制时 CPU 占用过高？

1. 减少同时录制的主播数量
2. 降低视频质量设置
3. 使用更强大的硬件
4. 分散到多台机器录制

## 故障排查

### 如何查看日志？

日志文件位置：

- **Linux/macOS**：`~/.biliup/logs/`
- **Windows**：`%USERPROFILE%\.biliup\logs\`
- **Docker**：使用 `docker logs biliup` 查看

### 程序崩溃或无响应怎么办？

1. 查看日志文件找出错误原因
2. 尝试重启服务：`biliup restart`
3. 更新到最新版本：`pip install --upgrade biliup`
4. 在 GitHub 提交 Issue 并附上日志

### WebUI 无法访问？

检查以下几点：

1. 确认服务已启动：`ps aux | grep biliup`
2. 检查端口是否正确：默认 `19159`
3. 检查防火墙设置
4. 尝试使用 `127.0.0.1:19159` 而不是 `localhost`

### 如何启用调试模式？

设置环境变量启用详细日志：

```bash
export RUST_LOG=debug
biliup start
```

### 更新后出现问题怎么办？

1. 清除缓存：删除 `~/.biliup/cache/` 目录
2. 重新生成配置文件
3. 回退到之前的版本：`pip install biliup==版本号`
4. 查看 [CHANGELOG](https://github.com/biliup/biliup/blob/master/CHANGELOG.md) 了解变更

## 搜索快捷键

在文档站点中使用以下快捷键：

- 聚焦搜索框：`/`
- 选择结果：`↓` 和 `↑`
- 打开结果：`Enter`
- 关闭搜索：`Esc`

## 获取帮助

如果以上内容无法解决你的问题，可以通过以下方式获取帮助：

- **GitHub Issues**：[提交问题](https://github.com/biliup/biliup/issues)
- **GitHub Discussions**：[参与讨论](https://github.com/biliup/biliup/discussions)
- **QQ 群**：[加群讨论](https://github.com/ForgQi/biliup/discussions/58#discussioncomment-2388776)

## 相关资源

- [快速上手视频教程](https://www.bilibili.com/video/BV1jB4y1p7TK/)
- [Ubuntu 安装教程](https://blog.waitsaber.org/archives/129)
- [Windows 安装教程](https://blog.waitsaber.org/archives/169)
- [常见问题解决方案](https://blog.waitsaber.org/archives/167)
