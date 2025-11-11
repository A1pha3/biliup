+++
title = "调试技巧"
description = "调试 biliup 项目的前端、后端和 Python 代码"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 80
template = "docs/page.html"

[extra]
lead = "本文档提供调试 biliup 各个组件的技巧和工具，包括前端、Rust 后端和 Python 代码的调试方法。"
toc = true
top = false
+++

## 前端调试

### Chrome DevTools

使用 Chrome 开发者工具调试前端代码：

1. 打开 DevTools (F12)
2. 在 Sources 标签设置断点
3. 刷新页面触发断点

**常用功能**:
- **Console**: 查看日志和错误
- **Network**: 查看网络请求
- **Sources**: 设置断点和单步调试
- **React DevTools**: 查看组件状态

### 日志调试

```typescript
// 添加日志
console.log('变量值:', variable);
console.error('错误信息:', error);
console.table(data);  // 表格形式显示数据

// 条件日志
if (process.env.NODE_ENV === 'development') {
  console.log('开发环境日志');
}
```

### React DevTools

安装 React DevTools 扩展：

1. 安装浏览器扩展
2. 打开 DevTools
3. 切换到 Components 或 Profiler 标签

**功能**:
- 查看组件树
- 检查 props 和 state
- 性能分析

## Rust 调试

### 使用 println! 调试

```rust
// 简单调试
println!("变量值: {:?}", variable);

// 格式化输出
println!("用户: {}, ID: {}", user.name, user.id);

// 调试格式
println!("{:#?}", complex_struct);
```

### 使用 dbg! 宏

```rust
// dbg! 会打印表达式和值
let result = dbg!(calculate_something());

// 链式调用
let value = dbg!(some_value)
    .process()
    .dbg!()
    .finalize();
```

### 使用 rust-lldb

```bash
# 编译调试版本
cargo build

# 启动调试器
rust-lldb target/debug/biliup-cli

# 设置断点
(lldb) b main.rs:10

# 运行程序
(lldb) run

# 单步执行
(lldb) step
(lldb) next

# 查看变量
(lldb) print variable_name

# 继续执行
(lldb) continue
```

### VS Code 调试

配置 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Debug biliup-cli",
      "cargo": {
        "args": [
          "build",
          "--bin=biliup-cli",
          "--package=biliup-cli"
        ],
        "filter": {
          "name": "biliup-cli",
          "kind": "bin"
        }
      },
      "args": ["server"],
      "cwd": "${workspaceFolder}"
    }
  ]
}
```

### 日志调试

```rust
use tracing::{debug, info, warn, error};

// 不同级别的日志
debug!("调试信息: {:?}", data);
info!("普通信息");
warn!("警告信息");
error!("错误信息: {}", err);

// 带字段的日志
info!(user_id = %user.id, "用户登录");
```

设置日志级别：

```bash
# 环境变量
export RUST_LOG=debug
export RUST_LOG=biliup=debug,tower_http=info

# 运行程序
cargo run
```

## Python 调试

### 使用 pdb

```python
# 插入断点
import pdb; pdb.set_trace()

# 或使用 breakpoint() (Python 3.7+)
breakpoint()
```

**pdb 命令**:
```
(Pdb) n          # 下一行
(Pdb) s          # 进入函数
(Pdb) c          # 继续执行
(Pdb) p variable # 打印变量
(Pdb) l          # 显示代码
(Pdb) q          # 退出
```

### 使用 ipdb

更友好的调试器：

```bash
pip install ipdb
```

```python
import ipdb; ipdb.set_trace()
```

### VS Code 调试

配置 `.vscode/launch.json`：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: biliup",
      "type": "python",
      "request": "launch",
      "module": "biliup",
      "args": ["download", "https://www.douyu.com/123456"],
      "console": "integratedTerminal"
    }
  ]
}
```

### 日志调试

```python
import logging

logger = logging.getLogger(__name__)

# 不同级别的日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
logger.exception("异常信息")  # 包含堆栈跟踪
```

配置日志级别：

```python
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 网络调试

### 使用 mitmproxy

抓包分析 HTTP/HTTPS 流量：

```bash
# 启动 mitmproxy
mitmproxy -p 8080

# 配置代理
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080

# 运行程序
python -m biliup download https://example.com/123456
```

### 使用 curl 测试 API

```bash
# GET 请求
curl -X GET "https://api.example.com/room/info?room_id=123456"

# POST 请求
curl -X POST "https://api.example.com/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"test"}'

# 带 Cookie
curl -X GET "https://api.example.com/user/info" \
  -H "Cookie: session=xxx"

# 显示响应头
curl -i "https://api.example.com/room/info"
```

## 常见问题调试

### 编译错误

```bash
# 清理构建缓存
cargo clean
rm -rf target/

# 重新构建
cargo build
```

### 运行时错误

```bash
# 启用详细日志
export RUST_LOG=debug
export RUST_BACKTRACE=1

# 运行程序
cargo run
```

### 网络请求失败

```python
# 添加详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看请求详情
import httpx
client = httpx.Client()
response = client.get(url)
print(f"状态码: {response.status_code}")
print(f"响应头: {response.headers}")
print(f"响应体: {response.text}")
```

### 内存泄漏

```bash
# 使用 valgrind (Linux)
valgrind --leak-check=full ./target/debug/biliup-cli

# 使用 heaptrack
heaptrack ./target/debug/biliup-cli
```

## 性能分析

### Rust 性能分析

```bash
# 安装 flamegraph
cargo install flamegraph

# 生成火焰图
cargo flamegraph --bin biliup-cli
```

### Python 性能分析

```python
import cProfile
import pstats

# 性能分析
cProfile.run('main()', 'profile_stats')

# 查看结果
p = pstats.Stats('profile_stats')
p.sort_stats('cumulative')
p.print_stats(20)
```

### 前端性能分析

使用 Chrome DevTools Profiler：

1. 打开 DevTools
2. 切换到 Profiler 标签
3. 点击 Record
4. 执行操作
5. 停止录制并分析

## 相关文档

- [测试指南](./testing.md)
- [源码编译](./building-from-source.md)
- [插件开发](./plugin-development.md)
