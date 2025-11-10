+++
title = "前端架构"
description = "深入了解基于 Next.js 的前端实现"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 20
template = "docs/page.html"

[extra]
lead = "biliup 的前端采用 Next.js 14 + React 18 + TypeScript 构建，使用 Semi UI 组件库提供现代化的用户界面。"
toc = true
top = false
+++

## 技术栈

### 核心框架

- **Next.js 14**: React 框架，支持静态导出和服务端渲染
- **React 18**: 用户界面库，支持并发特性和自动批处理
- **TypeScript 5.7**: 提供类型安全和更好的开发体验

### UI 组件库

- **Semi UI 2.86**: 字节跳动开源的 React 组件库
  - 提供丰富的组件（Table、Form、Modal、Toast 等）
  - 支持主题定制
  - 优秀的国际化支持

### 数据管理

- **SWR 2.3**: React Hooks 数据获取库
  - 自动缓存和重新验证
  - 实时数据更新
  - 乐观 UI 更新
  - 错误重试机制

### 其他依赖

- **react-use**: React Hooks 工具库
- **qrcode.react**: 二维码生成（用于登录）
- **artplayer**: 视频播放器
- **mpegts.js**: FLV 视频流播放支持
- **react-json-tree**: JSON 数据可视化

## 项目结构

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # 根布局组件
│   ├── page.tsx             # 首页
│   ├── globals.css          # 全局样式
│   └── ...                  # 其他页面和路由
├── components/              # React 组件
│   ├── StreamerList/        # 主播列表组件
│   ├── TaskManager/         # 任务管理组件
│   ├── LogViewer/           # 日志查看器
│   ├── ConfigEditor/        # 配置编辑器
│   └── ...                  # 其他组件
├── hooks/                   # 自定义 React Hooks
│   ├── useStreamers.ts      # 主播数据管理
│   ├── useWebSocket.ts      # WebSocket 连接
│   ├── useTasks.ts          # 任务状态管理
│   └── ...                  # 其他 Hooks
├── lib/                     # 工具函数和类型定义
│   ├── api.ts               # API 客户端
│   ├── types.ts             # TypeScript 类型定义
│   ├── utils.ts             # 工具函数
│   └── constants.ts         # 常量定义
├── public/                  # 静态资源
│   ├── favicon.ico
│   └── ...
├── package.json             # 项目依赖
├── next.config.js           # Next.js 配置
└── tsconfig.json            # TypeScript 配置
```

## 核心功能实现

### 1. API 交互

前端通过 REST API 与后端通信，使用 SWR 进行数据管理。

#### API 客户端封装

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_BASE || '';

export const api = {
  // 获取主播列表
  getStreamers: async () => {
    const res = await fetch(`${API_BASE}/api/streamers`);
    if (!res.ok) throw new Error('Failed to fetch streamers');
    return res.json();
  },
  
  // 创建主播配置
  createStreamer: async (data: StreamerConfig) => {
    const res = await fetch(`${API_BASE}/api/streamers`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to create streamer');
    return res.json();
  },
  
  // 启动录制任务
  startTask: async (id: string) => {
    const res = await fetch(`${API_BASE}/api/streamers/${id}/start`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to start task');
    return res.json();
  },
  
  // 停止录制任务
  stopTask: async (id: string) => {
    const res = await fetch(`${API_BASE}/api/streamers/${id}/stop`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Failed to stop task');
    return res.json();
  },
};
```

#### 使用 SWR 管理数据

```typescript
// hooks/useStreamers.ts
import useSWR from 'swr';
import { api } from '@/lib/api';

export function useStreamers() {
  const { data, error, mutate } = useSWR('streamers', api.getStreamers, {
    refreshInterval: 5000,  // 每 5 秒自动刷新
    revalidateOnFocus: true, // 窗口获得焦点时重新验证
  });

  return {
    streamers: data,
    isLoading: !error && !data,
    isError: error,
    refresh: mutate,
  };
}
```

### 2. WebSocket 实时通信

前端通过 WebSocket 接收后端推送的实时日志和状态更新。


#### WebSocket Hook 实现

```typescript
// hooks/useWebSocket.ts
import { useEffect, useRef, useState } from 'react';

interface WebSocketMessage {
  type: 'log' | 'status' | 'error';
  streamer_id?: string;
  level?: 'info' | 'warn' | 'error';
  message: string;
  timestamp: string;
}

export function useWebSocket(url: string) {
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      setMessages((prev) => [...prev, message]);
    };

    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
      // 自动重连
      setTimeout(() => {
        if (wsRef.current?.readyState === WebSocket.CLOSED) {
          // 重新连接逻辑
        }
      }, 3000);
    };

    return () => {
      ws.close();
    };
  }, [url]);

  const sendMessage = (message: any) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(message));
    }
  };

  return { messages, isConnected, sendMessage };
}
```

#### 日志查看器组件

```typescript
// components/LogViewer.tsx
import { useWebSocket } from '@/hooks/useWebSocket';
import { Card, Tag } from '@douyinfe/semi-ui';

export function LogViewer({ streamerId }: { streamerId?: string }) {
  const { messages, isConnected } = useWebSocket('ws://localhost:19159/api/ws');

  const filteredMessages = streamerId
    ? messages.filter(m => m.streamer_id === streamerId)
    : messages;

  return (
    <Card title="实时日志" extra={
      <Tag color={isConnected ? 'green' : 'red'}>
        {isConnected ? '已连接' : '未连接'}
      </Tag>
    }>
      <div style={{ maxHeight: '400px', overflow: 'auto' }}>
        {filteredMessages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: '8px' }}>
            <Tag color={getLevelColor(msg.level)}>{msg.level}</Tag>
            <span style={{ marginLeft: '8px' }}>{msg.message}</span>
            <span style={{ marginLeft: '8px', color: '#999', fontSize: '12px' }}>
              {new Date(msg.timestamp).toLocaleTimeString()}
            </span>
          </div>
        ))}
      </div>
    </Card>
  );
}

function getLevelColor(level?: string) {
  switch (level) {
    case 'error': return 'red';
    case 'warn': return 'orange';
    case 'info': return 'blue';
    default: return 'grey';
  }
}
```

### 3. 主要组件

#### 主播列表组件

```typescript
// components/StreamerList.tsx
import { Table, Button, Space, Toast } from '@douyinfe/semi-ui';
import { useStreamers } from '@/hooks/useStreamers';
import { api } from '@/lib/api';

export function StreamerList() {
  const { streamers, isLoading, refresh } = useStreamers();

  const handleStart = async (id: string) => {
    try {
      await api.startTask(id);
      Toast.success('任务已启动');
      refresh();
    } catch (error) {
      Toast.error('启动失败');
    }
  };

  const handleStop = async (id: string) => {
    try {
      await api.stopTask(id);
      Toast.success('任务已停止');
      refresh();
    } catch (error) {
      Toast.error('停止失败');
    }
  };

  const columns = [
    { title: '主播名称', dataIndex: 'name' },
    { title: '平台', dataIndex: 'platform' },
    { title: '状态', dataIndex: 'status', render: (status) => (
      <Tag color={status === 'recording' ? 'green' : 'grey'}>
        {status === 'recording' ? '录制中' : '空闲'}
      </Tag>
    )},
    { title: '操作', render: (_, record) => (
      <Space>
        {record.status === 'recording' ? (
          <Button size="small" type="danger" onClick={() => handleStop(record.id)}>
            停止
          </Button>
        ) : (
          <Button size="small" type="primary" onClick={() => handleStart(record.id)}>
            开始
          </Button>
        )}
        <Button size="small">编辑</Button>
        <Button size="small" type="danger">删除</Button>
      </Space>
    )},
  ];

  return (
    <Table
      columns={columns}
      dataSource={streamers}
      loading={isLoading}
      pagination={false}
    />
  );
}
```

#### 配置编辑器组件

```typescript
// components/ConfigEditor.tsx
import { Form, Button, Select, Input, InputNumber } from '@douyinfe/semi-ui';
import { api } from '@/lib/api';

export function ConfigEditor({ streamer, onSave }: ConfigEditorProps) {
  const [form] = Form.useForm();

  const handleSubmit = async (values: any) => {
    try {
      if (streamer?.id) {
        await api.updateStreamer(streamer.id, values);
      } else {
        await api.createStreamer(values);
      }
      onSave();
    } catch (error) {
      console.error('保存失败', error);
    }
  };

  return (
    <Form
      form={form}
      initialValues={streamer}
      onSubmit={handleSubmit}
      labelPosition="left"
      labelWidth={120}
    >
      <Form.Input field="name" label="主播名称" rules={[{ required: true }]} />
      <Form.Select field="platform" label="平台" rules={[{ required: true }]}>
        <Select.Option value="douyu">斗鱼</Select.Option>
        <Select.Option value="huya">虎牙</Select.Option>
        <Select.Option value="bilibili">B站</Select.Option>
        <Select.Option value="twitch">Twitch</Select.Option>
      </Form.Select>
      <Form.Input field="url" label="直播间地址" rules={[{ required: true }]} />
      <Form.InputNumber field="check_interval" label="检查间隔(秒)" min={10} />
      <Form.Switch field="auto_upload" label="自动上传" />
      <Button htmlType="submit" type="primary">保存</Button>
    </Form>
  );
}
```

### 4. 状态管理

前端使用 SWR 进行数据缓存和状态管理，不需要额外的状态管理库（如 Redux）。

#### 全局状态

```typescript
// hooks/useGlobalState.ts
import { create } from 'zustand';

interface GlobalState {
  user: User | null;
  setUser: (user: User | null) => void;
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useGlobalState = create<GlobalState>((set) => ({
  user: null,
  setUser: (user) => set({ user }),
  theme: 'light',
  setTheme: (theme) => set({ theme }),
}));
```

### 5. 路由结构

使用 Next.js App Router 进行路由管理：

```
app/
├── page.tsx                 # 首页 - 主播列表和任务管理
├── login/
│   └── page.tsx            # 登录页面
├── streamers/
│   ├── page.tsx            # 主播管理页面
│   ├── [id]/
│   │   └── page.tsx        # 主播详情页面
│   └── new/
│       └── page.tsx        # 创建主播页面
├── videos/
│   └── page.tsx            # 视频列表页面
├── settings/
│   └── page.tsx            # 系统设置页面
└── layout.tsx              # 根布局
```

## 构建和部署

### 开发模式

```bash
npm run dev
```

启动开发服务器，支持热重载，访问 `http://localhost:3000`。

### 生产构建

```bash
npm run build
```

Next.js 配置为静态导出模式（`output: 'export'`），构建后生成静态 HTML/CSS/JS 文件到 `out/` 目录。

### 集成到 Rust 后端

构建后的静态文件被复制到 Rust 项目的 `static/` 目录，由 Axum 服务器提供静态文件服务：

```rust
// Rust 后端代码
let app = Router::new()
    .nest("/api", api_routes())
    .nest_service("/", ServeDir::new("static"));
```

## 性能优化

### 1. 代码分割

Next.js 自动进行代码分割，每个页面只加载必要的代码。

### 2. 图片优化

虽然配置了 `images.unoptimized: true`（因为静态导出），但仍然使用 Next.js Image 组件进行懒加载。

### 3. 数据缓存

SWR 自动缓存 API 响应，减少不必要的网络请求：

```typescript
const { data } = useSWR('key', fetcher, {
  revalidateOnFocus: false,  // 不在焦点时重新验证
  dedupingInterval: 2000,    // 2秒内的重复请求会被去重
});
```

### 4. 懒加载组件

使用 React.lazy 和 Suspense 进行组件懒加载：

```typescript
import { lazy, Suspense } from 'react';

const VideoPlayer = lazy(() => import('./VideoPlayer'));

function App() {
  return (
    <Suspense fallback={<div>加载中...</div>}>
      <VideoPlayer />
    </Suspense>
  );
}
```

## 用户体验优化

### 1. 乐观更新

在等待 API 响应时，先更新 UI，提供即时反馈：

```typescript
const { mutate } = useSWR('streamers', fetcher);

const handleStart = async (id: string) => {
  // 乐观更新
  mutate(
    (data) => data.map(s => s.id === id ? { ...s, status: 'recording' } : s),
    false
  );
  
  try {
    await api.startTask(id);
  } catch (error) {
    // 失败时回滚
    mutate();
  }
};
```

### 2. 错误处理

统一的错误处理和用户提示：

```typescript
import { Toast } from '@douyinfe/semi-ui';

async function handleApiCall(apiFunc: () => Promise<any>) {
  try {
    const result = await apiFunc();
    Toast.success('操作成功');
    return result;
  } catch (error) {
    Toast.error(error.message || '操作失败');
    throw error;
  }
}
```

### 3. 加载状态

使用 Semi UI 的 Skeleton 组件显示加载状态：

```typescript
import { Skeleton } from '@douyinfe/semi-ui';

function StreamerList() {
  const { streamers, isLoading } = useStreamers();

  if (isLoading) {
    return <Skeleton.Paragraph rows={5} />;
  }

  return <Table dataSource={streamers} />;
}
```

## 国际化支持

虽然当前主要支持中文，但架构支持未来的国际化扩展：

```typescript
// lib/i18n.ts
const translations = {
  'zh-CN': {
    'streamer.start': '开始录制',
    'streamer.stop': '停止录制',
  },
  'en-US': {
    'streamer.start': 'Start Recording',
    'streamer.stop': 'Stop Recording',
  },
};

export function t(key: string, locale = 'zh-CN') {
  return translations[locale][key] || key;
}
```

## 安全性

### 1. 认证

前端通过 Cookie 或 Token 进行身份认证：

```typescript
// lib/auth.ts
export async function login(username: string, password: string) {
  const res = await fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
    credentials: 'include',  // 包含 Cookie
  });
  
  if (!res.ok) throw new Error('登录失败');
  return res.json();
}
```

### 2. XSS 防护

React 自动转义用户输入，防止 XSS 攻击。对于需要渲染 HTML 的场景，使用 DOMPurify 进行清理。

### 3. CSRF 防护

API 请求包含 CSRF Token：

```typescript
const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;

fetch('/api/endpoint', {
  headers: {
    'X-CSRF-Token': csrfToken,
  },
});
```

## 相关链接

- [后端架构](./backend.md) - 了解 Rust 后端实现
- [数据流设计](./data-flow.md) - 了解前后端数据交互
- [API 参考](../api-reference/) - 查看完整的 API 文档
