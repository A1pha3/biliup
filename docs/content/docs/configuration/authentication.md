+++
title = "认证配置"
description = "了解如何配置各平台的认证信息，包括 Cookie 获取、登录方法和多账号管理"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 50
template = "docs/page.html"

[extra]
lead = "本文档详细说明如何获取和配置各平台的认证信息，包括 B 站 Cookie、多账号配置和 Cookie 维护。"
toc = true
top = false
+++

## 概述

biliup 需要认证信息来访问直播流和上传视频。本文档介绍如何获取和配置各平台的认证信息。

## Bilibili 认证配置

### 为什么需要 Cookie

B 站修改了画质策略，不使用 Cookie 只能获取最低画质。因此，录制 B 站直播和上传视频都需要配置 Cookie。

**重要提示：**
- 将 Cookie 传入不信任的第三方 API 可能导致账号被盗
- 请妥善保管 Cookie 文件
- 定期更新 Cookie

### 方法 1：使用 biliup-rs 登录（推荐）

这是最简单和安全的方法。

**步骤：**

1. 安装 biliup-rs
   ```bash
   # 参考安装文档
   ```

2. 运行登录命令
   ```bash
   biliup login
   ```

3. 按提示完成登录
   - 扫描二维码
   - 或输入账号密码

4. 登录成功后会生成 `cookies.json` 文件

5. 在配置文件中引用
   ```toml
   [user]
   bili_cookie_file = "cookies.json"
   ```

### 方法 2：手动获取 Cookie

如果无法使用 biliup-rs，可以手动获取 Cookie。

**步骤：**

1. 使用浏览器登录 B 站（https://www.bilibili.com）

2. 打开浏览器开发者工具
   - Chrome/Edge：按 F12
   - Firefox：按 F12
   - Safari：开发 → 显示网页检查器

3. 切换到 "Network"（网络）标签

4. 刷新页面（F5）

5. 在请求列表中找到任意请求，查看请求头（Request Headers）

6. 找到 Cookie 字段，复制以下值：
   - `SESSDATA`
   - `bili_jct`
   - `DedeUserID`
   - `DedeUserID__ckMd5`

7. 在配置文件中填写
   ```toml
   [user]
   bili_cookie = "SESSDATA=xxx;bili_jct=xxx;DedeUserID__ckMd5=xxx;DedeUserID=xxx;"
   ```

### 方法 3：使用浏览器插件

使用 Cookie 导出插件可以更方便地获取 Cookie。

**推荐插件：**
- EditThisCookie（Chrome/Edge）
- Cookie-Editor（Firefox）

**步骤：**

1. 安装插件

2. 登录 B 站

3. 点击插件图标

4. 导出 Cookie（选择 Netscape 格式）

5. 保存为 `cookies.txt`

6. 在配置文件中引用
   ```toml
   [user]
   bili_cookie_file = "cookies.txt"
   ```

### cookies.json 文件格式

biliup-rs 生成的 `cookies.json` 文件格式：

```json
{
  "cookies": {
    "SESSDATA": "xxx",
    "bili_jct": "xxx",
    "DedeUserID": "xxx",
    "DedeUserID__ckMd5": "xxx"
  },
  "access_token": "xxx",
  "refresh_token": "xxx",
  "expires_in": 1234567890
}
```

**说明：**
- `cookies`：必需的 Cookie 信息
- `access_token`：访问令牌（可选）
- `refresh_token`：刷新令牌（可选）
- `expires_in`：过期时间（可选）

### 配置示例

**使用 Cookie 文件（推荐）：**

```toml
[user]
bili_cookie_file = "cookies.json"
```

```yaml
user:
  bili_cookie_file: cookies.json
```

**使用 Cookie 字符串：**

```toml
[user]
bili_cookie = "SESSDATA=xxx;bili_jct=xxx;DedeUserID__ckMd5=xxx;DedeUserID=xxx;"
```

```yaml
user:
  bili_cookie: 'SESSDATA=xxx;bili_jct=xxx;DedeUserID__ckMd5=xxx;DedeUserID=xxx;'
```

**优先级：**
- 同时存在时，优先使用 `bili_cookie_file`
- 主播配置中的 `user_cookie` 优先于全局配置

### 获取直播流用 Cookie

用于录制 B 站直播时获取高画质流。

```toml
[user]
bili_cookie_file = "cookies.json"
```

**说明：**
- 不使用 Cookie 只能获取最低画质
- 推荐使用 biliup-rs 生成的 Cookie 文件


## 多账号配置

biliup 支持使用多个 B 站账号上传视频。

### 配置方法

**全局默认账号：**

```toml
[user]
bili_cookie_file = "default.json"
```

**为主播指定账号：**

```toml
[streamers."主播A"]
url = ["https://example.com/A"]
user_cookie = "account1.json"

[streamers."主播B"]
url = ["https://example.com/B"]
user_cookie = "account2.json"

[streamers."主播C"]
url = ["https://example.com/C"]
# 使用全局默认账号
```

### 多账号示例

```toml
# 全局默认账号
[user]
bili_cookie_file = "main_account.json"

# 游戏区主播使用游戏账号
[streamers."游戏主播1"]
url = ["https://www.twitch.tv/gamer1"]
user_cookie = "game_account.json"
tid = 171

[streamers."游戏主播2"]
url = ["https://www.twitch.tv/gamer2"]
user_cookie = "game_account.json"
tid = 171

# 音乐区主播使用音乐账号
[streamers."音乐主播"]
url = ["https://www.youtube.com/@musician/live"]
user_cookie = "music_account.json"
tid = 130

# 其他主播使用默认账号
[streamers."其他主播"]
url = ["https://example.com"]
# 使用 main_account.json
```

### 多账号管理建议

1. **按内容分类**
   - 游戏内容用游戏账号
   - 音乐内容用音乐账号
   - 避免单账号内容过于杂乱

2. **避免单账号投稿过多**
   - B 站对单账号投稿频率有限制
   - 分散到多个账号可以避免限制

3. **定期检查 Cookie 有效性**
   - 每个账号的 Cookie 都可能过期
   - 及时更新失效的 Cookie

## Cookie 过期和刷新

### Cookie 有效期

- B 站 Cookie 通常有效期为几个月
- 长时间不使用可能会失效
- 修改密码后 Cookie 会立即失效

### 检测 Cookie 是否过期

**方法 1：查看日志**

```bash
tail -f biliup.log
```

如果看到类似错误，说明 Cookie 已过期：
```
ERROR: Authentication failed
ERROR: Invalid cookie
```

**方法 2：测试上传**

```bash
biliup upload --config config.toml test.mp4
```

如果提示认证失败，说明 Cookie 已过期。

### 刷新 Cookie

**使用 biliup-rs 刷新：**

```bash
biliup login
```

重新登录后会生成新的 `cookies.json` 文件。

**手动刷新：**

1. 重新登录 B 站
2. 按照前面的方法重新获取 Cookie
3. 更新配置文件或 Cookie 文件

### 自动刷新（实验性）

biliup-rs 生成的 Cookie 文件包含 `refresh_token`，理论上可以自动刷新，但此功能仍在实验中。

## 其他平台认证配置

### 抖音 Cookie

录制抖音 `www.douyin.com/user/` 类型链接或被风控时需要配置。

**获取方法：**

1. 登录抖音网页版
2. 打开开发者工具
3. 找到 Cookie 中的以下值：
   - `__ac_nonce`
   - `__ac_signature`
   - `sessionid`

**配置：**

```toml
[user]
douyin_cookie = "__ac_nonce=xxx; __ac_signature=xxx; sessionid=xxx;"
```

```yaml
user:
  douyin_cookie: '__ac_nonce=xxx; __ac_signature=xxx; sessionid=xxx;'
```

**注意：**
- 只需要这三个值，不要填入所有 Cookie
- Cookie 可能会过期，需要定期更新

### Twitch Cookie

录制 Twitch 时可以配置 Cookie 减少广告。

**获取方法：**

1. 登录 Twitch（https://www.twitch.tv）
2. 打开浏览器控制台（F12）
3. 在控制台中执行：
   ```javascript
   document.cookie.split("; ").find(item=>item.startsWith("auth-token="))?.split("=")[1]
   ```
4. 复制输出的值

**配置：**

```toml
[user]
twitch_cookie = "xxx"
```

```yaml
user:
  twitch_cookie: 'xxx'
```

**说明：**
- 需要账号开通 Twitch Turbo 会员才有效
- Cookie 有过期风险，失效后会在日志输出警告
- 需要 `downloader = "ffmpeg"` 才会生效

### YouTube Cookie

用于下载会限、私享等未登录账号无法访问的内容。

**获取方法：**

1. 安装浏览器插件 "Get cookies.txt"
2. 登录 YouTube
3. 使用插件导出 Cookie（Netscape 格式）
4. 保存为 `youtube_cookies.txt`

**配置：**

```toml
[user]
youtube_cookie = "youtube_cookies.txt"
```

```yaml
user:
  youtube_cookie: 'youtube_cookies.txt'
```

### Niconico 认证

**使用邮箱/密码：**

```toml
[user]
niconico-email = "your@email.com"
niconico-password = "your_password"
```

**使用 Session Token：**

```toml
[user]
niconico-user-session = "xxx"
```

**清除缓存凭证：**

```toml
[user]
niconico-purge-credentials = true
```

### AfreecaTV 认证

录制部分直播时需要登录。

```toml
[user]
afreecatv_username = "your_username"
afreecatv_password = "your_password"
```

```yaml
user:
  afreecatv_username: your_username
  afreecatv_password: your_password
```

### TwitCasting 密码

部分直播间需要密码。

**全局配置：**

```toml
twitcasting_password = "room_password"
```

**单个主播配置：**

```toml
[streamers."主播"]
url = ["https://twitcasting.tv/username"]
twitcasting_password = "room_password"
```

## 完整认证配置示例

```toml
[user]
# Bilibili
bili_cookie_file = "cookies.json"

# 抖音
douyin_cookie = "__ac_nonce=xxx; __ac_signature=xxx; sessionid=xxx;"

# Twitch
twitch_cookie = "xxx"

# YouTube
youtube_cookie = "youtube_cookies.txt"

# Niconico
niconico-email = "your@email.com"
niconico-password = "your_password"

# AfreecaTV
afreecatv_username = "your_username"
afreecatv_password = "your_password"

# TwitCasting
twitcasting_password = "default_password"
```


## 安全建议

### 保护 Cookie 文件

1. **设置文件权限**
   ```bash
   chmod 600 cookies.json
   ```

2. **不要提交到版本控制**
   ```bash
   # 添加到 .gitignore
   echo "cookies.json" >> .gitignore
   echo "*.json" >> .gitignore
   ```

3. **定期更换密码**
   - 定期更换 B 站密码
   - 更换后重新获取 Cookie

4. **使用独立账号**
   - 不要使用主账号
   - 创建专门用于录制上传的账号

### 避免 Cookie 泄露

1. **不要分享配置文件**
   - 配置文件包含敏感信息
   - 分享前删除所有认证信息

2. **不要使用不信任的第三方 API**
   - 默认使用官方 API
   - 谨慎使用第三方反代 API

3. **监控账号活动**
   - 定期检查账号登录记录
   - 发现异常立即修改密码

4. **使用环境变量（可选）**
   ```bash
   export BILI_COOKIE="SESSDATA=xxx;..."
   ```

## 常见问题

### Cookie 无效

**问题**：提示 Cookie 无效或认证失败

**解决方案：**
1. 确认 Cookie 格式正确
2. 检查是否包含所有必需字段
3. 重新获取 Cookie
4. 确认账号状态正常

### 无法获取高画质

**问题**：录制 B 站直播只能获取最低画质

**解决方案：**
1. 确认已配置 Cookie
   ```toml
   [user]
   bili_cookie_file = "cookies.json"
   ```

2. 检查 Cookie 是否有效
3. 确认账号有权限观看高画质

### 上传失败

**问题**：上传时提示认证失败

**解决方案：**
1. 检查 Cookie 是否过期
2. 确认使用的是上传账号的 Cookie
3. 检查账号是否有上传权限
4. 查看日志获取详细错误信息

### 多账号混乱

**问题**：不确定哪个主播使用哪个账号

**解决方案：**
1. 为 Cookie 文件使用描述性名称
   ```
   game_account.json
   music_account.json
   main_account.json
   ```

2. 在配置中添加注释
   ```toml
   [streamers."游戏主播"]
   url = ["https://example.com"]
   user_cookie = "game_account.json"  # 游戏专用账号
   ```

3. 建立账号管理文档

### Cookie 频繁过期

**问题**：Cookie 经常失效

**解决方案：**
1. 使用 biliup-rs 登录（支持自动刷新）
2. 避免在多个设备同时登录
3. 不要频繁修改密码
4. 检查账号是否被风控

## 测试认证配置

### 测试 B 站 Cookie

```bash
# 测试录制
biliup --config config.toml start

# 测试上传
biliup --config config.toml upload test.mp4
```

### 查看认证状态

```bash
# 查看配置
biliup --config config.toml config show

# 查看日志
tail -f biliup.log
```

### 验证 Cookie 有效性

**方法 1：使用 curl**

```bash
curl -H "Cookie: SESSDATA=xxx;bili_jct=xxx;..." \
  https://api.bilibili.com/x/web-interface/nav
```

如果返回用户信息，说明 Cookie 有效。

**方法 2：浏览器测试**

1. 打开浏览器隐私模式
2. 打开开发者工具
3. 在控制台中设置 Cookie
   ```javascript
   document.cookie = "SESSDATA=xxx"
   document.cookie = "bili_jct=xxx"
   // ...
   ```
4. 访问 B 站，检查是否已登录

## 相关链接

- [配置文件格式](./config-file-format.md)
- [主播配置详解](./streamer-config.md)
- [上传配置详解](./upload-config.md)
- [高级配置选项](./advanced-config.md)
- [配置示例集](./examples.md)
- [biliup-rs 项目](https://github.com/biliup/biliup-rs)
