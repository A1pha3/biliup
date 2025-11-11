+++
title = "Python API"
description = "将 biliup 作为 Python 库使用的 API 文档"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 63
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "在 Python 项目中集成 biliup 的录制和上传功能"
toc = true
top = false
+++

biliup 不仅可以作为命令行工具使用，还可以作为 Python 库集成到你的项目中。通过 Python API，你可以在代码中实现直播录制、视频上传等功能。

## 安装

首先安装 biliup 包：

```bash
pip install biliup
```

或从源码安装：

```bash
git clone https://github.com/biliup/biliup.git
cd biliup
pip install -e .
```


## 核心模块

### 下载引擎

biliup 提供了插件化的下载引擎，支持多个直播平台。

#### 基本使用

```python
import asyncio
from biliup.plugins.bilibili import Bililive

async def download_stream():
    # 创建下载器实例
    downloader = Bililive(
        fname='output',  # 输出文件名前缀
        url='https://live.bilibili.com/123456',  # 直播间 URL
        suffix='flv'  # 文件后缀
    )
    
    # 检查直播状态
    is_live = await downloader.acheck_stream()
    
    if is_live:
        print(f"直播间标题: {downloader.room_title}")
        print(f"直播流 URL: {downloader.raw_stream_url}")
        
        # 开始下载
        await downloader.astart()
    else:
        print("主播未开播")

# 运行
asyncio.run(download_stream())
```

#### 配置选项

下载器支持多种配置选项，可以通过 `biliup.config` 模块设置：

```python
from biliup.config import config

# 设置 B 站相关配置
config['bili_qn'] = 10000  # 画质（10000=原画）
config['bili_protocol'] = 'stream'  # 流协议（stream/hls_fmp4）
config['bili_cdn'] = ['cn-gotcha01']  # CDN 列表
config['bili_cookie'] = 'your_cookie_here'  # B 站 Cookie

# 设置弹幕录制
config['bilibili_danmaku'] = True  # 启用弹幕录制
config['bilibili_danmaku_detail'] = True  # 详细弹幕信息
config['bilibili_danmaku_raw'] = False  # 原始弹幕数据

# 设置用户信息
config['user'] = {
    'bili_cookie': 'your_cookie',
    'bili_cookie_file': 'cookies.json'
}
```

#### 画质选项

B 站支持的画质等级：

- `30000`: 杜比
- `25000`: 4K
- `10000`: 原画
- `400`: 蓝光
- `250`: 超清
- `150`: 高清
- `80`: 流畅


### 上传引擎

biliup 提供了视频上传功能，支持上传到 B 站。

#### 基本使用

```python
from biliup.engine.upload import UploadBase

class MyUploader(UploadBase):
    def upload(self, file_list):
        """
        上传视频文件
        
        Args:
            file_list: 文件列表，每个元素是 FileInfo(video, danmaku)
        
        Returns:
            上传后的文件列表
        """
        for file_info in file_list:
            video_path = file_info.video
            danmaku_path = file_info.danmaku
            
            print(f"上传视频: {video_path}")
            if danmaku_path:
                print(f"上传弹幕: {danmaku_path}")
            
            # 实现上传逻辑
            # ...
        
        return file_list

# 使用上传器
uploader = MyUploader(
    principal='user_id',  # 用户标识
    data={  # 上传参数
        'title': '视频标题',
        'tid': 171,  # 分区 ID
        'tag': '游戏,直播',
        'desc': '视频简介'
    },
    persistence_path='./upload_state.json'  # 持久化路径
)

# 准备文件列表
files = [
    UploadBase.FileInfo(video='video1.mp4', danmaku='video1.xml'),
    UploadBase.FileInfo(video='video2.mp4', danmaku=None)
]

# 执行上传
uploader.upload(files)
```

#### 使用 Rust 上传引擎

biliup 的 Rust 实现提供了更高性能的上传功能：

```python
import stream_gears

# 使用 Rust 上传引擎
# 注意：这需要安装 stream-gears 包
result = stream_gears.upload(
    video_path='video.mp4',
    cookie_file='cookies.json',
    title='视频标题',
    tid=171,
    tag='游戏,直播',
    desc='视频简介'
)

print(f"上传结果: {result}")
```


## 完整示例

### 自动录制并上传

```python
import asyncio
import logging
from pathlib import Path
from biliup.plugins.bilibili import Bililive
from biliup.config import config

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)
logger = logging.getLogger(__name__)

class AutoRecorder:
    def __init__(self, room_url, output_dir='./recordings'):
        self.room_url = room_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 配置下载器
        config['bili_qn'] = 10000  # 原画
        config['bili_protocol'] = 'stream'
        config['bilibili_danmaku'] = True
    
    async def check_and_record(self):
        """检查直播状态并录制"""
        downloader = Bililive(
            fname=str(self.output_dir / 'stream'),
            url=self.room_url,
            suffix='flv'
        )
        
        # 检查直播状态
        is_live = await downloader.acheck_stream()
        
        if is_live:
            logger.info(f"检测到开播: {downloader.room_title}")
            logger.info(f"开始录制: {downloader.raw_stream_url}")
            
            try:
                # 开始录制
                await downloader.astart()
                logger.info("录制完成")
                return True
            except Exception as e:
                logger.error(f"录制失败: {e}")
                return False
        else:
            logger.debug("主播未开播")
            return False
    
    async def monitor_loop(self, check_interval=60):
        """持续监控直播状态"""
        logger.info(f"开始监控 {self.room_url}")
        
        while True:
            try:
                await self.check_and_record()
            except Exception as e:
                logger.error(f"监控出错: {e}")
            
            # 等待下次检查
            await asyncio.sleep(check_interval)

# 使用示例
async def main():
    recorder = AutoRecorder(
        room_url='https://live.bilibili.com/123456',
        output_dir='./recordings'
    )
    
    await recorder.monitor_loop(check_interval=30)

if __name__ == '__main__':
    asyncio.run(main())
```

---

### 批量录制多个直播间

```python
import asyncio
import logging
from biliup.plugins.bilibili import Bililive
from biliup.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiRoomRecorder:
    def __init__(self, rooms):
        """
        Args:
            rooms: 直播间列表，格式 [{'url': '...', 'name': '...'}, ...]
        """
        self.rooms = rooms
        config['bili_qn'] = 10000
        config['bilibili_danmaku'] = True
    
    async def record_room(self, room):
        """录制单个直播间"""
        url = room['url']
        name = room['name']
        
        downloader = Bililive(
            fname=f'./recordings/{name}',
            url=url,
            suffix='flv'
        )
        
        try:
            is_live = await downloader.acheck_stream()
            if is_live:
                logger.info(f"[{name}] 开始录制: {downloader.room_title}")
                await downloader.astart()
                logger.info(f"[{name}] 录制完成")
        except Exception as e:
            logger.error(f"[{name}] 录制失败: {e}")
    
    async def monitor_all(self, check_interval=60):
        """监控所有直播间"""
        logger.info(f"开始监控 {len(self.rooms)} 个直播间")
        
        while True:
            # 并发检查所有直播间
            tasks = [
                self.record_room(room)
                for room in self.rooms
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            # 等待下次检查
            await asyncio.sleep(check_interval)

# 使用示例
async def main():
    rooms = [
        {'url': 'https://live.bilibili.com/123456', 'name': 'streamer1'},
        {'url': 'https://live.bilibili.com/789012', 'name': 'streamer2'},
        {'url': 'https://live.bilibili.com/345678', 'name': 'streamer3'},
    ]
    
    recorder = MultiRoomRecorder(rooms)
    await recorder.monitor_all(check_interval=30)

if __name__ == '__main__':
    asyncio.run(main())
```

---

### 录制后自动上传

```python
import asyncio
import logging
from pathlib import Path
from biliup.plugins.bilibili import Bililive
from biliup.engine.upload import UploadBase
from biliup.config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RecordAndUpload:
    def __init__(self, room_url, output_dir='./recordings'):
        self.room_url = room_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 配置
        config['bili_qn'] = 10000
        config['bilibili_danmaku'] = True
    
    async def record(self):
        """录制直播"""
        downloader = Bililive(
            fname=str(self.output_dir / 'stream'),
            url=self.room_url,
            suffix='flv'
        )
        
        is_live = await downloader.acheck_stream()
        if not is_live:
            return None
        
        logger.info(f"开始录制: {downloader.room_title}")
        
        try:
            await downloader.astart()
            
            # 获取录制的文件
            video_file = downloader.gen_download_filename()
            logger.info(f"录制完成: {video_file}")
            
            return {
                'video': video_file,
                'title': downloader.room_title,
                'danmaku': f"{video_file}.xml" if config.get('bilibili_danmaku') else None
            }
        except Exception as e:
            logger.error(f"录制失败: {e}")
            return None
    
    def upload(self, recording):
        """上传录制的视频"""
        if not recording:
            return
        
        logger.info(f"开始上传: {recording['video']}")
        
        # 创建上传器
        uploader = UploadBase(
            principal='user',
            data={
                'title': recording['title'],
                'tid': 171,  # 电子竞技分区
                'tag': '直播录像,游戏',
                'desc': f"直播录像 - {recording['title']}",
                'copyright': 1,  # 自制
            }
        )
        
        # 准备文件列表
        files = [
            UploadBase.FileInfo(
                video=recording['video'],
                danmaku=recording['danmaku']
            )
        ]
        
        try:
            uploader.upload(files)
            logger.info("上传完成")
        except Exception as e:
            logger.error(f"上传失败: {e}")
    
    async def run(self):
        """录制并上传"""
        recording = await self.record()
        if recording:
            self.upload(recording)

# 使用示例
async def main():
    recorder = RecordAndUpload(
        room_url='https://live.bilibili.com/123456',
        output_dir='./recordings'
    )
    
    await recorder.run()

if __name__ == '__main__':
    asyncio.run(main())
```


## API 参考

### Bililive 类

B 站直播下载器。

#### 构造函数

```python
Bililive(fname, url, suffix='flv')
```

**参数**:
- `fname` (str): 输出文件名前缀
- `url` (str): 直播间 URL
- `suffix` (str): 文件后缀，默认 'flv'

#### 方法

##### acheck_stream()

```python
async def acheck_stream(is_check=False) -> bool
```

检查直播状态。

**参数**:
- `is_check` (bool): 是否仅检查状态，不获取流信息

**返回**:
- `bool`: 是否正在直播

**示例**:

```python
downloader = Bililive('output', 'https://live.bilibili.com/123456')
is_live = await downloader.acheck_stream()
if is_live:
    print(f"直播标题: {downloader.room_title}")
```

##### astart()

```python
async def astart()
```

开始下载直播流。

**示例**:

```python
await downloader.astart()
```

##### danmaku_init()

```python
def danmaku_init()
```

初始化弹幕录制。需要在配置中启用 `bilibili_danmaku`。

#### 属性

- `room_title` (str): 直播间标题
- `raw_stream_url` (str): 直播流 URL
- `live_cover_url` (str): 直播封面 URL
- `live_start_time` (int): 开播时间戳

---

### UploadBase 类

视频上传基类。

#### 构造函数

```python
UploadBase(principal, data, persistence_path=None, postprocessor=None)
```

**参数**:
- `principal` (str): 用户标识
- `data` (dict): 上传参数
- `persistence_path` (str, optional): 持久化路径
- `postprocessor` (callable, optional): 后处理函数

#### 方法

##### upload()

```python
def upload(file_list: List[FileInfo]) -> List[FileInfo]
```

上传视频文件。

**参数**:
- `file_list`: 文件列表

**返回**:
- 上传后的文件列表

#### FileInfo

文件信息命名元组。

```python
FileInfo(video: str, danmaku: Optional[str])
```

**字段**:
- `video` (str): 视频文件路径
- `danmaku` (str, optional): 弹幕文件路径

---

### 配置模块

#### config 字典

全局配置字典，包含所有配置选项。

**常用配置项**:

```python
from biliup.config import config

# B 站配置
config['bili_qn'] = 10000  # 画质
config['bili_protocol'] = 'stream'  # 流协议
config['bili_cdn'] = []  # CDN 列表
config['bili_cookie'] = ''  # Cookie
config['bili_cookie_file'] = ''  # Cookie 文件路径
config['bili_cdn_fallback'] = False  # CDN 回退
config['bili_anonymous_origin'] = False  # 匿名源

# 弹幕配置
config['bilibili_danmaku'] = False  # 启用弹幕录制
config['bilibili_danmaku_detail'] = False  # 详细弹幕
config['bilibili_danmaku_raw'] = False  # 原始弹幕

# 用户配置
config['user'] = {
    'bili_cookie': '',
    'bili_cookie_file': ''
}
```


## 高级用法

### 自定义下载插件

创建自定义的下载插件：

```python
from biliup.engine.download import DownloadBase
from biliup.engine.decorators import Plugin

@Plugin.download(regexp=r'https?://example\.com/live/(\d+)')
class CustomDownloader(DownloadBase):
    def __init__(self, fname, url, suffix='flv'):
        super().__init__(fname, url, suffix)
    
    async def acheck_stream(self, is_check=False):
        """检查直播状态"""
        # 实现检查逻辑
        # 设置 self.raw_stream_url
        # 设置 self.room_title
        return True  # 返回是否正在直播
    
    async def astart(self):
        """开始下载"""
        # 实现下载逻辑
        pass
```

---

### 自定义上传插件

创建自定义的上传插件：

```python
from biliup.engine.upload import UploadBase

class CustomUploader(UploadBase):
    def __init__(self, principal, data, persistence_path=None):
        super().__init__(principal, data, persistence_path)
        self.api_url = 'https://api.example.com/upload'
    
    def upload(self, file_list):
        """上传视频"""
        for file_info in file_list:
            video_path = file_info.video
            
            # 实现上传逻辑
            with open(video_path, 'rb') as f:
                # 上传文件
                pass
        
        return file_list
```

---

### 使用事件回调

监听下载和上传事件：

```python
import asyncio
from biliup.plugins.bilibili import Bililive

class EventRecorder:
    def __init__(self, room_url):
        self.room_url = room_url
        self.downloader = None
    
    async def on_stream_start(self):
        """直播开始回调"""
        print(f"直播开始: {self.downloader.room_title}")
    
    async def on_stream_end(self):
        """直播结束回调"""
        print("直播结束")
    
    async def on_download_progress(self, downloaded, total):
        """下载进度回调"""
        progress = (downloaded / total) * 100 if total > 0 else 0
        print(f"下载进度: {progress:.2f}%")
    
    async def record(self):
        self.downloader = Bililive(
            fname='output',
            url=self.room_url,
            suffix='flv'
        )
        
        is_live = await self.downloader.acheck_stream()
        if is_live:
            await self.on_stream_start()
            await self.downloader.astart()
            await self.on_stream_end()

# 使用示例
async def main():
    recorder = EventRecorder('https://live.bilibili.com/123456')
    await recorder.record()

asyncio.run(main())
```

---

### 集成到 Web 应用

在 FastAPI 应用中使用 biliup：

```python
from fastapi import FastAPI, BackgroundTasks
from biliup.plugins.bilibili import Bililive
from biliup.config import config
import asyncio

app = FastAPI()

# 配置
config['bili_qn'] = 10000
config['bilibili_danmaku'] = True

class RecordingManager:
    def __init__(self):
        self.tasks = {}
    
    async def start_recording(self, room_url, task_id):
        """开始录制任务"""
        downloader = Bililive(
            fname=f'./recordings/{task_id}',
            url=room_url,
            suffix='flv'
        )
        
        is_live = await downloader.acheck_stream()
        if is_live:
            self.tasks[task_id] = {
                'status': 'recording',
                'title': downloader.room_title
            }
            await downloader.astart()
            self.tasks[task_id]['status'] = 'completed'
        else:
            self.tasks[task_id] = {'status': 'not_live'}

manager = RecordingManager()

@app.post("/record")
async def start_record(room_url: str, background_tasks: BackgroundTasks):
    """开始录制"""
    task_id = f"task_{len(manager.tasks)}"
    background_tasks.add_task(manager.start_recording, room_url, task_id)
    return {"task_id": task_id, "status": "started"}

@app.get("/status/{task_id}")
async def get_status(task_id: str):
    """获取任务状态"""
    return manager.tasks.get(task_id, {"status": "not_found"})

# 运行: uvicorn app:app --reload
```


## 注意事项

1. **异步编程**: biliup 的核心功能使用异步编程，需要使用 `asyncio` 运行

2. **配置管理**: 使用 `biliup.config` 模块管理全局配置，在创建下载器前设置

3. **Cookie 管理**: 录制高画质需要登录，通过 `bili_cookie` 或 `bili_cookie_file` 配置

4. **文件命名**: 下载的文件会自动添加时间戳和其他信息，避免文件名冲突

5. **错误处理**: 网络请求可能失败，建议添加异常处理和重试机制

6. **资源清理**: 下载完成后及时清理资源，避免内存泄漏

7. **并发控制**: 同时录制多个直播间时注意控制并发数，避免资源耗尽

8. **日志配置**: 使用 Python logging 模块配置日志，便于调试和监控

## 性能优化

### 使用连接池

```python
import httpx
from biliup.common.util import client

# 配置 HTTP 客户端
client._client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_keepalive_connections=20,
        max_connections=100
    ),
    timeout=httpx.Timeout(30.0)
)
```

### 批量处理

```python
import asyncio
from biliup.plugins.bilibili import Bililive

async def batch_check(room_urls):
    """批量检查直播状态"""
    tasks = []
    for url in room_urls:
        downloader = Bililive('output', url)
        tasks.append(downloader.acheck_stream(is_check=True))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results
```

### 限制并发数

```python
import asyncio

class ConcurrencyLimiter:
    def __init__(self, max_concurrent=5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def record_with_limit(self, room_url):
        async with self.semaphore:
            downloader = Bililive('output', room_url)
            is_live = await downloader.acheck_stream()
            if is_live:
                await downloader.astart()

# 使用
limiter = ConcurrencyLimiter(max_concurrent=3)
tasks = [limiter.record_with_limit(url) for url in room_urls]
await asyncio.gather(*tasks)
```

## 故障排查

### 常见问题

**问题 1: 无法录制高画质**

```python
# 解决方案：配置 Cookie
config['bili_cookie_file'] = 'cookies.json'
```

**问题 2: 连接超时**

```python
# 解决方案：增加超时时间
import httpx
from biliup.common.util import client

client._client = httpx.AsyncClient(timeout=60.0)
```

**问题 3: 内存占用过高**

```python
# 解决方案：限制并发数和缓冲区大小
config['download_limit'] = 3
```

**问题 4: 弹幕录制失败**

```python
# 解决方案：检查弹幕配置
config['bilibili_danmaku'] = True
config['bilibili_danmaku_detail'] = True
```

## 相关文档

- [REST API](./rest-api.md) - HTTP 接口文档
- [WebSocket API](./websocket-api.md) - 实时通信接口
- [CLI 参考](./cli-reference.md) - 命令行工具
- [配置文件格式](../configuration/config-file-format.md) - 配置说明
- [错误码](./error-codes.md) - 错误码说明
