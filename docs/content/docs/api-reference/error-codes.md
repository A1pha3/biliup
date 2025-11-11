+++
title = "错误码"
description = "biliup 错误码参考文档"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 65
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "了解 biliup 的错误码及其处理方法"
toc = true
top = false
+++

本文档列出了 biliup 可能返回的所有错误码、错误含义以及相应的解决方案。

## 错误响应格式

所有 API 错误响应遵循统一的 JSON 格式：

```json
{
  "errors": [],
  "message": "错误描述信息"
}
```

**字段说明**:
- `errors`: 详细错误列表（可选）
- `message`: 错误描述信息

## HTTP 状态码

### 2xx 成功

#### 200 OK

请求成功。

**示例**:

```json
{
  "id": 1,
  "url": "https://live.bilibili.com/123456",
  "status": "success"
}
```

---

### 4xx 客户端错误

#### 400 Bad Request

请求参数错误或格式不正确。

**常见原因**:
- 缺少必需参数
- 参数类型错误
- 参数值不合法
- URL 格式不正确

**错误示例**:

```json
{
  "errors": [],
  "message": "Not supported url"
}
```

**解决方案**:
1. 检查请求参数是否完整
2. 验证参数类型和格式
3. 确认 URL 是否为支持的平台
4. 查看 API 文档确认正确的参数格式

**示例**:

```bash
# 错误：不支持的 URL
curl -X POST http://localhost:19159/api/v1/streamers \
  -H "Content-Type: application/json" \
  -d '{"url": "https://unsupported-platform.com/123"}'

# 响应：400 Bad Request
{
  "errors": [],
  "message": "Not supported url"
}
```

---

#### 401 Unauthorized

未认证或认证失败。

**常见原因**:
- 未登录
- 登录信息过期
- Cookie 无效

**错误示例**:

```json
{
  "errors": [],
  "message": "Unauthorized"
}
```

**解决方案**:
1. 使用 `biliup login` 重新登录
2. 检查 Cookie 文件是否存在且有效
3. 使用 `biliup renew` 刷新登录信息
4. 确认请求中携带了正确的会话 Cookie

---

#### 404 Not Found

请求的资源不存在。

**常见原因**:
- 任务 ID 不存在
- 视频 BV 号错误
- 文件路径不存在
- API 端点错误

**错误示例**:

```json
{
  "errors": [],
  "message": "Resource not found"
}
```

**解决方案**:
1. 确认资源 ID 是否正确
2. 检查 API 端点路径
3. 验证文件是否存在
4. 使用 `biliup list` 查看可用资源


### 5xx 服务器错误

#### 500 Internal Server Error

服务器内部错误。

**常见原因**:
- 数据库操作失败
- 文件系统错误
- 网络请求失败
- 未捕获的异常

**错误示例**:

```json
{
  "errors": [],
  "message": "Internal server error"
}
```

**解决方案**:
1. 查看服务器日志获取详细错误信息
2. 检查磁盘空间是否充足
3. 验证数据库文件是否正常
4. 重启 biliup 服务
5. 如果问题持续，提交 Issue 到 GitHub

---

## 应用错误码

### 通用错误

#### Unknown Error

未知错误，通常是未预期的异常。

**错误消息**: `Unknown Error`

**解决方案**:
1. 查看详细日志
2. 检查系统资源（内存、磁盘）
3. 重启服务
4. 提交 Bug 报告

---

### 网络错误

#### Connection Timeout

连接超时。

**错误消息**: `Connection timeout`

**常见原因**:
- 网络不稳定
- 目标服务器无响应
- 防火墙阻止连接

**解决方案**:
1. 检查网络连接
2. 尝试使用代理
3. 增加超时时间
4. 检查防火墙设置

---

#### Network Unreachable

网络不可达。

**错误消息**: `Network unreachable`

**解决方案**:
1. 检查网络连接
2. 验证 DNS 解析
3. 尝试使用代理
4. 检查路由配置

---

### 认证错误

#### Invalid Cookie

Cookie 无效或已过期。

**错误消息**: `Invalid cookie` 或 `Cookie expired`

**解决方案**:
1. 使用 `biliup login` 重新登录
2. 使用 `biliup renew` 刷新登录信息
3. 检查 Cookie 文件格式是否正确
4. 确认账号状态正常

---

#### Login Required

需要登录才能访问。

**错误消息**: `Login required`

**解决方案**:
1. 使用 `biliup login` 登录
2. 在 Web 界面登录
3. 配置正确的 Cookie 文件

---

### 文件错误

#### File Not Found

文件不存在。

**错误消息**: `File not found: <path>`

**解决方案**:
1. 检查文件路径是否正确
2. 确认文件是否存在
3. 验证文件权限
4. 使用绝对路径

---

#### File Too Large

文件过大。

**错误消息**: `File too large`

**常见原因**:
- 视频文件超过 8GB
- 磁盘空间不足

**解决方案**:
1. 压缩视频文件
2. 分割视频为多个部分
3. 清理磁盘空间
4. 使用视频编辑工具降低码率

---

#### Invalid File Format

文件格式不支持。

**错误消息**: `Invalid file format`

**解决方案**:
1. 转换为支持的格式（MP4、FLV 等）
2. 检查文件是否损坏
3. 使用 FFmpeg 重新编码

---

### 上传错误

#### Upload Failed

上传失败。

**错误消息**: `Upload failed`

**常见原因**:
- 网络中断
- 服务器拒绝
- 文件损坏
- 账号限制

**解决方案**:
1. 检查网络连接
2. 重试上传
3. 验证文件完整性
4. 检查账号状态
5. 尝试更换上传线路

---

#### Upload Quota Exceeded

上传配额超限。

**错误消息**: `Upload quota exceeded`

**解决方案**:
1. 等待配额重置（通常为每日重置）
2. 使用其他账号
3. 联系 B 站客服提升配额

---

### 直播录制错误

#### Stream Not Available

直播流不可用。

**错误消息**: `Stream not available` 或 `未开播`

**解决方案**:
1. 确认主播是否正在直播
2. 检查直播间 URL 是否正确
3. 验证网络连接
4. 等待主播开播

---

#### Stream URL Expired

直播流 URL 已过期。

**错误消息**: `Stream URL expired`

**解决方案**:
1. 重新获取直播流 URL
2. 检查系统时间是否正确
3. 刷新直播间页面

---

#### Recording Failed

录制失败。

**错误消息**: `Recording failed`

**常见原因**:
- 磁盘空间不足
- 网络中断
- 直播流中断
- 文件写入权限不足

**解决方案**:
1. 检查磁盘空间
2. 验证网络连接
3. 检查文件写入权限
4. 查看详细日志


### 数据库错误

#### Database Error

数据库操作失败。

**错误消息**: `Database error`

**常见原因**:
- 数据库文件损坏
- 磁盘空间不足
- 文件权限问题
- 并发冲突

**解决方案**:
1. 检查磁盘空间
2. 验证数据库文件权限
3. 备份并重建数据库
4. 重启服务

---

#### Configuration Error

配置错误。

**错误消息**: `Configuration error` 或 `有多个空间配置同时存在`

**解决方案**:
1. 检查配置文件格式
2. 删除重复的配置项
3. 重置配置为默认值
4. 查看配置文档

---

### B 站 API 错误

#### API Rate Limit

API 请求频率超限。

**错误消息**: `Rate limit exceeded`

**解决方案**:
1. 降低请求频率
2. 等待限制解除
3. 使用多个账号分散请求

---

#### Area Block

地区限制。

**错误消息**: `非常抱歉，根据版权方要求，您所在的地区无法观看本直播`

**解决方案**:
1. 使用代理服务器
2. 更换网络环境
3. 联系主播确认地区限制

---

#### Video Not Found

视频不存在或已删除。

**错误消息**: `Video not found`

**解决方案**:
1. 确认 BV 号是否正确
2. 检查视频是否被删除
3. 验证账号权限

---

## 错误处理最佳实践

### 1. 日志记录

启用详细日志以便排查问题：

```bash
# 启用 debug 日志
RUST_LOG=debug biliup server

# 或在命令中指定
biliup --rust-log debug upload video.mp4
```

---

### 2. 错误重试

实现自动重试机制：

```python
import time
from biliup.plugins.bilibili import Bililive

async def download_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            downloader = Bililive('output', url)
            is_live = await downloader.acheck_stream()
            if is_live:
                await downloader.astart()
                return True
        except Exception as e:
            print(f"尝试 {attempt + 1} 失败: {e}")
            if attempt < max_retries - 1:
                time.sleep(60)  # 等待 60 秒后重试
    return False
```

---

### 3. 错误通知

发送错误通知：

```python
import requests

def send_notification(error_message):
    """发送错误通知到 Telegram"""
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": f"❌ biliup 错误: {error_message}"
    }
    
    requests.post(url, json=data)

# 使用
try:
    # 执行操作
    pass
except Exception as e:
    send_notification(str(e))
```

---

### 4. 健康检查

定期检查服务状态：

```bash
#!/bin/bash
# health_check.sh

check_service() {
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:19159/api/v1/status)
    
    if [ "$response" = "200" ]; then
        echo "✓ 服务正常"
        return 0
    else
        echo "✗ 服务异常 (HTTP $response)"
        return 1
    fi
}

# 检查服务
if ! check_service; then
    echo "尝试重启服务..."
    systemctl restart biliup
    sleep 5
    
    if check_service; then
        echo "服务已恢复"
    else
        echo "服务重启失败，请手动检查"
        # 发送告警
    fi
fi
```

---

### 5. 错误分类处理

根据错误类型采取不同的处理策略：

```python
class ErrorHandler:
    @staticmethod
    def handle_error(error):
        error_msg = str(error).lower()
        
        # 网络错误 - 重试
        if 'timeout' in error_msg or 'connection' in error_msg:
            return 'retry'
        
        # 认证错误 - 重新登录
        elif 'unauthorized' in error_msg or 'cookie' in error_msg:
            return 'reauth'
        
        # 文件错误 - 跳过
        elif 'file not found' in error_msg:
            return 'skip'
        
        # 配额错误 - 等待
        elif 'quota' in error_msg or 'limit' in error_msg:
            return 'wait'
        
        # 其他错误 - 报告
        else:
            return 'report'

# 使用
handler = ErrorHandler()
action = handler.handle_error(exception)

if action == 'retry':
    # 重试操作
    pass
elif action == 'reauth':
    # 重新认证
    pass
elif action == 'skip':
    # 跳过当前任务
    pass
elif action == 'wait':
    # 等待一段时间
    pass
elif action == 'report':
    # 报告错误
    pass
```


## 常见错误场景

### 场景 1: 上传失败

**错误信息**: `Upload failed`

**排查步骤**:

1. 检查网络连接
```bash
ping bilibili.com
```

2. 验证登录状态
```bash
biliup renew
```

3. 检查文件完整性
```bash
ffmpeg -v error -i video.mp4 -f null -
```

4. 尝试更换上传线路
```bash
biliup upload video.mp4 --title "测试" --tid 171 --line kodo
```

5. 查看详细日志
```bash
RUST_LOG=debug biliup upload video.mp4 --title "测试" --tid 171
```

---

### 场景 2: 录制中断

**错误信息**: `Recording failed` 或 `Stream not available`

**排查步骤**:

1. 确认主播是否在线
```bash
curl "https://api.live.bilibili.com/room/v1/Room/get_info?room_id=123456"
```

2. 检查磁盘空间
```bash
df -h
```

3. 验证网络连接
```bash
ping live.bilibili.com
```

4. 检查文件权限
```bash
ls -la ./recordings/
```

5. 查看录制日志
```bash
tail -f download.log
```

---

### 场景 3: 服务无法启动

**错误信息**: `Address already in use` 或 `Permission denied`

**排查步骤**:

1. 检查端口占用
```bash
lsof -i :19159
# 或
netstat -tulpn | grep 19159
```

2. 更换端口
```bash
biliup server -p 8080
```

3. 检查权限
```bash
# 确保有执行权限
chmod +x biliup

# 检查数据目录权限
ls -la ~/.biliup/
```

4. 查看服务日志
```bash
journalctl -u biliup -f
```

---

### 场景 4: Cookie 过期

**错误信息**: `Unauthorized` 或 `Cookie expired`

**解决方案**:

```bash
# 方法 1: 刷新登录信息
biliup renew

# 方法 2: 重新登录
biliup login

# 方法 3: 手动更新 Cookie 文件
# 编辑 cookies.json，更新 Cookie 内容
```

---

### 场景 5: 数据库损坏

**错误信息**: `Database error` 或 `Database is locked`

**解决方案**:

```bash
# 1. 停止服务
systemctl stop biliup

# 2. 备份数据库
cp ~/.biliup/biliup.db ~/.biliup/biliup.db.backup

# 3. 检查数据库完整性
sqlite3 ~/.biliup/biliup.db "PRAGMA integrity_check;"

# 4. 如果损坏，尝试修复
sqlite3 ~/.biliup/biliup.db ".recover" | sqlite3 ~/.biliup/biliup_new.db
mv ~/.biliup/biliup_new.db ~/.biliup/biliup.db

# 5. 重启服务
systemctl start biliup
```

---

## 获取帮助

如果以上方法都无法解决问题，可以通过以下方式获取帮助：

### 1. 查看文档

- [官方文档](https://docs.biliup.rs)
- [GitHub Wiki](https://github.com/biliup/biliup/wiki)
- [常见问题](../user-guide/troubleshooting.md)

### 2. 社区支持

- [Telegram 群组](https://t.me/+IkpIABHqy6U0ZTQ5)
- [论坛](https://bbs.biliup.rs)
- [GitHub Discussions](https://github.com/biliup/biliup/discussions)

### 3. 提交 Issue

在 GitHub 上提交 Issue 时，请提供以下信息：

1. **环境信息**:
   - 操作系统和版本
   - biliup 版本
   - Python 版本（如果使用 Python）

2. **错误描述**:
   - 详细的错误信息
   - 复现步骤
   - 预期行为

3. **日志信息**:
   - 完整的错误日志
   - 相关的配置文件

4. **其他信息**:
   - 是否使用代理
   - 网络环境
   - 已尝试的解决方案

**Issue 模板**:

```markdown
## 环境信息
- 操作系统: Ubuntu 22.04
- biliup 版本: 1.1.22
- Python 版本: 3.11

## 问题描述
上传视频时出现 "Upload failed" 错误

## 复现步骤
1. 执行命令: `biliup upload video.mp4 --title "测试" --tid 171`
2. 等待上传
3. 出现错误

## 错误日志
```
[ERROR] Upload failed: Connection timeout
```

## 已尝试的解决方案
- 检查了网络连接
- 重新登录了账号
- 尝试了不同的上传线路

## 其他信息
- 使用了代理: http://127.0.0.1:7890
- 文件大小: 2GB
```

---

## 相关文档

- [REST API](./rest-api.md) - HTTP 接口文档
- [WebSocket API](./websocket-api.md) - 实时通信接口
- [Python API](./python-api.md) - Python 库接口
- [CLI 参考](./cli-reference.md) - 命令行工具
- [故障排查](../user-guide/troubleshooting.md) - 常见问题解决
