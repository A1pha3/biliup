+++
title = "如何贡献"
description = "为 biliup 项目贡献代码、改进文档或提交功能建议"
date = 2021-05-01T18:10:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 410
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "欢迎为 biliup 项目做出贡献！本指南将帮助你了解如何参与项目开发。"
toc = true
top = false
+++

👉 在开始贡献之前，请务必阅读 [行为准则](../code-of-conduct/)。

## 贡献方式

你可以通过以下方式为 biliup 项目做出贡献：

- 报告 Bug 和问题
- 提交功能请求和改进建议
- 贡献代码（修复 Bug、实现新功能）
- 改进文档
- 帮助其他用户解决问题
- 分享使用经验和最佳实践

## 报告 Bug

如果你在使用 biliup 时遇到问题，欢迎提交 Bug 报告。

### 提交前的检查

在提交 Bug 报告之前，请先：

1. **搜索现有 Issues**：检查问题是否已被报告
2. **更新到最新版本**：确认问题在最新版本中仍然存在
3. **查看文档**：确认不是配置或使用方法的问题
4. **查看 FAQ**：检查 [常见问题](../../help/faq/) 中是否有解决方案

### 如何提交 Bug 报告

访问 [GitHub Issues](https://github.com/biliup/biliup/issues/new) 创建新的 Issue，并提供以下信息：

**必需信息**：

- **问题描述**：清晰描述遇到的问题
- **复现步骤**：详细说明如何重现问题
- **预期行为**：说明你期望的正确行为
- **实际行为**：说明实际发生的情况
- **环境信息**：
  - 操作系统和版本
  - Python 版本
  - biliup 版本
  - 相关依赖版本

**可选但有帮助的信息**：

- 错误日志和堆栈跟踪
- 配置文件（删除敏感信息）
- 截图或录屏
- 相关的代码片段

**示例**：

```markdown
## 问题描述
录制 Twitch 直播时，程序在 10 分钟后自动停止

## 复现步骤
1. 配置 Twitch 直播间 URL
2. 启动 biliup 服务
3. 等待约 10 分钟
4. 程序自动停止录制

## 预期行为
应该持续录制直到直播结束

## 实际行为
10 分钟后自动停止，日志显示连接超时

## 环境信息
- 操作系统：Ubuntu 22.04
- Python 版本：3.10.12
- biliup 版本：1.1.22
- 网络环境：国内

## 日志
[附上相关日志内容]
```

## 提交功能请求

我们欢迎新功能的建议和改进意见。

### 提交前的思考

在提交功能请求之前，请考虑：

1. **功能的必要性**：这个功能对多少用户有用？
2. **现有替代方案**：是否可以通过现有功能组合实现？
3. **实现的可行性**：技术上是否可行？
4. **维护成本**：功能是否会增加过多的复杂度？

### 如何提交功能请求

访问 [GitHub Issues](https://github.com/biliup/biliup/issues/new) 创建新的 Issue，并提供以下信息：

- **功能描述**：清晰描述建议的功能
- **使用场景**：说明什么情况下需要这个功能
- **预期效果**：说明功能应该如何工作
- **替代方案**：是否考虑过其他实现方式
- **额外信息**：相关的参考资料、示例等

**示例**：

```markdown
## 功能描述
支持录制后自动转码为 H.265 格式

## 使用场景
录制高清直播时，文件体积很大，希望能自动转码压缩

## 预期效果
在配置文件中添加 transcode 选项，录制完成后自动转码

## 替代方案
目前需要手动使用 FFmpeg 转码

## 额外信息
可以参考 FFmpeg 的 H.265 编码参数
```

## 贡献代码

欢迎提交代码贡献！无论是修复 Bug 还是实现新功能，我们都非常感谢。

### 开发环境搭建

1. **Fork 仓库**：在 GitHub 上 Fork [biliup 仓库](https://github.com/biliup/biliup)

2. **克隆代码**：
   ```bash
   git clone https://github.com/your-username/biliup.git
   cd biliup
   ```

3. **安装依赖**：
   ```bash
   # 安装 Python 依赖
   pip install -e ".[dev]"
   
   # 安装前端依赖
   npm install
   
   # 安装 Rust 工具链（如需修改 Rust 代码）
   curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
   ```

详细的开发环境搭建步骤请参考 [开发环境搭建](../../development/setup-dev-environment/)。

### 开发流程

1. **创建分支**：
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **编写代码**：
   - 遵循项目的代码风格
   - 添加必要的注释
   - 确保代码可读性

3. **测试代码**：
   ```bash
   # 运行测试
   pytest
   
   # 检查代码风格
   flake8
   black --check .
   ```

4. **提交更改**：
   ```bash
   git add .
   git commit -m "feat: add new feature"
   ```
   
   提交信息请遵循 [约定式提交规范](https://www.conventionalcommits.org/zh-hans/)：
   - `feat:` 新功能
   - `fix:` Bug 修复
   - `docs:` 文档更新
   - `style:` 代码格式调整
   - `refactor:` 代码重构
   - `test:` 测试相关
   - `chore:` 构建或辅助工具变动

5. **推送分支**：
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建 Pull Request**：
   - 访问 GitHub 仓库页面
   - 点击 "New Pull Request"
   - 填写 PR 描述，说明更改内容
   - 等待代码审查

### 代码规范

**Python 代码**：

- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 [Black](https://github.com/psf/black) 格式化代码
- 使用类型注解（Type Hints）
- 编写文档字符串（Docstrings）

**Rust 代码**：

- 遵循 [Rust 官方风格指南](https://doc.rust-lang.org/1.0.0/style/)
- 使用 `rustfmt` 格式化代码
- 使用 `clippy` 检查代码质量

**JavaScript/TypeScript 代码**：

- 遵循项目的 ESLint 配置
- 使用 Prettier 格式化代码
- 使用 TypeScript 类型系统

### Pull Request 指南

一个好的 Pull Request 应该：

- **单一职责**：一个 PR 只做一件事
- **清晰的描述**：说明更改的内容和原因
- **完整的测试**：包含必要的测试用例
- **更新文档**：如果更改了 API 或功能，更新相关文档
- **通过 CI 检查**：确保所有自动化测试通过

**PR 描述模板**：

```markdown
## 更改内容
简要描述这个 PR 的更改内容

## 相关 Issue
Closes #123

## 更改类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 测试
说明如何测试这些更改

## 截图（如适用）
添加相关截图

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已添加必要的测试
- [ ] 已更新相关文档
- [ ] 所有测试通过
- [ ] 已自我审查代码
```

## 改进文档

文档是项目的重要组成部分，我们欢迎文档方面的贡献。

### 文档类型

你可以贡献以下类型的文档：

- **用户文档**：使用指南、配置说明、常见问题
- **开发文档**：架构设计、API 文档、开发指南
- **教程**：入门教程、最佳实践、案例分享
- **翻译**：将文档翻译成其他语言

### 文档规范

- 使用清晰、简洁的中文表达
- 遵循 [文档写作规范](../../development/project-structure/)
- 提供实际可运行的代码示例
- 添加必要的截图和图表
- 保持文档与代码同步

### 提交文档更改

文档源文件位于 `docs/content/docs/` 目录：

1. Fork 并克隆仓库
2. 编辑或创建 Markdown 文件
3. 本地预览：`cd docs && zola serve`
4. 提交 Pull Request

详细的文档贡献指南请参考 [项目结构](../../development/project-structure/)。

## 帮助其他用户

你也可以通过以下方式帮助社区：

- **回答问题**：在 GitHub Issues 和 Discussions 中帮助其他用户
- **分享经验**：撰写博客文章、录制视频教程
- **改进示例**：提供更多配置示例和使用场景
- **测试功能**：测试新版本并提供反馈

## 行为准则

所有贡献者都应遵守项目的 [行为准则](../code-of-conduct/)。我们致力于营造一个友好、包容、尊重的社区环境。

## 许可证

通过向 biliup 项目提交贡献，你同意你的贡献将按照项目的许可证（MIT License）进行授权。

## 获取帮助

如果你在贡献过程中遇到问题，可以：

- 在 [GitHub Discussions](https://github.com/biliup/biliup/discussions) 提问
- 加入 QQ 群交流
- 查看 [开发指南](../../development/) 获取更多信息

## 致谢

感谢所有为 biliup 项目做出贡献的开发者和用户！你们的贡献让这个项目变得更好。

查看 [贡献者列表](https://github.com/biliup/biliup/graphs/contributors) 了解所有贡献者。
