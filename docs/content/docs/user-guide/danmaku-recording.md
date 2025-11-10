+++
title = "弹幕录制"
description = "了解如何使用 biliup 录制直播弹幕，保存观众互动内容"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 50
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "biliup 支持录制直播弹幕，将观众的评论和互动保存为 XML 文件，方便后期制作和回顾。"
toc = true
top = false
+++

## 弹幕录制简介

弹幕录制功能可以在录制直播视频的同时，保存直播间的弹幕消息。这些弹幕可以用于：

- **后期制作**：使用弹幕工具将弹幕嵌入视频
- **数据分析**：分析观众互动和热度
- **内容回顾**：查看观众的实时反应
- **精彩时刻**：根据弹幕密度找到精彩片段

## 支持的平台

目前 biliup 支持以下平台的弹幕录制：

### 完全支持

- **B 站直播** - 支持所有弹幕类型
- **斗鱼** - 支持文字弹幕和礼物消息
- **虎牙** - 支持文字弹幕和礼物消息

### 部分支持

- **抖音** - 仅支持文字弹幕
- **快手** - 仅支持文字弹幕

### 不支持

- Twitch（使用 IRC 协议，需要单独工具）
- YouTube（需要 API 权限）
- 其他国际平台

## 启用弹幕录制

### 通过配置文件启用

编辑 `config.yaml` 文件：

```yaml
streamers:
  主播名称:
    url: ["https://live.bilibili.com/123456"]
    format: "flv"
    danmaku:
      enabled: true  # 启用弹幕录制
```

### 通过 WebUI 启用

1. 打开 WebUI 界面
2. 进入"直播管理"页面
3. 编辑或创建录制任务
4. 找到"弹幕录制"选项
5. 勾选"启用弹幕录制"
6. 保存配置

### 全局启用

为所有任务启用弹幕录制：

```yaml
global:
  danmaku:
    enabled: true  # 全局启用
```

然后在特定任务中可以选择禁用：

```yaml
streamers:
  不需要弹幕的主播:
    url: ["直播间URL"]
    danmaku:
      enabled: false  # 禁用此任务的弹幕录制
```

## 弹幕文件格式

### XML 格式

biliup 将弹幕保存为 XML 格式，兼容主流弹幕工具。

**文件命名**：

```
视频文件名.xml
```

例如：
```
主播名称_2025-01-10_20-00-00.flv
主播名称_2025-01-10_20-00-00.xml
```

**XML 结构**：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<i>
  <chatserver>chat.bilibili.com</chatserver>
  <chatid>123456</chatid>
  <mission>0</mission>
  <maxlimit>8000</maxlimit>
  <state>0</state>
  <real_name>0</real_name>
  <source>k-v</source>
  
  <d p="0.00,1,25,16777215,1704891000,0,用户ID,弹幕ID">弹幕内容</d>
  <d p="1.50,1,25,16777215,1704891001,0,用户ID,弹幕ID">另一条弹幕</d>
  ...
</i>
```

**弹幕属性说明**：

`<d p="时间,类型,字号,颜色,时间戳,弹幕池,用户ID,弹幕ID">弹幕内容</d>`

- **时间**：弹幕出现的时间（秒）
- **类型**：1=滚动，4=底部，5=顶部
- **字号**：字体大小（25=标准）
- **颜色**：RGB 颜色值
- **时间戳**：发送时间的 Unix 时间戳
- **弹幕池**：0=普通，1=字幕，2=高级
- **用户ID**：发送者的用户 ID
- **弹幕ID**：弹幕的唯一标识

### ASS 格式（可选）

某些工具支持将 XML 转换为 ASS 字幕格式：

```bash
# 使用 DanmakuFactory 转换
DanmakuFactory -i input.xml -o output.ass
```

## 弹幕文件存储

### 默认存储位置

弹幕文件与视频文件保存在同一目录：

```
downloads/
  └── 主播名称/
      ├── 2025-01-10_20-00-00.flv
      └── 2025-01-10_20-00-00.xml
```

### 自定义存储位置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      output_dir: "/path/to/danmaku"  # 自定义弹幕目录
```

### 分离存储

将弹幕和视频分开存储：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    output_dir: "/videos"
    danmaku:
      enabled: true
      output_dir: "/danmaku"
```

## 弹幕录制配置

### 基本配置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      format: "xml"  # 弹幕格式
```

### 过滤配置

过滤不需要的弹幕：

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      filters:
        # 过滤关键词
        keywords: ["广告", "刷屏"]
        
        # 过滤用户
        users: ["spam_user_id"]
        
        # 只保留文字弹幕
        types: ["text"]  # text, gift, enter, follow
        
        # 最小弹幕长度
        min_length: 2
        
        # 最大弹幕长度
        max_length: 100
```

### 高级配置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      
      # 弹幕缓冲区大小
      buffer_size: 1000
      
      # 保存间隔（秒）
      save_interval: 60
      
      # 重连设置
      reconnect:
        enabled: true
        max_attempts: 5
        interval: 10
```

## 使用弹幕文件

### DanmakuFactory

DanmakuFactory 是一个强大的弹幕转换工具。

**安装**：

```bash
# 从 GitHub 下载
# https://github.com/hihkm/DanmakuFactory/releases
```

**使用**：

```bash
# 转换为 ASS 字幕
DanmakuFactory -i input.xml -o output.ass

# 自定义参数
DanmakuFactory -i input.xml -o output.ass \
  --resolution 1920x1080 \
  --fontsize 38 \
  --opacity 0.8
```

**嵌入视频**：

```bash
# 使用 ffmpeg 嵌入字幕
ffmpeg -i video.mp4 -vf "ass=output.ass" output_with_danmaku.mp4
```

### AList 弹幕播放

如果使用 AList 管理视频文件，可以直接播放带弹幕的视频。

**配置**：

1. 将视频和弹幕文件放在同一目录
2. 确保文件名相同（除扩展名）
3. 在 AList 中播放视频时会自动加载弹幕

### 弹弹play

弹弹play 支持本地视频弹幕播放。

**使用**：

1. 下载并安装弹弹play
2. 打开视频文件
3. 加载对应的 XML 弹幕文件
4. 享受带弹幕的观看体验

### B 站创作中心

如果要将弹幕嵌入视频后上传到 B 站：

1. 使用 DanmakuFactory 转换弹幕
2. 使用视频编辑软件嵌入弹幕
3. 导出最终视频
4. 上传到 B 站


## 弹幕数据分析

### 提取弹幕统计

使用 Python 脚本分析弹幕：

```python
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime

def analyze_danmaku(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    danmaku_list = []
    for d in root.findall('d'):
        attrs = d.get('p').split(',')
        danmaku_list.append({
            'time': float(attrs[0]),
            'content': d.text,
            'timestamp': int(attrs[4])
        })
    
    # 统计总数
    total = len(danmaku_list)
    print(f"总弹幕数: {total}")
    
    # 弹幕密度（每分钟）
    if danmaku_list:
        duration = max(d['time'] for d in danmaku_list)
        density = total / (duration / 60)
        print(f"弹幕密度: {density:.2f} 条/分钟")
    
    # 高频词汇
    words = ' '.join(d['content'] for d in danmaku_list).split()
    common_words = Counter(words).most_common(10)
    print("高频词汇:", common_words)
    
    return danmaku_list

# 使用
danmaku_data = analyze_danmaku('弹幕文件.xml')
```

### 找到精彩时刻

根据弹幕密度找到精彩片段：

```python
def find_highlights(danmaku_list, window=60):
    """
    找到弹幕密集的时间段
    window: 时间窗口（秒）
    """
    if not danmaku_list:
        return []
    
    max_time = max(d['time'] for d in danmaku_list)
    highlights = []
    
    for t in range(0, int(max_time), window):
        count = sum(1 for d in danmaku_list 
                   if t <= d['time'] < t + window)
        if count > 50:  # 阈值：60秒内超过50条弹幕
            highlights.append({
                'start': t,
                'end': t + window,
                'count': count
            })
    
    return highlights

# 使用
highlights = find_highlights(danmaku_data)
for h in highlights:
    print(f"精彩时刻: {h['start']}s - {h['end']}s, 弹幕数: {h['count']}")
```

### 情感分析

使用简单的关键词分析弹幕情感：

```python
def sentiment_analysis(danmaku_list):
    positive_words = ['哈哈', '666', '牛', '强', '好', '赞']
    negative_words = ['菜', '差', '烂', '垃圾']
    
    positive_count = 0
    negative_count = 0
    
    for d in danmaku_list:
        content = d['content']
        if any(word in content for word in positive_words):
            positive_count += 1
        if any(word in content for word in negative_words):
            negative_count += 1
    
    print(f"正面弹幕: {positive_count}")
    print(f"负面弹幕: {negative_count}")
    
    if positive_count + negative_count > 0:
        ratio = positive_count / (positive_count + negative_count)
        print(f"正面比例: {ratio:.2%}")

# 使用
sentiment_analysis(danmaku_data)
```

## 弹幕录制场景

### 场景 1：完整录制所有弹幕

适合：需要完整保存观众互动

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"
    danmaku:
      enabled: true
      format: "xml"
      # 不设置过滤器，保存所有弹幕
```

### 场景 2：只保存文字弹幕

适合：不需要礼物和进场消息

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      filters:
        types: ["text"]  # 只保存文字弹幕
```

### 场景 3：过滤广告和刷屏

适合：提高弹幕质量

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    danmaku:
      enabled: true
      filters:
        keywords: ["广告", "加群", "刷屏", "复制"]
        min_length: 2  # 过滤单字弹幕
```

### 场景 4：多平台弹幕录制

同时录制多个平台的弹幕：

```yaml
streamers:
  B站主播:
    url: ["https://live.bilibili.com/123456"]
    danmaku:
      enabled: true
      output_dir: "/danmaku/bilibili"
  
  斗鱼主播:
    url: ["https://www.douyu.com/123456"]
    danmaku:
      enabled: true
      output_dir: "/danmaku/douyu"
```

## 常见问题

### 弹幕文件为空？

**可能原因**：
- 直播间没有弹幕
- 弹幕录制未正确启用
- 网络连接问题
- 平台限制

**解决方案**：

1. 检查配置：
```yaml
danmaku:
  enabled: true  # 确保已启用
```

2. 查看日志：
```bash
grep "danmaku" biliup.log
```

3. 测试连接：
```bash
# 手动测试弹幕连接
# 查看是否能正常接收弹幕
```

### 弹幕时间不同步？

**可能原因**：
- 录制开始时间和弹幕开始时间不一致
- 网络延迟

**解决方案**：

使用工具调整弹幕时间：

```python
import xml.etree.ElementTree as ET

def adjust_danmaku_time(xml_file, offset):
    """
    调整弹幕时间
    offset: 时间偏移（秒），正数延后，负数提前
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    for d in root.findall('d'):
        attrs = d.get('p').split(',')
        time = float(attrs[0]) + offset
        attrs[0] = f"{time:.2f}"
        d.set('p', ','.join(attrs))
    
    tree.write(xml_file, encoding='UTF-8', xml_declaration=True)

# 使用：将弹幕延后 5 秒
adjust_danmaku_time('弹幕文件.xml', 5)
```

### 弹幕文件损坏？

**可能原因**：
- 录制中断
- 磁盘空间不足
- 程序崩溃

**解决方案**：

1. 检查 XML 格式：
```bash
xmllint --noout 弹幕文件.xml
```

2. 尝试修复：
```python
import xml.etree.ElementTree as ET

def repair_danmaku(xml_file):
    try:
        tree = ET.parse(xml_file)
        # 如果能解析，重新保存
        tree.write(xml_file + '.repaired', 
                  encoding='UTF-8', 
                  xml_declaration=True)
        print("修复成功")
    except ET.ParseError as e:
        print(f"无法修复: {e}")

repair_danmaku('弹幕文件.xml')
```

### 弹幕太多导致文件过大？

**解决方案**：

1. 启用过滤：
```yaml
danmaku:
  enabled: true
  filters:
    min_length: 2
    keywords: ["刷屏内容"]
```

2. 定期清理：
```bash
# 删除 30 天前的弹幕文件
find /path/to/danmaku -name "*.xml" -mtime +30 -delete
```

3. 压缩存储：
```bash
# 压缩弹幕文件
gzip *.xml
```

### 某些平台无法录制弹幕？

**支持情况**：
- ✅ B 站直播 - 完全支持
- ✅ 斗鱼 - 完全支持
- ✅ 虎牙 - 完全支持
- ⚠️ 抖音 - 部分支持
- ⚠️ 快手 - 部分支持
- ❌ Twitch - 不支持（需要单独工具）
- ❌ YouTube - 不支持（需要 API）

**Twitch 弹幕录制**：

使用专门的 IRC 客户端：

```bash
# 使用 Twitch IRC
# 需要单独配置
```

## 弹幕工具推荐

### DanmakuFactory

- **功能**：弹幕转换和渲染
- **支持格式**：XML、JSON、ASS
- **下载**：https://github.com/hihkm/DanmakuFactory

### 弹弹play

- **功能**：本地视频弹幕播放
- **支持格式**：XML、JSON
- **下载**：http://www.dandanplay.com/

### AList

- **功能**：网盘管理和在线播放
- **支持弹幕**：自动加载同名 XML 文件
- **下载**：https://alist.nn.ci/

### Aegisub

- **功能**：字幕编辑（可编辑 ASS 弹幕）
- **支持格式**：ASS、SRT
- **下载**：http://www.aegisub.org/

## 最佳实践

### 弹幕命名规范

保持弹幕文件和视频文件名一致：

```
视频文件: 主播名称_2025-01-10_20-00-00.flv
弹幕文件: 主播名称_2025-01-10_20-00-00.xml
```

### 弹幕备份

定期备份重要的弹幕文件：

```bash
# 备份脚本
#!/bin/bash
BACKUP_DIR="/backup/danmaku"
SOURCE_DIR="/downloads"

# 创建备份目录
mkdir -p "$BACKUP_DIR/$(date +%Y-%m-%d)"

# 复制弹幕文件
find "$SOURCE_DIR" -name "*.xml" -mtime -1 \
  -exec cp {} "$BACKUP_DIR/$(date +%Y-%m-%d)/" \;

# 压缩备份
cd "$BACKUP_DIR"
tar -czf "danmaku_$(date +%Y-%m-%d).tar.gz" "$(date +%Y-%m-%d)"
rm -rf "$(date +%Y-%m-%d)"
```

### 弹幕清理

定期清理旧的弹幕文件：

```bash
# 删除 90 天前的弹幕
find /downloads -name "*.xml" -mtime +90 -delete

# 或压缩后归档
find /downloads -name "*.xml" -mtime +30 -exec gzip {} \;
```

### 弹幕质量控制

使用过滤器提高弹幕质量：

```yaml
danmaku:
  enabled: true
  filters:
    # 过滤短弹幕
    min_length: 2
    
    # 过滤长弹幕（可能是刷屏）
    max_length: 50
    
    # 过滤关键词
    keywords: ["广告", "加群", "复制"]
    
    # 只保留文字弹幕
    types: ["text"]
```

## 下一步

- [平台支持](./platform-support.md) - 查看各平台的弹幕支持情况
- [故障排查](./troubleshooting.md) - 解决弹幕录制问题
- [高级配置](../configuration/advanced.md) - 深入配置选项
