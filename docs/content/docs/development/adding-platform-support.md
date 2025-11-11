+++
title = "添加平台支持"
description = "完整指南：如何为 biliup 添加新的直播平台支持"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 50
template = "docs/page.html"

[extra]
lead = "本文档提供完整的流程指导，教你如何分析新平台的直播协议并实现下载插件，包括认证、Cookie 处理和弹幕支持。"
toc = true
top = false
+++

## 概述

添加新平台支持需要完成以下步骤：

1. **分析平台协议**: 了解平台的 API 和流媒体协议
2. **实现下载插件**: 编写获取流地址的代码
3. **处理认证**: 实现 Cookie 和登录逻辑
4. **添加弹幕支持**: 实现弹幕协议（可选）
5. **测试和优化**: 测试各种场景并优化性能

## 第一步：分析平台协议

### 1.1 准备工具

- **浏览器开发者工具**: Chrome DevTools 或 Firefox Developer Tools
- **抓包工具**: mitmproxy、Charles 或 Fiddler
- **网络分析**: Wireshark（用于分析 WebSocket 和 TCP 协议）

### 1.2 分析直播间页面

打开目标直播间，使用浏览器开发者工具：

1. 打开 Network 标签
2. 刷新页面
3. 观察网络请求

**关键信息**:
- 房间信息 API
- 直播状态 API
- 流地址获取 API

**示例**:

```
# 房间信息请求
GET https://api.example.com/room/info?room_id=123456

# 响应
{
  "code": 0,
  "data": {
    "room_id": 123456,
    "title": "直播标题",
    "is_live": true,
    "owner": {
      "uid": 789,
      "name": "主播名称"
    }
  }
}
```

### 1.3 分析流媒体协议

查找视频播放器的网络请求：

**FLV 流**:
```
https://stream.example.com/live/room123456.flv?token=xxx
```

**HLS 流 (m3u8)**:
```
https://stream.example.com/live/room123456/playlist.m3u8
```

**RTMP 流**:
```
rtmp://stream.example.com/live/room123456
```

### 1.4 分析 API 签名

许多平台的 API 需要签名验证。查找签名算法：

1. 在 Network 标签中找到 API 请求
2. 查看请求参数中的 `sign`、`signature` 等字段
3. 在 Sources 标签中搜索相关 JavaScript 代码
4. 分析签名生成逻辑

**常见签名方式**:

```javascript
// MD5 签名
sign = MD5(param1 + param2 + secret_key)

// 时间戳 + MD5
timestamp = Date.now()
sign = MD5(timestamp + param1 + param2 + secret_key)

// 参数排序 + MD5
params = {room_id: 123, timestamp: 1234567890}
sorted_params = sort(params)
sign_str = "room_id=123&timestamp=1234567890&key=secret"
sign = MD5(sign_str)
```

### 1.5 使用抓包工具

对于加密的 HTTPS 流量，使用 mitmproxy：

```bash
# 启动 mitmproxy
mitmproxy -p 8080

# 配置浏览器代理
# HTTP Proxy: localhost:8080
# HTTPS Proxy: localhost:8080

# 安装 mitmproxy 证书
# 访问 http://mitm.it
```


## 第二步：实现下载插件

### 2.1 创建插件文件

在 `biliup/plugins/` 目录创建新文件 `example.py`：

```python
"""
Example Platform Downloader

支持的 URL 格式:
- https://example.com/123456
- https://example.com/room/123456
"""

import hashlib
import time
from ..common.util import client
from ..config import config
from ..engine.decorators import Plugin
from ..engine.download import DownloadBase
from ..plugins import logger, match1, json_loads, random_user_agent


@Plugin.download(regexp=r'https?://(?:www\.)?example\.com')
class ExampleDownloader(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        self.room_id = ""
        
        # 从配置读取选项
        self.example_cdn = config.get('example_cdn', 'default')
        self.example_quality = config.get('example_quality', 'high')
        self.example_cookies = config.get('example_cookies', '')
    
    async def acheck_stream(self, is_check=False):
        """检查直播状态并获取流地址"""
        # 1. 提取房间号
        self.room_id = self.extract_room_id()
        if not self.room_id:
            logger.error(f"{self.plugin_msg}: 无法提取房间号")
            return False
        
        # 2. 获取房间信息
        try:
            room_info = await self.get_room_info()
        except Exception as e:
            logger.error(f"{self.plugin_msg}: 获取房间信息失败 {e}")
            return False
        
        # 3. 检查直播状态
        if not room_info.get('is_live'):
            logger.debug(f"{self.plugin_msg}: 未开播")
            return False
        
        # 4. 设置房间标题
        self.room_title = room_info['title']
        
        # 5. 如果只检查状态，返回
        if is_check:
            return True
        
        # 6. 获取流地址
        try:
            stream_url = await self.get_stream_url()
            self.raw_stream_url = stream_url
        except Exception as e:
            logger.error(f"{self.plugin_msg}: 获取流地址失败 {e}")
            return False
        
        return True
    
    def extract_room_id(self):
        """提取房间号"""
        # 方式 1: 从 URL 直接提取
        room_id = match1(self.url, r'example\.com/(\d+)')
        if room_id:
            return room_id
        
        # 方式 2: 从 URL 路径提取
        room_id = match1(self.url, r'example\.com/room/(\d+)')
        if room_id:
            return room_id
        
        # 方式 3: 从短链接解析
        # 需要请求短链接获取真实房间号
        return None
    
    async def get_room_info(self):
        """获取房间信息"""
        headers = {
            'User-Agent': random_user_agent(),
            'Referer': 'https://example.com/',
        }
        
        # 如果需要登录
        if self.example_cookies:
            headers['Cookie'] = self.example_cookies
        
        response = await client.get(
            f'https://api.example.com/room/info',
            params={'room_id': self.room_id},
            headers=headers
        )
        
        response.raise_for_status()
        data = json_loads(response.text)
        
        if data['code'] != 0:
            raise Exception(f"API 错误: {data}")
        
        return data['data']
    
    async def get_stream_url(self):
        """获取流地址"""
        # 构造请求参数
        params = {
            'room_id': self.room_id,
            'cdn': self.example_cdn,
            'quality': self.example_quality,
            'timestamp': int(time.time()),
        }
        
        # 如果需要签名
        params['sign'] = self.generate_sign(params)
        
        headers = {
            'User-Agent': random_user_agent(),
            'Referer': self.url,
        }
        
        if self.example_cookies:
            headers['Cookie'] = self.example_cookies
        
        response = await client.get(
            'https://api.example.com/stream/url',
            params=params,
            headers=headers
        )
        
        response.raise_for_status()
        data = json_loads(response.text)
        
        if data['code'] != 0:
            raise Exception(f"获取流地址失败: {data}")
        
        return data['data']['stream_url']
    
    def generate_sign(self, params):
        """生成 API 签名"""
        # 实现平台的签名算法
        # 示例: MD5(sorted_params + secret_key)
        
        secret_key = "YOUR_SECRET_KEY"
        
        # 排序参数
        sorted_params = sorted(params.items())
        
        # 拼接字符串
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
        sign_str += f"&key={secret_key}"
        
        # MD5 哈希
        sign = hashlib.md5(sign_str.encode()).hexdigest()
        
        return sign
```

### 2.2 处理不同的流类型

#### FLV 流

```python
async def get_stream_url(self):
    # ... 获取流地址
    stream_url = data['stream_url']
    
    # FLV 流直接返回
    return stream_url
```

#### HLS 流 (m3u8)

```python
def __init__(self, fname, url, suffix='flv'):
    # 检测流类型
    super().__init__(fname, url, suffix)

async def get_stream_url(self):
    stream_url = data['stream_url']
    
    if stream_url.endswith('.m3u8'):
        # HLS 流，设置正确的后缀
        self.suffix = 'ts'
    
    return stream_url
```

#### 多画质支持

```python
async def get_stream_url(self):
    # 获取所有画质
    streams = data['streams']
    
    # 画质映射
    quality_map = {
        'low': streams['low'],
        'medium': streams['medium'],
        'high': streams['high'],
        'source': streams['source'],
    }
    
    # 选择目标画质
    target_quality = self.example_quality
    stream_url = quality_map.get(target_quality, streams['high'])
    
    logger.info(f"{self.plugin_msg}: 使用画质 {target_quality}")
    
    return stream_url
```


## 第三步：处理认证和 Cookie

### 3.1 Cookie 配置

在配置文件中添加 Cookie 支持：

```yaml
# config.yaml
example_cookies: "session=xxx; user_id=123; token=yyy"
```

在插件中读取：

```python
def __init__(self, fname, url, suffix='flv'):
    super().__init__(fname, url, suffix)
    self.example_cookies = config.get('example_cookies', '')
```

### 3.2 从文件读取 Cookie

支持从 JSON 文件读取 Cookie：

```python
import json

def __init__(self, fname, url, suffix='flv'):
    super().__init__(fname, url, suffix)
    
    # 从配置读取 Cookie 文件路径
    cookie_file = config.get('example_cookie_file', '')
    
    if cookie_file:
        self.example_cookies = self.load_cookies(cookie_file)
    else:
        self.example_cookies = config.get('example_cookies', '')

def load_cookies(self, cookie_file):
    """从文件加载 Cookie"""
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # 转换为 Cookie 字符串
        cookies = data.get('cookies', [])
        cookie_str = ';'.join([f"{c['name']}={c['value']}" for c in cookies])
        
        return cookie_str
    except Exception as e:
        logger.error(f"加载 Cookie 文件失败: {e}")
        return ''
```

Cookie 文件格式 (`example_cookies.json`):

```json
{
  "cookies": [
    {
      "name": "session",
      "value": "xxx"
    },
    {
      "name": "user_id",
      "value": "123"
    },
    {
      "name": "token",
      "value": "yyy"
    }
  ]
}
```

### 3.3 自动登录

实现自动登录功能：

```python
async def login(self, username, password):
    """登录平台"""
    # 1. 获取登录页面，提取 CSRF token
    login_page = await client.get('https://example.com/login')
    csrf_token = match1(login_page.text, r'csrf_token" value="([^"]+)"')
    
    # 2. 提交登录表单
    login_data = {
        'username': username,
        'password': password,
        'csrf_token': csrf_token,
    }
    
    response = await client.post(
        'https://example.com/api/login',
        data=login_data,
        headers={'Referer': 'https://example.com/login'}
    )
    
    # 3. 检查登录结果
    result = json_loads(response.text)
    if result['code'] != 0:
        raise Exception(f"登录失败: {result['message']}")
    
    # 4. 保存 Cookie
    cookies = response.cookies
    cookie_str = ';'.join([f"{k}={v}" for k, v in cookies.items()])
    
    logger.info(f"登录成功，Cookie: {cookie_str}")
    
    return cookie_str

async def check_login_status(self):
    """检查登录状态"""
    if not self.example_cookies:
        logger.warning(f"{self.plugin_msg}: 未配置 Cookie，可能无法获取高画质")
        return False
    
    try:
        response = await client.get(
            'https://api.example.com/user/info',
            headers={'Cookie': self.example_cookies}
        )
        
        data = json_loads(response.text)
        
        if data.get('is_login'):
            logger.info(f"已登录，用户: {data['username']}")
            return True
        else:
            logger.warning(f"{self.plugin_msg}: Cookie 已失效")
            return False
    except Exception as e:
        logger.error(f"{self.plugin_msg}: 检查登录状态失败 {e}")
        return False
```

### 3.4 处理 Token 刷新

某些平台使用 Token 认证，需要定期刷新：

```python
class ExampleDownloader(DownloadBase):
    # 类变量，所有实例共享
    _access_token = None
    _token_expire_time = 0
    
    async def get_access_token(self):
        """获取访问令牌"""
        # 检查 Token 是否过期
        if (self._access_token and 
            time.time() < self._token_expire_time):
            return self._access_token
        
        # 刷新 Token
        response = await client.post(
            'https://api.example.com/oauth/token',
            data={
                'grant_type': 'refresh_token',
                'refresh_token': self.refresh_token,
            }
        )
        
        data = json_loads(response.text)
        
        # 更新类变量
        ExampleDownloader._access_token = data['access_token']
        ExampleDownloader._token_expire_time = time.time() + data['expires_in']
        
        logger.info(f"Token 已刷新，有效期: {data['expires_in']}秒")
        
        return self._access_token
```

## 第四步：添加弹幕支持

### 4.1 分析弹幕协议

使用浏览器开发者工具查看 WebSocket 连接：

1. 打开 Network 标签
2. 筛选 WS (WebSocket)
3. 查看消息内容

**常见弹幕协议**:
- WebSocket (文本或二进制)
- TCP Socket
- HTTP 长轮询

### 4.2 创建弹幕客户端

在 `biliup/Danmaku/` 目录创建 `example.py`：

```python
"""
Example Platform Danmaku Client
"""

import asyncio
import json
import struct
from ..Danmaku import DanmakuClient


class ExampleDanmaku(DanmakuClient):
    def __init__(self, url, filename, content):
        super().__init__(url, filename, content)
        self.room_id = content['room_id']
        self.ws_url = f"wss://danmaku.example.com/room/{self.room_id}"
    
    async def start(self):
        """启动弹幕客户端"""
        async with self.session.ws_connect(self.ws_url) as ws:
            # 发送认证消息
            await self.send_auth(ws)
            
            # 启动心跳
            asyncio.create_task(self.heartbeat(ws))
            
            # 接收消息
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.BINARY:
                    await self.handle_message(msg.data)
                elif msg.type == aiohttp.WSMsgType.TEXT:
                    await self.handle_text_message(msg.data)
    
    async def send_auth(self, ws):
        """发送认证消息"""
        auth_data = {
            'type': 'auth',
            'room_id': self.room_id,
        }
        
        await ws.send_json(auth_data)
    
    async def heartbeat(self, ws):
        """发送心跳"""
        while True:
            try:
                await ws.send_json({'type': 'heartbeat'})
                await asyncio.sleep(30)
            except:
                break
    
    async def handle_message(self, data):
        """处理二进制消息"""
        # 解析消息头
        header_len = 16
        if len(data) < header_len:
            return
        
        # 解包消息头
        packet_len, header_len, protocol_ver, operation, seq_id = struct.unpack(
            '>IHHII', data[:16]
        )
        
        # 解析消息体
        body = data[header_len:packet_len]
        
        if operation == 5:  # 弹幕消息
            await self.handle_danmaku(body)
    
    async def handle_text_message(self, text):
        """处理文本消息"""
        try:
            data = json.loads(text)
            msg_type = data.get('type')
            
            if msg_type == 'danmaku':
                await self.handle_danmaku_json(data)
            elif msg_type == 'gift':
                await self.handle_gift(data)
        except:
            pass
    
    async def handle_danmaku(self, body):
        """处理弹幕"""
        try:
            # 解析弹幕数据
            data = json.loads(body.decode('utf-8'))
            
            # 提取弹幕信息
            danmaku = {
                'user': data['user']['name'],
                'content': data['content'],
                'timestamp': data['timestamp'],
            }
            
            # 写入文件
            await self.write_danmaku(danmaku)
            
        except Exception as e:
            logger.error(f"处理弹幕失败: {e}")
    
    async def handle_danmaku_json(self, data):
        """处理 JSON 格式弹幕"""
        danmaku = {
            'user': data['user'],
            'content': data['content'],
            'timestamp': data['timestamp'],
        }
        
        await self.write_danmaku(danmaku)
    
    async def handle_gift(self, data):
        """处理礼物"""
        gift = {
            'user': data['user'],
            'gift_name': data['gift_name'],
            'count': data['count'],
            'timestamp': data['timestamp'],
        }
        
        logger.info(f"收到礼物: {gift['user']} 送出 {gift['gift_name']} x{gift['count']}")
```

### 4.3 在下载插件中启用弹幕

```python
from ..Danmaku import DanmakuClient

class ExampleDownloader(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        self.example_danmaku = config.get('example_danmaku', False)
    
    def danmaku_init(self):
        """初始化弹幕客户端"""
        if self.example_danmaku:
            content = {
                'room_id': self.room_id,
            }
            self.danmaku = DanmakuClient(
                self.url, 
                self.gen_download_filename(), 
                content
            )
```

配置文件：

```yaml
# config.yaml
example_danmaku: true
```


## 第五步：测试和优化

### 5.1 单元测试

创建测试文件 `tests/test_example.py`：

```python
import pytest
from biliup.plugins.example import ExampleDownloader

@pytest.mark.asyncio
async def test_extract_room_id():
    """测试房间号提取"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/123456"
    )
    
    room_id = downloader.extract_room_id()
    assert room_id == "123456"

@pytest.mark.asyncio
async def test_check_stream_live():
    """测试直播中的房间"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/123456"
    )
    
    result = await downloader.acheck_stream(is_check=True)
    assert result == True
    assert downloader.room_title != ""

@pytest.mark.asyncio
async def test_check_stream_offline():
    """测试未开播的房间"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/999999"
    )
    
    result = await downloader.acheck_stream(is_check=True)
    assert result == False

@pytest.mark.asyncio
async def test_get_stream_url():
    """测试获取流地址"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/123456"
    )
    
    result = await downloader.acheck_stream()
    assert result == True
    assert downloader.raw_stream_url is not None
    assert downloader.raw_stream_url.startswith("http")
```

运行测试：

```bash
pytest tests/test_example.py -v
```

### 5.2 集成测试

测试完整的下载流程：

```bash
# 测试下载
python -m biliup download https://example.com/123456

# 测试配置
python -m biliup download https://example.com/123456 \
    --config config.yaml
```

### 5.3 性能优化

#### 使用缓存

```python
from async_lru import alru_cache

@alru_cache(maxsize=128, ttl=300)
async def get_room_info(self, room_id):
    """缓存房间信息 5 分钟"""
    response = await client.get(
        f'https://api.example.com/room/info',
        params={'room_id': room_id}
    )
    return json_loads(response.text)
```

#### 并发请求

```python
async def get_multiple_streams(self, room_ids):
    """并发获取多个房间的流地址"""
    tasks = [self.get_stream_url(room_id) for room_id in room_ids]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

#### 连接池

```python
# 使用全局 client，自动管理连接池
from ..common.util import client

# client 已配置连接池
# limits = httpx.Limits(max_keepalive_connections=20, max_connections=100)
```

### 5.4 错误处理

#### 重试机制

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def get_stream_url_with_retry(self):
    """带重试的获取流地址"""
    return await self.get_stream_url()
```

#### 超时处理

```python
import asyncio

async def get_room_info(self):
    """带超时的请求"""
    try:
        response = await asyncio.wait_for(
            client.get(
                f'https://api.example.com/room/info',
                params={'room_id': self.room_id}
            ),
            timeout=10.0  # 10 秒超时
        )
        return json_loads(response.text)
    except asyncio.TimeoutError:
        logger.error(f"{self.plugin_msg}: 请求超时")
        raise
```

#### 降级策略

```python
async def get_stream_url(self):
    """带降级的获取流地址"""
    # 尝试主 CDN
    try:
        return await self.get_stream_url_from_cdn('primary')
    except Exception as e:
        logger.warning(f"{self.plugin_msg}: 主 CDN 失败，尝试备用 CDN")
    
    # 降级到备用 CDN
    try:
        return await self.get_stream_url_from_cdn('backup')
    except Exception as e:
        logger.error(f"{self.plugin_msg}: 所有 CDN 均失败")
        raise
```

### 5.5 日志和监控

#### 详细日志

```python
async def acheck_stream(self, is_check=False):
    logger.info(f"{self.plugin_msg}: 开始检查直播状态")
    logger.debug(f"{self.plugin_msg}: URL: {self.url}")
    logger.debug(f"{self.plugin_msg}: 房间号: {self.room_id}")
    
    room_info = await self.get_room_info()
    logger.debug(f"{self.plugin_msg}: 房间信息: {room_info}")
    
    if room_info['is_live']:
        logger.info(f"{self.plugin_msg}: 直播中，标题: {room_info['title']}")
    else:
        logger.debug(f"{self.plugin_msg}: 未开播")
    
    return room_info['is_live']
```

#### 性能监控

```python
import time

async def acheck_stream(self, is_check=False):
    start_time = time.time()
    
    try:
        result = await self._acheck_stream_impl(is_check)
        
        elapsed = time.time() - start_time
        logger.debug(f"{self.plugin_msg}: 检查耗时 {elapsed:.2f}秒")
        
        return result
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"{self.plugin_msg}: 检查失败，耗时 {elapsed:.2f}秒")
        raise
```

## 完整示例

这是一个完整的平台支持示例，包含所有功能：

```python
"""
Example Platform Support

完整的平台支持示例，包含：
- 房间信息获取
- 流地址获取
- Cookie 认证
- 多画质支持
- 弹幕支持
- 错误处理
- 性能优化
"""

import hashlib
import time
import asyncio
from async_lru import alru_cache
from tenacity import retry, stop_after_attempt, wait_exponential

from ..common.util import client
from ..config import config
from ..Danmaku import DanmakuClient
from ..engine.decorators import Plugin
from ..engine.download import DownloadBase
from ..plugins import logger, match1, json_loads, random_user_agent


@Plugin.download(regexp=r'https?://(?:www\.)?example\.com')
class ExampleDownloader(DownloadBase):
    """Example 平台下载器"""
    
    # 类变量：共享的 Token
    _access_token = None
    _token_expire_time = 0
    
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        
        # 房间信息
        self.room_id = ""
        
        # 配置选项
        self.example_cdn = config.get('example_cdn', 'default')
        self.example_quality = config.get('example_quality', 'high')
        self.example_cookies = config.get('example_cookies', '')
        self.example_danmaku = config.get('example_danmaku', False)
        
        # 加载 Cookie 文件
        cookie_file = config.get('example_cookie_file', '')
        if cookie_file:
            self.example_cookies = self.load_cookies(cookie_file)
    
    async def acheck_stream(self, is_check=False):
        """检查直播状态并获取流地址"""
        logger.info(f"{self.plugin_msg}: 开始检查直播状态")
        start_time = time.time()
        
        try:
            # 1. 提取房间号
            self.room_id = self.extract_room_id()
            if not self.room_id:
                logger.error(f"{self.plugin_msg}: 无法提取房间号")
                return False
            
            logger.debug(f"{self.plugin_msg}: 房间号: {self.room_id}")
            
            # 2. 检查登录状态
            await self.check_login_status()
            
            # 3. 获取房间信息
            room_info = await self.get_room_info_cached(self.room_id)
            logger.debug(f"{self.plugin_msg}: 房间信息: {room_info}")
            
            # 4. 检查直播状态
            if not room_info.get('is_live'):
                logger.debug(f"{self.plugin_msg}: 未开播")
                return False
            
            # 5. 设置房间标题
            self.room_title = room_info['title']
            logger.info(f"{self.plugin_msg}: 直播中，标题: {self.room_title}")
            
            # 6. 如果只检查状态，返回
            if is_check:
                elapsed = time.time() - start_time
                logger.debug(f"{self.plugin_msg}: 检查完成，耗时 {elapsed:.2f}秒")
                return True
            
            # 7. 获取流地址
            stream_url = await self.get_stream_url_with_retry()
            self.raw_stream_url = stream_url
            logger.info(f"{self.plugin_msg}: 流地址: {stream_url}")
            
            elapsed = time.time() - start_time
            logger.debug(f"{self.plugin_msg}: 检查完成，耗时 {elapsed:.2f}秒")
            
            return True
            
        except Exception as e:
            elapsed = time.time() - start_time
            logger.error(f"{self.plugin_msg}: 检查失败，耗时 {elapsed:.2f}秒")
            logger.exception(f"{self.plugin_msg}: 异常详情")
            return False
    
    def extract_room_id(self):
        """提取房间号"""
        # 尝试多种格式
        patterns = [
            r'example\.com/(\d+)',
            r'example\.com/room/(\d+)',
            r'example\.com/live/(\d+)',
        ]
        
        for pattern in patterns:
            room_id = match1(self.url, pattern)
            if room_id:
                return room_id
        
        return None
    
    @alru_cache(maxsize=128, ttl=300)
    async def get_room_info_cached(self, room_id):
        """获取房间信息（带缓存）"""
        return await self.get_room_info(room_id)
    
    async def get_room_info(self, room_id):
        """获取房间信息"""
        headers = {
            'User-Agent': random_user_agent(),
            'Referer': 'https://example.com/',
        }
        
        if self.example_cookies:
            headers['Cookie'] = self.example_cookies
        
        try:
            response = await asyncio.wait_for(
                client.get(
                    'https://api.example.com/room/info',
                    params={'room_id': room_id},
                    headers=headers
                ),
                timeout=10.0
            )
            
            response.raise_for_status()
            data = json_loads(response.text)
            
            if data['code'] != 0:
                raise Exception(f"API 错误: {data}")
            
            return data['data']
            
        except asyncio.TimeoutError:
            logger.error(f"{self.plugin_msg}: 获取房间信息超时")
            raise
        except Exception as e:
            logger.error(f"{self.plugin_msg}: 获取房间信息失败 {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def get_stream_url_with_retry(self):
        """获取流地址（带重试）"""
        return await self.get_stream_url()
    
    async def get_stream_url(self):
        """获取流地址"""
        # 构造请求参数
        params = {
            'room_id': self.room_id,
            'cdn': self.example_cdn,
            'quality': self.example_quality,
            'timestamp': int(time.time()),
        }
        
        # 添加签名
        params['sign'] = self.generate_sign(params)
        
        headers = {
            'User-Agent': random_user_agent(),
            'Referer': self.url,
        }
        
        if self.example_cookies:
            headers['Cookie'] = self.example_cookies
        
        try:
            response = await client.get(
                'https://api.example.com/stream/url',
                params=params,
                headers=headers
            )
            
            response.raise_for_status()
            data = json_loads(response.text)
            
            if data['code'] != 0:
                raise Exception(f"获取流地址失败: {data}")
            
            # 处理多画质
            streams = data['data']['streams']
            stream_url = self.select_quality(streams)
            
            return stream_url
            
        except Exception as e:
            logger.error(f"{self.plugin_msg}: 获取流地址失败 {e}")
            raise
    
    def select_quality(self, streams):
        """选择画质"""
        quality_map = {
            'low': streams.get('low'),
            'medium': streams.get('medium'),
            'high': streams.get('high'),
            'source': streams.get('source'),
        }
        
        target_quality = self.example_quality
        stream_url = quality_map.get(target_quality)
        
        if not stream_url:
            # 降级到最高可用画质
            for quality in ['source', 'high', 'medium', 'low']:
                stream_url = quality_map.get(quality)
                if stream_url:
                    logger.warning(
                        f"{self.plugin_msg}: 目标画质 {target_quality} 不可用，"
                        f"降级到 {quality}"
                    )
                    break
        
        return stream_url
    
    def generate_sign(self, params):
        """生成 API 签名"""
        secret_key = "YOUR_SECRET_KEY"
        
        # 排序参数
        sorted_params = sorted(params.items())
        
        # 拼接字符串
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
        sign_str += f"&key={secret_key}"
        
        # MD5 哈希
        sign = hashlib.md5(sign_str.encode()).hexdigest()
        
        return sign
    
    def load_cookies(self, cookie_file):
        """从文件加载 Cookie"""
        try:
            import json
            with open(cookie_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            cookies = data.get('cookies', [])
            cookie_str = ';'.join([f"{c['name']}={c['value']}" for c in cookies])
            
            return cookie_str
        except Exception as e:
            logger.error(f"加载 Cookie 文件失败: {e}")
            return ''
    
    async def check_login_status(self):
        """检查登录状态"""
        if not self.example_cookies:
            logger.warning(f"{self.plugin_msg}: 未配置 Cookie，可能无法获取高画质")
            return False
        
        try:
            response = await client.get(
                'https://api.example.com/user/info',
                headers={'Cookie': self.example_cookies}
            )
            
            data = json_loads(response.text)
            
            if data.get('is_login'):
                logger.info(f"已登录，用户: {data['username']}")
                return True
            else:
                logger.warning(f"{self.plugin_msg}: Cookie 已失效")
                return False
        except Exception as e:
            logger.debug(f"{self.plugin_msg}: 检查登录状态失败 {e}")
            return False
    
    def danmaku_init(self):
        """初始化弹幕客户端"""
        if self.example_danmaku:
            content = {
                'room_id': self.room_id,
            }
            self.danmaku = DanmakuClient(
                self.url,
                self.gen_download_filename(),
                content
            )
```

## 提交代码

完成开发后，提交代码到 GitHub：

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 创建 Pull Request

详细步骤参考[插件开发文档](./plugin-development.md#提交插件)。

## 相关文档

- [插件开发](./plugin-development.md)
- [测试指南](./testing.md)
- [调试技巧](./debugging.md)
- [插件系统架构](../architecture/plugin-system.md)
