+++
title = "源码编译"
description = "从源码编译 biliup 项目的各个组件"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 30
template = "docs/page.html"

[extra]
lead = "本文档详细说明如何从源码编译 biliup 的前端、后端和 Python 模块，以及如何运行开发服务器和构建发布版本。"
toc = true
top = false
+++

## 前提条件

在开始编译之前，确保你已经：

1. 完成[开发环境搭建](./setup-dev-environment.md)
2. 克隆了项目代码
3. 安装了所有必需的依赖

## 编译前端

前端使用 Next.js 框架，支持开发模式和生产构建。

### 开发模式

开发模式支持热重载，适合开发调试：

```bash
# 在项目根目录执行
npm run dev
```

**输出示例**:

```
  ▲ Next.js 14.2.26
  - Local:        http://localhost:3000
  - Network:      http://192.168.1.100:3000

 ✓ Ready in 2.5s
```

访问 `http://localhost:3000` 查看应用。

**开发模式特性**:

- 快速刷新 (Fast Refresh)
- 源码映射 (Source Maps)
- 详细的错误信息
- 自动重新编译

### 生产构建

生产构建会优化代码，减小体积：

```bash
# 构建生产版本
npm run build
```

**构建过程**:

1. **类型检查**: 检查 TypeScript 类型错误
2. **代码检查**: 运行 ESLint
3. **编译**: 编译 TypeScript 和 React 代码
4. **优化**: 压缩和优化代码
5. **生成静态文件**: 生成 HTML、CSS、JS 文件

**输出示例**:

```
Route (app)                              Size     First Load JS
┌ ○ /                                    5.2 kB         95.3 kB
├ ○ /_not-found                          871 B          85.9 kB
├ ○ /dashboard                           8.1 kB         98.2 kB
├ ○ /history                             6.5 kB         96.6 kB
├ ○ /job                                 7.3 kB         97.4 kB
├ ○ /login                               4.8 kB         94.9 kB
├ ○ /streamers                           9.2 kB         99.3 kB
└ ○ /upload-manager                      8.7 kB         98.8 kB

○  (Static)  automatically rendered as static HTML
```

### 启动生产服务器

```bash
# 启动生产服务器
npm run start
```

这将启动一个优化的 Node.js 服务器，服务于构建好的应用。

### 前端构建选项

#### 环境变量

创建 `.env.production` 文件：

```bash
# API 地址
NEXT_PUBLIC_API_URL=http://localhost:19159

# 其他配置
NEXT_PUBLIC_ENABLE_ANALYTICS=false
```

#### 自定义配置

编辑 `next.config.js`：

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',  // 独立输出
  compress: true,        // 启用 gzip 压缩
  reactStrictMode: true, // React 严格模式
}

module.exports = nextConfig
```


## 编译 Rust 后端

Rust 后端包含三个 crate，使用 Cargo 工作空间管理。

### 开发构建

开发构建包含调试信息，编译速度快：

```bash
# 构建所有 crate
cargo build

# 构建特定 crate
cargo build -p biliup-cli
cargo build -p biliup
cargo build -p stream-gears
```

**输出位置**: `target/debug/`

**输出示例**:

```
   Compiling serde v1.0.193
   Compiling tokio v1.35.1
   Compiling biliup v1.1.22
   Compiling biliup-cli v1.1.22
   Compiling stream-gears v1.1.22
    Finished dev [unoptimized + debuginfo] target(s) in 2m 30s
```

### 发布构建

发布构建会进行优化，生成更小更快的二进制文件：

```bash
# 构建发布版本
cargo build --release

# 构建特定 crate
cargo build --release -p biliup-cli
```

**输出位置**: `target/release/`

**优化选项** (在 `Cargo.toml` 中配置):

```toml
[profile.release]
lto = true              # 链接时优化
codegen-units = 1       # 单个代码生成单元
strip = true            # 移除调试符号
opt-level = 3           # 最高优化级别
```

**构建时间对比**:

- 开发构建: ~2-3 分钟
- 发布构建: ~5-10 分钟 (首次)
- 增量构建: ~10-30 秒

### 运行 Rust 程序

#### 直接运行

```bash
# 开发模式运行
cargo run --bin biliup-cli -- server

# 发布模式运行
cargo run --release --bin biliup-cli -- server

# 传递参数
cargo run --bin biliup-cli -- server --port 8080 --auth
```

#### 运行编译好的二进制文件

```bash
# 开发版本
./target/debug/biliup-cli server

# 发布版本
./target/release/biliup-cli server --auth
```

### 检查代码

```bash
# 检查代码是否能编译 (不生成二进制文件)
cargo check

# 检查所有 crate
cargo check --workspace

# 检查特定 crate
cargo check -p biliup-cli
```

### 运行测试

```bash
# 运行所有测试
cargo test

# 运行特定 crate 的测试
cargo test -p biliup

# 运行特定测试
cargo test test_upload

# 显示测试输出
cargo test -- --nocapture
```

### 代码格式化和检查

```bash
# 格式化代码
cargo fmt

# 检查格式
cargo fmt -- --check

# 运行 Clippy (代码检查)
cargo clippy

# Clippy 严格模式
cargo clippy -- -D warnings
```


## 编译 Python 模块

Python 模块包含纯 Python 代码和 Rust 扩展 (stream-gears)。

### 使用 Maturin 开发模式

Maturin 是推荐的开发方式，支持快速迭代：

```bash
# 安装为可编辑模式 (开发模式)
maturin dev

# 发布模式编译
maturin dev --release
```

**maturin dev 做了什么**:

1. 编译 Rust 扩展 (stream-gears)
2. 安装 Python 依赖
3. 将包安装为可编辑模式
4. 可以直接导入 `biliup` 模块

**输出示例**:

```
🔗 Found pyo3 bindings
🐍 Found CPython 3.11 at /usr/bin/python3
   Compiling stream-gears v1.1.22
    Finished dev [unoptimized + debuginfo] target(s) in 45.2s
📦 Built wheel for CPython 3.11 to /tmp/.tmpXXXXXX/biliup-1.1.22-cp311-cp311-linux_x86_64.whl
✏️  Setting installed package as editable
🛠 Installed biliup-1.1.22
```

### 使用 pip 安装

```bash
# 安装为可编辑模式
pip install -e .

# 安装所有依赖
pip install -e ".[selenium]"
```

### 构建 Wheel 包

#### 使用 Maturin

```bash
# 构建 wheel 包
maturin build

# 发布模式构建
maturin build --release

# 指定 Python 版本
maturin build --release --interpreter python3.11
```

**输出位置**: `target/wheels/`

**输出示例**:

```
📦 Built wheel for CPython 3.11 to target/wheels/biliup-1.1.22-cp311-cp311-linux_x86_64.whl
```

#### 使用 Python build

```bash
# 安装 build 工具
pip install build

# 构建包
python -m build

# 只构建 wheel
python -m build --wheel

# 只构建 sdist
python -m build --sdist
```

**输出位置**: `dist/`

### 安装构建好的包

```bash
# 安装 wheel 包
pip install target/wheels/biliup-1.1.22-cp311-cp311-linux_x86_64.whl

# 或从 dist/ 安装
pip install dist/biliup-1.1.22-py3-none-any.whl
```

### 验证安装

```bash
# 检查版本
python -c "import biliup; print(biliup.__version__)"

# 运行命令行工具
biliup --version

# 测试导入
python -c "from biliup.engine import download; print('OK')"
```

### Python 开发模式

在开发模式下，修改 Python 代码会立即生效，无需重新安装：

```bash
# 安装为可编辑模式
maturin dev

# 修改 Python 代码
vim biliup/engine/download.py

# 直接测试，无需重新安装
python -m biliup download https://...
```

**注意**: 修改 Rust 代码需要重新运行 `maturin dev`。


## 运行开发服务器

### 完整开发环境

需要同时运行前端和后端服务器。

#### 方式 1: 使用多个终端

**终端 1 - 前端开发服务器**:

```bash
npm run dev
```

访问: `http://localhost:3000`

**终端 2 - 后端服务器**:

```bash
# 使用 cargo run
cargo run --bin biliup-cli -- server --auth

# 或使用 Python 模块
python -m biliup server --auth
```

访问: `http://localhost:19159`

#### 方式 2: 使用 tmux

```bash
# 创建新会话
tmux new -s biliup

# 分割窗口
Ctrl+b "

# 上窗口运行前端
npm run dev

# 切换到下窗口
Ctrl+b ↓

# 下窗口运行后端
cargo run --bin biliup-cli -- server --auth
```

#### 方式 3: 使用 Docker Compose

```bash
# 启动所有服务
docker-compose up

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 开发服务器配置

#### 前端代理配置

编辑 `next.config.js` 添加 API 代理：

```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:19159/api/:path*',
      },
    ]
  },
}
```

#### 后端 CORS 配置

后端默认允许跨域请求，可在代码中配置：

```rust
// crates/biliup-cli/src/main.rs
let cors = CorsLayer::new()
    .allow_origin("http://localhost:3000".parse::<HeaderValue>().unwrap())
    .allow_methods([Method::GET, Method::POST])
    .allow_headers(Any);
```

### 热重载

#### 前端热重载

Next.js 自动支持热重载，修改代码后浏览器会自动刷新。

#### 后端热重载

使用 `cargo-watch` 实现自动重新编译：

```bash
# 安装 cargo-watch
cargo install cargo-watch

# 监听文件变化并重新运行
cargo watch -x 'run --bin biliup-cli -- server'

# 只在成功编译后运行
cargo watch -x check -x 'run --bin biliup-cli -- server'
```

#### Python 热重载

Python 代码修改后自动生效（可编辑模式）：

```bash
# 安装为可编辑模式
maturin dev

# 修改 Python 代码后直接生效
# 修改 Rust 代码需要重新运行 maturin dev
```

## 构建发布版本

### 完整构建流程

```bash
# 1. 构建前端
npm run build

# 2. 构建 Rust 后端
cargo build --release

# 3. 构建 Python 包
maturin build --release

# 4. 复制前端静态文件到后端
cp -r .next/static public/
```

### 创建独立可执行文件

#### Linux

```bash
# 构建静态链接的二进制文件
cargo build --release --target x86_64-unknown-linux-musl

# 输出位置
ls -lh target/x86_64-unknown-linux-musl/release/biliup-cli
```

#### macOS

```bash
# 构建 universal binary (支持 Intel 和 Apple Silicon)
cargo build --release --target x86_64-apple-darwin
cargo build --release --target aarch64-apple-darwin

# 合并为 universal binary
lipo -create \
  target/x86_64-apple-darwin/release/biliup-cli \
  target/aarch64-apple-darwin/release/biliup-cli \
  -output biliup-cli-universal
```

#### Windows

```bash
# 在 Windows 上构建
cargo build --release --target x86_64-pc-windows-msvc

# 输出位置
dir target\x86_64-pc-windows-msvc\release\biliup-cli.exe
```

### 打包发布

#### 创建 tarball

```bash
# 创建发布目录
mkdir -p release/biliup-1.1.22

# 复制文件
cp target/release/biliup-cli release/biliup-1.1.22/
cp -r .next release/biliup-1.1.22/
cp -r public release/biliup-1.1.22/
cp README.md LICENSE release/biliup-1.1.22/

# 打包
cd release
tar czf biliup-1.1.22-linux-x86_64.tar.gz biliup-1.1.22/
```

#### 创建 Docker 镜像

```bash
# 构建镜像
docker build -t biliup:1.1.22 .

# 标记版本
docker tag biliup:1.1.22 biliup:latest

# 推送到仓库
docker push biliup:1.1.22
```

## 性能优化

### 编译速度优化

#### 使用 sccache

```bash
# 安装 sccache
cargo install sccache

# 配置环境变量
export RUSTC_WRAPPER=sccache

# 查看缓存统计
sccache --show-stats
```

#### 使用 mold 链接器

```bash
# 安装 mold (Linux)
sudo apt install mold

# 配置 Cargo
# .cargo/config.toml
[target.x86_64-unknown-linux-gnu]
linker = "clang"
rustflags = ["-C", "link-arg=-fuse-ld=mold"]
```

#### 并行编译

```bash
# 设置并行任务数
export CARGO_BUILD_JOBS=8

# 或在 Cargo.toml 中配置
[build]
jobs = 8
```

### 二进制文件大小优化

#### 移除调试符号

```toml
# Cargo.toml
[profile.release]
strip = true
```

#### 使用 UPX 压缩

```bash
# 安装 UPX
sudo apt install upx

# 压缩二进制文件
upx --best --lzma target/release/biliup-cli

# 压缩前后对比
ls -lh target/release/biliup-cli
```

## 常见问题

### Rust 编译内存不足

**解决方案**:

```bash
# 减少并行任务数
export CARGO_BUILD_JOBS=2

# 或使用 minimal profile
cargo build --profile minimal
```

### Python 扩展编译失败

**解决方案**:

```bash
# 确保安装了 Python 开发头文件
sudo apt install python3-dev

# 更新 maturin
pip install --upgrade maturin

# 清理并重新构建
cargo clean
maturin dev
```

### 前端构建内存不足

**解决方案**:

```bash
# 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=4096"

# 重新构建
npm run build
```

### 链接错误

**解决方案**:

```bash
# 更新 Rust 工具链
rustup update

# 清理构建缓存
cargo clean

# 重新构建
cargo build
```

## 下一步

构建完成后，你可以：

1. 阅读[插件开发](./plugin-development.md)了解如何扩展功能
2. 阅读[测试指南](./testing.md)了解如何测试代码
3. 阅读[调试技巧](./debugging.md)了解如何调试问题

## 相关链接

- [Cargo 文档](https://doc.rust-lang.org/cargo/)
- [Maturin 文档](https://www.maturin.rs/)
- [Next.js 构建文档](https://nextjs.org/docs/deployment)
