+++
title = "插件开发"
description = "开发 biliup 下载和上传插件，扩展支持新的直播平台"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 40
template = "docs/page.html"

[extra]
lead = "本文档详细说明如何开发 biliup 插件，包括下载插件和上传插件的完整开发流程。"
toc = true
top = false
+++

## 插件系统概述

biliup 的插件系统允许你扩展支持新的直播平台。插件系统包含两类插件：

- **下载插件**: 从直播平台获取流媒体并下载
- **上传插件**: 将录制的视频上传到视频平台

### 插件工作原理

1. **注册**: 使用装饰器注册插件，关联 URL 正则表达式
2. **匹配**: 根据 URL 自动选择对应的插件
3. **执行**: 调用插件的方法完成下载或上传

### 插件位置

- 下载插件: `biliup/plugins/`
- 上传插件: `biliup/plugins/`
- 弹幕插件: `biliup/Danmaku/`

## 下载插件开发

### 基础结构

下载插件继承自 `DownloadBase` 类，并使用 `@Plugin.download` 装饰器注册。

#### 最小示例

```python
from ..engine.decorators import Plugin
from ..engine.download import DownloadBase
from ..plugins import logger

@Plugin.download(regexp=r'https?://example\.com')
class ExampleDownloader(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        # 初始化插件特定的配置
        self.example_config = config.get('example_config', 'default')
    
    async def acheck_stream(self, is_check=False):
        """
        检查直播状态并获取流地址
        
        Args:
            is_check: 是否只检查状态，不获取流地址
            
        Returns:
            bool: True 表示直播中，False 表示未开播
        """
        # 1. 获取房间信息
        room_info = await self.get_room_info()
        
        # 2. 检查直播状态
        if not room_info['is_live']:
            logger.debug(f"{self.plugin_msg}: 未开播")
            return False
        
        # 3. 设置房间标题
        self.room_title = room_info['title']
        
        # 4. 如果只是检查状态，直接返回
        if is_check:
            return True
        
        # 5. 获取流地址
        stream_url = await self.get_stream_url()
        self.raw_stream_url = stream_url
        
        return True
    
    async def get_room_info(self):
        """获取房间信息"""
        # 实现获取房间信息的逻辑
        pass
    
    async def get_stream_url(self):
        """获取流地址"""
        # 实现获取流地址的逻辑
        pass
```

### 完整示例：斗鱼下载插件

让我们通过一个简化的斗鱼插件示例来学习：

```python
import hashlib
import time
from urllib.parse import parse_qs
from ..common.util import client
from ..config import config
from ..engine.decorators import Plugin
from ..engine.download import DownloadBase
from ..plugins import logger, match1, json_loads

@Plugin.download(regexp=r'https?://(?:(?:www|m)\.)?douyu\.com')
class Douyu(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
        self.room_id = ""
        # 从配置读取插件选项
        self.douyu_cdn = config.get('douyu_cdn', 'hw-h5')
        self.douyu_rate = config.get('douyu_rate', 0)
    
    async def acheck_stream(self, is_check=False):
        # 1. 提取房间号
        self.room_id = match1(self.url, r'douyu\.com/(\d+)')
        if not self.room_id:
            logger.error(f"{self.plugin_msg}: 无法提取房间号")
            return False
        
        # 2. 获取房间信息
        try:
            room_info = await client.get(
                f"https://www.douyu.com/betard/{self.room_id}",
                headers=self.fake_headers
            )
            room_info = json_loads(room_info.text)['room']
        except Exception as e:
            logger.error(f"{self.plugin_msg}: 获取房间信息失败 {e}")
            return False
        
        # 3. 检查直播状态
        if room_info['show_status'] != 1:
            logger.debug(f"{self.plugin_msg}: 未开播")
            return False
        
        # 4. 设置房间标题
        self.room_title = room_info['room_name']
        
        if is_check:
            return True
        
        # 5. 获取播放信息
        play_info = await self.get_play_info()
        
        # 6. 构造流地址
        self.raw_stream_url = f"{play_info['rtmp_url']}/{play_info['rtmp_live']}"
        
        return True
    
    async def get_play_info(self):
        """获取播放信息"""
        # 构造请求参数
        params = {
            'cdn': self.douyu_cdn,
            'rate': str(self.douyu_rate),
            'rid': self.room_id,
        }
        
        # 请求播放接口
        response = await client.post(
            f"https://www.douyu.com/lapi/live/getH5Play/{self.room_id}",
            headers=self.fake_headers,
            params=params
        )
        
        play_data = json_loads(response.text)
        if play_data['error'] != 0:
            raise ValueError(f"获取播放信息错误: {play_data}")
        
        return play_data['data']
```


### 关键方法说明

#### `__init__(self, fname, url, suffix='flv')`

初始化插件实例。

**参数**:
- `fname`: 文件名前缀
- `url`: 直播间 URL
- `suffix`: 文件后缀，默认 'flv'

**常见操作**:
```python
def __init__(self, fname, url, suffix='flv'):
    super().__init__(fname, url, suffix)
    
    # 读取配置
    self.platform_config = config.get('platform_config', 'default')
    
    # 初始化变量
    self.room_id = ""
    self.room_title = ""
```

#### `async def acheck_stream(self, is_check=False)`

检查直播状态并获取流地址。这是插件的核心方法。

**参数**:
- `is_check`: 是否只检查状态（不获取流地址）

**返回值**:
- `True`: 直播中
- `False`: 未开播或出错

**必须设置的属性**:
- `self.room_title`: 房间标题
- `self.raw_stream_url`: 流地址（当 `is_check=False` 时）

**实现流程**:
```python
async def acheck_stream(self, is_check=False):
    # 1. 提取房间号
    room_id = self.extract_room_id()
    
    # 2. 获取房间信息
    room_info = await self.get_room_info(room_id)
    
    # 3. 检查直播状态
    if not room_info['is_live']:
        return False
    
    # 4. 设置房间标题
    self.room_title = room_info['title']
    
    # 5. 如果只检查状态，返回
    if is_check:
        return True
    
    # 6. 获取流地址
    self.raw_stream_url = await self.get_stream_url(room_id)
    
    return True
```

#### `def danmaku_init(self)` (可选)

初始化弹幕客户端。

```python
def danmaku_init(self):
    if config.get('platform_danmaku', False):
        content = {
            'room_id': self.room_id,
        }
        self.danmaku = DanmakuClient(
            self.url, 
            self.gen_download_filename(), 
            content
        )
```

### 常用工具函数

#### `match1(text, *patterns)`

使用正则表达式提取文本。

```python
from ..plugins import match1

# 提取房间号
room_id = match1(url, r'example\.com/(\d+)')

# 提取多个值
title, status = match1(text, r'title="([^"]+)"', r'status="([^"]+)"')
```

#### `json_loads(text)`

安全地解析 JSON。

```python
from ..plugins import json_loads

data = json_loads(response.text)
```

#### `random_user_agent(device='desktop')`

生成随机 User-Agent。

```python
from ..plugins import random_user_agent

ua = random_user_agent('mobile')  # 移动端
ua = random_user_agent('desktop')  # 桌面端
```

### HTTP 请求

使用全局 `client` 对象发送请求：

```python
from ..common.util import client

# GET 请求
response = await client.get(url, headers=headers)

# POST 请求
response = await client.post(url, data=data, headers=headers)

# 带参数的请求
response = await client.get(url, params=params, headers=headers)

# 检查状态码
response.raise_for_status()

# 获取响应内容
text = response.text
json_data = response.json()
```

### 配置管理

从配置文件读取插件选项：

```python
from ..config import config

# 读取配置，提供默认值
cdn = config.get('platform_cdn', 'default_cdn')
quality = config.get('platform_quality', 1080)
enable_feature = config.get('platform_feature', False)
```

用户可以在 `config.yaml` 中配置：

```yaml
platform_cdn: "hw"
platform_quality: 1080
platform_feature: true
```

### 错误处理

使用日志记录错误：

```python
from ..plugins import logger

# 调试信息
logger.debug(f"{self.plugin_msg}: 调试信息")

# 警告信息
logger.warning(f"{self.plugin_msg}: 警告信息")

# 错误信息
logger.error(f"{self.plugin_msg}: 错误信息")

# 异常信息（包含堆栈）
logger.exception(f"{self.plugin_msg}: 异常信息")
```

`self.plugin_msg` 会自动包含插件名称和房间信息。


## 上传插件开发

### 基础结构

上传插件继承自 `BaseUploader` 类，并使用 `@Plugin.upload` 装饰器注册。

#### 最小示例

```python
from ..engine.decorators import Plugin

@Plugin.upload(platform="example")
class ExampleUploader:
    def __init__(self, principal, data, submit_api=None, copyright=2):
        self.principal = principal
        self.data = data
        self.submit_api = submit_api
        self.copyright = copyright
    
    async def upload(self, file_list):
        """
        上传视频
        
        Args:
            file_list: 视频文件路径列表
            
        Returns:
            上传结果
        """
        # 1. 上传视频文件
        video_urls = []
        for file_path in file_list:
            url = await self.upload_file(file_path)
            video_urls.append(url)
        
        # 2. 提交稿件
        result = await self.submit_video(video_urls)
        
        return result
    
    async def upload_file(self, file_path):
        """上传单个文件"""
        # 实现文件上传逻辑
        pass
    
    async def submit_video(self, video_urls):
        """提交稿件"""
        # 实现稿件提交逻辑
        pass
```

### 完整示例：Bilibili 上传插件

```python
import os
from ..engine.decorators import Plugin
from ..common.util import client
from ..plugins import logger

@Plugin.upload(platform="bili_web")
class BiliWebUploader:
    def __init__(self, principal, data, submit_api=None, copyright=2):
        self.principal = principal  # 账号信息
        self.data = data  # 视频元数据
        self.submit_api = submit_api
        self.copyright = copyright
        
        # 从 principal 获取登录信息
        self.access_token = principal.get('access_token')
        self.cookies = principal.get('cookies')
    
    async def upload(self, file_list):
        """上传视频"""
        logger.info(f"开始上传 {len(file_list)} 个文件")
        
        # 1. 预上传，获取上传参数
        upload_params = await self.pre_upload(file_list)
        
        # 2. 上传视频文件
        video_parts = []
        for i, file_path in enumerate(file_list):
            logger.info(f"上传第 {i+1}/{len(file_list)} 个文件: {file_path}")
            
            # 分片上传
            part_info = await self.upload_file(
                file_path, 
                upload_params[i]
            )
            video_parts.append(part_info)
        
        # 3. 提交稿件
        result = await self.submit_video(video_parts)
        
        logger.info(f"上传完成: {result}")
        return result
    
    async def pre_upload(self, file_list):
        """预上传，获取上传参数"""
        params = []
        for file_path in file_list:
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            
            # 请求预上传接口
            response = await client.post(
                'https://member.bilibili.com/preupload',
                params={
                    'name': file_name,
                    'size': file_size,
                    'r': 'upos',
                },
                headers={'Cookie': self.cookies}
            )
            
            data = response.json()
            params.append(data)
        
        return params
    
    async def upload_file(self, file_path, upload_params):
        """分片上传文件"""
        chunk_size = 4 * 1024 * 1024  # 4MB
        file_size = os.path.getsize(file_path)
        
        with open(file_path, 'rb') as f:
            chunk_index = 0
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                
                # 上传分片
                await self.upload_chunk(
                    chunk, 
                    chunk_index, 
                    upload_params
                )
                
                chunk_index += 1
                
                # 显示进度
                progress = min(100, (f.tell() / file_size) * 100)
                logger.debug(f"上传进度: {progress:.1f}%")
        
        # 完成上传
        return await self.complete_upload(upload_params)
    
    async def upload_chunk(self, chunk, index, params):
        """上传单个分片"""
        url = f"{params['endpoint']}/{params['upos_uri']}"
        
        response = await client.put(
            url,
            params={
                'partNumber': index + 1,
                'uploadId': params['upload_id'],
            },
            data=chunk,
            headers={
                'X-Upos-Auth': params['auth'],
            }
        )
        
        response.raise_for_status()
    
    async def complete_upload(self, params):
        """完成上传"""
        url = f"{params['endpoint']}/{params['upos_uri']}"
        
        response = await client.post(
            url,
            params={
                'output': 'json',
                'name': params['filename'],
                'uploadId': params['upload_id'],
            },
            headers={
                'X-Upos-Auth': params['auth'],
            }
        )
        
        return response.json()
    
    async def submit_video(self, video_parts):
        """提交稿件"""
        # 构造提交数据
        submit_data = {
            'title': self.data.get('title'),
            'desc': self.data.get('desc', ''),
            'tid': self.data.get('tid', 171),
            'tag': ','.join(self.data.get('tags', [])),
            'copyright': self.copyright,
            'videos': [
                {
                    'filename': part['filename'],
                    'title': f"P{i+1}",
                }
                for i, part in enumerate(video_parts)
            ],
        }
        
        # 提交稿件
        response = await client.post(
            'https://member.bilibili.com/x/vu/web/add',
            json=submit_data,
            headers={'Cookie': self.cookies}
        )
        
        result = response.json()
        if result['code'] != 0:
            raise Exception(f"提交失败: {result}")
        
        return result['data']
```

### 上传插件关键点

#### 1. 分片上传

大文件需要分片上传：

```python
chunk_size = 4 * 1024 * 1024  # 4MB

with open(file_path, 'rb') as f:
    chunk_index = 0
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        
        await upload_chunk(chunk, chunk_index)
        chunk_index += 1
```

#### 2. 进度回调

显示上传进度：

```python
def progress_callback(current, total):
    percent = (current / total) * 100
    logger.info(f"上传进度: {percent:.1f}%")
```

#### 3. 断点续传

保存上传状态，支持断点续传：

```python
# 保存上传状态
upload_state = {
    'upload_id': upload_id,
    'uploaded_parts': uploaded_parts,
}
save_state(upload_state)

# 恢复上传
if os.path.exists(state_file):
    upload_state = load_state(state_file)
    # 从断点继续上传
```

#### 4. 错误重试

上传失败时自动重试：

```python
max_retries = 3
for attempt in range(max_retries):
    try:
        await upload_chunk(chunk)
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        logger.warning(f"上传失败，重试 {attempt+1}/{max_retries}")
        await asyncio.sleep(2 ** attempt)  # 指数退避
```


## 插件测试

### 单元测试

创建测试文件 `tests/test_example_plugin.py`:

```python
import pytest
from biliup.plugins.example import ExampleDownloader

@pytest.mark.asyncio
async def test_check_stream():
    """测试直播状态检查"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/123456"
    )
    
    # 测试开播状态
    result = await downloader.acheck_stream(is_check=True)
    assert result == True
    assert downloader.room_title != ""

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

### 集成测试

测试完整的下载流程：

```python
@pytest.mark.asyncio
async def test_download_stream():
    """测试下载流"""
    downloader = ExampleDownloader(
        fname="test",
        url="https://example.com/123456"
    )
    
    # 检查直播状态
    is_live = await downloader.acheck_stream()
    if not is_live:
        pytest.skip("直播未开始")
    
    # 下载 10 秒
    await downloader.download()
    
    # 验证文件存在
    assert os.path.exists(downloader.gen_download_filename())
```

### 手动测试

使用命令行测试插件：

```bash
# 测试下载
python -m biliup download https://example.com/123456

# 测试上传
python -m biliup upload --platform example video.mp4
```

## 插件调试

### 启用调试日志

在配置文件中启用调试日志：

```yaml
log_level: DEBUG
```

或使用环境变量：

```bash
export RUST_LOG=debug
python -m biliup download https://example.com/123456
```

### 使用 pdb 调试

在代码中插入断点：

```python
async def acheck_stream(self, is_check=False):
    # 插入断点
    import pdb; pdb.set_trace()
    
    room_info = await self.get_room_info()
    # ...
```

### 打印调试信息

使用 logger 打印调试信息：

```python
logger.debug(f"房间信息: {room_info}")
logger.debug(f"流地址: {stream_url}")
logger.debug(f"请求参数: {params}")
```

### 抓包分析

使用 mitmproxy 或 Charles 抓包分析平台 API：

```bash
# 启动 mitmproxy
mitmproxy -p 8080

# 设置代理
export HTTP_PROXY=http://localhost:8080
export HTTPS_PROXY=http://localhost:8080

# 运行程序
python -m biliup download https://example.com/123456
```

## 常见问题

### 如何处理需要登录的平台？

从配置读取 Cookie：

```python
def __init__(self, fname, url, suffix='flv'):
    super().__init__(fname, url, suffix)
    self.cookies = config.get('platform_cookies', '')
    
async def acheck_stream(self, is_check=False):
    headers = {
        'Cookie': self.cookies,
        'User-Agent': random_user_agent(),
    }
    response = await client.get(url, headers=headers)
```

### 如何处理加密的流地址？

实现解密逻辑：

```python
async def get_stream_url(self):
    encrypted_url = await self.get_encrypted_url()
    
    # 解密
    decrypted_url = self.decrypt_url(encrypted_url)
    
    return decrypted_url

def decrypt_url(self, encrypted_url):
    # 实现解密算法
    # 可能需要使用 jsengine 执行 JavaScript
    pass
```

### 如何处理多种画质？

提供画质选项：

```python
def __init__(self, fname, url, suffix='flv'):
    super().__init__(fname, url, suffix)
    # 从配置读取画质
    self.quality = config.get('platform_quality', 'high')

async def get_stream_url(self):
    # 获取所有画质的流地址
    streams = await self.get_all_streams()
    
    # 选择目标画质
    quality_map = {
        'low': 0,
        'medium': 1,
        'high': 2,
        'source': 3,
    }
    
    quality_index = quality_map.get(self.quality, 2)
    return streams[quality_index]['url']
```

### 如何处理 HLS (m3u8) 流？

设置正确的后缀：

```python
def __init__(self, fname, url, suffix='flv'):
    # 检测流类型
    if self.is_hls_stream():
        suffix = 'ts'
    super().__init__(fname, url, suffix)

async def acheck_stream(self, is_check=False):
    stream_url = await self.get_stream_url()
    
    if stream_url.endswith('.m3u8'):
        # HLS 流
        self.raw_stream_url = stream_url
        self.suffix = 'ts'
    else:
        # FLV 流
        self.raw_stream_url = stream_url
        self.suffix = 'flv'
    
    return True
```

### 如何处理需要签名的 API？

实现签名算法：

```python
import hashlib
import time

def generate_sign(params):
    """生成 API 签名"""
    # 排序参数
    sorted_params = sorted(params.items())
    
    # 拼接字符串
    sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    # 添加密钥
    sign_str += '&key=YOUR_SECRET_KEY'
    
    # MD5 哈希
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    return sign

async def get_stream_url(self):
    params = {
        'room_id': self.room_id,
        'timestamp': int(time.time()),
    }
    
    # 添加签名
    params['sign'] = generate_sign(params)
    
    response = await client.get(api_url, params=params)
    return response.json()['stream_url']
```

## 最佳实践

### 1. 错误处理

始终处理可能的错误：

```python
async def acheck_stream(self, is_check=False):
    try:
        room_info = await self.get_room_info()
    except httpx.RequestError as e:
        logger.error(f"{self.plugin_msg}: 网络错误 {e}")
        return False
    except Exception as e:
        logger.exception(f"{self.plugin_msg}: 未知错误")
        return False
    
    # 处理逻辑
    return True
```

### 2. 配置化

将可配置的选项放到配置文件：

```python
# 不好的做法
cdn = "hw-h5"
quality = 1080

# 好的做法
cdn = config.get('platform_cdn', 'hw-h5')
quality = config.get('platform_quality', 1080)
```

### 3. 日志记录

记录关键信息：

```python
logger.info(f"{self.plugin_msg}: 开始检查直播状态")
logger.debug(f"{self.plugin_msg}: 房间号 {self.room_id}")
logger.debug(f"{self.plugin_msg}: 流地址 {stream_url}")
logger.info(f"{self.plugin_msg}: 直播中，标题: {self.room_title}")
```

### 4. 代码复用

提取公共逻辑：

```python
class BasePlatformDownloader(DownloadBase):
    """平台基类，提供公共方法"""
    
    async def get_room_info(self, room_id):
        """获取房间信息的通用实现"""
        pass
    
    def parse_stream_url(self, data):
        """解析流地址的通用实现"""
        pass

class Platform1Downloader(BasePlatformDownloader):
    """具体平台实现"""
    pass
```

### 5. 性能优化

使用缓存减少请求：

```python
from async_lru import alru_cache

@alru_cache(maxsize=128)
async def get_room_info(self, room_id):
    """缓存房间信息"""
    response = await client.get(f"https://api.example.com/room/{room_id}")
    return response.json()
```

## 提交插件

### 1. 代码规范

遵循 PEP 8 代码规范：

```bash
# 格式化代码
black biliup/plugins/example.py

# 检查代码
flake8 biliup/plugins/example.py
```

### 2. 编写文档

在插件文件顶部添加文档：

```python
"""
Example Platform Downloader

支持的 URL 格式:
- https://example.com/123456
- https://example.com/room/123456

配置选项:
- example_cdn: CDN 选择 (默认: 'default')
- example_quality: 画质选择 (默认: 1080)
- example_cookies: 登录 Cookie (可选)

示例配置:
```yaml
example_cdn: "hw"
example_quality: 1080
example_cookies: "session=xxx"
```
"""
```

### 3. 提交 Pull Request

1. Fork 项目
2. 创建功能分支: `git checkout -b feature/example-platform`
3. 提交代码: `git commit -m "Add Example platform support"`
4. 推送分支: `git push origin feature/example-platform`
5. 创建 Pull Request

## 相关文档

- [项目结构](./project-structure.md)
- [测试指南](./testing.md)
- [调试技巧](./debugging.md)
- [插件系统架构](../architecture/plugin-system.md)
