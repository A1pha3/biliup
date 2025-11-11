+++
title = "项目结构"
description = "详细说明 biliup 项目的目录结构和代码组织"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 20
template = "docs/page.html"

[extra]
lead = "本文档详细介绍 biliup 项目的目录结构，包括前端、后端和 Python 引擎的代码组织方式。"
toc = true
top = false
+++

## 项目概览

biliup 采用混合架构，包含三个主要部分：

- **前端**: Next.js + React + TypeScript
- **后端**: Rust (Axum Web 框架)
- **Python 引擎**: Python 3.9+ (下载和插件系统)

## 根目录结构

```
biliup/
├── app/                    # Next.js 前端应用
├── biliup/                 # Python 引擎包
├── crates/                 # Rust 后端代码
├── docs/                   # 文档站点 (Zola)
├── public/                 # 静态资源文件
├── tauri-app/              # Tauri 桌面应用 (可选)
├── .github/                # GitHub Actions 工作流
├── Cargo.toml              # Rust 工作空间配置
├── pyproject.toml          # Python 项目配置
├── package.json            # Node.js 项目配置
├── next.config.js          # Next.js 配置
├── tsconfig.json           # TypeScript 配置
├── docker-compose.yml      # Docker 编排配置
└── README.md               # 项目说明
```

## 前端代码结构 (app/)

前端使用 Next.js 14 的 App Router 架构。

### 目录组织

```
app/
├── (app)/                  # 主应用路由组
│   ├── dashboard/          # 仪表板页面
│   ├── history/            # 历史记录页面
│   ├── job/                # 任务管理页面
│   ├── logviewer/          # 日志查看器页面
│   ├── status/             # 状态监控页面
│   ├── streamers/          # 主播管理页面
│   ├── upload-manager/     # 上传管理页面
│   ├── layout.tsx          # 应用布局组件
│   └── page.tsx            # 首页
├── (auth)/                 # 认证路由组
│   └── login/              # 登录页面
├── lib/                    # 工具库和 API 客户端
│   ├── utils/              # 通用工具函数
│   ├── api-streamer.ts     # 主播 API 客户端
│   └── use-streamers.ts    # 主播数据 Hook
├── styles/                 # 样式文件
│   ├── dashboard.module.scss
│   ├── globals.css
│   └── Home.module.css
├── ui/                     # UI 组件
│   ├── AvatarCard/         # 头像卡片组件
│   ├── plugins/            # 插件相关组件
│   ├── StreamerActions/    # 主播操作组件
│   ├── OverrideModal.tsx   # 覆盖配置模态框
│   ├── Player.tsx          # 视频播放器
│   ├── QRcode.tsx          # 二维码组件
│   ├── TemplateFields.tsx  # 模板字段组件
│   ├── TemplateModal.tsx   # 模板模态框
│   ├── ThemeButton.tsx     # 主题切换按钮
│   └── UserList.tsx        # 用户列表组件
├── layout.tsx              # 根布局
├── globals.css             # 全局样式
└── favicon.ico             # 网站图标
```

### 关键文件说明

#### 路由组织

- **(app)/**: 使用括号创建路由组，不影响 URL 路径
- **layout.tsx**: 定义页面布局，包含导航栏和侧边栏
- **page.tsx**: 页面组件，对应具体路由

#### 组件组织

- **ui/**: 可复用的 UI 组件
- **lib/**: 业务逻辑和 API 调用
- **styles/**: CSS 模块和全局样式


## 后端代码结构 (crates/)

后端使用 Rust 编写，采用 Cargo 工作空间管理多个 crate。

### 目录组织

```
crates/
├── biliup/                 # 核心上传库
│   ├── src/
│   │   ├── bilibili/       # Bilibili API 客户端
│   │   ├── error.rs        # 错误类型定义
│   │   ├── lib.rs          # 库入口
│   │   └── uploader.rs     # 上传逻辑
│   └── Cargo.toml
├── biliup-cli/             # Web 服务器和 CLI
│   ├── src/
│   │   ├── api/            # REST API 路由
│   │   ├── auth/           # 认证中间件
│   │   ├── config/         # 配置管理
│   │   ├── database/       # 数据库操作
│   │   ├── models/         # 数据模型
│   │   ├── ws/             # WebSocket 处理
│   │   ├── main.rs         # 程序入口
│   │   └── lib.rs          # 库入口
│   └── Cargo.toml
└── stream-gears/           # Python 绑定
    ├── src/
    │   ├── lib.rs          # PyO3 绑定入口
    │   └── downloader.rs   # 下载器绑定
    └── Cargo.toml
```

### 关键模块说明

#### biliup (核心库)

- **bilibili/**: Bilibili API 封装
  - 登录认证
  - 视频上传
  - 稿件管理
- **uploader.rs**: 上传逻辑实现
  - 分片上传
  - 断点续传
  - 进度回调

#### biliup-cli (Web 服务)

- **api/**: REST API 端点
  - `/api/streamers`: 主播管理
  - `/api/upload`: 上传管理
  - `/api/config`: 配置管理
- **auth/**: 用户认证
  - JWT 令牌验证
  - 密码哈希
- **database/**: 数据库层
  - SQLite 连接池
  - 查询构建器
  - 迁移管理
- **ws/**: WebSocket 服务
  - 实时日志推送
  - 任务状态更新

#### stream-gears (Python 绑定)

- 使用 PyO3 将 Rust 功能暴露给 Python
- 提供高性能的下载器实现
- 桥接 Rust 和 Python 生态

### Cargo 工作空间配置

`Cargo.toml` 定义了工作空间和共享依赖：

```toml
[workspace]
members = [
    "crates/biliup",
    "crates/biliup-cli",
    "crates/stream-gears",
]

[workspace.dependencies]
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["macros", "rt-multi-thread"] }
# ... 其他共享依赖
```


## Python 代码结构 (biliup/)

Python 引擎负责下载和插件系统。

### 目录组织

```
biliup/
├── common/                 # 通用工具模块
│   ├── tars/               # TARS 协议支持
│   ├── __init__.py
│   ├── abogus.py           # 抖音 A-Bogus 签名
│   ├── configlog.ini       # 日志配置
│   ├── Daemon.py           # 守护进程
│   ├── log.py              # 日志工具
│   ├── reload.py           # 热重载
│   └── util.py             # 通用工具函数
├── Danmaku/                # 弹幕系统
│   ├── douyin_util/        # 抖音弹幕工具
│   ├── paramgen/           # 参数生成器
│   ├── __init__.py
│   ├── bilibili.py         # B站弹幕
│   ├── douyin.py           # 抖音弹幕
│   ├── douyu.py            # 斗鱼弹幕
│   ├── huya.py             # 虎牙弹幕
│   ├── twitcasting.py      # TwitCasting 弹幕
│   ├── twitch.py           # Twitch 弹幕
│   └── youtube.py          # YouTube 弹幕
├── engine/                 # 下载引擎
│   ├── __init__.py
│   ├── decorators.py       # 装饰器
│   ├── download.py         # 异步下载器
│   ├── sync_downloader.py  # 同步下载器
│   └── upload.py           # 上传调度
├── plugins/                # 平台插件
│   ├── huya_wup/           # 虎牙 WUP 协议
│   ├── __init__.py
│   ├── acfun.py            # AcFun
│   ├── afreecaTV.py        # AfreecaTV
│   ├── bigo.py             # Bigo Live
│   ├── bili_chromeup.py    # B站 Chrome 上传
│   ├── bili_webup_sync.py  # B站同步上传
│   ├── bili_webup.py       # B站异步上传
│   ├── bilibili.py         # B站下载
│   ├── biliuprs.py         # Rust 上传器
│   ├── cc.py               # 网易 CC
│   ├── douyin.py           # 抖音
│   ├── douyu.py            # 斗鱼
│   ├── general.py          # 通用下载器
│   ├── huya.py             # 虎牙
│   ├── inke.py             # 映客
│   ├── kilakila.py         # KilaKila
│   ├── kuaishou.py         # 快手
│   ├── missevan.py         # 猫耳FM
│   ├── nico.py             # Niconico
│   ├── noop_uploader.py    # 空上传器
│   ├── picarto.py          # Picarto
│   ├── stream_gears.py     # Rust 下载器
│   ├── ttinglive.py        # 听听直播
│   ├── twitcasting.py      # TwitCasting
│   ├── twitch.py           # Twitch
│   └── youtube.py          # YouTube
├── __init__.py             # 包初始化
├── __main__.py             # 命令行入口
└── config.py               # 配置管理
```

### 关键模块说明

#### common/ (通用工具)

- **util.py**: 通用工具函数
  - 文件操作
  - 时间处理
  - 字符串处理
- **log.py**: 日志配置和管理
- **Daemon.py**: 守护进程支持
- **abogus.py**: 抖音签名算法

#### Danmaku/ (弹幕系统)

每个平台一个模块，实现弹幕协议：

- **连接管理**: WebSocket 或 TCP 连接
- **消息解析**: 解析平台特定的弹幕格式
- **事件处理**: 处理弹幕、礼物、进入房间等事件

示例结构：

```python
class BilibiliDanmaku:
    async def connect(self):
        """连接弹幕服务器"""
        
    async def receive(self):
        """接收弹幕消息"""
        
    def parse_message(self, data):
        """解析消息"""
```

#### engine/ (下载引擎)

- **download.py**: 异步下载器
  - 流媒体下载
  - 分段下载
  - 重试机制
- **sync_downloader.py**: 同步下载器
  - 兼容旧代码
- **upload.py**: 上传调度
  - 任务队列
  - 上传管理
- **decorators.py**: 装饰器
  - 重试装饰器
  - 日志装饰器

#### plugins/ (平台插件)

每个平台一个插件文件，实现下载和上传逻辑。

**插件基类结构**:

```python
class BaseLive:
    def __init__(self, fname, url, suffix='flv'):
        self.fname = fname
        self.url = url
        self.suffix = suffix
    
    async def acheck(self):
        """检查直播状态"""
        
    async def download(self):
        """下载直播流"""
```

**上传器基类结构**:

```python
class BaseUploader:
    def __init__(self, config):
        self.config = config
    
    async def upload(self, file_path):
        """上传视频"""
```

### Python 包配置

`pyproject.toml` 定义了包信息和依赖：

```toml
[project]
name = "biliup"
requires-python = ">= 3.9"
dependencies = [
    "aiohttp[speedups] >= 3.9.5",
    "streamlink >= 7.5.0",
    "yt-dlp >= 2025.7.21",
    # ... 其他依赖
]

[project.scripts]
biliup = "biliup.__main__:arg_parser"
```


## 配置文件和资源

### 配置文件位置

```
项目根目录/
├── .env                    # 环境变量 (不提交)
├── .env.development        # 开发环境变量
├── .env.production         # 生产环境变量
├── next.config.js          # Next.js 配置
├── tsconfig.json           # TypeScript 配置
├── .eslintrc.json          # ESLint 配置
├── .prettierrc.toml        # Prettier 配置
├── docker-compose.yml      # Docker 编排
└── Dockerfile              # Docker 镜像构建

运行时配置/
├── config.yaml             # 主配置文件
├── cookies.json            # 登录凭证
└── biliup.db               # SQLite 数据库
```

### 配置文件说明

#### config.yaml

主配置文件，包含：

- 主播列表和录制配置
- 上传模板和参数
- 插件配置
- 系统设置

示例结构：

```yaml
streamers:
  主播名称:
    url: https://live.bilibili.com/123456
    template: 默认模板
    
templates:
  默认模板:
    title: "{streamer}的直播回放"
    tid: 171
    tags: ["直播", "录播"]
```

#### cookies.json

存储 Bilibili 登录凭证：

```json
{
  "cookies": {
    "SESSDATA": "...",
    "bili_jct": "...",
    "DedeUserID": "..."
  },
  "access_token": "...",
  "refresh_token": "..."
}
```

#### biliup.db

SQLite 数据库，存储：

- 用户账号信息
- 录制任务状态
- 上传历史记录
- 系统日志

### 静态资源 (public/)

```
public/
├── config.toml             # 示例配置
├── config.yaml             # 示例配置
├── favicon.png             # 网站图标
├── logo.png                # Logo
├── noface.jpg              # 默认头像
├── global.css              # 全局样式
└── index.html              # 静态首页
```

## 文档站点 (docs/)

使用 Zola 静态站点生成器构建。

```
docs/
├── content/                # 文档内容
│   └── docs/               # 文档章节
│       ├── getting-started/
│       ├── user-guide/
│       ├── configuration/
│       ├── architecture/
│       └── development/
├── themes/                 # 主题文件
├── config.toml             # Zola 配置
└── README.md
```

## 测试文件组织

### Rust 测试

```
crates/biliup/
├── src/
│   └── lib.rs
└── tests/                  # 集成测试
    └── upload_test.rs

# 单元测试在源文件中
// src/uploader.rs
#[cfg(test)]
mod tests {
    #[test]
    fn test_upload() {
        // 测试代码
    }
}
```

### Python 测试

```
tests/                      # 测试目录
├── __init__.py
├── test_download.py        # 下载测试
├── test_upload.py          # 上传测试
└── test_plugins.py         # 插件测试
```

### 前端测试

```
app/
├── __tests__/              # 测试文件
│   ├── components/
│   └── pages/
└── jest.config.js          # Jest 配置
```

## 构建产物

### 开发构建

```
target/                     # Rust 构建产物
├── debug/                  # 调试版本
│   ├── biliup-cli          # CLI 可执行文件
│   └── libbiliup.rlib      # 库文件
└── release/                # 发布版本

.next/                      # Next.js 构建产物
├── cache/                  # 构建缓存
└── server/                 # 服务器端代码

dist/                       # Python 构建产物
└── biliup-*.whl            # Wheel 包
```

### 生产构建

```
out/                        # Next.js 静态导出
├── _next/
├── index.html
└── ...

target/release/             # Rust 发布版本
└── biliup-cli              # 优化的可执行文件
```

## 开发工具配置

### VS Code 配置 (.vscode/)

```
.vscode/
├── settings.json           # 编辑器设置
├── launch.json             # 调试配置
└── extensions.json         # 推荐扩展
```

### Git 配置

```
.gitignore                  # Git 忽略文件
.gitmodules                 # Git 子模块
```

## 目录导航建议

### 前端开发

1. 页面开发: `app/(app)/`
2. 组件开发: `app/ui/`
3. API 调用: `app/lib/`
4. 样式调整: `app/styles/`

### 后端开发

1. API 开发: `crates/biliup-cli/src/api/`
2. 数据库: `crates/biliup-cli/src/database/`
3. 核心逻辑: `crates/biliup/src/`
4. Python 绑定: `crates/stream-gears/src/`

### Python 开发

1. 插件开发: `biliup/plugins/`
2. 弹幕开发: `biliup/Danmaku/`
3. 引擎开发: `biliup/engine/`
4. 工具开发: `biliup/common/`

## 相关文档

- [开发环境搭建](./setup-dev-environment.md)
- [源码编译](./building-from-source.md)
- [插件开发](./plugin-development.md)
- [架构设计](../architecture/overview.md)
