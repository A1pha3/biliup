+++
title = "快速开始"
description = "5 分钟快速上手 biliup，开始你的第一次直播录制。"
date = 2021-05-01T08:20:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 20
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "只需几个简单步骤，即可开始使用 biliup 录制直播。"
toc = true
top = false
+++

## 系统要求

在使用 biliup 之前，请确保你的系统满足以下要求：

- **Python**: 3.9 或更高版本
- **操作系统**: Windows、Linux 或 macOS
- **网络**: 稳定的互联网连接

## 快速安装

根据你的操作系统选择对应的安装方式：

### Windows

下载最新版本的 exe 可执行文件：

1. 访问 [Release 页面](https://github.com/biliup/biliup/releases/latest)
2. 下载 `biliup-windows-x86_64.exe`
3. 双击运行即可

### Linux 或 macOS

使用 uv 工具安装（推荐）：

```bash
# 1. 安装 uv（如果尚未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. 安装 biliup
uv tool install biliup

# 3. 启动服务
biliup server --auth
```

### 使用 pip 安装

如果你已经安装了 Python 3.9+，可以直接使用 pip：

```bash
pip install biliup
```

### 使用 Docker

```bash
docker pull ghcr.io/biliup/caution:latest
docker run -d -p 19159:19159 ghcr.io/biliup/caution:latest
```

> 💡 **提示**: 需要更详细的安装说明？查看[完整安装指南](../installation/)。

## 启动服务

安装完成后，启动 biliup 服务：

```bash
biliup server --auth
```

你会看到类似以下的输出：

```
2025-01-10T12:00:00.000Z  INFO biliup_cli::server: Starting server on 0.0.0.0:19159
2025-01-10T12:00:00.000Z  INFO biliup_cli::server: Authentication enabled
```

## 访问 WebUI

在浏览器中访问：

```
http://localhost:19159
```

如果你在远程服务器上运行，将 `localhost` 替换为服务器的 IP 地址：

```
http://your-server-ip:19159
```

首次访问时，你需要设置登录密码（如果使用了 `--auth` 参数）。

## 简单配置示例

### 方式一：通过 WebUI 配置（推荐）

1. 在 WebUI 中点击"添加主播"
2. 输入直播间 URL（例如：`https://www.twitch.tv/username`）
3. 设置视频标签和其他选项
4. 点击"保存"

### 方式二：手动创建配置文件

在当前目录创建 `config.toml` 文件：

```toml
# 录制 Twitch 直播
[streamers."主播名称"]
url = ["https://www.twitch.tv/username"]
tags = ["游戏", "直播录像"]
```

或者使用 YAML 格式（`config.yaml`）：

```yaml
streamers:
  主播名称:
    url:
      - https://www.twitch.tv/username
    tags:
      - 游戏
      - 直播录像
```

> 📝 **注意**: 将 `username` 替换为实际的主播用户名。

## 开始录制

配置完成后，biliup 会自动监控直播状态：

- **开播时**: 自动开始录制
- **下播时**: 自动停止录制并保存文件
- **上传**: 如果配置了 B 站登录信息，会自动上传到 B 站

### 查看录制状态

在 WebUI 中，你可以：

- 查看当前录制任务的状态
- 查看实时日志输出
- 手动启动或停止录制任务
- 查看已录制的视频文件

## 预期结果

成功配置后，你应该能看到：

1. **WebUI 界面**: 显示所有配置的主播和任务状态
2. **日志输出**: 显示录制进度和状态信息
3. **视频文件**: 录制完成后保存在当前目录的 `downloads/` 文件夹中

## 下一步

恭喜！你已经完成了 biliup 的基本设置。接下来你可以：

- [配置 B 站登录](../first-recording/#登录-b-站账号)，启用自动上传功能
- [了解更多配置选项](../../configuration/)，自定义录制和上传参数
- [查看完整的用户指南](../../user-guide/)，掌握所有功能

## 常见问题

### 无法访问 WebUI？

- 检查防火墙是否允许 19159 端口
- 确认服务已成功启动
- 尝试使用 `0.0.0.0` 而不是 `localhost`

### 录制失败？

- 确认直播间 URL 正确
- 检查网络连接是否正常
- 查看日志输出了解具体错误信息

### 需要更多帮助？

查看[故障排查指南](../../user-guide/troubleshooting/)或加入我们的 [Telegram 群组](https://t.me/+IkpIABHqy6U0ZTQ5)。
