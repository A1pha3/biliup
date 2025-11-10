+++
title = "平台支持"
description = "查看 biliup 支持的所有直播平台及其配置说明"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 60
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "biliup 支持 20+ 个主流直播平台，本文档详细说明各平台的配置方法和注意事项。"
toc = true
top = false
+++

## 平台支持概览

biliup 支持以下直播平台的录制：

### 国内平台

| 平台 | 支持状态 | 弹幕录制 | 需要 Cookie | 备注 |
|------|---------|---------|------------|------|
| B 站直播 | ✅ 完全支持 | ✅ | ❌ | 稳定性最好 |
| 斗鱼 | ✅ 完全支持 | ✅ | ❌ | 支持所有画质 |
| 虎牙 | ✅ 完全支持 | ✅ | ❌ | 支持所有画质 |
| 抖音 | ✅ 完全支持 | ⚠️ 部分 | ❌ | 需要特殊处理 |
| 快手 | ✅ 完全支持 | ⚠️ 部分 | ✅ | 需要登录 |
| CC 直播 | ✅ 完全支持 | ❌ | ❌ | 网易 CC |
| 映客 | ✅ 完全支持 | ❌ | ❌ | - |
| 猫耳 FM | ✅ 完全支持 | ❌ | ❌ | 音频直播 |
| AcFun | ✅ 完全支持 | ❌ | ❌ | - |
| 千千音乐 | ✅ 完全支持 | ❌ | ❌ | 音频直播 |
| KilaKila | ✅ 完全支持 | ❌ | ❌ | - |

### 国际平台

| 平台 | 支持状态 | 弹幕录制 | 需要 Cookie | 备注 |
|------|---------|---------|------------|------|
| Twitch | ✅ 完全支持 | ❌ | ✅ | 需要登录获取高画质 |
| YouTube Live | ✅ 完全支持 | ❌ | ❌ | 支持所有画质 |
| Afreeca TV | ✅ 完全支持 | ❌ | ❌ | 韩国平台 |
| Niconico | ✅ 完全支持 | ❌ | ✅ | 日本平台，需要登录 |
| Twitcasting | ✅ 完全支持 | ❌ | ❌ | 日本平台 |
| Picarto | ✅ 完全支持 | ❌ | ❌ | 艺术创作平台 |
| Bigo Live | ✅ 完全支持 | ❌ | ❌ | 东南亚平台 |

## 国内平台详解

### B 站直播

**URL 格式**：
```
https://live.bilibili.com/房间号
```

**配置示例**：
```yaml
streamers:
  B站主播:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
    quality: "best"
```

**特点**：
- ✅ 稳定性最好
- ✅ 支持所有画质
- ✅ 支持弹幕录制
- ✅ 无需登录
- ✅ 支持 4K 直播

**注意事项**：
- 某些付费直播间可能需要大会员
- 建议使用 FLV 格式录制

### 斗鱼

**URL 格式**：
```
https://www.douyu.com/房间号
```

**配置示例**：
```yaml
streamers:
  斗鱼主播:
    url: ["https://www.douyu.com/123456"]
    format: "flv"
    quality: "best"
```

**特点**：
- ✅ 支持所有画质
- ✅ 支持弹幕录制
- ✅ 无需登录
- ✅ 稳定性好

**画质选项**：
- `best` - 蓝光（最高）
- `1080p` - 超清
- `720p` - 高清
- `480p` - 标清

**注意事项**：
- 某些主播可能限制录制
- 建议使用 FLV 格式

### 虎牙

**URL 格式**：
```
https://www.huya.com/房间号
```

**配置示例**：
```yaml
streamers:
  虎牙主播:
    url: ["https://www.huya.com/123456"]
    format: "flv"
    quality: "best"
```

**特点**：
- ✅ 支持所有画质
- ✅ 支持弹幕录制
- ✅ 无需登录
- ✅ 稳定性好

**画质选项**：
- `best` - 蓝光（最高）
- `1080p` - 超清
- `720p` - 高清

**注意事项**：
- 虎牙的 CDN 节点较多，速度通常很快
- 支持 HDR 直播

### 抖音

**URL 格式**：
```
https://live.douyin.com/房间号
```

**配置示例**：
```yaml
streamers:
  抖音主播:
    url: ["https://live.douyin.com/123456"]
    format: "flv"
    quality: "best"
```

**特点**：
- ✅ 支持高画质
- ⚠️ 弹幕录制不稳定
- ✅ 无需登录
- ⚠️ 可能需要特殊处理

**注意事项**：
- 抖音的直播 URL 可能会变化
- 建议定期检查录制状态
- 某些直播可能有地区限制

### 快手

**URL 格式**：
```
https://live.kuaishou.com/u/用户ID
```

**配置示例**：
```yaml
streamers:
  快手主播:
    url: ["https://live.kuaishou.com/u/用户ID"]
    format: "flv"
    quality: "best"
    cookies: "kuaishou_cookies.txt"
```

**特点**：
- ✅ 支持高画质
- ⚠️ 需要登录
- ⚠️ 弹幕录制不稳定

**Cookie 配置**：

快手需要登录才能录制，配置 Cookie 方法：

1. 使用浏览器登录快手
2. 打开开发者工具（F12）
3. 复制 Cookie
4. 保存到文件

```yaml
streamers:
  快手主播:
    url: ["https://live.kuaishou.com/u/用户ID"]
    cookies: "kuaishou_cookies.txt"
```

**注意事项**：
- Cookie 有效期约 30 天
- 需要定期更新 Cookie


### CC 直播（网易 CC）

**URL 格式**：
```
https://cc.163.com/房间号
```

**配置示例**：
```yaml
streamers:
  CC主播:
    url: ["https://cc.163.com/123456"]
    format: "flv"
```

**特点**：
- ✅ 稳定性好
- ❌ 不支持弹幕录制
- ✅ 无需登录

### 映客

**URL 格式**：
```
https://www.inke.cn/live.html?uid=用户ID
```

**配置示例**：
```yaml
streamers:
  映客主播:
    url: ["https://www.inke.cn/live.html?uid=123456"]
    format: "flv"
```

### 猫耳 FM

**URL 格式**：
```
https://fm.missevan.com/live/房间号
```

**配置示例**：
```yaml
streamers:
  猫耳主播:
    url: ["https://fm.missevan.com/live/123456"]
    format: "mp3"  # 音频直播
```

**特点**：
- ✅ 音频直播平台
- ✅ 支持高音质
- ✅ 无需登录

**注意事项**：
- 这是音频直播，不是视频
- 建议使用 MP3 格式

### AcFun

**URL 格式**：
```
https://live.acfun.cn/live/房间号
```

**配置示例**：
```yaml
streamers:
  AcFun主播:
    url: ["https://live.acfun.cn/live/123456"]
    format: "flv"
```

## 国际平台详解

### Twitch

**URL 格式**：
```
https://www.twitch.tv/username
```

**配置示例**：
```yaml
streamers:
  Twitch主播:
    url: ["https://www.twitch.tv/shroud"]
    format: "ts"
    quality: "best"
```

**特点**：
- ✅ 支持所有画质
- ✅ 稳定性好
- ⚠️ 高画质需要登录
- ❌ 不支持内置弹幕录制

**画质选项**：
- `best` - Source（原画）
- `1080p60` - 1080P 60FPS
- `720p60` - 720P 60FPS
- `720p` - 720P
- `480p` - 480P
- `360p` - 360P
- `worst` - 最低画质

**Cookie 配置**：

录制高画质需要登录：

1. 登录 Twitch
2. 获取 Cookie
3. 配置到 biliup

```yaml
streamers:
  Twitch主播:
    url: ["https://www.twitch.tv/username"]
    cookies: "twitch_cookies.txt"
    quality: "best"
```

**代理配置**：

Twitch 在某些地区可能需要代理：

```yaml
streamers:
  Twitch主播:
    url: ["https://www.twitch.tv/username"]
    proxy: "http://127.0.0.1:7890"
```

**注意事项**：
- Twitch 使用 HLS 流，建议使用 TS 格式
- 某些地区访问可能较慢
- 建议配置代理以获得更好的速度

### YouTube Live

**URL 格式**：
```
https://www.youtube.com/watch?v=视频ID
或
https://www.youtube.com/channel/频道ID/live
```

**配置示例**：
```yaml
streamers:
  YouTube主播:
    url: ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    format: "mp4"
    quality: "best"
```

**特点**：
- ✅ 支持 4K 直播
- ✅ 支持 60FPS
- ✅ 无需登录
- ✅ 稳定性好

**画质选项**：
- `best` - 最高画质（可能是 4K）
- `1080p60` - 1080P 60FPS
- `1080p` - 1080P
- `720p60` - 720P 60FPS
- `720p` - 720P

**代理配置**：

YouTube 在某些地区需要代理：

```yaml
streamers:
  YouTube主播:
    url: ["https://www.youtube.com/watch?v=视频ID"]
    proxy: "http://127.0.0.1:7890"
```

**注意事项**：
- YouTube 的直播 URL 可能会变化
- 建议使用频道的 /live 链接
- 4K 直播需要较大带宽

### Afreeca TV

**URL 格式**：
```
https://play.afreecatv.com/username
或
https://play.afreecatv.com/username/房间号
```

**配置示例**：
```yaml
streamers:
  Afreeca主播:
    url: ["https://play.afreecatv.com/username"]
    format: "flv"
```

**特点**：
- ✅ 韩国最大直播平台
- ✅ 支持高画质
- ✅ 无需登录

**注意事项**：
- 某些直播可能有地区限制
- 建议使用韩国代理

### Niconico

**URL 格式**：
```
https://live.nicovideo.jp/watch/lv房间号
```

**配置示例**：
```yaml
streamers:
  Nico主播:
    url: ["https://live.nicovideo.jp/watch/lv123456"]
    format: "ts"
    cookies: "nico_cookies.txt"
```

**特点**：
- ✅ 日本最大弹幕网站
- ⚠️ 需要登录
- ⚠️ 某些直播需要会员

**Cookie 配置**：

Niconico 需要登录：

1. 登录 Niconico
2. 获取 Cookie
3. 配置到 biliup

```yaml
streamers:
  Nico主播:
    url: ["https://live.nicovideo.jp/watch/lv123456"]
    cookies: "nico_cookies.txt"
```

**注意事项**：
- 某些直播需要付费会员
- Cookie 有效期约 30 天

### Twitcasting

**URL 格式**：
```
https://twitcasting.tv/username
```

**配置示例**：
```yaml
streamers:
  Twitcasting主播:
    url: ["https://twitcasting.tv/username"]
    format: "mp4"
```

**特点**：
- ✅ 日本流行的直播平台
- ✅ 无需登录
- ✅ 移动端友好

### Picarto

**URL 格式**：
```
https://picarto.tv/username
```

**配置示例**：
```yaml
streamers:
  Picarto主播:
    url: ["https://picarto.tv/username"]
    format: "flv"
```

**特点**：
- ✅ 艺术创作直播平台
- ✅ 无需登录
- ✅ 支持高画质

### Bigo Live

**URL 格式**：
```
https://www.bigo.tv/用户ID
```

**配置示例**：
```yaml
streamers:
  Bigo主播:
    url: ["https://www.bigo.tv/123456"]
    format: "flv"
```

**特点**：
- ✅ 东南亚流行平台
- ✅ 无需登录

## 平台特殊配置

### Cookie 配置方法

某些平台需要 Cookie 才能录制。

#### 方法 1：使用浏览器插件

1. 安装 Cookie 导出插件（如 EditThisCookie）
2. 登录目标平台
3. 导出 Cookie 为 Netscape 格式
4. 保存为文本文件

#### 方法 2：手动复制

1. 登录目标平台
2. 打开开发者工具（F12）
3. 进入 Network 标签
4. 刷新页面
5. 找到请求，复制 Cookie 头
6. 保存到文件

**Cookie 文件格式**（Netscape）：

```
# Netscape HTTP Cookie File
.twitch.tv	TRUE	/	FALSE	1735689600	auth-token	your_token_here
.twitch.tv	TRUE	/	FALSE	1735689600	persistent	your_persistent_here
```

**配置使用**：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    cookies: "platform_cookies.txt"
```

### 代理配置

某些国际平台需要代理访问。

**全局代理**：

```yaml
global:
  proxy: "http://127.0.0.1:7890"
```

**单个平台代理**：

```yaml
streamers:
  Twitch主播:
    url: ["https://www.twitch.tv/username"]
    proxy: "http://127.0.0.1:7890"
  
  YouTube主播:
    url: ["https://www.youtube.com/watch?v=视频ID"]
    proxy: "http://127.0.0.1:7890"
```

**SOCKS5 代理**：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    proxy: "socks5://127.0.0.1:1080"
```


## 平台已知限制

### B 站直播

**限制**：
- 某些付费直播需要大会员
- 4K 直播需要较大带宽

**解决方案**：
- 使用有大会员的账号 Cookie
- 降低画质到 1080p

### 斗鱼

**限制**：
- 某些主播可能限制录制
- 高峰期可能限速

**解决方案**：
- 尝试不同时间段录制
- 使用多个 CDN 节点

### 虎牙

**限制**：
- 某些特殊直播可能无法录制

**解决方案**：
- 检查直播间是否公开
- 尝试使用不同画质

### 抖音

**限制**：
- URL 可能频繁变化
- 某些直播有地区限制

**解决方案**：
- 使用房间号而不是临时 URL
- 配置代理

### 快手

**限制**：
- 必须登录才能录制
- Cookie 有效期较短

**解决方案**：
- 定期更新 Cookie
- 使用自动刷新 Cookie 的脚本

### Twitch

**限制**：
- 高画质需要登录
- 某些地区访问慢

**解决方案**：
- 配置 Twitch 账号 Cookie
- 使用代理加速

### YouTube

**限制**：
- 某些地区无法访问
- 4K 直播需要大带宽

**解决方案**：
- 配置代理
- 降低画质

### Niconico

**限制**：
- 必须登录
- 某些直播需要付费会员

**解决方案**：
- 配置有会员的账号 Cookie
- 选择免费直播

## 多平台录制配置

### 同时录制多个平台

```yaml
streamers:
  B站主播:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
    
  斗鱼主播:
    url: ["https://www.douyu.com/123456"]
    format: "flv"
    
  Twitch主播:
    url: ["https://www.twitch.tv/username"]
    format: "ts"
    proxy: "http://127.0.0.1:7890"
```

### 同一主播多平台

某些主播在多个平台同时直播：

```yaml
streamers:
  主播名称_B站:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
    output_dir: "/recordings/主播名称/bilibili"
    
  主播名称_斗鱼:
    url: ["https://www.douyu.com/123456"]
    format: "flv"
    output_dir: "/recordings/主播名称/douyu"
```

### 按平台分组

```yaml
groups:
  国内平台:
    streamers:
      - B站主播
      - 斗鱼主播
      - 虎牙主播
  
  国际平台:
    streamers:
      - Twitch主播
      - YouTube主播
    proxy: "http://127.0.0.1:7890"  # 组级别代理
```

## 平台选择建议

### 根据需求选择

**追求稳定性**：
1. B 站直播
2. 斗鱼
3. 虎牙

**追求画质**：
1. YouTube（支持 4K）
2. B 站直播（支持 4K）
3. Twitch（支持 1080p60）

**国际内容**：
1. Twitch
2. YouTube
3. Afreeca TV

**音频直播**：
1. 猫耳 FM
2. 千千音乐

### 根据地区选择

**中国大陆**：
- B 站直播
- 斗鱼
- 虎牙
- 抖音
- 快手

**日本**：
- Niconico
- Twitcasting

**韩国**：
- Afreeca TV

**全球**：
- Twitch
- YouTube

## 常见问题

### 如何找到直播间 URL？

**B 站**：
```
打开直播间 → 地址栏复制
https://live.bilibili.com/123456
```

**斗鱼**：
```
打开直播间 → 地址栏复制
https://www.douyu.com/123456
```

**Twitch**：
```
打开频道 → 地址栏复制
https://www.twitch.tv/username
```

### 如何测试平台是否支持？

```bash
# 使用 download 命令测试
biliup download "直播间URL" --output test.flv

# 如果能下载，说明支持
```

### 某个平台无法录制？

**检查步骤**：

1. 确认 URL 格式正确
2. 检查直播间是否开播
3. 查看日志错误信息
4. 尝试手动访问直播间

```bash
# 查看详细日志
biliup server --rust-log=debug
```

### 如何添加新平台支持？

biliup 使用插件系统，可以添加新平台：

1. 在 `biliup/plugins/` 目录创建新插件
2. 实现平台的下载逻辑
3. 注册插件
4. 测试并提交 PR

参考现有插件代码：
```python
# biliup/plugins/your_platform.py
class YourPlatform(Plugin):
    def __init__(self, url):
        self.url = url
    
    def download(self):
        # 实现下载逻辑
        pass
```

### Cookie 如何保持有效？

**方法 1：定期手动更新**

每 30 天更新一次 Cookie。

**方法 2：自动刷新脚本**

```python
import time
from selenium import webdriver

def refresh_cookie(platform):
    driver = webdriver.Chrome()
    driver.get(f"https://{platform}.com")
    # 自动登录逻辑
    cookies = driver.get_cookies()
    # 保存 cookies
    driver.quit()

# 定期执行
while True:
    refresh_cookie("twitch")
    time.sleep(86400 * 7)  # 每周刷新
```

**方法 3：使用长期有效的 Token**

某些平台支持 API Token，有效期更长。

## 平台对比

### 画质对比

| 平台 | 最高画质 | 帧率 | HDR | 备注 |
|------|---------|------|-----|------|
| YouTube | 4K | 60fps | ✅ | 最高画质 |
| B 站直播 | 4K | 60fps | ✅ | 国内最好 |
| Twitch | 1080p | 60fps | ❌ | 稳定性好 |
| 斗鱼 | 1080p | 60fps | ❌ | - |
| 虎牙 | 1080p | 60fps | ✅ | 支持 HDR |
| 抖音 | 1080p | 30fps | ❌ | - |

### 稳定性对比

| 平台 | 稳定性 | 断流率 | 重连速度 | 评分 |
|------|--------|--------|---------|------|
| B 站直播 | ⭐⭐⭐⭐⭐ | 低 | 快 | 9.5/10 |
| 斗鱼 | ⭐⭐⭐⭐⭐ | 低 | 快 | 9.0/10 |
| 虎牙 | ⭐⭐⭐⭐ | 中 | 中 | 8.5/10 |
| Twitch | ⭐⭐⭐⭐ | 中 | 中 | 8.0/10 |
| YouTube | ⭐⭐⭐⭐ | 中 | 慢 | 8.0/10 |
| 抖音 | ⭐⭐⭐ | 高 | 慢 | 7.0/10 |

### 功能对比

| 平台 | 弹幕录制 | 多画质 | 需要登录 | 代理需求 |
|------|---------|--------|---------|---------|
| B 站直播 | ✅ | ✅ | ❌ | ❌ |
| 斗鱼 | ✅ | ✅ | ❌ | ❌ |
| 虎牙 | ✅ | ✅ | ❌ | ❌ |
| Twitch | ❌ | ✅ | ⚠️ | ⚠️ |
| YouTube | ❌ | ✅ | ❌ | ⚠️ |
| 快手 | ⚠️ | ✅ | ✅ | ❌ |

## 最佳实践

### 平台选择

1. **优先选择国内平台**：稳定性更好
2. **国际平台配置代理**：提高速度和稳定性
3. **根据内容选择平台**：游戏选 Twitch，综合选 B 站

### Cookie 管理

1. **定期更新**：每月更新一次
2. **备份 Cookie**：防止丢失
3. **使用专用账号**：避免影响主账号

### 代理配置

1. **选择稳定的代理**：避免频繁断线
2. **测试代理速度**：选择最快的节点
3. **备用代理**：准备多个代理节点

### 多平台管理

1. **分组管理**：按平台或主播分组
2. **独立配置**：每个平台独立配置
3. **监控状态**：定期检查录制状态

## 下一步

- [故障排查](./troubleshooting.md) - 解决平台相关问题
- [高级配置](../configuration/advanced.md) - 深入配置选项
- [录制功能](./recording-streams.md) - 了解录制配置
