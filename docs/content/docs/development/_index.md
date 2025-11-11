+++
title = "开发指南"
description = "biliup 项目开发指南，包含开发环境搭建、项目结构、插件开发等内容"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 50
sort_by = "weight"
template = "docs/section.html"

[extra]
lead = "本章节为开发者提供完整的开发指南，包括环境搭建、项目结构、插件开发、测试和调试等内容，帮助你参与 biliup 项目的开发和扩展。"
toc = true
top = false
+++

## 开发指南概览

biliup 是一个混合架构的项目，包含 Rust 后端、Python 引擎和 Next.js 前端。本章节将指导你：

- **搭建开发环境**: 配置必需的开发工具和依赖
- **理解项目结构**: 了解代码组织和模块划分
- **编译和构建**: 从源码构建各个组件
- **开发插件**: 扩展支持新的直播平台
- **集成 API**: 添加新的后端接口
- **测试和调试**: 确保代码质量

## 开始之前

在开始开发之前，建议你：

1. 阅读[架构设计](../architecture/)章节，了解系统整体架构
2. 熟悉 Rust、Python 和 TypeScript/React 的基础知识
3. 了解直播协议和视频处理的基本概念

## 开发流程

典型的开发流程包括：

1. **Fork 和克隆**: Fork 项目仓库并克隆到本地
2. **搭建环境**: 安装必需的开发工具和依赖
3. **创建分支**: 为你的功能或修复创建新分支
4. **编写代码**: 实现功能并编写测试
5. **测试验证**: 运行测试确保代码正常工作
6. **提交 PR**: 提交 Pull Request 并等待审查

## 贡献指南

在开始开发之前，请阅读[贡献指南](../contributing/how-to-contribute.md)了解：

- 代码风格规范
- 提交信息格式
- Pull Request 流程
- 社区行为准则

## 获取帮助

如果在开发过程中遇到问题：

- 查看[常见问题](../help/faq.md)
- 在 [GitHub Issues](https://github.com/biliup/biliup/issues) 提问
- 加入社区讨论
