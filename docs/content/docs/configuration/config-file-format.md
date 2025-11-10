+++
title = "配置文件格式"
description = "了解 biliup 配置文件的格式、结构和查找规则"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 10
template = "docs/page.html"

[extra]
lead = "biliup 支持 TOML 和 YAML 两种配置文件格式，本文档详细说明配置文件的基本结构、查找路径和编写规范。"
toc = true
top = false
+++

## 概述

biliup 使用配置文件来控制录制、上传和其他行为。配置文件支持两种格式：

- **TOML 格式**：`config.toml`（推荐）
- **YAML 格式**：`config.yaml`

两种格式功能完全相同，你可以根据个人喜好选择使用。TOML 格式更简洁直观，YAML 格式层次更清晰。

## 配置文件查找路径

biliup 按以下顺序查找配置文件：

1. **命令行指定的路径**：使用 `--config` 参数指定
   ```bash
   biliup --config /path/to/config.toml start
   ```

2. **当前工作目录**：
   - `./config.toml`
   - `./config.yaml`

3. **用户配置目录**：
   - Linux/macOS: `~/.config/biliup/config.toml`
   - Windows: `%APPDATA%\biliup\config.toml`

4. **系统配置目录**：
   - Linux: `/etc/biliup/config.toml`

如果找到多个配置文件，将使用第一个找到的文件。

## 配置文件优先级

当同时存在多个配置文件时，优先级从高到低为：

1. 命令行 `--config` 参数指定的文件
2. 当前目录的 `config.toml`
3. 当前目录的 `config.yaml`
4. 用户配置目录的配置文件
5. 系统配置目录的配置文件

## 配置文件基本结构

配置文件分为三个主要部分：

1. **全局配置**：控制录制、上传、任务调度等全局行为
2. **主播配置**：为每个主播单独配置录制和上传参数
3. **用户认证**：配置各平台的 Cookie 和登录信息

### TOML 格式示例

```toml
# 全局录播与上传设置
file_size = 2621440000
filtering_threshold = 20
lines = "AUTO"
threads = 3
delay = 300

# 主播配置
[streamers."主播名称"]
url = ["https://www.twitch.tv/username"]
tags = ["游戏", "娱乐"]
tid = 171

# 用户认证（可选）
[user]
bili_cookie_file = "cookies.json"
```

### YAML 格式示例

```yaml
# 全局录播与上传设置
file_size: 2621440000
filtering_threshold: 20
lines: AUTO
threads: 3
delay: 300

# 主播配置
streamers:
  主播名称:
    url:
      - https://www.twitch.tv/username
    tags:
      - 游戏
      - 娱乐
    tid: 171

# 用户认证（可选）
user:
  bili_cookie_file: cookies.json
```

## 最小化配置示例

以下是一个可以立即使用的最小化配置：

### TOML 格式

```toml
# 最小化配置示例
[streamers."我的主播"]
url = ["https://www.twitch.tv/username"]
```

### YAML 格式

```yaml
# 最小化配置示例
streamers:
  我的主播:
    url:
      - https://www.twitch.tv/username
```

这个最小配置将使用所有默认值：
- 使用 stream-gears 下载器
- 自动选择最优上传线路
- 文件大小限制为 2.5GB
- 过滤小于 20MB 的文件
- 下播后延迟 300 秒再检测

## 配置文件编写规范

### TOML 格式规范

1. **注释**：使用 `#` 开头
   ```toml
   # 这是注释
   file_size = 2621440000  # 行尾注释
   ```

2. **字符串**：使用双引号或单引号
   ```toml
   title = "视频标题"
   description = '''
   多行字符串
   第二行
   '''
   ```

3. **数组**：使用方括号
   ```toml
   tags = ["标签1", "标签2"]
   url = [
       "https://example.com/1",
       "https://example.com/2"
   ]
   ```

4. **表（对象）**：使用方括号定义
   ```toml
   [streamers."主播名称"]
   url = ["https://example.com"]
   
   [streamers."另一个主播"]
   url = ["https://example.com"]
   ```

5. **布尔值**：使用 `true` 或 `false`
   ```toml
   use_live_cover = true
   bili_cdn_fallback = false
   ```

### YAML 格式规范

1. **注释**：使用 `#` 开头
   ```yaml
   # 这是注释
   file_size: 2621440000  # 行尾注释
   ```

2. **缩进**：使用空格（不要使用 Tab），通常使用 2 或 4 个空格
   ```yaml
   streamers:
     主播名称:
       url:
         - https://example.com
   ```

3. **字符串**：可以不使用引号，特殊字符需要引号
   ```yaml
   title: 视频标题
   description: "包含特殊字符: 的标题"
   multiline: |-
     多行字符串
     第二行
   ```

4. **数组**：使用 `-` 或方括号
   ```yaml
   # 方式1：多行
   tags:
     - 标签1
     - 标签2
   
   # 方式2：单行
   tags: [标签1, 标签2]
   ```

5. **布尔值**：使用 `true`/`false` 或 `yes`/`no`
   ```yaml
   use_live_cover: true
   bili_cdn_fallback: false
   ```

## 配置验证

启动 biliup 时，会自动验证配置文件：

```bash
biliup --config config.toml start
```

如果配置文件有错误，会显示详细的错误信息：

```
Error: Failed to parse config file
  --> config.toml:15:1
   |
15 | [streamers."主播名称"
   | ^^^^^^^^^^^^^^^^^^^^^^ expected closing bracket
```

## 配置文件模板

biliup 提供了完整的配置文件模板，包含所有可用选项和详细注释：

- TOML 模板：[public/config.toml](https://github.com/biliup/biliup/blob/master/public/config.toml)
- YAML 模板：[public/config.yaml](https://github.com/biliup/biliup/blob/master/public/config.yaml)

你可以下载模板文件作为起点，根据需要修改配置项。

## 配置热重载

biliup 支持配置文件热重载。当检测到配置文件变化时，会在空闲时自动重启：

```toml
# 检测源码文件变化间隔，单位：秒
check_sourcecode = 15
```

设置为 `0` 可以禁用自动重载功能。

## 环境变量

部分配置项可以通过环境变量覆盖：

```bash
# 设置日志级别
export RUST_LOG=debug

# 指定配置文件
export BILIUP_CONFIG=/path/to/config.toml

# 启动服务
biliup start
```

## 常见问题

### 配置文件找不到

**问题**：启动时提示 "Config file not found"

**解决方案**：
1. 确认配置文件在当前目录或用户配置目录
2. 使用 `--config` 参数明确指定配置文件路径
3. 检查文件名是否正确（`config.toml` 或 `config.yaml`）

### 配置文件格式错误

**问题**：启动时提示解析错误

**解决方案**：
1. 检查 TOML/YAML 语法是否正确
2. 确认缩进使用空格而非 Tab（YAML）
3. 确认字符串中的特殊字符已正确转义
4. 使用在线工具验证格式：
   - TOML: https://www.toml-lint.com/
   - YAML: https://www.yamllint.com/

### 配置不生效

**问题**：修改配置后没有生效

**解决方案**：
1. 确认修改的是正在使用的配置文件
2. 重启 biliup 服务使配置生效
3. 检查是否有其他配置文件覆盖了设置
4. 查看日志确认配置是否被正确加载

## 相关链接

- [主播配置详解](./streamer-config.md)
- [上传配置详解](./upload-config.md)
- [高级配置选项](./advanced-config.md)
- [认证配置](./authentication.md)
- [配置示例集](./examples.md)
