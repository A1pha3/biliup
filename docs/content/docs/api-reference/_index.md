+++
title = "API 参考"
description = "biliup 的完整 API 参考文档，包括 REST API、WebSocket API、Python API 和 CLI 命令"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 60
sort_by = "weight"
template = "docs/section.html"

[extra]
lead = "完整的 API 参考文档，帮助你集成和扩展 biliup"
toc = true
top = false
+++

本章节提供 biliup 的完整 API 参考文档，涵盖所有可用的接口和命令。

## 内容概览

### REST API
详细的 HTTP API 文档，包括认证、任务管理、配置管理和视频管理等接口。适用于需要通过 HTTP 接口集成 biliup 的场景。

### WebSocket API
实时通信接口文档，用于接收日志推送和任务状态更新。适用于需要实时监控任务状态的应用。

### Python API
将 biliup 作为 Python 库使用的接口文档。适用于需要在 Python 项目中集成录制和上传功能的场景。

### CLI 参考
命令行工具的完整参考文档，包括所有命令和选项的详细说明。适用于通过命令行使用 biliup 的场景。

### 错误码
所有可能的错误码及其含义和处理方法。帮助你快速定位和解决问题。

## 使用场景

- **Web 应用集成**: 使用 REST API 和 WebSocket API
- **Python 项目集成**: 使用 Python API
- **命令行使用**: 使用 CLI 命令
- **自动化脚本**: 结合 CLI 和 Python API
- **故障排查**: 参考错误码文档

## 认证说明

大部分 API 需要认证才能访问。biliup 支持以下认证方式：

1. **会话认证**: 通过 Web 界面登录后使用 Cookie
2. **配置文件**: 在配置文件中设置 B 站 Cookie
3. **命令行登录**: 使用 `biliup login` 命令登录

详细的认证配置方法请参考 [认证配置文档](../configuration/authentication.md)。

## 版本说明

本文档对应 biliup v1.1.22 及以上版本。不同版本的 API 可能存在差异，请以实际版本为准。
