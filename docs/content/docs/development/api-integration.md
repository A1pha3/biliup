+++
title = "API 集成"
description = "如何添加新的 REST API 端点和 WebSocket 消息处理"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 60
template = "docs/page.html"

[extra]
lead = "本文档说明如何在 biliup 后端添加新的 REST API 端点、实现 WebSocket 消息处理，以及如何与前端集成。"
toc = true
top = false
+++

## REST API 开发

### 添加新的 API 端点

在 `crates/biliup-cli/src/api/` 目录创建新的路由模块。

#### 示例：添加统计 API

```rust
// crates/biliup-cli/src/api/stats.rs

use axum::{
    extract::State,
    http::StatusCode,
    Json,
    response::IntoResponse,
};
use serde::{Deserialize, Serialize};

use crate::AppState;

#[derive(Serialize)]
pub struct StatsResponse {
    total_downloads: u64,
    total_uploads: u64,
    active_tasks: u32,
}

/// 获取统计信息
pub async fn get_stats(
    State(state): State<AppState>,
) -> Result<Json<StatsResponse>, StatusCode> {
    // 从数据库获取统计信息
    let stats = StatsResponse {
        total_downloads: 100,
        total_uploads: 50,
        active_tasks: 5,
    };
    
    Ok(Json(stats))
}
```

#### 注册路由

```rust
// crates/biliup-cli/src/api/mod.rs

mod stats;

use axum::{
    routing::{get, post},
    Router,
};

pub fn create_router(state: AppState) -> Router {
    Router::new()
        .route("/api/stats", get(stats::get_stats))
        .with_state(state)
}
```

### 请求参数处理

```rust
use axum::extract::{Path, Query};
use serde::Deserialize;

#[derive(Deserialize)]
pub struct PaginationParams {
    page: Option<u32>,
    page_size: Option<u32>,
}

pub async fn list_items(
    Query(params): Query<PaginationParams>,
) -> Json<Vec<Item>> {
    let page = params.page.unwrap_or(1);
    let page_size = params.page_size.unwrap_or(20);
    
    // 查询数据
    let items = query_items(page, page_size).await;
    
    Json(items)
}
```

### 错误处理

```rust
use axum::{
    http::StatusCode,
    response::{IntoResponse, Response},
    Json,
};
use serde_json::json;

pub enum ApiError {
    NotFound,
    BadRequest(String),
    InternalError,
}

impl IntoResponse for ApiError {
    fn into_response(self) -> Response {
        let (status, message) = match self {
            ApiError::NotFound => (StatusCode::NOT_FOUND, "Not found"),
            ApiError::BadRequest(msg) => (StatusCode::BAD_REQUEST, msg.as_str()),
            ApiError::InternalError => (StatusCode::INTERNAL_SERVER_ERROR, "Internal error"),
        };
        
        (status, Json(json!({ "error": message }))).into_response()
    }
}
```

## WebSocket 集成

### 实现 WebSocket 处理器

```rust
// crates/biliup-cli/src/ws/handler.rs

use axum::{
    extract::ws::{Message, WebSocket},
    extract::WebSocketUpgrade,
    response::Response,
};
use futures::{sink::SinkExt, stream::StreamExt};

pub async fn ws_handler(ws: WebSocketUpgrade) -> Response {
    ws.on_upgrade(handle_socket)
}

async fn handle_socket(socket: WebSocket) {
    let (mut sender, mut receiver) = socket.split();
    
    // 接收消息
    while let Some(msg) = receiver.next().await {
        if let Ok(msg) = msg {
            match msg {
                Message::Text(text) => {
                    // 处理文本消息
                    handle_text_message(&text, &mut sender).await;
                }
                Message::Close(_) => {
                    break;
                }
                _ => {}
            }
        }
    }
}

async fn handle_text_message(text: &str, sender: &mut SplitSink<WebSocket, Message>) {
    // 解析消息
    if let Ok(data) = serde_json::from_str::<serde_json::Value>(text) {
        let msg_type = data["type"].as_str().unwrap_or("");
        
        match msg_type {
            "subscribe" => {
                // 处理订阅
            }
            "unsubscribe" => {
                // 处理取消订阅
            }
            _ => {}
        }
    }
}
```

## 数据库操作

### 查询数据

```rust
use sqlx::SqlitePool;

pub async fn query_streamers(pool: &SqlitePool) -> Result<Vec<Streamer>, sqlx::Error> {
    let streamers = sqlx::query_as!(
        Streamer,
        r#"
        SELECT id, name, url, status
        FROM streamers
        WHERE status = 'active'
        "#
    )
    .fetch_all(pool)
    .await?;
    
    Ok(streamers)
}
```

### 插入数据

```rust
pub async fn create_streamer(
    pool: &SqlitePool,
    name: &str,
    url: &str,
) -> Result<i64, sqlx::Error> {
    let result = sqlx::query!(
        r#"
        INSERT INTO streamers (name, url, status)
        VALUES (?, ?, 'active')
        "#,
        name,
        url
    )
    .execute(pool)
    .await?;
    
    Ok(result.last_insert_rowid())
}
```

## 前端集成

### API 调用

```typescript
// app/lib/api.ts

export async function getStats() {
  const response = await fetch('/api/stats');
  if (!response.ok) {
    throw new Error('Failed to fetch stats');
  }
  return response.json();
}

export async function createStreamer(name: string, url: string) {
  const response = await fetch('/api/streamers', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name, url }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to create streamer');
  }
  
  return response.json();
}
```

### WebSocket 连接

```typescript
// app/lib/websocket.ts

export class WebSocketClient {
  private ws: WebSocket | null = null;
  
  connect(url: string) {
    this.ws = new WebSocket(url);
    
    this.ws.onopen = () => {
      console.log('WebSocket connected');
    };
    
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };
    
    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    this.ws.onclose = () => {
      console.log('WebSocket closed');
      // 重连逻辑
      setTimeout(() => this.connect(url), 5000);
    };
  }
  
  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }
  
  private handleMessage(data: any) {
    // 处理消息
  }
}
```

## 认证和权限

### JWT 认证

```rust
use jsonwebtoken::{encode, decode, Header, Validation, EncodingKey, DecodingKey};
use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
struct Claims {
    sub: String,
    exp: usize,
}

pub fn create_token(user_id: &str) -> Result<String, jsonwebtoken::errors::Error> {
    let expiration = chrono::Utc::now()
        .checked_add_signed(chrono::Duration::hours(24))
        .unwrap()
        .timestamp() as usize;
    
    let claims = Claims {
        sub: user_id.to_owned(),
        exp: expiration,
    };
    
    encode(
        &Header::default(),
        &claims,
        &EncodingKey::from_secret("secret".as_ref())
    )
}
```

## 相关文档

- [项目结构](./project-structure.md)
- [源码编译](./building-from-source.md)
- [测试指南](./testing.md)
