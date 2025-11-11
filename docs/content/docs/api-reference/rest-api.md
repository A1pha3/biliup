+++
title = "REST API"
description = "biliup REST API 完整参考文档"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 61
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "通过 HTTP 接口管理录制任务、配置和视频上传"
toc = true
top = false
+++

biliup 提供了完整的 REST API，允许你通过 HTTP 请求管理录制任务、配置系统和上传视频。所有 API 端点都基于 `/api/v1` 路径。

## 基础信息

### Base URL

```
http://localhost:19159/api/v1
```

默认端口为 19159，可以通过启动参数修改。

### 认证方式

大部分 API 需要通过会话认证。你需要先通过登录接口获取会话，然后在后续请求中携带会话 Cookie。

### 响应格式

所有 API 响应均为 JSON 格式。成功响应返回 200 状态码，错误响应返回相应的 HTTP 错误码和错误信息。

### 错误处理

错误响应格式：

```json
{
  "error": "错误描述信息"
}
```

常见 HTTP 状态码：
- `200 OK`: 请求成功
- `400 Bad Request`: 请求参数错误
- `401 Unauthorized`: 未认证
- `404 Not Found`: 资源不存在
- `500 Internal Server Error`: 服务器内部错误


## 认证 API

### 用户注册

创建新用户账号。

**端点**: `POST /users/register`

**请求体**:

```json
{
  "username": "admin",
  "password": "password123"
}
```

**响应**: `200 OK`

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"password123"}'
```

---

### 用户登录

使用用户名和密码登录系统。

**端点**: `POST /users/login`

**请求体**:

```json
{
  "username": "admin",
  "password": "password123",
  "next": "/dashboard"
}
```

**参数说明**:
- `username`: 用户名（必需）
- `password`: 密码（必需）
- `next`: 登录后跳转的 URL（可选）

**响应**: `200 OK`

成功后会设置会话 Cookie，后续请求需要携带此 Cookie。

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"admin","password":"password123"}'
```

---

### 检查用户状态

检查当前用户是否已登录。

**端点**: `GET /users/biliup`

**响应**: 
- `200 OK`: 用户已登录
- `404 Not Found`: 用户未登录

**示例**:

```bash
curl http://localhost:19159/api/v1/users/biliup \
  -b cookies.txt
```

---

### 用户登出

退出当前登录会话。

**端点**: `GET /logout`

**响应**: 重定向到登录页面

**示例**:

```bash
curl http://localhost:19159/api/v1/logout \
  -b cookies.txt
```


## 录制任务 API

### 获取所有录制任务

获取所有录制任务及其状态。

**端点**: `GET /streamers`

**响应**:

```json
[
  {
    "status": "Working",
    "upload_status": "Idle",
    "inner": {
      "id": 1,
      "url": "https://live.bilibili.com/123456",
      "template_name": "默认模板",
      "remark": "主播备注",
      "split_time": 3600,
      "split_size": 2048
    }
  }
]
```

**字段说明**:
- `status`: 录制状态（Idle/Working/Pause）
- `upload_status`: 上传状态（Idle/Working）
- `inner.id`: 任务 ID
- `inner.url`: 直播间 URL
- `inner.template_name`: 使用的上传模板名称
- `inner.remark`: 任务备注
- `inner.split_time`: 分段时长（秒）
- `inner.split_size`: 分段大小（MB）

**示例**:

```bash
curl http://localhost:19159/api/v1/streamers \
  -b cookies.txt
```

---

### 创建录制任务

添加新的录制任务。

**端点**: `POST /streamers`

**请求体**:

```json
{
  "url": "https://live.bilibili.com/123456",
  "template_name": "默认模板",
  "remark": "主播备注",
  "split_time": 3600,
  "split_size": 2048
}
```

**参数说明**:
- `url`: 直播间 URL（必需）
- `template_name`: 上传模板名称（可选）
- `remark`: 任务备注（可选）
- `split_time`: 分段时长，单位秒（可选，默认 3600）
- `split_size`: 分段大小，单位 MB（可选，默认 2048）

**响应**: `200 OK`

```json
{
  "id": 1,
  "url": "https://live.bilibili.com/123456",
  "template_name": "默认模板",
  "remark": "主播备注",
  "split_time": 3600,
  "split_size": 2048
}
```

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/streamers \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "url": "https://live.bilibili.com/123456",
    "template_name": "默认模板",
    "remark": "测试主播"
  }'
```

---

### 更新录制任务

更新现有录制任务的配置。

**端点**: `PUT /streamers`

**请求体**:

```json
{
  "id": 1,
  "url": "https://live.bilibili.com/123456",
  "template_name": "新模板",
  "remark": "更新后的备注",
  "split_time": 7200,
  "split_size": 4096
}
```

**响应**: `200 OK`

返回更新后的任务信息。

**示例**:

```bash
curl -X PUT http://localhost:19159/api/v1/streamers \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id": 1,
    "url": "https://live.bilibili.com/123456",
    "template_name": "新模板",
    "remark": "更新后的备注"
  }'
```

---

### 删除录制任务

删除指定的录制任务。

**端点**: `DELETE /streamers/{id}`

**路径参数**:
- `id`: 任务 ID

**响应**: `200 OK`

返回被删除的任务信息。

**示例**:

```bash
curl -X DELETE http://localhost:19159/api/v1/streamers/1 \
  -b cookies.txt
```

---

### 暂停/恢复录制任务

暂停正在运行的任务或恢复已暂停的任务。

**端点**: `POST /streamers/{id}/pause`

**路径参数**:
- `id`: 任务 ID

**行为**:
- 如果任务正在录制（Working），则暂停任务
- 如果任务已暂停（Pause），则恢复任务为空闲状态（Idle）
- 如果任务处于其他状态，则设置为暂停状态

**响应**: `200 OK`

**示例**:

```bash
# 暂停任务
curl -X POST http://localhost:19159/api/v1/streamers/1/pause \
  -b cookies.txt

# 再次调用恢复任务
curl -X POST http://localhost:19159/api/v1/streamers/1/pause \
  -b cookies.txt
```


## 配置管理 API

### 获取全局配置

获取系统的全局配置。

**端点**: `GET /configuration`

**响应**:

```json
{
  "lines": "bda2",
  "threads": 3,
  "submit_api": null,
  "download_limit": 5,
  "upload_limit": 2
}
```

**字段说明**:
- `lines`: 上传线路（bda2/kodo/ws/qn 等）
- `threads`: 上传线程数
- `submit_api`: 自定义提交 API（可选）
- `download_limit`: 同时下载任务数限制
- `upload_limit`: 同时上传任务数限制

**示例**:

```bash
curl http://localhost:19159/api/v1/configuration \
  -b cookies.txt
```

---

### 更新全局配置

更新系统的全局配置。

**端点**: `PUT /configuration`

**请求体**:

```json
{
  "lines": "bda2",
  "threads": 5,
  "submit_api": null,
  "download_limit": 10,
  "upload_limit": 3
}
```

**响应**: `200 OK`

返回更新后的配置。

**示例**:

```bash
curl -X PUT http://localhost:19159/api/v1/configuration \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "lines": "bda2",
    "threads": 5,
    "download_limit": 10,
    "upload_limit": 3
  }'
```


## 上传模板 API

### 获取所有上传模板

获取所有配置的上传模板。

**端点**: `GET /upload_streamers`

**响应**:

```json
[
  {
    "id": 1,
    "template_name": "默认模板",
    "title": "{{title}}",
    "tid": 171,
    "tag": "游戏,直播录像",
    "copyright": 1,
    "source": "",
    "desc": "直播录像",
    "dynamic": "",
    "cover": "",
    "dolby": 0,
    "hires": 0,
    "no_reprint": 1,
    "open_elec": 1,
    "user_cookie": "cookies.json"
  }
]
```

**示例**:

```bash
curl http://localhost:19159/api/v1/upload_streamers \
  -b cookies.txt
```

---

### 获取单个上传模板

获取指定 ID 的上传模板详情。

**端点**: `GET /upload_streamers/{id}`

**路径参数**:
- `id`: 模板 ID

**响应**: `200 OK`

返回模板详细信息。

**示例**:

```bash
curl http://localhost:19159/api/v1/upload_streamers/1 \
  -b cookies.txt
```

---

### 创建或更新上传模板

创建新模板或更新现有模板。

**端点**: `POST /upload_streamers`

**请求体**:

```json
{
  "id": null,
  "template_name": "新模板",
  "title": "{{title}}",
  "tid": 171,
  "tag": "游戏,直播",
  "copyright": 1,
  "source": "",
  "desc": "直播录像",
  "dynamic": "",
  "cover": "",
  "dolby": 0,
  "hires": 0,
  "no_reprint": 1,
  "open_elec": 1,
  "user_cookie": "cookies.json"
}
```

**参数说明**:
- `id`: 模板 ID（null 表示创建新模板，有值表示更新）
- `template_name`: 模板名称
- `title`: 视频标题模板（支持变量）
- `tid`: 分区 ID
- `tag`: 标签（逗号分隔）
- `copyright`: 版权声明（1=自制，2=转载）
- `source`: 转载来源
- `desc`: 视频简介
- `dynamic`: 动态内容
- `cover`: 封面图片路径
- `dolby`: 是否杜比音效（0/1）
- `hires`: 是否高分辨率（0/1）
- `no_reprint`: 禁止转载（0/1）
- `open_elec`: 开启充电（0/1）
- `user_cookie`: 使用的 Cookie 文件名

**响应**: `200 OK`

返回创建或更新后的模板信息。

**示例**:

```bash
# 创建新模板
curl -X POST http://localhost:19159/api/v1/upload_streamers \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id": null,
    "template_name": "新模板",
    "title": "{{title}}",
    "tid": 171,
    "tag": "游戏,直播"
  }'

# 更新模板
curl -X POST http://localhost:19159/api/v1/upload_streamers \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id": 1,
    "template_name": "更新的模板",
    "title": "新标题"
  }'
```

---

### 删除上传模板

删除指定的上传模板。

**端点**: `DELETE /upload_streamers/{id}`

**路径参数**:
- `id`: 模板 ID

**响应**: `200 OK`

**示例**:

```bash
curl -X DELETE http://localhost:19159/api/v1/upload_streamers/1 \
  -b cookies.txt
```


## 视频管理 API

### 获取视频列表

获取当前目录下的所有视频文件。

**端点**: `GET /videos`

**响应**:

```json
[
  {
    "key": 1,
    "name": "recording_20250110_120000.mp4",
    "updateTime": 1704873600,
    "size": 1073741824
  }
]
```

**字段说明**:
- `key`: 视频序号
- `name`: 文件名
- `updateTime`: 修改时间（Unix 时间戳）
- `size`: 文件大小（字节）

**示例**:

```bash
curl http://localhost:19159/api/v1/videos \
  -b cookies.txt
```

---

### 上传视频

手动上传指定的视频文件到 B 站。

**端点**: `POST /uploads`

**请求体**:

```json
{
  "files": [
    "recording_20250110_120000.mp4",
    "recording_20250110_130000.mp4"
  ],
  "params": {
    "template_name": "默认模板",
    "title": "直播录像 2025-01-10",
    "tid": 171,
    "tag": "游戏,直播录像",
    "copyright": 1,
    "source": "",
    "desc": "直播录像",
    "dynamic": "",
    "cover": "",
    "dolby": 0,
    "hires": 0,
    "no_reprint": 1,
    "open_elec": 1,
    "user_cookie": "cookies.json"
  }
}
```

**参数说明**:
- `files`: 要上传的视频文件路径数组
- `params`: 上传参数（与上传模板字段相同）

**响应**: `200 OK`

```json
{}
```

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/uploads \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "files": ["recording.mp4"],
    "params": {
      "template_name": "默认模板",
      "title": "测试视频",
      "tid": 171,
      "tag": "测试",
      "user_cookie": "cookies.json"
    }
  }'
```


## B 站账号管理 API

### 获取 B 站账号列表

获取所有已配置的 B 站账号 Cookie。

**端点**: `GET /users`

**响应**:

```json
[
  {
    "id": 1,
    "name": "cookies.json",
    "value": "cookies.json",
    "platform": "bilibili-cookies"
  }
]
```

**示例**:

```bash
curl http://localhost:19159/api/v1/users \
  -b cookies.txt
```

---

### 添加 B 站账号

添加新的 B 站账号 Cookie 配置。

**端点**: `POST /users`

**请求体**:

```json
{
  "key": "bilibili-cookies",
  "value": "new_cookies.json"
}
```

**响应**: `200 OK`

返回添加的配置信息。

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/users \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "key": "bilibili-cookies",
    "value": "new_cookies.json"
  }'
```

---

### 删除 B 站账号

删除指定的 B 站账号配置。

**端点**: `DELETE /users/{id}`

**路径参数**:
- `id`: 配置 ID

**响应**: `200 OK`

**示例**:

```bash
curl -X DELETE http://localhost:19159/api/v1/users/1 \
  -b cookies.txt
```

---

### 获取二维码登录

获取 B 站登录二维码。

**端点**: `GET /qrcode`

**响应**:

```json
{
  "url": "https://passport.bilibili.com/...",
  "qrcode_key": "..."
}
```

**字段说明**:
- `url`: 二维码 URL
- `qrcode_key`: 二维码密钥（用于轮询登录状态）

**示例**:

```bash
curl http://localhost:19159/api/v1/qrcode
```

---

### 二维码登录

使用二维码完成登录。

**端点**: `POST /login_by_qrcode`

**请求体**:

```json
{
  "qrcode_key": "..."
}
```

**响应**: `200 OK`

```json
{
  "filename": "data/123456789.json"
}
```

成功后会将登录信息保存到指定文件。

**示例**:

```bash
curl -X POST http://localhost:19159/api/v1/login_by_qrcode \
  -H "Content-Type: application/json" \
  -d '{
    "qrcode_key": "..."
  }'
```


## B 站 API 代理

### 获取投稿预处理信息

获取 B 站投稿所需的预处理信息（分区、标签等）。

**端点**: `GET /archive_pre`

**响应**:

```json
{
  "typelist": [...],
  "archive_tags": [...],
  ...
}
```

**示例**:

```bash
curl http://localhost:19159/api/v1/archive_pre \
  -b cookies.txt
```

---

### 获取 B 站用户信息

获取指定 B 站账号的用户信息。

**端点**: `GET /myinfo`

**查询参数**:
- `user`: Cookie 文件名

**响应**:

```json
{
  "mid": 123456789,
  "uname": "用户名",
  "face": "头像URL",
  ...
}
```

**示例**:

```bash
curl "http://localhost:19159/api/v1/myinfo?user=cookies.json" \
  -b cookies.txt
```

---

### HTTP 代理

代理 HTTP 请求，用于获取外部资源。

**端点**: `GET /proxy`

**查询参数**:
- `url`: 要代理的 URL

**响应**: 返回目标 URL 的响应内容

**示例**:

```bash
curl "http://localhost:19159/api/v1/proxy?url=https://example.com/image.jpg" \
  -b cookies.txt
```


## 系统状态 API

### 获取系统状态

获取系统运行状态和统计信息。

**端点**: `GET /status`

**响应**:

```json
{
  "version": "1.1.22",
  "rooms": [
    {
      "downloader_status": "Working",
      "uploader_status": "Idle",
      "live_streamer": {
        "id": 1,
        "url": "https://live.bilibili.com/123456",
        "template_name": "默认模板",
        "remark": "主播备注"
      },
      "upload_streamer": {
        "template_name": "默认模板",
        "title": "{{title}}",
        "tid": 171
      }
    }
  ],
  "download_semaphore": 5,
  "update_semaphore": 2,
  "config": {
    "lines": "bda2",
    "threads": 3,
    "download_limit": 5,
    "upload_limit": 2
  }
}
```

**字段说明**:
- `version`: biliup 版本号
- `rooms`: 所有录制任务的详细状态
- `download_semaphore`: 可用下载槽位数
- `update_semaphore`: 可用上传槽位数
- `config`: 全局配置

**示例**:

```bash
curl http://localhost:19159/api/v1/status \
  -b cookies.txt
```

---

### 获取录制信息

获取已录制的视频信息。

**端点**: `GET /streamer_info`

**响应**:

```json
[
  {
    "id": 1,
    "template_name": "默认模板",
    "stream_title": "直播标题",
    "streamer_name": "主播名称",
    "start_time": "2025-01-10T12:00:00Z",
    "video_path": "/path/to/video.mp4"
  }
]
```

**示例**:

```bash
curl http://localhost:19159/api/v1/streamer_info \
  -b cookies.txt
```

---

### 获取录制文件列表

获取指定录制信息的文件列表。

**端点**: `GET /streamer_info/{id}/files`

**路径参数**:
- `id`: 录制信息 ID

**响应**:

```json
[
  {
    "id": 1,
    "streamer_info_id": 1,
    "file_path": "/path/to/video_part1.mp4",
    "file_size": 1073741824,
    "duration": 3600
  }
]
```

**示例**:

```bash
curl http://localhost:19159/api/v1/streamer_info/1/files \
  -b cookies.txt
```


## 完整示例

### Python 示例

使用 Python requests 库调用 API：

```python
import requests

# 基础 URL
BASE_URL = "http://localhost:19159/api/v1"

# 创建会话
session = requests.Session()

# 登录
login_data = {
    "username": "admin",
    "password": "password123"
}
response = session.post(f"{BASE_URL}/users/login", json=login_data)
print(f"登录状态: {response.status_code}")

# 获取所有录制任务
response = session.get(f"{BASE_URL}/streamers")
streamers = response.json()
print(f"录制任务数量: {len(streamers)}")

# 创建新任务
new_streamer = {
    "url": "https://live.bilibili.com/123456",
    "template_name": "默认模板",
    "remark": "测试主播"
}
response = session.post(f"{BASE_URL}/streamers", json=new_streamer)
streamer = response.json()
print(f"创建任务 ID: {streamer['id']}")

# 暂停任务
streamer_id = streamer['id']
response = session.post(f"{BASE_URL}/streamers/{streamer_id}/pause")
print(f"暂停任务: {response.status_code}")

# 获取系统状态
response = session.get(f"{BASE_URL}/status")
status = response.json()
print(f"系统版本: {status['version']}")
print(f"运行中的任务: {len(status['rooms'])}")
```

---

### JavaScript 示例

使用 fetch API 调用：

```javascript
const BASE_URL = 'http://localhost:19159/api/v1';

// 登录
async function login(username, password) {
  const response = await fetch(`${BASE_URL}/users/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  });
  return response.ok;
}

// 获取录制任务
async function getStreamers() {
  const response = await fetch(`${BASE_URL}/streamers`, {
    credentials: 'include',
  });
  return await response.json();
}

// 创建录制任务
async function createStreamer(url, templateName, remark) {
  const response = await fetch(`${BASE_URL}/streamers`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({
      url,
      template_name: templateName,
      remark,
    }),
  });
  return await response.json();
}

// 使用示例
(async () => {
  await login('admin', 'password123');
  const streamers = await getStreamers();
  console.log('录制任务:', streamers);
  
  const newStreamer = await createStreamer(
    'https://live.bilibili.com/123456',
    '默认模板',
    '测试主播'
  );
  console.log('新任务 ID:', newStreamer.id);
})();
```

---

### cURL 完整工作流

```bash
# 1. 登录
curl -X POST http://localhost:19159/api/v1/users/login \
  -H "Content-Type: application/json" \
  -c cookies.txt \
  -d '{"username":"admin","password":"password123"}'

# 2. 获取系统状态
curl http://localhost:19159/api/v1/status \
  -b cookies.txt

# 3. 创建录制任务
curl -X POST http://localhost:19159/api/v1/streamers \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "url": "https://live.bilibili.com/123456",
    "template_name": "默认模板",
    "remark": "测试主播"
  }'

# 4. 获取所有任务
curl http://localhost:19159/api/v1/streamers \
  -b cookies.txt

# 5. 暂停任务（假设 ID 为 1）
curl -X POST http://localhost:19159/api/v1/streamers/1/pause \
  -b cookies.txt

# 6. 获取视频列表
curl http://localhost:19159/api/v1/videos \
  -b cookies.txt

# 7. 手动上传视频
curl -X POST http://localhost:19159/api/v1/uploads \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "files": ["recording.mp4"],
    "params": {
      "template_name": "默认模板",
      "title": "测试视频",
      "tid": 171,
      "tag": "测试",
      "user_cookie": "cookies.json"
    }
  }'

# 8. 登出
curl http://localhost:19159/api/v1/logout \
  -b cookies.txt
```

## 注意事项

1. **会话管理**: 所有需要认证的 API 都需要先登录并携带会话 Cookie
2. **并发限制**: 系统会根据配置限制同时运行的下载和上传任务数
3. **文件路径**: 上传视频时的文件路径相对于 biliup 运行目录
4. **Cookie 文件**: B 站账号的 Cookie 需要提前配置好文件
5. **错误处理**: 建议在生产环境中添加完善的错误处理和重试机制
6. **API 版本**: 当前文档对应 v1 版本的 API，未来版本可能会有变化

## 相关文档

- [WebSocket API](./websocket-api.md) - 实时通信接口
- [Python API](./python-api.md) - Python 库接口
- [CLI 参考](./cli-reference.md) - 命令行工具
- [错误码](./error-codes.md) - 错误码说明
