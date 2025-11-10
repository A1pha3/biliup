+++
title = "Python 引擎"
description = "深入了解 Python 引擎的实现原理和工作机制"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 40
template = "docs/page.html"

[extra]
lead = "Python 引擎是 biliup 的核心组件，负责下载直播流、管理任务调度、处理弹幕，并通过插件系统支持 20+ 直播平台。"
toc = true
top = false
+++

## 概述

Python 引擎承担了 biliup 最核心的业务逻辑，包括：

- **下载器**: 从各个直播平台下载视频流
- **上传器**: 将录制的视频上传到 Bilibili
- **任务调度**: 管理多个录制任务的并发执行
- **插件系统**: 支持扩展新的直播平台
- **弹幕系统**: 实时获取和保存弹幕

## 技术栈

- **Python 3.9+**: 核心语言
- **asyncio**: 异步 I/O 框架
- **aiohttp**: 异步 HTTP 客户端
- **aiofiles**: 异步文件操作
- **websockets**: WebSocket 客户端
- **ffmpeg**: 视频处理（外部依赖）

## 项目结构

```
biliup/
├── __init__.py
├── __main__.py              # 程序入口
├── config.py                # 配置管理
├── engine/                  # 核心引擎
│   ├── __init__.py
│   ├── download.py         # 下载器
│   ├── upload.py           # 上传器
│   └── decorators.py       # 装饰器
├── plugins/                 # 下载插件
│   ├── __init__.py
│   ├── base_adapter.py     # 插件基类
│   ├── douyu.py            # 斗鱼
│   ├── huya.py             # 虎牙
│   ├── bilibili.py         # B站
│   ├── twitch.py           # Twitch
│   └── ...                 # 其他平台
├── danmaku/                 # 弹幕系统
│   ├── __init__.py
│   ├── base.py             # 弹幕基类
│   ├── douyu.py            # 斗鱼弹幕
│   ├── huya.py             # 虎牙弹幕
│   └── ...
├── common/                  # 通用工具
│   ├── __init__.py
│   ├── util.py             # 工具函数
│   └── reload.py           # 热重载
└── Naga/                    # 事件驱动框架
    ├── __init__.py
    ├── event.py            # 事件系统
    └── handler.py          # 事件处理器
```

## 核心组件

### 1. 下载器

下载器负责从直播平台获取视频流并保存到本地或直接上传。

#### 下载器基类

```python
# engine/download.py
import asyncio
import aiohttp
import aiofiles
from typing import Optional, Callable

class Downloader:
    def __init__(self, url: str, output_path: str):
        self.url = url
        self.output_path = output_path
        self.session: Optional[aiohttp.ClientSession] = None
        self.is_running = False
        
    async def start(self, progress_callback: Optional[Callable] = None):
        """开始下载"""
        self.is_running = True
        self.session = aiohttp.ClientSession()
        
        try:
            async with self.session.get(self.url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                
                total_size = 0
                async with aiofiles.open(self.output_path, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        if not self.is_running:
                            break
                        
                        await f.write(chunk)
                        total_size += len(chunk)
                        
                        if progress_callback:
                            progress_callback(total_size)
        finally:
            await self.session.close()
    
    async def stop(self):
        """停止下载"""
        self.is_running = False
        if self.session:
            await self.session.close()
```

#### FLV 下载器

```python
# engine/download.py
class FLVDownloader(Downloader):
    """HTTP-FLV 协议下载器"""
    
    def __init__(self, url: str, output_path: str, segment_time: int = 3600):
        super().__init__(url, output_path)
        self.segment_time = segment_time  # 分段时间（秒）
        self.current_segment = 0
        
    async def start(self, progress_callback: Optional[Callable] = None):
        """开始下载，支持自动分段"""
        self.is_running = True
        self.session = aiohttp.ClientSession()
        
        try:
            while self.is_running:
                segment_path = self._get_segment_path()
                start_time = asyncio.get_event_loop().time()
                
                async with self.session.get(self.url) as response:
                    async with aiofiles.open(segment_path, 'wb') as f:
                        async for chunk in response.content.iter_chunked(8192):
                            if not self.is_running:
                                break
                            
                            await f.write(chunk)
                            
                            # 检查是否需要分段
                            elapsed = asyncio.get_event_loop().time() - start_time
                            if elapsed >= self.segment_time:
                                self.current_segment += 1
                                break
                
                # 如果启用了边录边传，触发上传
                if self.auto_upload:
                    asyncio.create_task(self._upload_segment(segment_path))
        finally:
            await self.session.close()
    
    def _get_segment_path(self) -> str:
        """获取分段文件路径"""
        base, ext = os.path.splitext(self.output_path)
        return f"{base}_part{self.current_segment}{ext}"
    
    async def _upload_segment(self, file_path: str):
        """上传分段文件"""
        from .upload import upload_video
        try:
            await upload_video(file_path)
            # 上传成功后删除本地文件
            os.remove(file_path)
        except Exception as e:
            print(f"Upload failed: {e}")
```

#### HLS 下载器

```python
# engine/download.py
import m3u8

class HLSDownloader(Downloader):
    """HLS 协议下载器"""
    
    async def start(self, progress_callback: Optional[Callable] = None):
        """下载 HLS 流"""
        self.is_running = True
        self.session = aiohttp.ClientSession()
        
        try:
            # 获取 m3u8 播放列表
            async with self.session.get(self.url) as response:
                playlist_content = await response.text()
            
            playlist = m3u8.loads(playlist_content)
            
            # 下载所有 ts 分片
            async with aiofiles.open(self.output_path, 'wb') as f:
                for segment in playlist.segments:
                    if not self.is_running:
                        break
                    
                    segment_url = self._resolve_url(segment.uri)
                    async with self.session.get(segment_url) as resp:
                        data = await resp.read()
                        await f.write(data)
                        
                        if progress_callback:
                            progress_callback(len(data))
        finally:
            await self.session.close()
    
    def _resolve_url(self, uri: str) -> str:
        """解析相对 URL"""
        if uri.startswith('http'):
            return uri
        base_url = '/'.join(self.url.split('/')[:-1])
        return f"{base_url}/{uri}"
```

### 2. 上传器

上传器负责将录制的视频上传到 Bilibili，通过 stream-gears 调用 Rust 实现。

```python
# engine/upload.py
import stream_gears
from typing import Dict, Optional

async def upload_video(
    file_path: str,
    title: str,
    desc: str = "",
    tags: list = None,
    cover: Optional[str] = None,
    cookies: Optional[str] = None,
) -> str:
    """
    上传视频到 Bilibili
    
    Args:
        file_path: 视频文件路径
        title: 视频标题
        desc: 视频简介
        tags: 视频标签
        cover: 封面图片路径
        cookies: B站登录 Cookie
    
    Returns:
        bvid: 视频 BV 号
    """
    if cookies is None:
        cookies = load_cookies()
    
    # 调用 Rust 实现的上传函数
    bvid = await asyncio.to_thread(
        stream_gears.upload_video,
        cookies=cookies,
        file_path=file_path,
        title=title,
        desc=desc,
    )
    
    return bvid

def load_cookies() -> str:
    """从配置文件加载 Cookie"""
    import json
    with open('cookies.json', 'r') as f:
        cookies_dict = json.load(f)
    
    # 转换为 Cookie 字符串
    return '; '.join(f"{k}={v}" for k, v in cookies_dict.items())
```

### 3. 任务调度

任务调度器管理多个录制任务的并发执行。


```python
# engine/scheduler.py
import asyncio
from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: str
    streamer_id: str
    platform: str
    url: str
    status: str  # 'idle', 'checking', 'recording', 'uploading'
    check_interval: int = 60
    auto_upload: bool = True

class TaskScheduler:
    def __init__(self, max_concurrent: int = 10):
        self.tasks: Dict[str, Task] = {}
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        
    def add_task(self, task: Task):
        """添加任务"""
        self.tasks[task.id] = task
        
    def remove_task(self, task_id: str):
        """移除任务"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            del self.running_tasks[task_id]
        if task_id in self.tasks:
            del self.tasks[task_id]
    
    async def start_task(self, task_id: str):
        """启动单个任务"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        if task_id in self.running_tasks:
            raise ValueError(f"Task {task_id} is already running")
        
        # 创建异步任务
        async_task = asyncio.create_task(self._run_task(task))
        self.running_tasks[task_id] = async_task
    
    async def stop_task(self, task_id: str):
        """停止单个任务"""
        if task_id in self.running_tasks:
            self.running_tasks[task_id].cancel()
            try:
                await self.running_tasks[task_id]
            except asyncio.CancelledError:
                pass
            del self.running_tasks[task_id]
    
    async def _run_task(self, task: Task):
        """运行任务主循环"""
        async with self.semaphore:
            while True:
                try:
                    # 检查直播状态
                    task.status = 'checking'
                    is_live, stream_url = await self._check_live_status(task)
                    
                    if is_live:
                        # 开始录制
                        task.status = 'recording'
                        file_path = await self._record_stream(task, stream_url)
                        
                        # 自动上传
                        if task.auto_upload and file_path:
                            task.status = 'uploading'
                            await self._upload_video(task, file_path)
                    
                    task.status = 'idle'
                    
                    # 等待下次检查
                    await asyncio.sleep(task.check_interval)
                    
                except asyncio.CancelledError:
                    break
                except Exception as e:
                    print(f"Task {task.id} error: {e}")
                    await asyncio.sleep(60)  # 错误后等待 1 分钟
    
    async def _check_live_status(self, task: Task) -> tuple[bool, str]:
        """检查直播状态"""
        from .plugins import get_plugin
        
        plugin = get_plugin(task.platform)
        return await plugin.get_live_status(task.url)
    
    async def _record_stream(self, task: Task, stream_url: str) -> str:
        """录制直播流"""
        from .download import FLVDownloader
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"videos/{task.streamer_id}_{timestamp}.flv"
        
        downloader = FLVDownloader(stream_url, output_path)
        await downloader.start()
        
        return output_path
    
    async def _upload_video(self, task: Task, file_path: str):
        """上传视频"""
        from .upload import upload_video
        
        title = f"{task.streamer_id} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        await upload_video(file_path, title)
```

### 4. 插件系统

插件系统是 Python 引擎最重要的特性之一，支持轻松扩展新的直播平台。

#### 插件基类

```python
# plugins/base_adapter.py
from abc import ABC, abstractmethod
from typing import Optional, Dict

class BaseAdapter(ABC):
    """下载插件基类"""
    
    def __init__(self):
        self.name = self.__class__.__name__
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    @abstractmethod
    async def get_live_status(self, url: str) -> tuple[bool, Optional[str]]:
        """
        检查直播状态
        
        Returns:
            (is_live, stream_url): 是否在直播，流地址
        """
        pass
    
    @abstractmethod
    async def get_room_info(self, url: str) -> Dict:
        """
        获取直播间信息
        
        Returns:
            {
                'title': 直播标题,
                'streamer': 主播名称,
                'cover': 封面图片,
            }
        """
        pass
    
    def parse_url(self, url: str) -> str:
        """解析 URL，提取房间号"""
        return url
```

#### 装饰器注册机制

```python
# engine/decorators.py
from typing import Dict, Type
from .plugins.base_adapter import BaseAdapter

# 全局插件注册表
_plugin_registry: Dict[str, Type[BaseAdapter]] = {}

def plugin(name: str):
    """插件注册装饰器"""
    def decorator(cls: Type[BaseAdapter]):
        _plugin_registry[name] = cls
        return cls
    return decorator

def get_plugin(name: str) -> BaseAdapter:
    """获取插件实例"""
    if name not in _plugin_registry:
        raise ValueError(f"Plugin {name} not found")
    return _plugin_registry[name]()

def list_plugins() -> list[str]:
    """列出所有已注册的插件"""
    return list(_plugin_registry.keys())
```

#### 斗鱼插件示例

```python
# plugins/douyu.py
import re
import aiohttp
from .base_adapter import BaseAdapter
from ..engine.decorators import plugin

@plugin('douyu')
class DouyuAdapter(BaseAdapter):
    """斗鱼直播插件"""
    
    API_URL = "https://www.douyu.com/betard/{room_id}"
    
    async def get_live_status(self, url: str) -> tuple[bool, str]:
        room_id = self.parse_url(url)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.API_URL.format(room_id=room_id),
                headers=self.headers
            ) as response:
                data = await response.json()
                
                room_info = data['room']
                is_live = room_info['show_status'] == 1
                
                if is_live:
                    stream_url = await self._get_stream_url(room_id)
                    return True, stream_url
                
                return False, None
    
    async def get_room_info(self, url: str) -> dict:
        room_id = self.parse_url(url)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.API_URL.format(room_id=room_id),
                headers=self.headers
            ) as response:
                data = await response.json()
                room_info = data['room']
                
                return {
                    'title': room_info['room_name'],
                    'streamer': room_info['owner_name'],
                    'cover': room_info['room_pic'],
                }
    
    def parse_url(self, url: str) -> str:
        """从 URL 提取房间号"""
        match = re.search(r'douyu\.com/(\d+)', url)
        if match:
            return match.group(1)
        return url
    
    async def _get_stream_url(self, room_id: str) -> str:
        """获取真实流地址"""
        # 实现获取流地址的逻辑
        # 这里简化处理
        return f"https://stream.douyu.com/{room_id}.flv"
```

#### 虎牙插件示例

```python
# plugins/huya.py
import re
import aiohttp
from .base_adapter import BaseAdapter
from ..engine.decorators import plugin

@plugin('huya')
class HuyaAdapter(BaseAdapter):
    """虎牙直播插件"""
    
    async def get_live_status(self, url: str) -> tuple[bool, str]:
        room_id = self.parse_url(url)
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
                
                # 从 HTML 中提取直播状态
                is_live = 'isOn":true' in html
                
                if is_live:
                    stream_url = self._extract_stream_url(html)
                    return True, stream_url
                
                return False, None
    
    async def get_room_info(self, url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
                
                # 提取房间信息
                title_match = re.search(r'"introduction":"([^"]+)"', html)
                streamer_match = re.search(r'"nick":"([^"]+)"', html)
                
                return {
                    'title': title_match.group(1) if title_match else '',
                    'streamer': streamer_match.group(1) if streamer_match else '',
                    'cover': '',
                }
    
    def parse_url(self, url: str) -> str:
        match = re.search(r'huya\.com/(\w+)', url)
        if match:
            return match.group(1)
        return url
    
    def _extract_stream_url(self, html: str) -> str:
        """从 HTML 中提取流地址"""
        # 实现提取逻辑
        match = re.search(r'"sFlvUrl":"([^"]+)"', html)
        if match:
            return match.group(1).replace('\\/', '/')
        return ""
```

### 5. 弹幕系统

弹幕系统实时获取直播弹幕并保存为 XML 格式。

#### 弹幕基类

```python
# danmaku/base.py
from abc import ABC, abstractmethod
import asyncio
from typing import Callable

class BaseDanmaku(ABC):
    """弹幕客户端基类"""
    
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.is_running = False
        self.callbacks = []
    
    def on_message(self, callback: Callable):
        """注册消息回调"""
        self.callbacks.append(callback)
    
    @abstractmethod
    async def connect(self):
        """连接弹幕服务器"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """断开连接"""
        pass
    
    async def _emit_message(self, message: dict):
        """触发消息回调"""
        for callback in self.callbacks:
            await callback(message)
```

#### 斗鱼弹幕客户端

```python
# danmaku/douyu.py
import asyncio
import websockets
from .base import BaseDanmaku

class DouyuDanmaku(BaseDanmaku):
    """斗鱼弹幕客户端"""
    
    WS_URL = "wss://danmuproxy.douyu.com:8506/"
    
    async def connect(self):
        self.is_running = True
        
        async with websockets.connect(self.WS_URL) as ws:
            # 发送登录包
            await self._send_login(ws)
            
            # 发送加入房间包
            await self._send_join_room(ws)
            
            # 接收消息
            while self.is_running:
                try:
                    data = await asyncio.wait_for(ws.recv(), timeout=30)
                    await self._handle_message(data)
                except asyncio.TimeoutError:
                    # 发送心跳
                    await self._send_heartbeat(ws)
    
    async def disconnect(self):
        self.is_running = False
    
    async def _send_login(self, ws):
        """发送登录包"""
        msg = f"type@=loginreq/roomid@={self.room_id}/"
        await ws.send(self._encode_message(msg))
    
    async def _send_join_room(self, ws):
        """发送加入房间包"""
        msg = f"type@=joingroup/rid@={self.room_id}/gid@=-9999/"
        await ws.send(self._encode_message(msg))
    
    async def _send_heartbeat(self, ws):
        """发送心跳包"""
        msg = "type@=mrkl/"
        await ws.send(self._encode_message(msg))
    
    async def _handle_message(self, data: bytes):
        """处理接收到的消息"""
        msg = self._decode_message(data)
        
        if 'type@=chatmsg' in msg:
            # 解析弹幕消息
            danmaku = self._parse_danmaku(msg)
            await self._emit_message(danmaku)
    
    def _encode_message(self, msg: str) -> bytes:
        """编码消息"""
        # 斗鱼协议编码
        data = msg.encode('utf-8')
        length = len(data) + 9
        header = length.to_bytes(4, 'little') + length.to_bytes(4, 'little') + b'\xb1\x02\x00\x00'
        return header + data + b'\x00'
    
    def _decode_message(self, data: bytes) -> str:
        """解码消息"""
        return data[12:-1].decode('utf-8', errors='ignore')
    
    def _parse_danmaku(self, msg: str) -> dict:
        """解析弹幕消息"""
        parts = msg.split('/')
        result = {}
        for part in parts:
            if '@=' in part:
                key, value = part.split('@=', 1)
                result[key] = value
        
        return {
            'type': 'danmaku',
            'user': result.get('nn', ''),
            'content': result.get('txt', ''),
            'timestamp': result.get('cst', ''),
        }
```

### 6. 事件驱动框架

Naga 是一个轻量级的事件驱动框架，用于处理录制过程中的各种事件。

```python
# Naga/event.py
from typing import Callable, Dict, List
from dataclasses import dataclass
from enum import Enum

class EventType(Enum):
    """事件类型"""
    STREAM_START = "stream_start"      # 直播开始
    STREAM_END = "stream_end"          # 直播结束
    RECORD_START = "record_start"      # 录制开始
    RECORD_END = "record_end"          # 录制结束
    UPLOAD_START = "upload_start"      # 上传开始
    UPLOAD_END = "upload_end"          # 上传结束
    ERROR = "error"                    # 错误

@dataclass
class Event:
    """事件对象"""
    type: EventType
    data: dict

class EventBus:
    """事件总线"""
    
    def __init__(self):
        self.handlers: Dict[EventType, List[Callable]] = {}
    
    def on(self, event_type: EventType, handler: Callable):
        """注册事件处理器"""
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)
    
    def off(self, event_type: EventType, handler: Callable):
        """移除事件处理器"""
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)
    
    async def emit(self, event: Event):
        """触发事件"""
        if event.type in self.handlers:
            for handler in self.handlers[event.type]:
                await handler(event)

# 全局事件总线
event_bus = EventBus()
```

使用示例：

```python
from Naga.event import event_bus, Event, EventType

# 注册事件处理器
async def on_stream_start(event: Event):
    print(f"直播开始: {event.data['streamer']}")

event_bus.on(EventType.STREAM_START, on_stream_start)

# 触发事件
await event_bus.emit(Event(
    type=EventType.STREAM_START,
    data={'streamer': '主播名称'}
))
```



## 与 Rust 后端的集成

### 1. 进程启动

Rust 后端通过 `subprocess` 启动 Python 进程：

```rust
// Rust 代码
let child = Command::new("python3")
    .arg("-m")
    .arg("biliup")
    .arg("start")
    .arg(&streamer_id)
    .stdout(Stdio::piped())
    .stderr(Stdio::piped())
    .spawn()?;
```

### 2. 日志传递

Python 引擎通过标准输出输出日志，Rust 后端读取并推送到前端：

```python
# Python 代码
import sys
import json

def log(level: str, message: str):
    """输出结构化日志"""
    log_entry = {
        'level': level,
        'message': message,
        'timestamp': datetime.now().isoformat(),
    }
    print(json.dumps(log_entry), file=sys.stdout, flush=True)

log('info', '开始录制...')
```

### 3. 函数调用

通过 stream-gears 直接调用 Rust 函数：

```python
# Python 代码
import stream_gears

# 调用 Rust 实现的上传函数
bvid = stream_gears.upload_video(
    cookies=cookies,
    file_path=file_path,
    title=title,
    desc=desc,
)
```

## 配置管理

### 配置文件格式

```yaml
# config.yaml
streamers:
  - name: "主播1"
    platform: "douyu"
    url: "https://www.douyu.com/123456"
    check_interval: 60
    auto_upload: true
    upload_config:
      title_template: "{streamer} - {date}"
      tags: ["直播录像", "游戏"]
      copyright: 2  # 2=转载

  - name: "主播2"
    platform: "huya"
    url: "https://www.huya.com/abcdef"
    check_interval: 120
    auto_upload: false

upload:
  cookies_file: "cookies.json"
  concurrent_uploads: 3
  chunk_size: 4194304  # 4MB
  
download:
  output_dir: "videos"
  segment_time: 3600  # 1小时分段
  quality: "origin"  # 原画质量
```

### 配置加载

```python
# config.py
import yaml
from dataclasses import dataclass
from typing import List

@dataclass
class StreamerConfig:
    name: str
    platform: str
    url: str
    check_interval: int = 60
    auto_upload: bool = True

@dataclass
class Config:
    streamers: List[StreamerConfig]
    upload: dict
    download: dict

def load_config(config_file: str = "config.yaml") -> Config:
    """加载配置文件"""
    with open(config_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    streamers = [
        StreamerConfig(**s) for s in data.get('streamers', [])
    ]
    
    return Config(
        streamers=streamers,
        upload=data.get('upload', {}),
        download=data.get('download', {}),
    )
```

## 错误处理和重试

### 自动重连

```python
async def download_with_retry(url: str, output: str, max_retries: int = 3):
    """带重试的下载"""
    retries = 0
    
    while retries < max_retries:
        try:
            downloader = FLVDownloader(url, output)
            await downloader.start()
            break
        except Exception as e:
            retries += 1
            if retries >= max_retries:
                raise
            
            wait_time = 2 ** retries  # 指数退避
            print(f"下载失败，{wait_time}秒后重试... ({retries}/{max_retries})")
            await asyncio.sleep(wait_time)
```

### 异常捕获

```python
try:
    await record_stream(streamer)
except NetworkError as e:
    log('error', f'网络错误: {e}')
    # 等待后重试
except FileSystemError as e:
    log('error', f'文件系统错误: {e}')
    # 清理并重试
except Exception as e:
    log('error', f'未知错误: {e}')
    # 记录详细错误信息
    import traceback
    traceback.print_exc()
```

## 性能优化

### 1. 异步 I/O

所有网络和文件操作都使用异步 I/O，避免阻塞：

```python
# 使用 aiohttp 进行异步 HTTP 请求
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        data = await response.read()

# 使用 aiofiles 进行异步文件操作
async with aiofiles.open(file_path, 'wb') as f:
    await f.write(data)
```

### 2. 并发控制

使用信号量限制并发数，避免资源耗尽：

```python
semaphore = asyncio.Semaphore(10)  # 最多 10 个并发任务

async def limited_task():
    async with semaphore:
        await do_work()
```

### 3. 内存优化

使用流式处理，避免一次性加载大文件到内存：

```python
async def stream_download(url: str, output: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async with aiofiles.open(output, 'wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    await f.write(chunk)
```

### 4. 边录边传

不落盘直接上传，节省磁盘空间和 I/O：

```python
import asyncio
from asyncio import Queue

async def record_and_upload(stream_url: str):
    """边录边传"""
    queue = Queue(maxsize=10)  # 缓冲队列
    
    # 启动下载任务
    download_task = asyncio.create_task(
        download_to_queue(stream_url, queue)
    )
    
    # 启动上传任务
    upload_task = asyncio.create_task(
        upload_from_queue(queue)
    )
    
    await asyncio.gather(download_task, upload_task)

async def download_to_queue(url: str, queue: Queue):
    """下载到队列"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            async for chunk in response.content.iter_chunked(1024 * 1024):
                await queue.put(chunk)
    await queue.put(None)  # 结束标记

async def upload_from_queue(queue: Queue):
    """从队列上传"""
    chunks = []
    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        chunks.append(chunk)
        
        # 累积到一定大小后上传
        if sum(len(c) for c in chunks) >= 4 * 1024 * 1024:
            await upload_chunk(b''.join(chunks))
            chunks.clear()
    
    # 上传剩余数据
    if chunks:
        await upload_chunk(b''.join(chunks))
```

## 日志系统

### 结构化日志

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(name)
    
    def log(self, level: str, message: str, **kwargs):
        """输出结构化日志"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'logger': self.name,
            'message': message,
            **kwargs
        }
        print(json.dumps(log_entry, ensure_ascii=False))
    
    def info(self, message: str, **kwargs):
        self.log('info', message, **kwargs)
    
    def error(self, message: str, **kwargs):
        self.log('error', message, **kwargs)
    
    def warning(self, message: str, **kwargs):
        self.log('warning', message, **kwargs)

# 使用示例
logger = StructuredLogger('biliup.engine')
logger.info('开始录制', streamer='主播1', platform='douyu')
```

## 测试

### 单元测试

```python
# tests/test_downloader.py
import pytest
from biliup.engine.download import FLVDownloader

@pytest.mark.asyncio
async def test_flv_downloader():
    """测试 FLV 下载器"""
    url = "https://example.com/stream.flv"
    output = "/tmp/test.flv"
    
    downloader = FLVDownloader(url, output)
    
    # 模拟下载
    await downloader.start()
    
    # 验证文件存在
    assert os.path.exists(output)

@pytest.mark.asyncio
async def test_plugin_registration():
    """测试插件注册"""
    from biliup.engine.decorators import list_plugins
    
    plugins = list_plugins()
    assert 'douyu' in plugins
    assert 'huya' in plugins
```

### 集成测试

```python
# tests/test_integration.py
import pytest
from biliup.engine.scheduler import TaskScheduler, Task

@pytest.mark.asyncio
async def test_full_workflow():
    """测试完整工作流"""
    scheduler = TaskScheduler()
    
    task = Task(
        id='test-1',
        streamer_id='streamer-1',
        platform='douyu',
        url='https://www.douyu.com/123456',
        status='idle',
    )
    
    scheduler.add_task(task)
    await scheduler.start_task(task.id)
    
    # 等待一段时间
    await asyncio.sleep(10)
    
    await scheduler.stop_task(task.id)
    
    # 验证任务状态
    assert task.status in ['idle', 'recording']
```

## 相关链接

- [后端架构](./backend.md) - 了解 Rust 后端如何调用 Python 引擎
- [插件系统](./plugin-system.md) - 深入了解插件系统设计
- [数据流设计](./data-flow.md) - 了解完整的数据流转
- [开发指南](../development/) - 学习如何开发新的插件
