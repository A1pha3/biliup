+++
title = "WebSocket API"
description = "biliup WebSocket API 实时通信接口文档"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 62
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "通过 WebSocket 实时接收日志和任务状态更新"
toc = true
top = false
+++

biliup 提供 WebSocket 接口用于实时推送日志信息和任务状态更新。通过 WebSocket 连接，你可以实时监控系统运行状态，无需轮询 REST API。

## 基础信息

### WebSocket URL

```
ws://localhost:19159/api/v1/ws/logs
```

默认端口为 19159，可以通过启动参数修改。

### 连接方式

WebSocket 连接使用标准的 WebSocket 协议。客户端需要发起 WebSocket 握手请求，服务器升级连接后开始推送消息。

### 消息格式

所有消息均为文本格式（UTF-8 编码）。服务器会逐行推送日志内容，每条消息对应一行日志。


## 日志推送接口

### 连接日志流

实时接收系统日志推送。

**端点**: `ws://localhost:19159/api/v1/ws/logs`

**查询参数**:
- `file`: 日志文件名（可选，默认为 `ds_update.log`）

**支持的日志文件**:
- `ds_update.log`: 系统更新日志（默认）
- `download.log`: 下载日志
- `upload.log`: 上传日志

**连接流程**:

1. 客户端发起 WebSocket 连接
2. 服务器发送最近 50 行历史日志
3. 服务器持续推送新增的日志行
4. 客户端可以发送 Ping 消息保持连接
5. 任一方可以发送 Close 消息关闭连接

**消息类型**:

- **Text**: 日志内容，每条消息一行日志
- **Ping/Pong**: 心跳消息，保持连接活跃
- **Close**: 关闭连接

**特殊情况**:

- 如果日志文件不存在，服务器会发送错误消息并关闭连接
- 如果日志文件被截断（如日志轮转），服务器会重新发送最近 50 行
- 如果日志文件被删除，服务器会发送通知并关闭连接


## 使用示例

### JavaScript 示例

使用浏览器原生 WebSocket API：

```javascript
// 连接到系统更新日志
const ws = new WebSocket('ws://localhost:19159/api/v1/ws/logs?file=ds_update.log');

// 连接建立
ws.onopen = () => {
  console.log('WebSocket 连接已建立');
};

// 接收消息
ws.onmessage = (event) => {
  console.log('日志:', event.data);
  // 将日志显示在页面上
  const logContainer = document.getElementById('logs');
  const logLine = document.createElement('div');
  logLine.textContent = event.data;
  logContainer.appendChild(logLine);
  
  // 自动滚动到底部
  logContainer.scrollTop = logContainer.scrollHeight;
};

// 连接关闭
ws.onclose = (event) => {
  console.log('WebSocket 连接已关闭', event.code, event.reason);
};

// 连接错误
ws.onerror = (error) => {
  console.error('WebSocket 错误:', error);
};

// 发送心跳（可选）
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);

// 关闭连接
// ws.close();
```

---

### Python 示例

使用 `websockets` 库：

```python
import asyncio
import websockets

async def watch_logs(log_file='ds_update.log'):
    uri = f"ws://localhost:19159/api/v1/ws/logs?file={log_file}"
    
    async with websockets.connect(uri) as websocket:
        print(f"已连接到 {log_file}")
        
        try:
            async for message in websocket:
                print(f"[日志] {message}")
        except websockets.exceptions.ConnectionClosed:
            print("连接已关闭")

# 运行
asyncio.run(watch_logs('ds_update.log'))
```

使用 `websocket-client` 库（同步方式）：

```python
import websocket

def on_message(ws, message):
    print(f"[日志] {message}")

def on_error(ws, error):
    print(f"[错误] {error}")

def on_close(ws, close_status_code, close_msg):
    print("连接已关闭")

def on_open(ws):
    print("连接已建立")

# 创建 WebSocket 连接
ws = websocket.WebSocketApp(
    "ws://localhost:19159/api/v1/ws/logs?file=download.log",
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# 运行（阻塞）
ws.run_forever()
```

---

### Node.js 示例

使用 `ws` 库：

```javascript
const WebSocket = require('ws');

// 连接到上传日志
const ws = new WebSocket('ws://localhost:19159/api/v1/ws/logs?file=upload.log');

ws.on('open', () => {
  console.log('WebSocket 连接已建立');
});

ws.on('message', (data) => {
  console.log('[日志]', data.toString());
});

ws.on('close', () => {
  console.log('WebSocket 连接已关闭');
});

ws.on('error', (error) => {
  console.error('WebSocket 错误:', error);
});

// 发送心跳
const heartbeat = setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.ping();
  }
}, 30000);

// 优雅关闭
process.on('SIGINT', () => {
  clearInterval(heartbeat);
  ws.close();
  process.exit(0);
});
```

---

### Rust 示例

使用 `tokio-tungstenite` 库：

```rust
use tokio_tungstenite::{connect_async, tungstenite::Message};
use futures_util::{SinkExt, StreamExt};

#[tokio::main]
async fn main() {
    let url = "ws://localhost:19159/api/v1/ws/logs?file=ds_update.log";
    
    match connect_async(url).await {
        Ok((mut ws_stream, _)) => {
            println!("WebSocket 连接已建立");
            
            while let Some(msg) = ws_stream.next().await {
                match msg {
                    Ok(Message::Text(text)) => {
                        println!("[日志] {}", text);
                    }
                    Ok(Message::Close(_)) => {
                        println!("连接已关闭");
                        break;
                    }
                    Err(e) => {
                        eprintln!("错误: {}", e);
                        break;
                    }
                    _ => {}
                }
            }
        }
        Err(e) => {
            eprintln!("连接失败: {}", e);
        }
    }
}
```


## 实际应用场景

### 实时日志监控面板

创建一个实时日志监控面板，同时显示多个日志流：

```javascript
class LogMonitor {
  constructor() {
    this.connections = new Map();
  }

  // 连接到指定日志文件
  connect(logFile, containerId) {
    const ws = new WebSocket(
      `ws://localhost:19159/api/v1/ws/logs?file=${logFile}`
    );
    
    const container = document.getElementById(containerId);
    
    ws.onmessage = (event) => {
      const line = document.createElement('div');
      line.className = 'log-line';
      line.textContent = `[${new Date().toLocaleTimeString()}] ${event.data}`;
      container.appendChild(line);
      
      // 保持最多 1000 行
      while (container.children.length > 1000) {
        container.removeChild(container.firstChild);
      }
      
      // 自动滚动
      container.scrollTop = container.scrollHeight;
    };
    
    ws.onclose = () => {
      console.log(`${logFile} 连接已关闭`);
      this.connections.delete(logFile);
    };
    
    this.connections.set(logFile, ws);
  }

  // 断开指定日志
  disconnect(logFile) {
    const ws = this.connections.get(logFile);
    if (ws) {
      ws.close();
      this.connections.delete(logFile);
    }
  }

  // 断开所有连接
  disconnectAll() {
    this.connections.forEach(ws => ws.close());
    this.connections.clear();
  }
}

// 使用示例
const monitor = new LogMonitor();

// 监控三个日志文件
monitor.connect('ds_update.log', 'system-logs');
monitor.connect('download.log', 'download-logs');
monitor.connect('upload.log', 'upload-logs');

// 页面卸载时清理
window.addEventListener('beforeunload', () => {
  monitor.disconnectAll();
});
```

---

### 日志过滤和搜索

实时过滤和搜索日志内容：

```javascript
class FilteredLogViewer {
  constructor(logFile, containerId) {
    this.logFile = logFile;
    this.container = document.getElementById(containerId);
    this.filters = [];
    this.allLogs = [];
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket(
      `ws://localhost:19159/api/v1/ws/logs?file=${this.logFile}`
    );
    
    this.ws.onmessage = (event) => {
      const logLine = event.data;
      this.allLogs.push(logLine);
      
      // 保持最多 5000 行历史
      if (this.allLogs.length > 5000) {
        this.allLogs.shift();
      }
      
      // 应用过滤器
      if (this.shouldDisplay(logLine)) {
        this.displayLog(logLine);
      }
    };
  }

  // 添加过滤器
  addFilter(keyword, type = 'include') {
    this.filters.push({ keyword, type });
    this.refresh();
  }

  // 移除过滤器
  removeFilter(keyword) {
    this.filters = this.filters.filter(f => f.keyword !== keyword);
    this.refresh();
  }

  // 检查是否应该显示
  shouldDisplay(logLine) {
    if (this.filters.length === 0) return true;
    
    for (const filter of this.filters) {
      const matches = logLine.includes(filter.keyword);
      if (filter.type === 'include' && !matches) return false;
      if (filter.type === 'exclude' && matches) return false;
    }
    return true;
  }

  // 显示日志
  displayLog(logLine) {
    const line = document.createElement('div');
    line.className = 'log-line';
    
    // 高亮关键词
    let html = logLine;
    this.filters.forEach(filter => {
      if (filter.type === 'include') {
        html = html.replace(
          new RegExp(filter.keyword, 'gi'),
          `<mark>${filter.keyword}</mark>`
        );
      }
    });
    
    line.innerHTML = html;
    this.container.appendChild(line);
    this.container.scrollTop = this.container.scrollHeight;
  }

  // 刷新显示
  refresh() {
    this.container.innerHTML = '';
    this.allLogs.forEach(log => {
      if (this.shouldDisplay(log)) {
        this.displayLog(log);
      }
    });
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// 使用示例
const viewer = new FilteredLogViewer('ds_update.log', 'filtered-logs');
viewer.connect();

// 只显示包含 "ERROR" 的日志
viewer.addFilter('ERROR', 'include');

// 排除包含 "DEBUG" 的日志
viewer.addFilter('DEBUG', 'exclude');
```

---

### 日志导出功能

将实时日志保存到本地文件：

```javascript
class LogExporter {
  constructor(logFile) {
    this.logFile = logFile;
    this.logs = [];
    this.ws = null;
  }

  start() {
    this.ws = new WebSocket(
      `ws://localhost:19159/api/v1/ws/logs?file=${this.logFile}`
    );
    
    this.ws.onmessage = (event) => {
      this.logs.push({
        timestamp: new Date().toISOString(),
        content: event.data
      });
    };
  }

  stop() {
    if (this.ws) {
      this.ws.close();
    }
  }

  // 导出为文本文件
  exportAsText() {
    const content = this.logs
      .map(log => `[${log.timestamp}] ${log.content}`)
      .join('\n');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${this.logFile}_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  }

  // 导出为 JSON 文件
  exportAsJSON() {
    const content = JSON.stringify(this.logs, null, 2);
    const blob = new Blob([content], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${this.logFile}_${Date.now()}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  // 清空日志
  clear() {
    this.logs = [];
  }
}

// 使用示例
const exporter = new LogExporter('download.log');
exporter.start();

// 5 分钟后导出日志
setTimeout(() => {
  exporter.exportAsText();
  exporter.stop();
}, 5 * 60 * 1000);
```


## 连接管理

### 心跳机制

WebSocket 连接支持 Ping/Pong 心跳机制，用于保持连接活跃和检测连接状态。

**客户端发送 Ping**:

```javascript
const ws = new WebSocket('ws://localhost:19159/api/v1/ws/logs');

// 每 30 秒发送一次心跳
const heartbeat = setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send('ping');
  }
}, 30000);

ws.onclose = () => {
  clearInterval(heartbeat);
};
```

**服务器响应**: 服务器会自动响应 Pong 消息。

---

### 断线重连

实现自动重连机制：

```javascript
class ReconnectingWebSocket {
  constructor(url, options = {}) {
    this.url = url;
    this.reconnectInterval = options.reconnectInterval || 3000;
    this.maxReconnectAttempts = options.maxReconnectAttempts || 10;
    this.reconnectAttempts = 0;
    this.ws = null;
    this.onMessageCallback = null;
    this.shouldReconnect = true;
  }

  connect() {
    this.ws = new WebSocket(this.url);
    
    this.ws.onopen = () => {
      console.log('WebSocket 连接已建立');
      this.reconnectAttempts = 0;
    };
    
    this.ws.onmessage = (event) => {
      if (this.onMessageCallback) {
        this.onMessageCallback(event.data);
      }
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket 连接已关闭');
      if (this.shouldReconnect) {
        this.reconnect();
      }
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket 错误:', error);
    };
  }

  reconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('达到最大重连次数，停止重连');
      return;
    }
    
    this.reconnectAttempts++;
    console.log(`尝试重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
    
    setTimeout(() => {
      this.connect();
    }, this.reconnectInterval);
  }

  onMessage(callback) {
    this.onMessageCallback = callback;
  }

  close() {
    this.shouldReconnect = false;
    if (this.ws) {
      this.ws.close();
    }
  }
}

// 使用示例
const rws = new ReconnectingWebSocket(
  'ws://localhost:19159/api/v1/ws/logs?file=ds_update.log',
  {
    reconnectInterval: 3000,
    maxReconnectAttempts: 10
  }
);

rws.onMessage((data) => {
  console.log('[日志]', data);
});

rws.connect();
```

---

### 连接状态监控

监控 WebSocket 连接状态：

```javascript
class WebSocketMonitor {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.status = 'disconnected';
    this.statusCallbacks = [];
  }

  connect() {
    this.ws = new WebSocket(this.url);
    this.updateStatus('connecting');
    
    this.ws.onopen = () => {
      this.updateStatus('connected');
    };
    
    this.ws.onclose = () => {
      this.updateStatus('disconnected');
    };
    
    this.ws.onerror = () => {
      this.updateStatus('error');
    };
  }

  updateStatus(newStatus) {
    this.status = newStatus;
    this.statusCallbacks.forEach(callback => callback(newStatus));
  }

  onStatusChange(callback) {
    this.statusCallbacks.push(callback);
  }

  getStatus() {
    return this.status;
  }
}

// 使用示例
const monitor = new WebSocketMonitor('ws://localhost:19159/api/v1/ws/logs');

monitor.onStatusChange((status) => {
  const indicator = document.getElementById('connection-status');
  indicator.textContent = status;
  indicator.className = `status-${status}`;
});

monitor.connect();
```


## 错误处理

### 常见错误

**文件不存在**:

```
日志文件 download.log 不存在
```

处理方式：检查日志文件名是否正确，或等待日志文件生成。

**文件访问被拒绝**:

```
不允许访问请求的文件: custom.log
```

处理方式：只能访问允许的日志文件（`ds_update.log`、`download.log`、`upload.log`）。

**文件被截断**:

```
日志文件被截断，重新加载...
```

说明：日志文件发生了轮转，服务器会自动重新加载最近的日志。

**文件被删除**:

```
日志文件 upload.log 不再存在
```

处理方式：连接会被关闭，需要重新连接。

---

### 错误处理示例

完整的错误处理实现：

```javascript
class RobustLogViewer {
  constructor(logFile, containerId) {
    this.logFile = logFile;
    this.container = document.getElementById(containerId);
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
  }

  connect() {
    try {
      this.ws = new WebSocket(
        `ws://localhost:19159/api/v1/ws/logs?file=${this.logFile}`
      );
      
      this.ws.onopen = () => {
        this.reconnectAttempts = 0;
        this.showStatus('已连接', 'success');
      };
      
      this.ws.onmessage = (event) => {
        const message = event.data;
        
        // 检查是否是错误消息
        if (message.includes('不允许访问') || 
            message.includes('不存在') ||
            message.includes('错误')) {
          this.showStatus(message, 'error');
          return;
        }
        
        // 检查是否是系统通知
        if (message.includes('被截断') || 
            message.includes('重新加载')) {
          this.showStatus(message, 'warning');
          return;
        }
        
        // 正常日志
        this.displayLog(message);
      };
      
      this.ws.onclose = (event) => {
        if (event.wasClean) {
          this.showStatus('连接已关闭', 'info');
        } else {
          this.showStatus('连接意外断开', 'error');
          this.attemptReconnect();
        }
      };
      
      this.ws.onerror = (error) => {
        console.error('WebSocket 错误:', error);
        this.showStatus('连接错误', 'error');
      };
      
    } catch (error) {
      console.error('创建 WebSocket 失败:', error);
      this.showStatus('无法创建连接', 'error');
    }
  }

  attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.showStatus('重连失败，请刷新页面', 'error');
      return;
    }
    
    this.reconnectAttempts++;
    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    
    this.showStatus(
      `${delay / 1000} 秒后重连 (${this.reconnectAttempts}/${this.maxReconnectAttempts})`,
      'warning'
    );
    
    setTimeout(() => this.connect(), delay);
  }

  displayLog(message) {
    const line = document.createElement('div');
    line.className = 'log-line';
    line.textContent = message;
    this.container.appendChild(line);
    
    // 限制显示行数
    while (this.container.children.length > 1000) {
      this.container.removeChild(this.container.firstChild);
    }
    
    this.container.scrollTop = this.container.scrollHeight;
  }

  showStatus(message, type) {
    const statusBar = document.getElementById('status-bar');
    statusBar.textContent = message;
    statusBar.className = `status-${type}`;
    
    // 3 秒后清除非错误状态
    if (type !== 'error') {
      setTimeout(() => {
        statusBar.textContent = '';
        statusBar.className = '';
      }, 3000);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }
  }
}

// 使用示例
const viewer = new RobustLogViewer('ds_update.log', 'log-container');
viewer.connect();
```


## 性能优化

### 消息缓冲

当日志更新频繁时，使用消息缓冲减少 DOM 操作：

```javascript
class BufferedLogViewer {
  constructor(logFile, containerId) {
    this.logFile = logFile;
    this.container = document.getElementById(containerId);
    this.buffer = [];
    this.bufferSize = 50;
    this.flushInterval = 100; // 毫秒
    this.ws = null;
    
    // 定期刷新缓冲区
    setInterval(() => this.flush(), this.flushInterval);
  }

  connect() {
    this.ws = new WebSocket(
      `ws://localhost:19159/api/v1/ws/logs?file=${this.logFile}`
    );
    
    this.ws.onmessage = (event) => {
      this.buffer.push(event.data);
      
      // 缓冲区满时立即刷新
      if (this.buffer.length >= this.bufferSize) {
        this.flush();
      }
    };
  }

  flush() {
    if (this.buffer.length === 0) return;
    
    // 批量创建 DOM 元素
    const fragment = document.createDocumentFragment();
    this.buffer.forEach(log => {
      const line = document.createElement('div');
      line.className = 'log-line';
      line.textContent = log;
      fragment.appendChild(line);
    });
    
    this.container.appendChild(fragment);
    this.buffer = [];
    
    // 限制总行数
    while (this.container.children.length > 1000) {
      this.container.removeChild(this.container.firstChild);
    }
    
    this.container.scrollTop = this.container.scrollHeight;
  }

  disconnect() {
    this.flush(); // 断开前刷新剩余日志
    if (this.ws) {
      this.ws.close();
    }
  }
}
```

---

### 虚拟滚动

对于大量日志，使用虚拟滚动提升性能：

```javascript
class VirtualLogViewer {
  constructor(logFile, containerId) {
    this.logFile = logFile;
    this.container = document.getElementById(containerId);
    this.logs = [];
    this.visibleStart = 0;
    this.visibleCount = 50;
    this.lineHeight = 20;
    this.ws = null;
    
    this.setupContainer();
    this.setupScrollHandler();
  }

  setupContainer() {
    this.viewport = document.createElement('div');
    this.viewport.style.height = '600px';
    this.viewport.style.overflow = 'auto';
    
    this.content = document.createElement('div');
    this.viewport.appendChild(this.content);
    this.container.appendChild(this.viewport);
  }

  setupScrollHandler() {
    this.viewport.addEventListener('scroll', () => {
      const scrollTop = this.viewport.scrollTop;
      const newStart = Math.floor(scrollTop / this.lineHeight);
      
      if (newStart !== this.visibleStart) {
        this.visibleStart = newStart;
        this.render();
      }
    });
  }

  connect() {
    this.ws = new WebSocket(
      `ws://localhost:19159/api/v1/ws/logs?file=${this.logFile}`
    );
    
    this.ws.onmessage = (event) => {
      this.logs.push(event.data);
      this.render();
      
      // 自动滚动到底部
      if (this.isScrolledToBottom()) {
        this.scrollToBottom();
      }
    };
  }

  render() {
    const totalHeight = this.logs.length * this.lineHeight;
    this.content.style.height = `${totalHeight}px`;
    
    const visibleEnd = Math.min(
      this.visibleStart + this.visibleCount,
      this.logs.length
    );
    
    const fragment = document.createDocumentFragment();
    for (let i = this.visibleStart; i < visibleEnd; i++) {
      const line = document.createElement('div');
      line.className = 'log-line';
      line.style.position = 'absolute';
      line.style.top = `${i * this.lineHeight}px`;
      line.style.height = `${this.lineHeight}px`;
      line.textContent = this.logs[i];
      fragment.appendChild(line);
    }
    
    this.content.innerHTML = '';
    this.content.appendChild(fragment);
  }

  isScrolledToBottom() {
    const threshold = 50;
    return (
      this.viewport.scrollHeight - this.viewport.scrollTop - 
      this.viewport.clientHeight < threshold
    );
  }

  scrollToBottom() {
    this.viewport.scrollTop = this.viewport.scrollHeight;
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
```


## 注意事项

1. **连接限制**: 每个客户端可以同时建立多个 WebSocket 连接，但建议不要超过 10 个以避免资源浪费

2. **日志文件权限**: 只能访问预定义的日志文件（`ds_update.log`、`download.log`、`upload.log`），其他文件会被拒绝

3. **历史日志**: 连接建立后会先发送最近 50 行历史日志，然后推送新增日志

4. **日志轮转**: 当日志文件被轮转（截断）时，服务器会自动重新加载最近的日志

5. **编码格式**: 所有日志均为 UTF-8 编码，非 UTF-8 字符会被转换为有效的 UTF-8

6. **心跳间隔**: 建议每 30 秒发送一次心跳消息，保持连接活跃

7. **断线重连**: 实现自动重连机制，使用指数退避策略避免频繁重连

8. **性能考虑**: 对于高频日志更新，使用消息缓冲或虚拟滚动优化性能

9. **内存管理**: 限制客户端保存的日志行数，避免内存溢出

10. **跨域问题**: WebSocket 连接不受同源策略限制，但需要注意安全性

## 安全建议

1. **认证**: 虽然 WebSocket 端点当前不需要认证，但建议在生产环境中添加认证机制

2. **加密**: 在生产环境中使用 WSS（WebSocket Secure）协议加密通信

3. **访问控制**: 限制可访问的日志文件，避免泄露敏感信息

4. **速率限制**: 实现连接速率限制，防止滥用

5. **日志脱敏**: 确保日志中不包含敏感信息（密码、密钥等）

## 相关文档

- [REST API](./rest-api.md) - HTTP 接口文档
- [Python API](./python-api.md) - Python 库接口
- [CLI 参考](./cli-reference.md) - 命令行工具
- [错误码](./error-codes.md) - 错误码说明
