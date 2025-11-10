# 设计文档

## 概述

本设计文档详细规划了 biliup 项目中文文档的整体架构、内容组织、文档结构和实施方案。文档系统将基于现有的 Zola 静态站点生成器，通过系统化的内容规划和清晰的导航结构，为用户提供从入门到进阶的完整学习路径。

### 设计目标

1. **完整性**: 覆盖项目的所有核心功能和使用场景
2. **易用性**: 提供清晰的导航和搜索功能，帮助用户快速找到所需信息
3. **专业性**: 使用规范的中文语法和统一的文档风格
4. **准确性**: 确保文档内容与代码完全同步
5. **可维护性**: 建立易于更新和扩展的文档结构

### 目标用户

1. **新手用户**: 首次接触 biliup，需要快速上手
2. **普通用户**: 日常使用 biliup 进行直播录制和上传
3. **高级用户**: 需要深入了解系统架构和自定义配置
4. **开发者**: 需要了解代码结构和扩展开发

## 架构设计

### 文档站点架构

```
docs/
├── content/
│   └── docs/
│       ├── getting-started/      # 快速入门
│       ├── user-guide/            # 用户指南（新增）
│       ├── configuration/         # 配置参考（新增）
│       ├── architecture/          # 架构设计（新增）
│       ├── development/           # 开发指南（新增）
│       ├── api-reference/         # API参考（新增）
│       ├── guide/                 # 进阶指南（现有）
│       ├── help/                  # 帮助中心（现有）
│       └── contributing/          # 贡献指南（现有）
├── static/                        # 静态资源
├── templates/                     # 模板文件
└── config.toml                    # Zola配置
```

### 文档层次结构

文档按照用户学习路径分为四个层次：

1. **入门层** (Getting Started): 快速上手，5-10分钟完成首次使用
2. **使用层** (User Guide): 详细的功能使用说明和配置指南
3. **理解层** (Architecture): 深入理解系统架构和设计原理
4. **扩展层** (Development): 开发者文档和API参考


## 组件和接口

### 文档分类详细设计

#### 1. 快速入门 (getting-started/)

**目标**: 帮助新用户在10分钟内完成安装和首次使用

**文件结构**:
```
getting-started/
├── _index.md              # 章节索引
├── introduction.md        # 项目介绍（需更新）
├── quick-start.md         # 快速开始（需更新）
├── installation.md        # 详细安装指南（新增）
└── first-recording.md     # 第一次录制（新增）
```

**内容要点**:
- `introduction.md`: 项目简介、核心功能、适用场景、技术栈概览
- `quick-start.md`: 最简安装步骤、基础配置、启动服务、访问WebUI
- `installation.md`: 各平台详细安装（Windows/Linux/macOS/Docker/源码）
- `first-recording.md`: 配置第一个直播间、开始录制、查看结果

#### 2. 用户指南 (user-guide/) - 新增

**目标**: 提供完整的功能使用说明

**文件结构**:
```
user-guide/
├── _index.md                    # 章节索引
├── web-interface.md             # Web界面使用
├── recording-streams.md         # 直播录制
├── uploading-videos.md          # 视频上传
├── managing-tasks.md            # 任务管理
├── danmaku-recording.md         # 弹幕录制
├── platform-support.md          # 平台支持列表
└── troubleshooting.md           # 常见问题排查
```

**内容要点**:
- Web界面各功能模块说明
- 录制功能详解（多主播、分段录制、格式选择）
- 上传功能详解（线路选择、并发设置、延时发布）
- 任务管理（启动/停止/查看日志）
- 弹幕录制和使用方法
- 支持的直播平台列表和特殊配置

#### 3. 配置参考 (configuration/) - 新增

**目标**: 提供完整的配置文件说明和最佳实践

**文件结构**:
```
configuration/
├── _index.md                    # 章节索引
├── config-file-format.md        # 配置文件格式
├── streamer-config.md           # 主播配置
├── upload-config.md             # 上传配置
├── advanced-config.md           # 高级配置
├── authentication.md            # 认证配置
└── examples.md                  # 配置示例集
```

**内容要点**:
- TOML/YAML 配置文件格式说明
- 所有配置项的详细说明（参数名、类型、默认值、示例）
- 主播配置（URL、标签、分区、标题模板）
- 上传配置（线路、并发、Cookie、代理）
- 高级配置（分段、过滤、事件钩子）
- 多种场景的完整配置示例

#### 4. 架构设计 (architecture/) - 新增

**目标**: 帮助高级用户和开发者理解系统设计

**文件结构**:
```
architecture/
├── _index.md                    # 章节索引
├── overview.md                  # 架构概览
├── frontend.md                  # 前端架构
├── backend.md                   # 后端架构
├── python-engine.md             # Python引擎
├── data-flow.md                 # 数据流设计
├── plugin-system.md             # 插件系统
└── design-decisions.md          # 设计决策
```

**内容要点**:
- 整体架构图（Rust后端 + Python引擎 + Next.js前端）
- 前端技术栈（Next.js、React、Semi UI、TypeScript）
- 后端技术栈（Rust、Axum、SQLite、Tower）
- Python引擎（下载器、上传器、插件系统）
- 数据流和组件交互
- 插件系统设计原理
- 关键设计决策和权衡

#### 5. 开发指南 (development/) - 新增

**目标**: 指导开发者参与项目开发和扩展

**文件结构**:
```
development/
├── _index.md                    # 章节索引
├── setup-dev-environment.md     # 开发环境搭建
├── project-structure.md         # 项目结构
├── building-from-source.md      # 源码编译
├── plugin-development.md        # 插件开发
├── adding-platform-support.md   # 添加平台支持
├── api-integration.md           # API集成
├── testing.md                   # 测试指南
└── debugging.md                 # 调试技巧
```

**内容要点**:
- 开发环境要求和搭建步骤
- 项目目录结构详解
- 前端/后端/Python模块的编译和调试
- 插件开发完整教程
- 如何添加新的直播平台支持
- API开发和集成
- 单元测试和集成测试
- 常见问题调试方法

#### 6. API参考 (api-reference/) - 新增

**目标**: 提供完整的API文档

**文件结构**:
```
api-reference/
├── _index.md                    # 章节索引
├── rest-api.md                  # REST API
├── websocket-api.md             # WebSocket API
├── python-api.md                # Python API
├── cli-reference.md             # 命令行参考
└── error-codes.md               # 错误码说明
```

**内容要点**:
- REST API 完整列表（认证、任务、配置、视频）
- WebSocket API（实时日志、状态推送）
- Python API（作为库使用时的接口）
- CLI 命令完整参考
- 错误码和处理方法


## 数据模型

### 文档元数据结构

每个文档文件使用 Zola 的 front matter 格式，包含以下元数据：

```toml
+++
title = "文档标题"
description = "文档简短描述（用于SEO和搜索）"
date = 2025-01-10T00:00:00+00:00
updated = 2025-01-10T00:00:00+00:00
draft = false
weight = 10                    # 排序权重，数字越小越靠前
sort_by = "weight"
template = "docs/page.html"

[extra]
lead = "文档引导语（显示在标题下方）"
toc = true                     # 是否显示目录
top = false                    # 是否置顶
version = "1.1.22"            # 对应的代码版本
+++
```

### 文档命名规范

1. **文件命名**: 使用小写字母和连字符，如 `quick-start.md`、`plugin-development.md`
2. **特殊文件**: 保留大写的特殊文件名，如 `README.md`、`CHANGELOG.md`
3. **索引文件**: 每个目录包含 `_index.md` 作为章节索引
4. **URL映射**: 文件名直接映射为URL路径，保持简洁和语义化

### 内容组织模式

每个文档页面遵循统一的结构：

```markdown
# 页面标题

## 概述
简要说明本页面的内容和目标

## 前置条件（可选）
列出阅读本文档需要的前置知识或完成的步骤

## 主要内容
### 子章节1
详细内容...

### 子章节2
详细内容...

## 示例
提供实际的使用示例

## 最佳实践（可选）
推荐的使用方法和注意事项

## 常见问题（可选）
针对本主题的常见问题

## 相关链接
- [相关文档1](链接)
- [相关文档2](链接)
```

## 错误处理

### 文档质量检查

建立文档质量检查机制，确保：

1. **语法检查**: 
   - 使用中文标点符号（，。！？）
   - 避免中英文混用时的空格问题
   - 统一术语翻译

2. **链接检查**:
   - 所有内部链接有效
   - 外部链接可访问
   - 图片资源存在

3. **代码示例检查**:
   - 代码语法正确
   - 示例可以实际运行
   - 与当前版本代码一致

4. **结构检查**:
   - 标题层级正确（不跳级）
   - 目录结构清晰
   - 元数据完整

### 过时内容处理

1. **标记废弃**: 在文档顶部添加废弃警告
   ```markdown
   > ⚠️ **已废弃**: 此功能在 v1.2.0 中已废弃，请使用 [新功能](链接) 替代。
   ```

2. **版本说明**: 在功能说明中标注版本信息
   ```markdown
   > 📌 **版本要求**: 此功能需要 v1.1.0 或更高版本
   ```

3. **归档机制**: 将过时文档移至 `archived/` 目录，保留历史参考

### 错误报告机制

在每个文档页面底部提供反馈入口：

```markdown
---

## 文档反馈

发现文档问题？请通过以下方式反馈：
- [提交 Issue](https://github.com/biliup/biliup/issues)
- [编辑此页面](GitHub编辑链接)
```

## 测试策略

### 文档测试方法

1. **构建测试**:
   ```bash
   cd docs
   zola build
   ```
   确保所有文档可以正常构建，无语法错误

2. **链接测试**:
   使用工具检查所有内部和外部链接的有效性

3. **代码示例测试**:
   - 提取文档中的代码示例
   - 在测试环境中执行
   - 验证输出结果

4. **可读性测试**:
   - 邀请新用户阅读文档
   - 收集反馈和改进建议
   - 持续优化表达方式

### 文档审查流程

1. **自我审查**: 作者完成初稿后自我检查
2. **同行审查**: 其他开发者审查技术准确性
3. **用户测试**: 邀请目标用户测试可理解性
4. **最终审核**: 文档维护者进行最终审核

### 持续集成

在 CI/CD 流程中集成文档检查：

```yaml
# 示例 GitHub Actions 工作流
- name: Build Documentation
  run: |
    cd docs
    zola build
    
- name: Check Links
  run: |
    # 使用链接检查工具
    
- name: Validate Code Examples
  run: |
    # 提取并测试代码示例
```


## 文档内容规范

### 中文写作规范

1. **标点符号**:
   - 使用中文标点：，。！？；：""''（）
   - 数字和英文使用半角字符
   - 中英文之间添加空格：`使用 biliup 进行录制`

2. **术语规范**:
   - 首次出现时提供中英文对照：`插件系统（Plugin System）`
   - 保持术语翻译一致性
   - 专有名词保持原文：Bilibili、Twitch、Docker

3. **语气和风格**:
   - 使用第二人称"你"而非"您"
   - 使用主动语态
   - 简洁明了，避免冗长
   - 专业但友好的语气

4. **格式规范**:
   - 代码使用反引号：`biliup server`
   - 文件路径使用反引号：`config.toml`
   - 强调使用加粗：**重要提示**
   - 引用使用引用块：`> 注意事项`

### 代码示例规范

1. **代码块格式**:
   ````markdown
   ```bash
   # 安装 biliup
   pip install biliup
   ```
   ````

2. **注释说明**:
   ```toml
   # 这是注释说明
   [streamers."主播名称"]
   url = ["https://www.twitch.tv/username"]  # 直播间URL
   tags = ["游戏", "娱乐"]                    # 视频标签
   ```

3. **完整示例**:
   - 提供可直接运行的完整代码
   - 包含必要的导入和初始化
   - 说明预期的输出结果

4. **占位符规范**:
   - 使用尖括号：`<your-username>`
   - 使用大写：`YOUR_API_KEY`
   - 在代码后说明需要替换的内容

### 图表和视觉元素

1. **架构图**:
   - 使用 Mermaid 绘制流程图和架构图
   - 保持风格统一
   - 添加中文标注

2. **截图**:
   - 使用高清截图
   - 标注关键区域
   - 保存为 PNG 格式
   - 存放在 `docs/static/images/` 目录

3. **表格**:
   - 用于展示配置项、API参数等结构化信息
   - 保持列宽合理
   - 添加表头说明

示例表格：

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `url` | Array | 必填 | 直播间URL列表 |
| `tags` | Array | `[]` | 视频标签 |
| `format` | String | `"flv"` | 录制格式 |

### 链接规范

1. **内部链接**:
   - 使用相对路径：`[配置指南](../configuration/config-file-format.md)`
   - 链接到具体章节：`[安装步骤](#安装步骤)`

2. **外部链接**:
   - 使用完整URL
   - 优先链接到中文资源
   - 标注外部链接：`[Zola官网](https://www.getzola.org/) (英文)`

3. **参考链接**:
   - 在文档底部统一列出相关链接
   - 分类组织（官方文档、社区资源、相关项目）

## 实施计划

### 阶段一：基础文档更新（优先级：高）

1. 更新现有文档
   - 修正 `getting-started/introduction.md` 的过时内容
   - 完善 `getting-started/quick-start.md` 的安装步骤
   - 更新 `help/faq.md` 为 biliup 相关内容

2. 补充缺失的入门文档
   - 创建详细的安装指南
   - 创建第一次使用教程

### 阶段二：用户指南编写（优先级：高）

1. 创建 `user-guide/` 目录结构
2. 编写核心功能使用文档
   - Web界面使用
   - 直播录制功能
   - 视频上传功能
   - 任务管理

### 阶段三：配置参考编写（优先级：中）

1. 创建 `configuration/` 目录结构
2. 编写完整的配置文档
   - 配置文件格式说明
   - 所有配置项详解
   - 配置示例集合

### 阶段四：架构和开发文档（优先级：中）

1. 创建 `architecture/` 目录结构
2. 编写架构设计文档
3. 创建 `development/` 目录结构
4. 编写开发者指南

### 阶段五：API参考和完善（优先级：低）

1. 创建 `api-reference/` 目录结构
2. 编写 API 文档
3. 完善所有文档的交叉引用
4. 添加搜索优化

### 文档维护机制

1. **版本同步**:
   - 每次代码发布时检查文档更新
   - 在 CHANGELOG 中记录文档变更

2. **定期审查**:
   - 每季度审查一次文档准确性
   - 更新过时的截图和示例

3. **社区贡献**:
   - 鼓励用户提交文档改进
   - 建立文档贡献指南
   - 及时处理文档相关的 Issue

## 技术实现细节

### Zola 配置优化

在 `docs/config.toml` 中配置：

```toml
base_url = "https://docs.biliup.rs"
title = "biliup 文档"
description = "biliup 自动录制和上传工具的完整文档"
default_language = "zh"

[markdown]
highlight_code = true
highlight_theme = "base16-ocean-dark"
render_emoji = true
external_links_target_blank = true
external_links_no_follow = true
external_links_no_referrer = true

[search]
include_title = true
include_description = true
include_content = true
```

### 搜索功能增强

1. 配置中文分词支持
2. 优化搜索索引
3. 添加搜索结果高亮
4. 提供搜索建议

### 导航结构设计

```
顶部导航:
- 快速入门
- 用户指南
- 配置参考
- 架构设计
- 开发指南
- API参考
- 帮助中心

侧边栏:
- 当前章节的目录树
- 展开/折叠功能
- 高亮当前页面

底部导航:
- 上一页/下一页
- 编辑此页面
- 反馈问题
```

### 响应式设计

确保文档在不同设备上的可读性：

1. **桌面端**: 三栏布局（导航-内容-目录）
2. **平板**: 两栏布局（导航-内容）
3. **移动端**: 单栏布局，汉堡菜单

## 成功指标

### 文档质量指标

1. **完整性**: 覆盖所有核心功能和API
2. **准确性**: 代码示例可运行，配置说明正确
3. **可读性**: 新用户能在30分钟内完成首次使用
4. **可维护性**: 文档更新时间不超过代码发布后1周

### 用户反馈指标

1. **搜索成功率**: 用户能通过搜索找到所需信息
2. **文档评分**: 每个页面的有用性评分
3. **Issue数量**: 文档相关的Issue数量下降
4. **社区贡献**: 文档PR数量增加

## 总结

本设计文档提供了一个完整的文档系统架构，包括：

1. **清晰的文档层次**: 从入门到进阶的四层结构
2. **完整的内容规划**: 涵盖使用、配置、架构、开发等各个方面
3. **统一的规范标准**: 中文写作、代码示例、格式规范
4. **可执行的实施计划**: 分阶段推进，优先级明确
5. **持续的维护机制**: 确保文档长期保持准确和最新

通过实施这个设计，biliup 项目将拥有一套专业、完整、易用的中文文档系统，大大降低用户的学习成本，提升项目的可用性和社区活跃度。
