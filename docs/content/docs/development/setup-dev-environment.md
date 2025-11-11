+++
title = "开发环境搭建"
description = "配置 biliup 项目的开发环境，包括必需的工具和依赖安装"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 10
template = "docs/page.html"

[extra]
lead = "本文档将指导你搭建 biliup 项目的完整开发环境，包括前端、后端和 Python 引擎的开发工具配置。"
toc = true
top = false
+++

## 系统要求

在开始之前，确保你的系统满足以下要求：

### 操作系统

- **Linux**: Ubuntu 20.04+、Debian 11+、Fedora 35+ 或其他主流发行版
- **macOS**: macOS 11 (Big Sur) 或更高版本
- **Windows**: Windows 10/11（推荐使用 WSL2）

### 硬件要求

- **CPU**: 双核或更高
- **内存**: 至少 4GB RAM（推荐 8GB+）
- **磁盘**: 至少 10GB 可用空间

## 必需的开发工具

### 1. Git

用于版本控制和代码管理。

**安装方法**:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install git

# macOS (使用 Homebrew)
brew install git

# Windows
# 下载安装包: https://git-scm.com/download/win
```

**验证安装**:

```bash
git --version
# 输出示例: git version 2.34.1
```

### 2. Node.js

用于前端开发，需要 Node.js 18 或更高版本。

**安装方法**:

```bash
# 使用 nvm (推荐)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 18
nvm use 18

# Ubuntu/Debian (使用 NodeSource)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# macOS (使用 Homebrew)
brew install node@18

# Windows
# 下载安装包: https://nodejs.org/
```

**验证安装**:

```bash
node --version
# 输出示例: v18.17.0

npm --version
# 输出示例: 9.6.7
```

### 3. Rust

用于后端开发，需要 Rust 1.70 或更高版本。

**安装方法**:

```bash
# Linux/macOS
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 选择默认安装选项 (1)
# 安装完成后，重新加载环境变量
source $HOME/.cargo/env

# Windows
# 下载安装包: https://rustup.rs/
```

**验证安装**:

```bash
rustc --version
# 输出示例: rustc 1.75.0 (82e1608df 2023-12-21)

cargo --version
# 输出示例: cargo 1.75.0 (1d8b05cdd 2023-11-20)
```

### 4. Python

用于 Python 引擎开发，需要 Python 3.9 或更高版本。

**安装方法**:

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS (使用 Homebrew)
brew install python@3.11

# Windows
# 下载安装包: https://www.python.org/downloads/
```

**验证安装**:

```bash
python3 --version
# 输出示例: Python 3.11.5

pip3 --version
# 输出示例: pip 23.2.1
```

### 5. uv (Python 包管理器)

uv 是一个快速的 Python 包管理器，用于管理 Python 依赖。

**安装方法**:

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 使用 pip
pip install uv
```

**验证安装**:

```bash
uv --version
# 输出示例: uv 0.1.0
```

### 6. Maturin

用于构建 Rust 和 Python 的混合项目。

**安装方法**:

```bash
# 使用 pip
pip install maturin

# 或使用 cargo
cargo install maturin
```

**验证安装**:

```bash
maturin --version
# 输出示例: maturin 1.4.0
```

## 克隆代码仓库

### Fork 项目

1. 访问 [biliup GitHub 仓库](https://github.com/biliup/biliup)
2. 点击右上角的 "Fork" 按钮
3. 等待 Fork 完成

### 克隆到本地

```bash
# 克隆你 Fork 的仓库
git clone https://github.com/YOUR_USERNAME/biliup.git
cd biliup

# 添加上游仓库
git remote add upstream https://github.com/biliup/biliup.git

# 验证远程仓库
git remote -v
# 输出:
# origin    https://github.com/YOUR_USERNAME/biliup.git (fetch)
# origin    https://github.com/YOUR_USERNAME/biliup.git (push)
# upstream  https://github.com/biliup/biliup.git (fetch)
# upstream  https://github.com/biliup/biliup.git (push)
```

## 安装项目依赖

### 1. 安装前端依赖

```bash
# 在项目根目录执行
npm install

# 或使用 yarn
yarn install
```

这将安装 `package.json` 中定义的所有前端依赖，包括：
- Next.js 框架
- React 和 React DOM
- Semi UI 组件库
- TypeScript 和类型定义

### 2. 安装 Rust 依赖

Rust 依赖会在编译时自动下载，但你可以提前下载：

```bash
# 在项目根目录执行
cargo fetch
```

这将下载 `Cargo.toml` 中定义的所有 Rust 依赖。

### 3. 安装 Python 依赖

```bash
# 使用 maturin 开发模式安装
maturin dev

# 或使用 pip 安装可编辑模式
pip install -e .
```

`maturin dev` 会：
1. 编译 Rust 代码（stream-gears）
2. 安装 Python 依赖
3. 将项目安装为可编辑模式

## 配置开发环境变量

### 创建环境变量文件

在项目根目录创建 `.env.development` 文件：

```bash
# 数据库配置
DATABASE_URL=sqlite:./biliup.db

# 日志级别
RUST_LOG=tower_http=debug,info

# 开发服务器端口
PORT=19159

# 前端开发服务器端口
NEXT_PUBLIC_API_URL=http://localhost:19159
```

### 配置 IDE

#### VS Code

推荐安装以下扩展：

- **Rust Analyzer**: Rust 语言支持
- **Python**: Python 语言支持
- **ESLint**: JavaScript/TypeScript 代码检查
- **Prettier**: 代码格式化

创建 `.vscode/settings.json`：

```json
{
  "rust-analyzer.cargo.features": "all",
  "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
  "editor.formatOnSave": true,
  "[rust]": {
    "editor.defaultFormatter": "rust-lang.rust-analyzer"
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.python"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  }
}
```

#### PyCharm / IntelliJ IDEA

1. 打开项目
2. 配置 Python 解释器：Settings → Project → Python Interpreter
3. 配置 Rust 插件：Settings → Plugins → 搜索并安装 "Rust"
4. 配置 Node.js：Settings → Languages & Frameworks → Node.js

## 验证开发环境

### 1. 编译前端

```bash
npm run build
```

成功输出示例：
```
✓ Compiled successfully
✓ Linting and checking validity of types
✓ Collecting page data
✓ Generating static pages (10/10)
✓ Finalizing page optimization
```

### 2. 编译 Rust 后端

```bash
cargo build
```

成功输出示例：
```
   Compiling biliup v1.1.22
   Compiling biliup-cli v1.1.22
   Compiling stream-gears v1.1.22
    Finished dev [unoptimized + debuginfo] target(s) in 2m 30s
```

### 3. 测试 Python 模块

```bash
python3 -c "import biliup; print(biliup.__version__)"
# 输出: 1.1.22
```

### 4. 运行开发服务器

```bash
# 终端 1: 启动前端开发服务器
npm run dev

# 终端 2: 启动后端服务器
cargo run --bin biliup-cli -- server
```

访问 `http://localhost:3000` 查看前端界面。

## 常见问题

### Rust 编译速度慢

**解决方案**:

1. 使用国内镜像源，编辑 `~/.cargo/config.toml`：

```toml
[source.crates-io]
replace-with = 'ustc'

[source.ustc]
registry = "sparse+https://mirrors.ustc.edu.cn/crates.io-index/"
```

2. 使用 `sccache` 加速编译：

```bash
cargo install sccache
export RUSTC_WRAPPER=sccache
```

### Python 依赖安装失败

**解决方案**:

1. 使用国内 PyPI 镜像：

```bash
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

2. 升级 pip：

```bash
pip install --upgrade pip
```

### Node.js 依赖安装失败

**解决方案**:

1. 使用国内 npm 镜像：

```bash
npm config set registry https://registry.npmmirror.com
```

2. 清除缓存：

```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### maturin dev 失败

**解决方案**:

1. 确保 Rust 工具链已安装：

```bash
rustup default stable
rustup update
```

2. 安装 Python 开发头文件：

```bash
# Ubuntu/Debian
sudo apt install python3-dev

# macOS
# 通常不需要额外安装
```

## 下一步

环境搭建完成后，你可以：

1. 阅读[项目结构](./project-structure.md)了解代码组织
2. 阅读[源码编译](./building-from-source.md)了解构建流程
3. 开始[插件开发](./plugin-development.md)扩展功能

## 相关链接

- [Rust 官方文档](https://www.rust-lang.org/learn)
- [Python 官方文档](https://docs.python.org/3/)
- [Next.js 官方文档](https://nextjs.org/docs)
- [Maturin 文档](https://www.maturin.rs/)
