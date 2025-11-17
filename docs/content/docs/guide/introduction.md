+++
title = "进阶使用指南"
description = "biliup 进阶使用技巧和最佳实践"
date = 2021-05-01T08:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 10
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "深入了解 biliup 的高级功能和使用技巧"
toc = true
top = false
+++

## 概述

本指南面向已经熟悉 biliup 基本使用的用户，介绍更高级的功能和使用技巧。如果你是新手，建议先阅读 [快速开始](../getting-started/quick-start/) 和 [用户指南](../user-guide/)。

## 进阶主题

### 配置优化

深入了解如何优化 biliup 的配置以获得最佳性能：

- [高级配置选项](../configuration/advanced-config/) - 探索所有可用的配置参数
- [上传配置优化](../configuration/upload-config/) - 优化上传速度和稳定性
- [主播配置技巧](../configuration/streamer-config/) - 管理多个主播的最佳实践
- [配置示例](../configuration/examples/) - 实际使用场景的配置示例

### 架构与原理

了解 biliup 的内部工作原理：

- [架构概览](../architecture/overview/) - 系统整体架构设计
- [前端架构](../architecture/frontend/) - Web UI 的实现
- [后端架构](../architecture/backend/) - 服务端的设计
- [Python 引擎](../architecture/python-engine/) - 核心录制引擎
- [数据流](../architecture/data-flow/) - 数据在系统中的流转
- [插件系统](../architecture/plugin-system/) - 可扩展的插件机制

### 开发与扩展

为 biliup 开发新功能或扩展现有功能：

- [开发环境搭建](../development/setup-dev-environment/) - 配置开发环境
- [项目结构](../development/project-structure/) - 了解代码组织
- [从源码构建](../development/building-from-source/) - 编译和打包
- [插件开发](../development/plugin-development/) - 开发自定义插件
- [添加平台支持](../development/adding-platform-support/) - 支持新的直播平台
- [API 集成](../development/api-integration/) - 集成外部 API
- [测试](../development/testing/) - 编写和运行测试
- [调试](../development/debugging/) - 调试技巧和工具

### API 参考

使用 biliup 的各种 API：

- [命令行接口](../api-reference/cli-reference/) - CLI 命令详解
- [Python API](../api-reference/python-api/) - 作为 Python 库使用
- [REST API](../api-reference/rest-api/) - HTTP API 接口
- [WebSocket API](../api-reference/websocket-api/) - 实时通信接口
- [错误码](../api-reference/error-codes/) - 错误码说明

## 嵌入式使用

如果你不想使用完全自动化的功能，而是希望将 biliup 作为库嵌入到自己的项目中，可以参考以下示例。

### 作为 Python 库使用

**上传视频示例**：

```python
from biliup.plugins.bili_webup import BiliBili, Data

# 创建视频对象
video = Data()
video.title = '视频标题'
video.desc = '视频简介'
video.source = '转载来源（如适用）'
video.tid = 171  # 分区ID（171=电子竞技）
video.set_tag(['标签1', '标签2'])
video.dynamic = '动态内容'

# 配置上传参数
lines = 'AUTO'  # 自动选择线路
tasks = 3       # 并发数
dtime = 7200    # 延后发布时间（秒）

# 上传视频
with BiliBili(video) as bili:
    # 使用 Cookie 登录
    bili.login("bili.cookie", {
        'cookies': {
            'SESSDATA': 'your_sessdata',
            'bili_jct': 'your_bili_jct',
            'DedeUserID__ckMd5': 'your_ckmd5',
            'DedeUserID': 'your_dedeuserid'
        },
        'access_token': 'your_access_token'
    })
    
    # 上传视频文件
    for file in file_list:
        video_part = bili.upload_file(file, lines=lines, tasks=tasks)
        video.append(video_part)
    
    # 设置延后发布
    video.delay_time(dtime)
    
    # 上传封面
    video.cover = bili.cover_up('/path/to/cover.jpg').replace('http:', '')
    
    # 提交视频
    ret = bili.submit()
    print(f"视频提交成功: {ret}")
```

**下载直播流示例**：

```python
from biliup.downloader import download

# 下载直播流
download(
    filename='直播录像',
    url='https://www.twitch.tv/streamer',
    suffix='flv'
)
```

详细的 API 文档请参考 [Python API 参考](../api-reference/python-api/)。

## 最佳实践

### VPS 上传线路选择

针对不同网络环境选择合适的上传线路可以显著提升上传速度：

**B 站上传模式**：

- **bup 模式**：国内常用，视频直接上传到 B 站投稿系统
  - `ws`（网宿）
  - `qn`（七牛）
  - `bda2`（百度）

- **bupfetch 模式**：国外网络环境，视频先上传到第三方存储，再由 B 站拉取
  - 注意：kodo、gcs、bos 线路已失效

**推荐配置**：

- **国内 VPS**：使用 `bda2` 线路
- **国外 VPS**：使用 `ws` 或 `qn` 线路，或设置为 `AUTO` 自动选择
- 根据服务器资源合理设置并发数，避免磁盘占满

详细配置请参考 [上传配置](../configuration/upload-config/)。

### 弹幕文件使用

录制的 XML 弹幕文件有多种使用方式：

- **转换为字幕**：使用 [DanmakuFactory](https://github.com/hihkm/DanmakuFactory) 转换为 ASS 字幕文件
- **在线播放**：使用 [AList](https://alist.nn.ci/zh/) 自动挂载弹幕
- **本地播放**：使用 [弹弹play](https://www.dandanplay.com/) 直接加载 XML 弹幕

详细说明请参考 [弹幕录制](../user-guide/danmaku-recording/)。

### 系统服务配置

在 Linux 系统上配置 biliup 开机自启：

1. 创建 systemd service 文件：
   ```bash
   nano ~/.config/systemd/user/biliupd.service
   ```

2. 添加以下内容：
   ```ini
   [Unit]
   Description=Biliup Startup
   Documentation=https://biliup.github.io/biliup
   Wants=network-online.target
   After=network-online.target

   [Service]
   Type=simple
   WorkingDirectory=/path/to/your/config
   ExecStart=/usr/bin/biliup start

   [Install]
   WantedBy=default.target
   ```

3. 启用并启动服务：
   ```bash
   systemctl --user enable biliupd
   systemctl --user start biliupd
   ```

## 插件开发

biliup 采用插件化架构，支持扩展下载和上传功能。

### 下载插件

创建自定义下载插件：

```python
from biliup.plugins.base_adapter import BaseAdapter
from biliup.plugins import Plugin

@Plugin.download(platform="custom_platform")
class CustomDownloader(BaseAdapter):
    def __init__(self, config):
        super().__init__(config)
    
    def download(self, url):
        # 实现下载逻辑
        pass
```

### 上传插件

创建自定义上传插件：

```python
from biliup.plugins.upload import BaseUploader
from biliup.plugins import Plugin

@Plugin.upload(platform="custom_platform")
class CustomUploader(BaseUploader):
    def upload(self, file_path):
        # 实现上传逻辑
        pass
```

### 事件驱动

使用事件系统添加自定义功能：

```python
from biliup.event import event_manager

# 监听下载完成事件
@event_manager.register("download_finish", block=True)
def on_download_finish(data):
    # 处理下载完成后的逻辑
    # 例如：转码、压缩等
    pass
```

详细的插件开发指南请参考 [插件开发](../development/plugin-development/)。

## 社区资源

### 教程和文章

- [快速上手视频教程](https://www.bilibili.com/video/BV1jB4y1p7TK/) by [@milk](https://github.com/by123456by)
- [Ubuntu 安装教程](https://blog.waitsaber.org/archives/129) by [@waitsaber](https://github.com/waitsaber)
- [CentOS 安装教程](https://blog.waitsaber.org/archives/163) by [@waitsaber](https://github.com/waitsaber)
- [Windows 安装教程](https://blog.waitsaber.org/archives/169) by [@waitsaber](https://github.com/waitsaber)
- [常见问题解决方案](https://blog.waitsaber.org/archives/167) by [@waitsaber](https://github.com/waitsaber)

### 获取帮助

- [GitHub Discussions](https://github.com/biliup/biliup/discussions) - 讨论和交流
- [GitHub Issues](https://github.com/biliup/biliup/issues) - 报告问题
- [QQ 群](https://github.com/ForgQi/biliup/discussions/58#discussioncomment-2388776) - 即时交流

## 下一步

- 探索 [配置选项](../configuration/) 优化你的设置
- 了解 [架构设计](../architecture/) 深入理解系统
- 参与 [开发](../development/) 贡献代码
- 查看 [API 文档](../api-reference/) 集成到你的项目
