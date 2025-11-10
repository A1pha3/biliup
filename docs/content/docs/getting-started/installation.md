+++
title = "详细安装指南"
description = "biliup 在各个平台上的详细安装步骤和配置说明。"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 30
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "根据你的操作系统和使用场景，选择最适合的安装方式。"
toc = true
top = false
+++

## 概述

biliup 支持多种安装方式，你可以根据自己的需求选择：

- **Windows**: exe 可执行文件（推荐）或 pip 安装
- **Linux**: uv 安装（推荐）、pip 安装或包管理器
- **macOS**: uv 安装（推荐）或 Homebrew
- **Docker**: 跨平台容器化部署
- **源码安装**: 适合开发者和高级用户

## Windows 平台

### 方式一：使用 exe 可执行文件（推荐）

这是 Windows 用户最简单的安装方式，无需安装 Python 环境。

#### 下载和安装

1. 访问 [GitHub Release 页面](https://github.com/biliup/biliup/releases/latest)
2. 下载 `biliup-windows-x86_64.exe`
3. 将文件保存到你想要的位置（例如：`C:\Program Files\biliup\`）
4. （可选）将该目录添加到系统 PATH 环境变量

#### 启动服务

打开命令提示符（CMD）或 PowerShell，运行：

```powershell
# 进入 biliup 所在目录
cd "C:\Program Files\biliup"

# 启动服务
.\biliup-windows-x86_64.exe server --auth
```

#### 配置开机自启动

1. 按 `Win + R`，输入 `shell:startup` 打开启动文件夹
2. 创建一个批处理文件 `start-biliup.bat`：

```batch
@echo off
cd /d "C:\Program Files\biliup"
start "" "biliup-windows-x86_64.exe" server --auth
```

3. 将该文件放入启动文件夹

### 方式二：使用 pip 安装

如果你已经安装了 Python 3.9+，可以使用 pip 安装。

#### 前置要求

- Python 3.9 或更高版本
- pip 包管理器

#### 安装步骤

```powershell
# 安装 biliup
pip install biliup

# 验证安装
biliup --version

# 启动服务
biliup server --auth
```

#### 升级版本

```powershell
pip install --upgrade biliup
```

## Linux 平台

### 方式一：使用 uv 安装（推荐）

uv 是一个快速的 Python 包管理器，推荐用于安装和管理 biliup。

#### 安装 uv

```bash
# 使用官方安装脚本
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或者使用 pip 安装
pip install uv
```

#### 安装 biliup

```bash
# 使用 uv tool 安装
uv tool install biliup

# 验证安装
biliup --version

# 启动服务
biliup server --auth
```

#### 升级版本

```bash
uv tool upgrade biliup
```

### 方式二：使用 pip 安装

```bash
# 安装 biliup
pip install biliup

# 或者使用 pip3（如果系统同时有 Python 2 和 3）
pip3 install biliup

# 验证安装
biliup --version
```

### 方式三：使用包管理器

某些 Linux 发行版可能提供了 biliup 的预编译包。

#### Arch Linux (AUR)

```bash
# 使用 yay 或其他 AUR 助手
yay -S biliup
```

### 配置后台运行

#### 使用 nohup

```bash
# 后台运行
nohup biliup server --auth > biliup.log 2>&1 &

# 查看日志
tail -f biliup.log

# 停止服务
pkill biliup
```

#### 使用 systemd（推荐）

创建 systemd 服务文件 `/etc/systemd/system/biliup.service`：

```ini
[Unit]
Description=Biliup Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/biliup
ExecStart=/home/your-username/.local/bin/biliup server --auth
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启用和启动服务：

```bash
# 重新加载 systemd 配置
sudo systemctl daemon-reload

# 启用开机自启动
sudo systemctl enable biliup

# 启动服务
sudo systemctl start biliup

# 查看状态
sudo systemctl status biliup

# 查看日志
sudo journalctl -u biliup -f
```

#### 使用 screen 或 tmux

```bash
# 使用 screen
screen -S biliup
biliup server --auth
# 按 Ctrl+A 然后按 D 分离会话

# 重新连接
screen -r biliup

# 使用 tmux
tmux new -s biliup
biliup server --auth
# 按 Ctrl+B 然后按 D 分离会话

# 重新连接
tmux attach -t biliup
```

## macOS 平台

### 方式一：使用 uv 安装（推荐）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装 biliup
uv tool install biliup

# 验证安装
biliup --version

# 启动服务
biliup server --auth
```

### 方式二：使用 Homebrew

```bash
# 安装 Python（如果尚未安装）
brew install python@3.9

# 使用 pip 安装 biliup
pip3 install biliup

# 验证安装
biliup --version
```

### 配置开机自启动

创建 LaunchAgent 配置文件 `~/Library/LaunchAgents/com.biliup.server.plist`：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.biliup.server</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/your-username/.local/bin/biliup</string>
        <string>server</string>
        <string>--auth</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/your-username/biliup</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/Users/your-username/biliup/biliup.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/your-username/biliup/biliup.error.log</string>
</dict>
</plist>
```

加载服务：

```bash
# 加载服务
launchctl load ~/Library/LaunchAgents/com.biliup.server.plist

# 卸载服务
launchctl unload ~/Library/LaunchAgents/com.biliup.server.plist
```

## Docker 安装

Docker 提供了跨平台的容器化部署方案，适合在服务器上运行。

### 拉取镜像

```bash
docker pull ghcr.io/biliup/caution:latest
```

### 基本运行

```bash
docker run -d \
  --name biliup \
  -p 19159:19159 \
  ghcr.io/biliup/caution:latest
```

### 数据持久化

为了保存配置文件和录制的视频，需要挂载数据卷：

```bash
docker run -d \
  --name biliup \
  -p 19159:19159 \
  -v /path/to/config:/app/config \
  -v /path/to/downloads:/app/downloads \
  -v /path/to/cookies:/app/cookies \
  ghcr.io/biliup/caution:latest
```

### 使用 Docker Compose

创建 `docker-compose.yml` 文件：

```yaml
version: '3.8'

services:
  biliup:
    image: ghcr.io/biliup/caution:latest
    container_name: biliup
    ports:
      - "19159:19159"
    volumes:
      - ./config:/app/config
      - ./downloads:/app/downloads
      - ./cookies:/app/cookies
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
```

启动服务：

```bash
# 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止
docker-compose down
```

### Docker 常用命令

```bash
# 查看容器状态
docker ps

# 查看日志
docker logs -f biliup

# 进入容器
docker exec -it biliup /bin/bash

# 重启容器
docker restart biliup

# 停止容器
docker stop biliup

# 删除容器
docker rm biliup
```

## 从源码安装

适合开发者和需要最新功能的高级用户。

### 前置要求

- **Node.js**: 18 或更高版本
- **Rust**: 最新稳定版
- **Python**: 3.9 或更高版本
- **Git**: 用于克隆代码仓库

### 克隆代码仓库

```bash
git clone https://github.com/biliup/biliup.git
cd biliup
```

### 安装前端依赖

```bash
# 安装 Node.js 依赖
npm install

# 构建前端
npm run build
```

### 编译 Rust 后端

```bash
# 安装 maturin（Python 打包工具）
pip install maturin

# 开发模式编译
maturin dev

# 或者构建发布版本
maturin build --release
```

### 安装 Python 依赖

```bash
# 安装依赖
pip install -e .

# 或者使用 uv
uv pip install -e .
```

### 运行开发服务器

```bash
# 启动 biliup
python -m biliup server --auth

# 或者直接使用命令
biliup server --auth
```

### 更新代码

```bash
# 拉取最新代码
git pull

# 重新构建前端
npm run build

# 重新编译后端
maturin dev
```

## Termux 安装

在 Android 设备上使用 Termux 运行 biliup。

详细安装步骤请参考：[Termux 中使用 biliup](https://github.com/biliup/biliup/wiki/Termux-%E4%B8%AD%E4%BD%BF%E7%94%A8-biliup)

## 常见安装问题

### Python 版本不兼容

**问题**: 提示 Python 版本过低

**解决方案**:
```bash
# 检查 Python 版本
python --version

# 如果版本低于 3.9，需要升级 Python
# Linux: 使用包管理器安装
sudo apt install python3.9  # Debian/Ubuntu
sudo yum install python39   # CentOS/RHEL

# macOS: 使用 Homebrew
brew install python@3.9

# Windows: 从官网下载安装
# https://www.python.org/downloads/
```

### pip 安装失败

**问题**: 网络问题导致安装失败

**解决方案**:
```bash
# 使用国内镜像源
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple biliup

# 或者配置永久镜像源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### 权限问题

**问题**: Linux/macOS 上提示权限不足

**解决方案**:
```bash
# 使用 --user 参数安装到用户目录
pip install --user biliup

# 或者使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows
pip install biliup
```

### 端口被占用

**问题**: 19159 端口已被其他程序占用

**解决方案**:
```bash
# 使用其他端口启动
biliup server --port 8080

# 或者查找并关闭占用端口的程序
# Linux/macOS
lsof -i :19159
kill -9 <PID>

# Windows
netstat -ano | findstr :19159
taskkill /PID <PID> /F
```

### Docker 网络问题

**问题**: Docker 容器无法访问外网

**解决方案**:
```bash
# 检查 Docker 网络配置
docker network ls

# 使用主机网络模式
docker run -d --network host ghcr.io/biliup/caution:latest
```

### 依赖冲突

**问题**: 安装时提示依赖包冲突

**解决方案**:
```bash
# 使用虚拟环境隔离依赖
python -m venv biliup-env
source biliup-env/bin/activate  # Linux/macOS
# 或 biliup-env\Scripts\activate  # Windows
pip install biliup

# 或者使用 uv 管理依赖
uv venv
source .venv/bin/activate
uv pip install biliup
```

## 验证安装

安装完成后，运行以下命令验证：

```bash
# 查看版本信息
biliup --version

# 查看帮助信息
biliup --help

# 启动服务测试
biliup server --auth
```

如果一切正常，你应该能看到服务启动的日志信息，并能在浏览器中访问 `http://localhost:19159`。

## 下一步

安装完成后，你可以：

- [完成第一次录制](../first-recording/)，体验 biliup 的核心功能
- [查看配置参考](../../configuration/)，了解所有配置选项
- [阅读用户指南](../../user-guide/)，掌握高级功能

## 获取帮助

如果遇到安装问题：

- 查看[常见问题](../../help/faq/)
- 查看[故障排查指南](../../user-guide/troubleshooting/)
- 在 [GitHub Issues](https://github.com/biliup/biliup/issues) 提问
- 加入 [Telegram 群组](https://t.me/+IkpIABHqy6U0ZTQ5) 获取社区帮助
