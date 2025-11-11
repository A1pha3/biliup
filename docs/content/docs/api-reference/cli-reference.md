+++
title = "CLI 参考"
description = "biliup 命令行工具完整参考文档"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 64
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "通过命令行使用 biliup 的所有功能"
toc = true
top = false
+++

biliup 提供了功能完整的命令行工具，支持视频上传、直播录制、账号管理等操作。

## 基本用法

```bash
biliup [OPTIONS] <COMMAND>
```

### 全局选项

- `-p, --proxy <PROXY>`: 配置代理服务器
- `-u, --user-cookie <USER_COOKIE>`: 指定登录信息文件（默认: `cookies.json`）
- `--rust-log <RUST_LOG>`: 设置日志级别（默认: `tower_http=debug,info`）
- `-h, --help`: 显示帮助信息
- `-V, --version`: 显示版本信息

### 获取帮助

```bash
# 查看主命令帮助
biliup --help

# 查看子命令帮助
biliup upload --help
```


## 命令列表

### login - 登录 B 站

登录 B 站账号并保存登录信息。

**用法**:

```bash
biliup login [OPTIONS]
```

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 指定保存登录信息的文件名（默认: `cookies.json`）

**示例**:

```bash
# 使用默认文件名登录
biliup login

# 指定登录信息文件
biliup login -u my_account.json
```

**说明**:

登录过程会打开浏览器或显示二维码，扫码登录后会自动保存登录信息到指定文件。登录信息包含 Cookie 和 Token，用于后续的上传和 API 调用。

---

### renew - 刷新登录信息

手动验证并刷新登录信息。

**用法**:

```bash
biliup renew [OPTIONS]
```

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 指定登录信息文件（默认: `cookies.json`）

**示例**:

```bash
# 刷新默认账号的登录信息
biliup renew

# 刷新指定账号的登录信息
biliup renew -u my_account.json
```

**说明**:

当登录信息过期或需要重新验证时使用此命令。会重新进行登录验证并更新登录信息文件。

---

### upload - 上传视频

上传视频到 B 站。

**用法**:

```bash
biliup upload [OPTIONS] <VIDEO_PATH>...
```

**参数**:

- `<VIDEO_PATH>...`: 要上传的视频文件路径（支持多个文件）

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 使用的登录信息文件（默认: `cookies.json`）
- `--title <TITLE>`: 视频标题
- `--tid <TID>`: 分区 ID
- `--tag <TAG>`: 视频标签（逗号分隔）
- `--desc <DESC>`: 视频简介
- `--source <SOURCE>`: 转载来源
- `--cover <COVER>`: 封面图片路径
- `--copyright <COPYRIGHT>`: 版权声明（1=自制，2=转载）
- `--no-reprint`: 禁止转载
- `--open-elec`: 开启充电
- `--dolby`: 启用杜比音效
- `--hires`: 启用高分辨率
- `--line <LINE>`: 上传线路（bda2/kodo/ws/qn 等）
- `--limit <LIMIT>`: 上传线程数
- `-p, --proxy <PROXY>`: 代理服务器

**示例**:

```bash
# 基本上传
biliup upload video.mp4 --title "我的视频" --tid 171

# 上传多个视频（合集）
biliup upload part1.mp4 part2.mp4 part3.mp4 \
  --title "系列视频" \
  --tid 171 \
  --tag "游戏,教程"

# 完整参数上传
biliup upload video.mp4 \
  --title "精彩直播录像" \
  --tid 171 \
  --tag "游戏,直播录像,LOL" \
  --desc "2025年1月10日直播录像" \
  --cover cover.jpg \
  --copyright 1 \
  --no-reprint \
  --open-elec \
  --line bda2 \
  --limit 3

# 使用代理上传
biliup upload video.mp4 \
  --title "视频标题" \
  --tid 171 \
  -p http://127.0.0.1:7890

# 使用指定账号上传
biliup upload video.mp4 \
  --title "视频标题" \
  --tid 171 \
  -u account2.json
```

**常用分区 ID**:

- `171`: 电子竞技
- `172`: 网络游戏
- `65`: 网络游戏（其他）
- `136`: 音乐综合
- `160`: 生活
- `138`: 搞笑
- `21`: 日常

完整分区列表请参考 [B 站分区文档](https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/video/video_zone.md)。

---

### append - 追加视频

向已发布的稿件追加视频。

**用法**:

```bash
biliup append [OPTIONS] <BVID> <VIDEO_PATH>...
```

**参数**:

- `<BVID>`: 稿件的 BV 号（如 BV1xx411c7mD）
- `<VIDEO_PATH>...`: 要追加的视频文件路径

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 使用的登录信息文件（默认: `cookies.json`）
- `--line <LINE>`: 上传线路
- `--limit <LIMIT>`: 上传线程数

**示例**:

```bash
# 追加单个视频
biliup append BV1xx411c7mD part4.mp4

# 追加多个视频
biliup append BV1xx411c7mD part4.mp4 part5.mp4 part6.mp4

# 使用指定账号追加
biliup append BV1xx411c7mD part4.mp4 -u account2.json
```

**说明**:

只能向自己发布的稿件追加视频。追加的视频会作为新的分P添加到稿件中。

---

### show - 查看视频详情

打印视频的详细信息。

**用法**:

```bash
biliup show [OPTIONS] <BVID>
```

**参数**:

- `<BVID>`: 视频的 BV 号

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 使用的登录信息文件（默认: `cookies.json`）

**示例**:

```bash
# 查看视频详情
biliup show BV1xx411c7mD

# 使用指定账号查看
biliup show BV1xx411c7mD -u account2.json
```

**输出示例**:

```json
{
  "bvid": "BV1xx411c7mD",
  "title": "视频标题",
  "desc": "视频简介",
  "tid": 171,
  "tname": "电子竞技",
  "copyright": 1,
  "pic": "封面URL",
  "pubdate": 1704873600,
  "stat": {
    "view": 1000,
    "danmaku": 50,
    "reply": 20,
    "favorite": 30,
    "coin": 10,
    "share": 5,
    "like": 100
  }
}
```


### list - 列出已上传视频

列出所有已上传的视频。

**用法**:

```bash
biliup list [OPTIONS]
```

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 使用的登录信息文件（默认: `cookies.json`）
- `--page <PAGE>`: 页码（默认: 1）
- `--page-size <PAGE_SIZE>`: 每页数量（默认: 30）

**示例**:

```bash
# 列出第一页视频
biliup list

# 列出第二页视频
biliup list --page 2

# 自定义每页数量
biliup list --page-size 50

# 使用指定账号列出
biliup list -u account2.json
```

**输出示例**:

```
共 100 个视频

BV1xx411c7mD | 视频标题1 | 2025-01-10 12:00:00 | 播放: 1000
BV1yy411c7mE | 视频标题2 | 2025-01-09 18:30:00 | 播放: 500
BV1zz411c7mF | 视频标题3 | 2025-01-08 20:15:00 | 播放: 2000
...
```

---

### download - 下载视频

下载 B 站视频。

**用法**:

```bash
biliup download [OPTIONS] <URL>
```

**参数**:

- `<URL>`: 视频 URL（支持 BV 号、AV 号、短链接等）

**选项**:

- `-u, --user-cookie <USER_COOKIE>`: 使用的登录信息文件（默认: `cookies.json`）
- `-o, --output <OUTPUT>`: 输出文件路径
- `--quality <QUALITY>`: 视频画质（默认: 最高画质）
- `-p, --proxy <PROXY>`: 代理服务器

**示例**:

```bash
# 下载视频（默认最高画质）
biliup download https://www.bilibili.com/video/BV1xx411c7mD

# 指定输出文件名
biliup download BV1xx411c7mD -o my_video.mp4

# 指定画质下载
biliup download BV1xx411c7mD --quality 1080p

# 使用代理下载
biliup download BV1xx411c7mD -p http://127.0.0.1:7890

# 使用指定账号下载（可下载大会员专享视频）
biliup download BV1xx411c7mD -u vip_account.json
```

**支持的画质**:

- `4K`: 4K 超清
- `1080p60`: 1080P 60帧
- `1080p`: 1080P 高清
- `720p60`: 720P 60帧
- `720p`: 720P 高清
- `480p`: 480P 清晰
- `360p`: 360P 流畅

---

### server - 启动 Web 服务

启动 Web 服务器，提供 WebUI 界面和 API 接口。

**用法**:

```bash
biliup server [OPTIONS]
```

**选项**:

- `-b, --bind <BIND>`: 绑定地址（默认: `0.0.0.0`）
- `-p, --port <PORT>`: 端口号（默认: `19159`）
- `--auth`: 开启登录密码认证
- `--rust-log <RUST_LOG>`: 日志级别

**示例**:

```bash
# 使用默认配置启动
biliup server

# 指定端口启动
biliup server -p 8080

# 开启认证启动
biliup server --auth

# 只监听本地
biliup server -b 127.0.0.1

# 自定义日志级别
biliup server --rust-log debug

# 后台运行（Linux/macOS）
nohup biliup server --auth > server.log 2>&1 &

# 使用 systemd 管理（推荐）
# 参考: https://docs.biliup.rs/docs/guide/introduction/#linuxxia-pei-zhi-kai-ji-zi-qi
```

**访问 WebUI**:

启动后访问 `http://localhost:19159` 即可使用 Web 界面。

**认证说明**:

开启 `--auth` 后，首次访问需要创建管理员账号。后续访问需要登录才能使用。

---

### dump-flv - 输出 FLV 元数据

输出 FLV 文件的元数据信息。

**用法**:

```bash
biliup dump-flv <FILE_PATH>
```

**参数**:

- `<FILE_PATH>`: FLV 文件路径

**示例**:

```bash
# 输出 FLV 元数据
biliup dump-flv recording.flv
```

**输出示例**:

```json
{
  "duration": 3600.5,
  "width": 1920,
  "height": 1080,
  "videodatarate": 2500,
  "audiodatarate": 128,
  "framerate": 30,
  "videocodecid": 7,
  "audiocodecid": 10
}
```

**说明**:

此命令用于调试和分析 FLV 文件，可以查看视频的编码信息、时长、分辨率等元数据。


## 使用场景

### 场景 1: 快速上传视频

```bash
# 1. 登录账号
biliup login

# 2. 上传视频
biliup upload my_video.mp4 \
  --title "我的第一个视频" \
  --tid 171 \
  --tag "游戏,教程" \
  --desc "这是我的第一个视频"
```

---

### 场景 2: 批量上传系列视频

```bash
# 上传系列视频作为合集
biliup upload \
  episode1.mp4 \
  episode2.mp4 \
  episode3.mp4 \
  --title "系列教程" \
  --tid 171 \
  --tag "教程,系列" \
  --desc "完整系列教程"
```

---

### 场景 3: 定时上传脚本

```bash
#!/bin/bash
# upload_daily.sh - 每日自动上传脚本

DATE=$(date +%Y-%m-%d)
VIDEO_FILE="recording_${DATE}.mp4"

if [ -f "$VIDEO_FILE" ]; then
    biliup upload "$VIDEO_FILE" \
        --title "每日直播录像 ${DATE}" \
        --tid 171 \
        --tag "直播录像,游戏" \
        --desc "每日直播录像" \
        --no-reprint \
        --open-elec
    
    echo "上传完成: $VIDEO_FILE"
else
    echo "文件不存在: $VIDEO_FILE"
fi
```

配置 crontab 定时执行：

```bash
# 每天凌晨 2 点执行上传
0 2 * * * /path/to/upload_daily.sh
```

---

### 场景 4: 多账号管理

```bash
# 账号 1 登录
biliup login -u account1.json

# 账号 2 登录
biliup login -u account2.json

# 使用账号 1 上传
biliup upload video1.mp4 --title "视频1" --tid 171 -u account1.json

# 使用账号 2 上传
biliup upload video2.mp4 --title "视频2" --tid 171 -u account2.json

# 列出账号 1 的视频
biliup list -u account1.json

# 列出账号 2 的视频
biliup list -u account2.json
```

---

### 场景 5: 使用代理上传

```bash
# 设置代理环境变量
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 或者直接在命令中指定代理
biliup upload video.mp4 \
  --title "视频标题" \
  --tid 171 \
  -p http://127.0.0.1:7890
```

---

### 场景 6: 启动录制服务

```bash
# 前台运行（测试用）
biliup server --auth

# 后台运行
nohup biliup server --auth > server.log 2>&1 &

# 查看日志
tail -f server.log

# 停止服务
pkill -f "biliup server"
```

---

### 场景 7: 视频管理

```bash
# 查看已上传的视频列表
biliup list

# 查看特定视频详情
biliup show BV1xx411c7mD

# 向视频追加新的分P
biliup append BV1xx411c7mD new_part.mp4

# 下载自己上传的视频
biliup download BV1xx411c7mD -o backup.mp4
```


## 高级用法

### 环境变量

biliup 支持通过环境变量配置：

```bash
# 代理设置
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890

# 日志级别
export RUST_LOG=debug

# 默认 Cookie 文件
export BILIUP_COOKIE=my_account.json
```

---

### 配置文件

创建配置文件 `~/.biliup/config.toml`：

```toml
[upload]
default_tid = 171
default_tag = "游戏,直播"
default_copyright = 1
no_reprint = true
open_elec = true

[network]
proxy = "http://127.0.0.1:7890"
timeout = 300

[server]
bind = "0.0.0.0"
port = 19159
auth = true
```

---

### Shell 别名

在 `~/.bashrc` 或 `~/.zshrc` 中添加别名：

```bash
# 快速上传别名
alias bup='biliup upload --tid 171 --tag "游戏,直播" --no-reprint --open-elec'

# 使用别名上传
bup video.mp4 --title "我的视频"

# 快速启动服务
alias bserver='biliup server --auth'

# 查看日志
alias blog='tail -f ~/.biliup/server.log'
```

---

### 管道操作

结合其他命令使用：

```bash
# 查找并上传所有 MP4 文件
find ./recordings -name "*.mp4" -type f | while read file; do
    biliup upload "$file" \
        --title "$(basename "$file" .mp4)" \
        --tid 171 \
        --tag "录像"
done

# 批量重命名并上传
for file in *.mp4; do
    new_name="直播录像_$(date +%Y%m%d)_${file}"
    mv "$file" "$new_name"
    biliup upload "$new_name" --title "$new_name" --tid 171
done
```

---

### 错误处理

添加错误处理和重试机制：

```bash
#!/bin/bash
# upload_with_retry.sh

MAX_RETRIES=3
RETRY_DELAY=60

upload_video() {
    local file=$1
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        echo "尝试上传 $file (第 $((retries+1)) 次)"
        
        if biliup upload "$file" \
            --title "$(basename "$file" .mp4)" \
            --tid 171 \
            --tag "录像"; then
            echo "上传成功: $file"
            return 0
        else
            echo "上传失败，等待 $RETRY_DELAY 秒后重试..."
            sleep $RETRY_DELAY
            retries=$((retries+1))
        fi
    done
    
    echo "上传失败，已达到最大重试次数: $file"
    return 1
}

# 使用
upload_video "my_video.mp4"
```

---

### 日志管理

```bash
# 启用详细日志
RUST_LOG=debug biliup upload video.mp4 --title "测试" --tid 171

# 将日志输出到文件
biliup upload video.mp4 --title "测试" --tid 171 2>&1 | tee upload.log

# 只保留错误日志
biliup upload video.mp4 --title "测试" --tid 171 2>&1 | grep -i error

# 日志轮转（使用 logrotate）
# /etc/logrotate.d/biliup
/var/log/biliup/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```


## 常见问题

### 登录相关

**Q: 登录信息保存在哪里？**

A: 默认保存在当前目录的 `cookies.json` 文件中。可以通过 `-u` 参数指定其他文件。

**Q: 登录信息会过期吗？**

A: 会的。B 站的登录信息有效期约为 30 天。过期后需要使用 `biliup renew` 重新登录。

**Q: 如何管理多个账号？**

A: 使用不同的 Cookie 文件：

```bash
biliup login -u account1.json
biliup login -u account2.json
biliup upload video.mp4 --title "视频" --tid 171 -u account1.json
```

---

### 上传相关

**Q: 上传失败怎么办？**

A: 检查以下几点：
1. 登录信息是否有效（`biliup renew`）
2. 网络连接是否正常
3. 视频文件是否完整
4. 是否需要使用代理（`-p` 参数）

**Q: 如何提高上传速度？**

A: 
1. 使用 `--line` 参数选择更快的线路
2. 增加 `--limit` 参数提高并发数
3. 使用有线网络而非 WiFi
4. 选择网络空闲时段上传

**Q: 支持哪些视频格式？**

A: 支持 MP4、FLV、AVI、WMV、MOV、MKV 等常见格式。推荐使用 MP4 格式。

---

### 服务器相关

**Q: 如何设置开机自启？**

A: 使用 systemd（Linux）：

```bash
# 创建服务文件
sudo nano /etc/systemd/system/biliup.service

# 内容如下：
[Unit]
Description=Biliup Service
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/biliup
ExecStart=/usr/local/bin/biliup server --auth
Restart=always

[Install]
WantedBy=multi-user.target

# 启用服务
sudo systemctl enable biliup
sudo systemctl start biliup
```

**Q: 如何修改默认端口？**

A: 使用 `-p` 参数：

```bash
biliup server -p 8080
```

**Q: 如何远程访问 WebUI？**

A: 
1. 确保防火墙开放端口
2. 使用 `--bind 0.0.0.0` 监听所有网卡
3. 通过 `http://服务器IP:19159` 访问

---

### 其他问题

**Q: 如何查看命令执行日志？**

A: 使用 `--rust-log` 参数：

```bash
biliup --rust-log debug upload video.mp4 --title "测试" --tid 171
```

**Q: 如何使用代理？**

A: 两种方式：
1. 环境变量：`export HTTP_PROXY=http://127.0.0.1:7890`
2. 命令参数：`biliup -p http://127.0.0.1:7890 upload ...`

**Q: 命令执行很慢怎么办？**

A: 
1. 检查网络连接
2. 尝试使用代理
3. 检查磁盘空间是否充足
4. 查看日志排查具体问题

## 注意事项

1. **登录信息安全**: Cookie 文件包含敏感信息，请妥善保管，不要分享给他人

2. **上传限制**: B 站对视频上传有限制：
   - 单个视频最大 8GB
   - 时长最长 4 小时
   - 每日上传数量有限制

3. **版权声明**: 上传视频时请正确设置版权信息，避免侵权

4. **网络稳定性**: 上传大文件时建议使用稳定的网络连接

5. **磁盘空间**: 确保有足够的磁盘空间存储临时文件

6. **命令行转义**: 在 Shell 中使用特殊字符时需要转义或使用引号

7. **并发控制**: 同时上传多个视频时注意控制并发数，避免被限流

8. **日志查看**: 遇到问题时查看详细日志有助于排查

## 相关文档

- [REST API](./rest-api.md) - HTTP 接口文档
- [WebSocket API](./websocket-api.md) - 实时通信接口
- [Python API](./python-api.md) - Python 库接口
- [配置文件格式](../configuration/config-file-format.md) - 配置说明
- [错误码](./error-codes.md) - 错误码说明
- [快速开始](../getting-started/quick-start.md) - 入门教程
