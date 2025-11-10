+++
title = "故障排查"
description = "解决 biliup 使用过程中遇到的常见问题和错误"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 70
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "本文档整理了 biliup 使用过程中的常见问题、错误信息及解决方案，帮助你快速定位和解决问题。"
toc = true
top = false
+++

## 快速诊断

遇到问题时，首先进行以下检查：

### 1. 检查版本

确保使用最新版本：

```bash
biliup --version
```

更新到最新版本：

```bash
pip install --upgrade biliup
```

### 2. 查看日志

日志文件包含详细的错误信息：

```bash
# 查看最新日志
tail -f biliup.log

# 查看错误日志
grep "ERROR" biliup.log

# 查看警告日志
grep "WARN" biliup.log
```

### 3. 检查配置

验证配置文件语法：

```bash
# 检查 YAML 语法
biliup config check
```

### 4. 测试网络

检查网络连接：

```bash
# 测试直播平台连接
curl -I https://live.bilibili.com

# 测试 B 站 API
curl -I https://api.bilibili.com
```

## 安装问题

### pip 安装失败

**错误信息**：
```
ERROR: Could not find a version that satisfies the requirement biliup
```

**原因**：
- Python 版本过低
- pip 版本过旧
- 网络连接问题

**解决方案**：

1. 检查 Python 版本（需要 3.8+）：
```bash
python --version
```

2. 升级 pip：
```bash
pip install --upgrade pip
```

3. 使用国内镜像源：
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple biliup
```

### 依赖安装失败

**错误信息**：
```
ERROR: Failed building wheel for xxx
```

**解决方案**：

**macOS**：
```bash
# 安装 Xcode Command Line Tools
xcode-select --install

# 使用 Homebrew 安装依赖
brew install python@3.11
```

**Linux**：
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc
```

**Windows**：
- 安装 [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- 或使用预编译的二进制包

### FFmpeg 未安装

**错误信息**：
```
ERROR: FFmpeg not found
```

**解决方案**：

**macOS**：
```bash
brew install ffmpeg
```

**Linux**：
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# CentOS/RHEL
sudo yum install ffmpeg
```

**Windows**：
1. 从 [FFmpeg 官网](https://ffmpeg.org/download.html) 下载
2. 解压到目录（如 `C:\ffmpeg`）
3. 添加到系统 PATH 环境变量

验证安装：
```bash
ffmpeg -version
```

## 录制问题

### 无法获取直播流

**错误信息**：
```
ERROR: Failed to get stream url
ERROR: 404 Not Found
```

**可能原因**：
1. 直播间地址错误
2. 主播未开播
3. 直播间需要登录
4. 平台限制或封禁

**解决方案**：

1. 验证直播间地址：
```bash
# 测试直播间是否可访问
curl -I "直播间URL"
```

2. 检查主播是否开播：
- 在浏览器中打开直播间
- 确认直播状态

3. 配置 Cookie（如需登录）：
```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    cookies: "cookies.txt"
```

4. 使用代理（如有地区限制）：
```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    proxy: "http://127.0.0.1:7890"
```

### 录制中断

**错误信息**：
```
ERROR: Connection reset by peer
ERROR: Read timeout
```

**可能原因**：
- 网络不稳定
- 主播断流
- 直播平台限制

**解决方案**：

1. 启用自动重连：
```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    retry_times: 5
    retry_interval: 60
```

2. 调整超时设置：
```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    timeout: 60
    read_timeout: 120
```

3. 使用更稳定的格式：
```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"  # FLV 格式最稳定
```

### 录制文件损坏

**症状**：
- 视频无法播放
- 播放卡顿或花屏
- 文件大小异常

**可能原因**：
- 录制中断未正常结束
- 磁盘空间不足
- 使用了不稳定的格式（MP4）

**解决方案**：

1. 使用 FLV 格式（最稳定）：
```yaml
streamers:
  主播名称:
    format: "flv"
```

2. 启用文件分段：
```yaml
streamers:
  主播名称:
    segment_size: "2G"
```

3. 尝试修复损坏的视频：
```bash
# 使用 FFmpeg 修复
ffmpeg -i broken.mp4 -c copy fixed.mp4

# 或转换格式
ffmpeg -i broken.flv -c copy fixed.mp4
```

4. 确保磁盘空间充足：
```bash
# 检查磁盘空间
df -h
```

### 画质不是最高

**症状**：
- 录制的画质低于预期
- 画面模糊

**可能原因**：
- 主播未开启高画质
- 配置未设置最高画质
- 平台需要登录才能获取高画质

**解决方案**：

1. 设置最高画质：
```yaml
streamers:
  主播名称:
    quality: "best"
```

2. 配置平台 Cookie：
```yaml
streamers:
  主播名称:
    cookies: "cookies.txt"
```

3. 检查主播设置：
- 确认主播是否开启了高画质推流
- 某些平台需要会员才能观看高画质

### 录制延迟很大

**症状**：
- 录制内容比实时直播延迟 30 秒以上

**说明**：
这是正常现象。直播本身就有延迟（通常 10-30 秒），录制会在此基础上增加一些延迟。

**如果延迟过大（超过 1 分钟）**：

1. 检查网络延迟：
```bash
ping live.bilibili.com
```

2. 减少缓冲：
```yaml
streamers:
  主播名称:
    buffer_size: "1M"  # 减小缓冲区
```

注意：延迟不影响录制质量，录制的是完整的直播内容。


## 上传问题

### Cookie 过期

**错误信息**：
```
ERROR: Login required
ERROR: Cookie expired
ERROR: 412 Precondition Failed
```

**解决方案**：

重新登录：
```bash
biliup login
```

选择扫码登录（推荐）或账号密码登录。

验证登录状态：
```bash
biliup renew
```

**预防措施**：
- 定期运行 `biliup renew` 刷新 Cookie
- 设置定时任务自动刷新：
```bash
# 添加到 crontab（每天刷新）
0 0 * * * /usr/local/bin/biliup renew
```

### 上传速度慢

**症状**：
- 上传速度远低于带宽
- 上传时间过长

**解决方案**：

1. 测试上传带宽：
```bash
# 使用 speedtest
speedtest-cli
```

2. 尝试不同上传线路：
```bash
# 测试 upos 线路
biliup upload video.mp4 --line upos

# 测试 bupfetch 线路
biliup upload video.mp4 --line bupfetch
```

3. 调整并发数：
```yaml
upload_config:
  limit: 5  # 增加并发数
```

4. 避开高峰期：
- 晚上 8-11 点是高峰期，上传较慢
- 建议深夜或清晨上传

5. 使用有线网络：
- 有线网络比 WiFi 更稳定快速

### 上传失败

**错误信息**：
```
ERROR: Upload failed
ERROR: Network error
ERROR: 500 Internal Server Error
```

**解决方案**：

1. 启用自动重试：
```yaml
upload_config:
  retry_times: 3
  retry_interval: 300
```

2. 检查视频文件：
```bash
# 验证视频文件完整性
ffmpeg -v error -i video.mp4 -f null -

# 如果有错误，尝试修复
ffmpeg -i video.mp4 -c copy fixed.mp4
```

3. 检查文件大小：
- B 站单个视频限制 8GB
- 如果超过限制，需要分割：
```bash
ffmpeg -i large.mp4 -c copy -f segment -segment_time 3600 output%03d.mp4
```

4. 检查网络连接：
```bash
# 测试 B 站 API 连接
curl -I https://member.bilibili.com/preupload
```

### 视频审核不通过

**症状**：
- 视频上传成功但无法发布
- 收到审核不通过通知

**常见原因**：
1. 标题、标签包含违规词汇
2. 内容违反社区规范
3. 版权问题
4. 分区选择错误

**解决方案**：

1. 检查标题和标签：
- 避免使用敏感词汇
- 不要使用误导性标题
- 标签要与内容相关

2. 确认版权：
```yaml
upload_config:
  copyright: 2  # 转载内容
  source: "原视频地址"  # 标注来源
```

3. 选择正确分区：
- 查看 B 站分区规则
- 参考类似视频的分区

4. 内容自查：
- 确保内容符合 B 站社区规范
- 避免低俗、暴力、违法内容

### 上传后找不到视频

**可能原因**：
1. 视频在审核中
2. 设置了定时发布
3. 视频被设为私密

**解决方案**：

1. 登录 B 站查看投稿管理：
- 打开 https://member.bilibili.com/platform/upload-manager/article
- 查看视频状态

2. 检查是否设置了定时发布：
```yaml
upload_config:
  dtime: "2025-01-10 20:00:00"  # 检查此配置
```

3. 等待审核：
- 通常几分钟到几小时
- 高峰期可能更长

## 配置问题

### YAML 语法错误

**错误信息**：
```
ERROR: Invalid YAML syntax
ERROR: mapping values are not allowed here
```

**常见错误**：

1. 缩进错误（必须使用空格，不能用 Tab）：
```yaml
# 错误
streamers:
	主播名称:  # 使用了 Tab

# 正确
streamers:
  主播名称:  # 使用空格
```

2. 冒号后缺少空格：
```yaml
# 错误
title:"视频标题"

# 正确
title: "视频标题"
```

3. 字符串包含特殊字符未加引号：
```yaml
# 错误
title: 主播的直播: 游戏实况

# 正确
title: "主播的直播: 游戏实况"
```

**解决方案**：

使用在线 YAML 验证工具：
- https://www.yamllint.com/
- 复制配置文件内容进行验证

或使用命令行工具：
```bash
# 安装 yamllint
pip install yamllint

# 验证配置文件
yamllint config.yaml
```

### 配置不生效

**症状**：
- 修改配置后没有变化
- 使用了默认值而不是配置的值

**可能原因**：
1. 配置文件路径错误
2. 配置文件未保存
3. 使用了错误的配置项名称

**解决方案**：

1. 确认配置文件位置：
```bash
# 查看当前使用的配置文件
biliup config show

# 指定配置文件
biliup --config /path/to/config.yaml server
```

2. 验证配置已加载：
```bash
# 显示当前配置
biliup config dump
```

3. 检查配置项名称：
- 参考官方文档
- 查看示例配置文件

### 路径配置问题

**错误信息**：
```
ERROR: No such file or directory
ERROR: Permission denied
```

**解决方案**：

1. 使用绝对路径：
```yaml
# Linux/macOS
download_dir: "/home/user/recordings"

# Windows
download_dir: "D:/recordings"
```

2. 确保目录存在：
```bash
# 创建目录
mkdir -p /path/to/recordings
```

3. 检查权限：
```bash
# 检查目录权限
ls -la /path/to/recordings

# 修改权限
chmod 755 /path/to/recordings
```

4. Windows 路径注意事项：
```yaml
# 使用正斜杠
download_dir: "D:/recordings"

# 或使用双反斜杠
download_dir: "D:\\recordings"
```

## WebUI 问题

### 无法访问 WebUI

**症状**：
- 浏览器无法打开 http://localhost:19159
- 连接被拒绝

**解决方案**：

1. 检查服务是否运行：
```bash
# 查看进程
ps aux | grep biliup

# 或
pgrep -f biliup
```

2. 检查端口占用：
```bash
# macOS/Linux
lsof -i :19159

# 或
netstat -an | grep 19159
```

3. 更换端口：
```bash
biliup --port 8080 server
```

4. 检查防火墙：
```bash
# macOS
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate

# Linux (ufw)
sudo ufw status
```

5. 远程访问配置：
```bash
# 允许外部访问
biliup --host 0.0.0.0 server
```

### WebUI 加载缓慢

**可能原因**：
- 任务过多
- 日志文件过大
- 系统资源不足

**解决方案**：

1. 清理旧任务：
- 在 WebUI 中删除已完成的任务

2. 清理日志：
```bash
# 备份并清空日志
mv biliup.log biliup.log.old
touch biliup.log
```

3. 限制日志大小：
```yaml
logging:
  max_size: "10M"
  max_files: 5
```

### WebUI 操作无响应

**症状**：
- 点击按钮无反应
- 页面卡死

**解决方案**：

1. 刷新页面（Ctrl+F5 强制刷新）

2. 清除浏览器缓存

3. 检查浏览器控制台错误：
- 按 F12 打开开发者工具
- 查看 Console 标签页

4. 重启 biliup 服务：
```bash
# 停止服务
pkill -f biliup

# 重新启动
biliup server
```

## 性能问题

### CPU 占用过高

**可能原因**：
- 同时录制过多直播
- 视频转码
- 并发上传过多

**解决方案**：

1. 限制并发录制：
```yaml
global:
  max_concurrent_downloads: 3
```

2. 禁用转码：
```yaml
upload_config:
  transcode: false
```

3. 降低录制画质：
```yaml
streamers:
  主播名称:
    quality: "720p"
```

4. 限制上传并发：
```yaml
global:
  max_concurrent_uploads: 1
```

### 内存占用过高

**可能原因**：
- 缓冲区设置过大
- 内存泄漏
- 同时处理大文件

**解决方案**：

1. 减小缓冲区：
```yaml
streamers:
  主播名称:
    buffer_size: "1M"
```

2. 启用文件分段：
```yaml
streamers:
  主播名称:
    segment_size: "1G"
```

3. 重启服务释放内存：
```bash
pkill -f biliup
biliup server
```

### 磁盘空间不足

**错误信息**：
```
ERROR: No space left on device
```

**解决方案**：

1. 清理已上传的文件：
```yaml
upload_config:
  delete_after_upload: true
```

2. 启用边录边传：
```yaml
streamers:
  主播名称:
    upload_while_recording: true
    delete_after_upload: true
```

3. 更换存储位置：
```yaml
global:
  download_dir: "/path/to/larger/disk"
```

4. 定期清理：
```bash
# 查找大文件
find /path/to/recordings -type f -size +1G

# 删除旧文件（30 天前）
find /path/to/recordings -type f -mtime +30 -delete
```


## 日志文件

### 日志位置

默认日志文件位置：

```
biliup.log
```

或在配置文件中指定：

```yaml
logging:
  file: "/path/to/biliup.log"
```

### 查看日志

**实时查看日志**：
```bash
tail -f biliup.log
```

**查看最后 100 行**：
```bash
tail -n 100 biliup.log
```

**查看特定时间的日志**：
```bash
# 查看今天的日志
grep "2025-01-10" biliup.log

# 查看最近 1 小时的日志
grep "$(date -d '1 hour ago' '+%Y-%m-%d %H')" biliup.log
```

**按级别过滤**：
```bash
# 只看错误
grep "ERROR" biliup.log

# 只看警告
grep "WARN" biliup.log

# 只看信息
grep "INFO" biliup.log
```

**按功能过滤**：
```bash
# 录制相关
grep "record" biliup.log

# 上传相关
grep "upload" biliup.log

# 特定主播
grep "主播名称" biliup.log
```

### 日志级别

配置日志详细程度：

```yaml
logging:
  level: "INFO"  # DEBUG, INFO, WARN, ERROR
```

**级别说明**：
- **DEBUG**：最详细，包含调试信息
- **INFO**：正常信息，推荐日常使用
- **WARN**：警告信息
- **ERROR**：只记录错误

**调试时使用 DEBUG 级别**：
```yaml
logging:
  level: "DEBUG"
```

### 日志轮转

防止日志文件过大：

```yaml
logging:
  max_size: "10M"      # 单个日志文件最大 10MB
  max_files: 5         # 保留最近 5 个日志文件
  compress: true       # 压缩旧日志
```

### 常见日志信息

**正常运行**：
```
INFO: Server started on http://0.0.0.0:19159
INFO: Checking stream: 主播名称
INFO: Stream is live, start recording
INFO: Recording saved: video.flv
INFO: Upload started: video.flv
INFO: Upload completed: BV1xx411c7mD
```

**录制问题**：
```
WARN: Stream is offline
ERROR: Failed to get stream url: 404 Not Found
ERROR: Connection timeout
ERROR: Disk space insufficient
```

**上传问题**：
```
ERROR: Login required
ERROR: Upload failed: Network error
ERROR: Video file corrupted
WARN: Upload speed is slow
```

## 调试录制失败

### 步骤 1：验证直播间地址

```bash
# 在浏览器中打开直播间
# 确认地址正确且主播正在直播
```

### 步骤 2：测试直播流获取

```bash
# 使用 biliup 测试
biliup test "直播间URL"
```

这会显示：
- 直播间状态（开播/未开播）
- 可用画质
- 直播流地址

### 步骤 3：手动录制测试

```bash
# 使用 FFmpeg 直接录制
ffmpeg -i "直播流地址" -c copy test.flv
```

如果 FFmpeg 能录制，说明直播流没问题，检查 biliup 配置。

### 步骤 4：检查网络

```bash
# 测试直播平台连接
curl -I "直播间URL"

# 测试 DNS 解析
nslookup live.bilibili.com

# 测试网络延迟
ping live.bilibili.com
```

### 步骤 5：查看详细日志

```bash
# 启用 DEBUG 日志
biliup --log-level DEBUG server

# 查看日志
tail -f biliup.log
```

### 步骤 6：尝试不同配置

```yaml
streamers:
  主播名称:
    url: ["直播间URL"]
    format: "flv"        # 尝试不同格式
    quality: "720p"      # 降低画质
    timeout: 60          # 增加超时
    retry_times: 5       # 增加重试
```

## 调试上传失败

### 步骤 1：验证登录状态

```bash
# 检查 Cookie 是否有效
biliup renew

# 如果失败，重新登录
biliup login
```

### 步骤 2：检查视频文件

```bash
# 验证视频文件完整性
ffmpeg -v error -i video.mp4 -f null -

# 查看视频信息
ffmpeg -i video.mp4
```

### 步骤 3：测试上传

```bash
# 使用小文件测试上传
biliup upload test.mp4 --title "测试" --tid 171
```

### 步骤 4：尝试不同线路

```bash
# 测试 upos 线路
biliup upload video.mp4 --line upos --title "测试" --tid 171

# 测试 bupfetch 线路
biliup upload video.mp4 --line bupfetch --title "测试" --tid 171
```

### 步骤 5：检查网络上传速度

```bash
# 使用 speedtest 测试
speedtest-cli

# 或上传小文件测试
curl -T test.txt https://httpbin.org/post
```

### 步骤 6：查看上传日志

```bash
# 查看上传相关日志
grep "upload" biliup.log

# 查看错误信息
grep "ERROR.*upload" biliup.log
```

## 报告 Bug

如果以上方法都无法解决问题，可以报告 Bug。

### 报告前的准备

1. **确认使用最新版本**：
```bash
pip install --upgrade biliup
biliup --version
```

2. **收集信息**：
- 操作系统和版本
- Python 版本
- biliup 版本
- 完整的错误信息
- 相关配置（隐藏敏感信息）

3. **重现问题**：
- 记录重现步骤
- 确认问题可以稳定重现

4. **收集日志**：
```bash
# 启用 DEBUG 日志重现问题
biliup --log-level DEBUG server

# 保存相关日志
grep "ERROR" biliup.log > error.log
```

### 提交 Bug 报告

访问 GitHub Issues：
https://github.com/biliup/biliup/issues

**Bug 报告模板**：

```markdown
### 问题描述
简要描述遇到的问题

### 环境信息
- 操作系统：macOS 14.0 / Ubuntu 22.04 / Windows 11
- Python 版本：3.11.0
- biliup 版本：0.4.0

### 重现步骤
1. 第一步
2. 第二步
3. 第三步

### 预期行为
描述你期望发生什么

### 实际行为
描述实际发生了什么

### 错误信息
```
粘贴完整的错误信息和相关日志
```

### 配置文件（隐藏敏感信息）
```yaml
粘贴相关配置
```

### 其他信息
其他可能有帮助的信息
```

### 敏感信息处理

提交前务必隐藏：
- Cookie 内容
- 账号密码
- 个人信息
- API 密钥

## 获取帮助

### 官方文档

- **GitHub 仓库**：https://github.com/biliup/biliup
- **Wiki 文档**：https://github.com/biliup/biliup/wiki
- **更新日志**：https://github.com/biliup/biliup/releases

### 社区支持

- **GitHub Issues**：报告 Bug 和功能请求
- **GitHub Discussions**：讨论和交流
- **QQ 群**：加入用户交流群（群号见 GitHub README）

### 常见问题 FAQ

**Q: biliup 是否支持 XX 平台？**

A: 查看[平台支持文档](./platform-support.md)了解所有支持的平台。

**Q: 录制的视频可以自动剪辑吗？**

A: biliup 主要负责录制和上传，复杂的剪辑建议使用专业视频编辑软件。

**Q: 可以同时上传到多个平台吗？**

A: 目前只支持上传到 B 站，其他平台需要使用其他工具。

**Q: 录制会被主播发现吗？**

A: 不会。biliup 只是获取公开的直播流，不会在直播间留下任何痕迹。

**Q: 可以录制会员专属直播吗？**

A: 可以，需要配置对应平台的会员 Cookie。

**Q: 上传会消耗主播的流量吗？**

A: 不会。上传使用的是你自己的网络，与主播无关。

**Q: 可以商用吗？**

A: biliup 是开源软件，遵循 GPL-3.0 协议。商用需遵守协议条款。

**Q: 录制的视频版权归谁？**

A: 直播内容版权归主播所有。录制和上传需遵守平台规则和法律法规。

## 预防性维护

### 定期检查

建议定期执行以下检查：

**每周**：
```bash
# 检查磁盘空间
df -h

# 清理旧日志
find . -name "*.log.*" -mtime +7 -delete

# 检查更新
pip list --outdated | grep biliup
```

**每月**：
```bash
# 更新 biliup
pip install --upgrade biliup

# 刷新登录
biliup renew

# 备份配置
cp config.yaml config.yaml.backup
```

### 监控建议

设置监控脚本：

```bash
#!/bin/bash
# monitor.sh

# 检查进程
if ! pgrep -f biliup > /dev/null; then
    echo "biliup is not running, restarting..."
    biliup server &
fi

# 检查磁盘空间
DISK_USAGE=$(df -h /path/to/recordings | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 90 ]; then
    echo "Disk usage is high: ${DISK_USAGE}%"
    # 发送通知或清理文件
fi

# 检查日志错误
ERROR_COUNT=$(grep -c "ERROR" biliup.log)
if [ $ERROR_COUNT -gt 10 ]; then
    echo "Too many errors in log: ${ERROR_COUNT}"
    # 发送通知
fi
```

添加到 crontab：
```bash
# 每小时检查一次
0 * * * * /path/to/monitor.sh
```

### 备份策略

**配置文件备份**：
```bash
# 每次修改后备份
cp config.yaml config.yaml.$(date +%Y%m%d)
```

**重要录像备份**：
```bash
# 定期备份到其他位置
rsync -av /path/to/recordings/ /backup/recordings/
```

**Cookie 备份**：
```bash
# 备份登录信息
cp cookies.json cookies.json.backup
```

## 性能优化建议

### 硬件优化

1. **使用 SSD**：提高文件读写速度
2. **增加内存**：支持更多并发任务
3. **有线网络**：比 WiFi 更稳定
4. **独立磁盘**：录制和系统分开

### 软件优化

1. **使用 FLV 格式**：最稳定高效
2. **合理设置并发**：根据硬件配置
3. **启用文件分段**：避免单文件过大
4. **定期清理**：释放磁盘空间

### 网络优化

1. **使用代理**：某些平台可能需要
2. **选择合适线路**：测试不同上传线路
3. **避开高峰期**：深夜上传更快
4. **限制带宽**：避免影响其他应用

## 下一步

- [直播录制功能](./recording-streams.md) - 了解录制配置
- [视频上传功能](./uploading-videos.md) - 了解上传配置
- [平台支持](./platform-support.md) - 查看支持的平台
- [任务管理](./managing-tasks.md) - 了解任务管理

---

如果本文档未能解决你的问题，欢迎在 [GitHub Issues](https://github.com/biliup/biliup/issues) 提问或报告 Bug。
