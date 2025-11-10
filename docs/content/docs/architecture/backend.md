+++
title = "后端架构"
description = "深入了解基于 Rust 的后端服务实现"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 30
template = "docs/page.html"

[extra]
lead = "biliup 的后端采用 Rust 构建，使用 Axum 框架提供高性能的 Web API 服务，SQLite 存储数据，实现了完整的认证、任务管理和视频上传功能。"
toc = true
top = false
+++

## 技术栈

### 核心框架

- **Rust 1.70+**: 系统编程语言，提供内存安全和高性能
- **Axum 0.6+**: 基于 Tokio 的 Web 框架，专注于人机工程学和模块化
- **Tokio**: 异步运行时，提供高效的异步 I/O
- **Tower**: 服务抽象层，提供中间件支持

### 数据存储

- **SQLite**: 轻量级嵌入式数据库
- **SQLx**: 异步 SQL 工具包，编译时检查 SQL 语句
- **Diesel** (可选): ORM 框架

### HTTP 和序列化

- **Serde**: 序列化/反序列化框架
- **serde_json**: JSON 支持
- **reqwest**: HTTP 客户端，用于调用 Bilibili API

### 其他依赖

- **PyO3**: Rust 和 Python 互操作
- **tokio-tungstenite**: WebSocket 支持
- **tracing**: 结构化日志
- **anyhow**: 错误处理

## 项目结构

biliup 后端由三个主要的 Rust crate 组成：

```
biliup-rs/
├── biliup/                  # 核心上传库
│   ├── src/
│   │   ├── lib.rs          # 库入口
│   │   ├── client.rs       # Bilibili API 客户端
│   │   ├── uploader.rs     # 上传器实现
│   │   ├── line.rs         # 上传线路管理
│   │   └── error.rs        # 错误类型定义
│   └── Cargo.toml
├── biliup-cli/              # Web API 服务器
│   ├── src/
│   │   ├── main.rs         # 程序入口
│   │   ├── api/            # API 路由
│   │   │   ├── mod.rs
│   │   │   ├── streamers.rs   # 主播管理 API
│   │   │   ├── tasks.rs       # 任务管理 API
│   │   │   ├── auth.rs        # 认证 API
│   │   │   └── ws.rs          # WebSocket 处理
│   │   ├── db/             # 数据库操作
│   │   │   ├── mod.rs
│   │   │   ├── models.rs      # 数据模型
│   │   │   └── schema.rs      # 数据库 schema
│   │   ├── middleware/     # 中间件
│   │   │   ├── auth.rs        # 认证中间件
│   │   │   └── logging.rs     # 日志中间件
│   │   └── config.rs       # 配置管理
│   └── Cargo.toml
└── stream-gears/            # Python 绑定
    ├── src/
    │   ├── lib.rs          # PyO3 绑定
    │   └── upload.rs       # 上传函数暴露
    └── Cargo.toml
```

## 核心组件

### 1. biliup - 核心上传库

核心上传库封装了与 Bilibili API 的所有交互逻辑。

#### Bilibili API 客户端

```rust
// biliup/src/client.rs
use reqwest::Client;
use serde::{Deserialize, Serialize};

pub struct BiliClient {
    client: Client,
    cookies: String,
}

impl BiliClient {
    pub fn new(cookies: String) -> Self {
        Self {
            client: Client::new(),
            cookies,
        }
    }

    /// 获取上传凭证
    pub async fn get_upload_credential(&self) -> Result<UploadCredential> {
        let url = "https://member.bilibili.com/preupload";
        let resp = self.client
            .get(url)
            .header("Cookie", &self.cookies)
            .send()
            .await?;
        
        let credential: UploadCredential = resp.json().await?;
        Ok(credential)
    }

    /// 上传视频分片
    pub async fn upload_chunk(
        &self,
        url: &str,
        chunk: &[u8],
        chunk_index: usize,
        total_chunks: usize,
    ) -> Result<ChunkUploadResponse> {
        // 实现分片上传逻辑
        // ...
    }

    /// 提交视频信息
    pub async fn submit_video(&self, video_info: VideoInfo) -> Result<String> {
        let url = "https://member.bilibili.com/x/vu/web/add";
        let resp = self.client
            .post(url)
            .header("Cookie", &self.cookies)
            .json(&video_info)
            .send()
            .await?;
        
        let result: SubmitResponse = resp.json().await?;
        Ok(result.bvid)
    }
}
```

#### 上传器实现

```rust
// biliup/src/uploader.rs
use tokio::fs::File;
use tokio::io::AsyncReadExt;

pub struct Uploader {
    client: BiliClient,
    chunk_size: usize,
    concurrent_uploads: usize,
}

impl Uploader {
    pub fn new(client: BiliClient) -> Self {
        Self {
            client,
            chunk_size: 4 * 1024 * 1024,  // 4MB
            concurrent_uploads: 3,
        }
    }

    /// 上传视频文件
    pub async fn upload_video(
        &self,
        file_path: &str,
        progress_callback: impl Fn(f64),
    ) -> Result<String> {
        // 1. 获取上传凭证
        let credential = self.client.get_upload_credential().await?;
        
        // 2. 读取文件并分片
        let mut file = File::open(file_path).await?;
        let file_size = file.metadata().await?.len();
        let total_chunks = (file_size as usize + self.chunk_size - 1) / self.chunk_size;
        
        // 3. 并发上传分片
        let mut tasks = Vec::new();
        for chunk_index in 0..total_chunks {
            let mut buffer = vec![0u8; self.chunk_size];
            let bytes_read = file.read(&mut buffer).await?;
            buffer.truncate(bytes_read);
            
            let task = self.upload_chunk_with_retry(
                &credential.upload_url,
                buffer,
                chunk_index,
                total_chunks,
            );
            tasks.push(task);
            
            // 控制并发数
            if tasks.len() >= self.concurrent_uploads {
                let _ = futures::future::join_all(tasks.drain(..)).await;
            }
            
            // 报告进度
            let progress = (chunk_index + 1) as f64 / total_chunks as f64;
            progress_callback(progress);
        }
        
        // 等待剩余任务完成
        futures::future::join_all(tasks).await;
        
        // 4. 返回上传结果
        Ok(credential.file_id)
    }

    async fn upload_chunk_with_retry(
        &self,
        url: &str,
        chunk: Vec<u8>,
        index: usize,
        total: usize,
    ) -> Result<()> {
        let mut retries = 3;
        loop {
            match self.client.upload_chunk(url, &chunk, index, total).await {
                Ok(_) => return Ok(()),
                Err(e) if retries > 0 => {
                    retries -= 1;
                    tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
                }
                Err(e) => return Err(e),
            }
        }
    }
}
```

#### 上传线路管理

```rust
// biliup/src/line.rs
use std::time::Duration;

pub struct LineSelector {
    lines: Vec<UploadLine>,
}

impl LineSelector {
    /// 测试所有线路的速度
    pub async fn test_all_lines(&self) -> Vec<LineTestResult> {
        let mut results = Vec::new();
        
        for line in &self.lines {
            let start = std::time::Instant::now();
            match self.test_line(line).await {
                Ok(_) => {
                    let latency = start.elapsed();
                    results.push(LineTestResult {
                        line: line.clone(),
                        latency,
                        success: true,
                    });
                }
                Err(_) => {
                    results.push(LineTestResult {
                        line: line.clone(),
                        latency: Duration::MAX,
                        success: false,
                    });
                }
            }
        }
        
        results.sort_by_key(|r| r.latency);
        results
    }

    /// 选择最快的线路
    pub async fn select_fastest_line(&self) -> Option<UploadLine> {
        let results = self.test_all_lines().await;
        results.into_iter()
            .find(|r| r.success)
            .map(|r| r.line)
    }
}
```

### 2. biliup-cli - Web API 服务器

Web API 服务器提供 REST API 和 WebSocket 服务。


#### 主程序入口

```rust
// biliup-cli/src/main.rs
use axum::{Router, Server};
use tower_http::services::ServeDir;
use std::net::SocketAddr;

#[tokio::main]
async fn main() -> Result<()> {
    // 初始化日志
    tracing_subscriber::fmt::init();

    // 初始化数据库
    let db = Database::new("biliup.db").await?;
    db.run_migrations().await?;

    // 创建应用状态
    let state = AppState {
        db: Arc::new(db),
        ws_clients: Arc::new(Mutex::new(HashMap::new())),
    };

    // 构建路由
    let app = Router::new()
        .nest("/api", api_routes())
        .nest_service("/", ServeDir::new("static"))
        .layer(middleware::from_fn(logging_middleware))
        .with_state(state);

    // 启动服务器
    let addr = SocketAddr::from(([0, 0, 0, 0], 19159));
    tracing::info!("Server listening on {}", addr);
    
    Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;

    Ok(())
}
```

#### API 路由定义

```rust
// biliup-cli/src/api/mod.rs
use axum::{Router, routing::{get, post, put, delete}};

pub fn api_routes() -> Router<AppState> {
    Router::new()
        // 认证相关
        .route("/login", post(auth::login))
        .route("/logout", post(auth::logout))
        .route("/qrcode", get(auth::get_qrcode))
        
        // 主播管理
        .route("/streamers", get(streamers::list))
        .route("/streamers", post(streamers::create))
        .route("/streamers/:id", get(streamers::get))
        .route("/streamers/:id", put(streamers::update))
        .route("/streamers/:id", delete(streamers::delete))
        
        // 任务管理
        .route("/streamers/:id/start", post(tasks::start))
        .route("/streamers/:id/stop", post(tasks::stop))
        .route("/tasks", get(tasks::list))
        .route("/tasks/:id/status", get(tasks::get_status))
        
        // WebSocket
        .route("/ws", get(ws::websocket_handler))
        
        // 视频管理
        .route("/videos", get(videos::list))
        .route("/videos/:id", get(videos::get))
}
```

#### 主播管理 API

```rust
// biliup-cli/src/api/streamers.rs
use axum::{Json, extract::{State, Path}};
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
pub struct CreateStreamerRequest {
    name: String,
    platform: String,
    url: String,
    check_interval: u64,
    auto_upload: bool,
}

/// 获取主播列表
pub async fn list(
    State(state): State<AppState>,
) -> Result<Json<Vec<Streamer>>> {
    let streamers = state.db.get_all_streamers().await?;
    Ok(Json(streamers))
}

/// 创建主播配置
pub async fn create(
    State(state): State<AppState>,
    Json(req): Json<CreateStreamerRequest>,
) -> Result<Json<Streamer>> {
    let streamer = Streamer {
        id: uuid::Uuid::new_v4().to_string(),
        name: req.name,
        platform: req.platform,
        url: req.url,
        check_interval: req.check_interval,
        auto_upload: req.auto_upload,
        status: StreamerStatus::Idle,
        created_at: chrono::Utc::now(),
    };
    
    state.db.insert_streamer(&streamer).await?;
    Ok(Json(streamer))
}

/// 更新主播配置
pub async fn update(
    State(state): State<AppState>,
    Path(id): Path<String>,
    Json(req): Json<CreateStreamerRequest>,
) -> Result<Json<Streamer>> {
    let mut streamer = state.db.get_streamer(&id).await?;
    streamer.name = req.name;
    streamer.platform = req.platform;
    streamer.url = req.url;
    streamer.check_interval = req.check_interval;
    streamer.auto_upload = req.auto_upload;
    
    state.db.update_streamer(&streamer).await?;
    Ok(Json(streamer))
}

/// 删除主播配置
pub async fn delete(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<StatusCode> {
    state.db.delete_streamer(&id).await?;
    Ok(StatusCode::NO_CONTENT)
}
```

#### 任务管理 API

```rust
// biliup-cli/src/api/tasks.rs
use std::process::Stdio;
use tokio::process::Command;

/// 启动录制任务
pub async fn start(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<TaskResponse>> {
    let streamer = state.db.get_streamer(&id).await?;
    
    // 启动 Python 录制进程
    let child = Command::new("python3")
        .arg("-m")
        .arg("biliup")
        .arg("start")
        .arg(&streamer.id)
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()?;
    
    // 保存进程信息
    let task = Task {
        id: uuid::Uuid::new_v4().to_string(),
        streamer_id: streamer.id.clone(),
        pid: child.id().unwrap(),
        status: TaskStatus::Running,
        started_at: chrono::Utc::now(),
    };
    
    state.db.insert_task(&task).await?;
    
    // 启动日志读取任务
    tokio::spawn(read_task_logs(child, state.clone(), task.id.clone()));
    
    Ok(Json(TaskResponse {
        task_id: task.id,
        status: "started".to_string(),
    }))
}

/// 停止录制任务
pub async fn stop(
    State(state): State<AppState>,
    Path(id): Path<String>,
) -> Result<Json<TaskResponse>> {
    let task = state.db.get_task_by_streamer(&id).await?;
    
    // 发送终止信号
    #[cfg(unix)]
    {
        use nix::sys::signal::{kill, Signal};
        use nix::unistd::Pid;
        kill(Pid::from_raw(task.pid as i32), Signal::SIGTERM)?;
    }
    
    #[cfg(windows)]
    {
        // Windows 实现
    }
    
    // 更新任务状态
    state.db.update_task_status(&task.id, TaskStatus::Stopped).await?;
    
    Ok(Json(TaskResponse {
        task_id: task.id,
        status: "stopped".to_string(),
    }))
}

/// 读取任务日志并通过 WebSocket 推送
async fn read_task_logs(
    mut child: tokio::process::Child,
    state: AppState,
    task_id: String,
) {
    use tokio::io::{AsyncBufReadExt, BufReader};
    
    let stdout = child.stdout.take().unwrap();
    let mut reader = BufReader::new(stdout).lines();
    
    while let Ok(Some(line)) = reader.next_line().await {
        // 解析日志
        let log = LogMessage {
            task_id: task_id.clone(),
            level: "info".to_string(),
            message: line,
            timestamp: chrono::Utc::now(),
        };
        
        // 推送到所有 WebSocket 客户端
        broadcast_log(&state, log).await;
    }
}
```

#### WebSocket 处理

```rust
// biliup-cli/src/api/ws.rs
use axum::extract::ws::{WebSocket, WebSocketUpgrade, Message};
use futures::{StreamExt, SinkExt};

pub async fn websocket_handler(
    ws: WebSocketUpgrade,
    State(state): State<AppState>,
) -> impl IntoResponse {
    ws.on_upgrade(|socket| handle_socket(socket, state))
}

async fn handle_socket(socket: WebSocket, state: AppState) {
    let (mut sender, mut receiver) = socket.split();
    let client_id = uuid::Uuid::new_v4().to_string();
    
    // 注册客户端
    state.ws_clients.lock().await.insert(
        client_id.clone(),
        sender.clone(),
    );
    
    // 处理客户端消息
    while let Some(Ok(msg)) = receiver.next().await {
        match msg {
            Message::Text(text) => {
                // 处理文本消息
                tracing::debug!("Received: {}", text);
            }
            Message::Close(_) => {
                break;
            }
            _ => {}
        }
    }
    
    // 移除客户端
    state.ws_clients.lock().await.remove(&client_id);
}

/// 广播日志到所有客户端
pub async fn broadcast_log(state: &AppState, log: LogMessage) {
    let message = serde_json::to_string(&log).unwrap();
    let mut clients = state.ws_clients.lock().await;
    
    // 移除已断开的客户端
    clients.retain(|_, sender| {
        sender.send(Message::Text(message.clone())).is_ok()
    });
}
```

### 3. 数据库设计

#### Schema 定义

```sql
-- 主播配置表
CREATE TABLE streamers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    platform TEXT NOT NULL,
    url TEXT NOT NULL,
    check_interval INTEGER NOT NULL DEFAULT 60,
    auto_upload BOOLEAN NOT NULL DEFAULT 1,
    status TEXT NOT NULL DEFAULT 'idle',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 任务表
CREATE TABLE tasks (
    id TEXT PRIMARY KEY,
    streamer_id TEXT NOT NULL,
    pid INTEGER NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP NOT NULL,
    stopped_at TIMESTAMP,
    FOREIGN KEY (streamer_id) REFERENCES streamers(id) ON DELETE CASCADE
);

-- 视频记录表
CREATE TABLE videos (
    id TEXT PRIMARY KEY,
    streamer_id TEXT NOT NULL,
    task_id TEXT NOT NULL,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    duration INTEGER NOT NULL,
    bvid TEXT,
    uploaded_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (streamer_id) REFERENCES streamers(id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);

-- 用户表（认证）
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 会话表
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

#### 数据库操作

```rust
// biliup-cli/src/db/mod.rs
use sqlx::{SqlitePool, sqlite::SqlitePoolOptions};

pub struct Database {
    pool: SqlitePool,
}

impl Database {
    pub async fn new(database_url: &str) -> Result<Self> {
        let pool = SqlitePoolOptions::new()
            .max_connections(5)
            .connect(database_url)
            .await?;
        
        Ok(Self { pool })
    }

    pub async fn run_migrations(&self) -> Result<()> {
        sqlx::migrate!("./migrations")
            .run(&self.pool)
            .await?;
        Ok(())
    }

    pub async fn get_all_streamers(&self) -> Result<Vec<Streamer>> {
        let streamers = sqlx::query_as!(
            Streamer,
            "SELECT * FROM streamers ORDER BY created_at DESC"
        )
        .fetch_all(&self.pool)
        .await?;
        
        Ok(streamers)
    }

    pub async fn insert_streamer(&self, streamer: &Streamer) -> Result<()> {
        sqlx::query!(
            "INSERT INTO streamers (id, name, platform, url, check_interval, auto_upload, status)
             VALUES (?, ?, ?, ?, ?, ?, ?)",
            streamer.id,
            streamer.name,
            streamer.platform,
            streamer.url,
            streamer.check_interval,
            streamer.auto_upload,
            streamer.status
        )
        .execute(&self.pool)
        .await?;
        
        Ok(())
    }
}
```

### 4. 认证和会话管理

#### 密码认证

```rust
// biliup-cli/src/api/auth.rs
use argon2::{Argon2, PasswordHash, PasswordHasher, PasswordVerifier};
use argon2::password_hash::SaltString;

pub async fn login(
    State(state): State<AppState>,
    Json(req): Json<LoginRequest>,
) -> Result<Json<LoginResponse>> {
    // 查询用户
    let user = state.db.get_user_by_username(&req.username).await?;
    
    // 验证密码
    let parsed_hash = PasswordHash::new(&user.password_hash)?;
    Argon2::default()
        .verify_password(req.password.as_bytes(), &parsed_hash)
        .map_err(|_| Error::InvalidCredentials)?;
    
    // 创建会话
    let session = Session {
        id: uuid::Uuid::new_v4().to_string(),
        user_id: user.id.clone(),
        token: generate_token(),
        expires_at: chrono::Utc::now() + chrono::Duration::days(7),
    };
    
    state.db.insert_session(&session).await?;
    
    Ok(Json(LoginResponse {
        token: session.token,
        user: user.into(),
    }))
}

fn generate_token() -> String {
    use rand::Rng;
    let mut rng = rand::thread_rng();
    (0..32)
        .map(|_| format!("{:02x}", rng.gen::<u8>()))
        .collect()
}
```

#### 认证中间件

```rust
// biliup-cli/src/middleware/auth.rs
use axum::http::{Request, StatusCode};
use axum::middleware::Next;

pub async fn auth_middleware<B>(
    State(state): State<AppState>,
    mut req: Request<B>,
    next: Next<B>,
) -> Result<Response, StatusCode> {
    // 从 Header 或 Cookie 获取 token
    let token = req.headers()
        .get("Authorization")
        .and_then(|v| v.to_str().ok())
        .and_then(|v| v.strip_prefix("Bearer "))
        .ok_or(StatusCode::UNAUTHORIZED)?;
    
    // 验证 token
    let session = state.db
        .get_session_by_token(token)
        .await
        .map_err(|_| StatusCode::UNAUTHORIZED)?;
    
    // 检查是否过期
    if session.expires_at < chrono::Utc::now() {
        return Err(StatusCode::UNAUTHORIZED);
    }
    
    // 将用户信息添加到请求扩展
    req.extensions_mut().insert(session.user_id);
    
    Ok(next.run(req).await)
}
```

### 5. stream-gears - Python 绑定

使用 PyO3 将 Rust 上传功能暴露给 Python。

```rust
// stream-gears/src/lib.rs
use pyo3::prelude::*;
use biliup::{BiliClient, Uploader};

#[pyfunction]
fn upload_video(
    cookies: String,
    file_path: String,
    title: String,
    desc: String,
) -> PyResult<String> {
    let rt = tokio::runtime::Runtime::new()?;
    
    rt.block_on(async {
        let client = BiliClient::new(cookies);
        let uploader = Uploader::new(client);
        
        // 上传视频
        let file_id = uploader.upload_video(&file_path, |progress| {
            println!("Upload progress: {:.2}%", progress * 100.0);
        }).await?;
        
        // 提交视频信息
        let video_info = VideoInfo {
            title,
            desc,
            file_id,
            ..Default::default()
        };
        
        let bvid = client.submit_video(video_info).await?;
        Ok(bvid)
    })
}

#[pymodule]
fn stream_gears(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(upload_video, m)?)?;
    Ok(())
}
```

## 性能优化

### 1. 异步 I/O

所有 I/O 操作都使用 Tokio 异步运行时，避免阻塞线程。

### 2. 连接池

数据库使用连接池，复用连接，减少连接开销。

### 3. 并发上传

支持多个分片并发上传，充分利用带宽。

### 4. 零拷贝

stream-gears 使用 PyO3 的零拷贝特性，高效传递数据。

## 错误处理

使用 `anyhow` 和自定义错误类型进行统一的错误处理：

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum BiliupError {
    #[error("Network error: {0}")]
    Network(#[from] reqwest::Error),
    
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    
    #[error("Invalid credentials")]
    InvalidCredentials,
    
    #[error("Task not found")]
    TaskNotFound,
}
```

## 日志记录

使用 `tracing` 进行结构化日志记录：

```rust
use tracing::{info, warn, error, debug};

#[tracing::instrument]
async fn upload_video(file_path: &str) -> Result<String> {
    info!("Starting video upload: {}", file_path);
    
    match uploader.upload(file_path).await {
        Ok(bvid) => {
            info!("Upload successful: {}", bvid);
            Ok(bvid)
        }
        Err(e) => {
            error!("Upload failed: {}", e);
            Err(e)
        }
    }
}
```

## 相关链接

- [前端架构](./frontend.md) - 了解前端实现
- [Python 引擎](./python-engine.md) - 了解 Python 引擎
- [数据流设计](./data-flow.md) - 了解完整的数据流转
