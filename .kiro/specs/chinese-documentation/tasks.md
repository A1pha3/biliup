# 实施计划

本文档列出了完善 biliup 中文文档的所有实施任务。任务按照优先级和依赖关系组织，每个任务都包含具体的实施步骤和验收标准。

## 任务列表

- [x] 1. 更新和完善快速入门文档
  - 更新现有的入门文档，修正过时内容，补充缺失信息
  - _需求: 1.1, 1.2, 1.3, 3.1, 3.2, 4.1_

- [x] 1.1 更新项目介绍文档
  - 修改 `docs/content/docs/getting-started/introduction.md`
  - 更新项目简介，准确描述当前版本的核心功能
  - 更新技术栈说明（Rust + Python + Next.js）
  - 移除过时的安装说明，链接到详细安装指南
  - 添加适用场景和用户群体说明
  - _需求: 1.1, 3.1, 4.1_

- [x] 1.2 完善快速开始文档
  - 修改 `docs/content/docs/getting-started/quick-start.md`
  - 更新 Python 版本要求为 3.9+（与 pyproject.toml 一致）
  - 简化快速开始步骤，聚焦最简安装路径
  - 添加 Windows、Linux、macOS 三个平台的快速安装命令
  - 添加首次启动和访问 WebUI 的说明
  - 提供简单的配置示例和预期结果
  - _需求: 1.1, 1.2, 3.1, 4.1_

- [x] 1.3 创建详细安装指南
  - 创建 `docs/content/docs/getting-started/installation.md`
  - 编写 Windows 平台详细安装步骤（exe 下载、环境配置）
  - 编写 Linux 平台详细安装步骤（uv 安装、pip 安装、包管理器）
  - 编写 macOS 平台详细安装步骤（uv 安装、Homebrew）
  - 编写 Docker 安装和使用指南（镜像拉取、容器配置、数据持久化）
  - 编写从源码安装的完整步骤（前端构建、后端编译、Python 环境）
  - 添加 Termux 安装说明的链接
  - 添加常见安装问题和解决方案
  - _需求: 1.1, 3.1, 6.1_

- [x] 1.4 创建第一次使用教程
  - 创建 `docs/content/docs/getting-started/first-recording.md`
  - 编写登录 B 站账号的步骤（使用 `biliup login` 命令）
  - 编写创建第一个配置文件的步骤（config.toml 格式）
  - 编写添加第一个直播间的步骤
  - 编写启动服务和访问 WebUI 的步骤
  - 编写开始录制和查看结果的步骤
  - 添加预期输出和成功标志的说明
  - _需求: 1.1, 1.3, 6.1, 6.2_

- [x] 2. 创建用户指南文档
  - 创建完整的用户指南，覆盖所有核心功能的使用方法
  - _需求: 1.2, 1.3, 6.1, 6.2_

- [x] 2.1 创建用户指南目录结构
  - 创建 `docs/content/docs/user-guide/` 目录
  - 创建 `docs/content/docs/user-guide/_index.md` 索引文件
  - 配置章节元数据（标题、描述、权重）
  - _需求: 1.2, 5.1_

- [x] 2.2 编写 Web 界面使用文档
  - 创建 `docs/content/docs/user-guide/web-interface.md`
  - 说明 WebUI 的访问方式和端口配置
  - 介绍主界面的各个功能模块（任务列表、配置管理、日志查看）
  - 添加界面截图和功能说明
  - 说明用户认证功能的使用（--auth 参数）
  - _需求: 1.2, 1.3, 6.1_

- [x] 2.3 编写直播录制功能文档
  - 创建 `docs/content/docs/user-guide/recording-streams.md`
  - 说明支持的直播平台列表
  - 详细说明录制配置项（URL、格式、分段、过滤）
  - 说明多主播同时录制的配置方法
  - 说明录制文件的命名规则和存储位置
  - 说明边录边传功能的使用
  - 添加常见录制场景的配置示例
  - _需求: 1.2, 1.3, 6.2, 6.3_

- [x] 2.4 编写视频上传功能文档
  - 创建 `docs/content/docs/user-guide/uploading-videos.md`
  - 说明 B 站登录和 Cookie 配置方法
  - 详细说明上传配置项（线路选择、并发数、分区、标签）
  - 说明多 P 上传和追加视频的使用方法
  - 说明延时发布功能的配置
  - 说明上传线路选择策略（upos、bupfetch）
  - 添加不同上传场景的配置示例
  - _需求: 1.2, 1.3, 6.2, 6.3_

- [x] 2.5 编写任务管理文档
  - 创建 `docs/content/docs/user-guide/managing-tasks.md`
  - 说明如何启动、停止、重启录制任务
  - 说明如何查看任务状态和日志
  - 说明如何通过 WebUI 管理任务
  - 说明如何通过 CLI 管理任务
  - 说明任务的自动重试机制
  - _需求: 1.2, 1.3, 6.1_

- [x] 2.6 编写弹幕录制文档
  - 创建 `docs/content/docs/user-guide/danmaku-recording.md`
  - 说明弹幕录制功能的启用方法
  - 说明支持弹幕录制的平台列表
  - 说明 XML 弹幕文件的格式和存储位置
  - 提供弹幕文件的使用方法（DanmakuFactory、AList、弹弹play）
  - _需求: 1.2, 1.3, 6.1, 6.4_

- [x] 2.7 编写平台支持文档
  - 创建 `docs/content/docs/user-guide/platform-support.md`
  - 列出所有支持的直播平台（Twitch、斗鱼、虎牙、B站等）
  - 说明每个平台的特殊配置要求
  - 说明平台特定的 Cookie 配置（如 Twitch、快手）
  - 说明平台的已知限制和注意事项
  - _需求: 1.2, 1.3, 6.3_

- [x] 2.8 编写故障排查文档
  - 创建 `docs/content/docs/user-guide/troubleshooting.md`
  - 整理常见错误和解决方案
  - 说明日志文件的位置和查看方法
  - 说明如何调试录制失败问题
  - 说明如何调试上传失败问题
  - 说明如何报告 Bug 和获取帮助
  - _需求: 1.4, 6.1_

- [x] 3. 创建配置参考文档
  - 创建完整的配置参考文档，详细说明所有配置项
  - _需求: 1.2, 3.1, 3.2, 4.1, 6.2_

- [x] 3.1 创建配置参考目录结构
  - 创建 `docs/content/docs/configuration/` 目录
  - 创建 `docs/content/docs/configuration/_index.md` 索引文件
  - 配置章节元数据
  - _需求: 1.2, 5.1_

- [x] 3.2 编写配置文件格式文档
  - 创建 `docs/content/docs/configuration/config-file-format.md`
  - 说明 TOML 和 YAML 两种配置格式
  - 说明配置文件的查找路径和优先级
  - 说明配置文件的基本结构
  - 提供最小化配置示例
  - _需求: 1.2, 3.1, 3.2, 6.1_

- [x] 3.3 编写主播配置文档
  - 创建 `docs/content/docs/configuration/streamer-config.md`
  - 详细说明 `streamers` 配置段的所有选项
  - 说明 URL、tags、format、split_time、split_size 等配置项
  - 说明标题模板和文件名模板的使用
  - 说明分区（tid）的配置和可选值
  - 提供多种场景的配置示例
  - _需求: 1.2, 3.1, 3.2, 6.2, 6.3_

- [x] 3.4 编写上传配置文档
  - 创建 `docs/content/docs/configuration/upload-config.md`
  - 详细说明上传相关的所有配置项
  - 说明线路选择（line）、并发数（limit）的配置
  - 说明视频元信息配置（title、desc、source、dynamic）
  - 说明封面上传和延时发布的配置
  - 提供不同上传策略的配置示例
  - _需求: 1.2, 3.1, 3.2, 6.2, 6.3_

- [x] 3.5 编写高级配置文档
  - 创建 `docs/content/docs/configuration/advanced-config.md`
  - 说明代理配置（proxy）
  - 说明日志配置（rust_log）
  - 说明数据库配置
  - 说明事件钩子配置
  - 说明性能优化相关配置
  - _需求: 1.2, 3.1, 3.2, 6.3_

- [x] 3.6 编写认证配置文档
  - 创建 `docs/content/docs/configuration/authentication.md`
  - 说明 B 站 Cookie 的获取和配置方法
  - 说明 cookies.json 文件的格式和位置
  - 说明使用 biliup-rs 登录的方法
  - 说明 Cookie 过期和刷新的处理
  - 说明多账号配置方法
  - _需求: 1.2, 3.1, 6.1, 6.2_

- [x] 3.7 创建配置示例集
  - 创建 `docs/content/docs/configuration/examples.md`
  - 提供单主播录制的完整配置示例
  - 提供多主播录制的完整配置示例
  - 提供边录边传的配置示例
  - 提供分段录制的配置示例
  - 提供自定义上传参数的配置示例
  - 提供 Docker 环境的配置示例
  - _需求: 1.2, 6.2, 6.3, 6.4, 6.5_

- [x] 4. 创建架构设计文档
  - 创建架构设计文档，帮助高级用户理解系统设计
  - _需求: 2.1, 2.2, 2.3, 2.4_

- [x] 4.1 创建架构文档目录结构
  - 创建 `docs/content/docs/architecture/` 目录
  - 创建 `docs/content/docs/architecture/_index.md` 索引文件
  - 配置章节元数据
  - _需求: 2.1, 5.1_

- [x] 4.2 编写架构概览文档
  - 创建 `docs/content/docs/architecture/overview.md`
  - 使用 Mermaid 绘制整体架构图（参考 README.md 中的架构图）
  - 说明三层架构：前端层、后端层、引擎层
  - 说明各层的职责和技术选型
  - 说明组件之间的通信方式
  - _需求: 2.1, 2.2, 2.5_

- [x] 4.3 编写前端架构文档
  - 创建 `docs/content/docs/architecture/frontend.md`
  - 说明前端技术栈（Next.js、React、TypeScript、Semi UI）
  - 说明前端项目结构和主要组件
  - 说明与后端的 API 交互方式
  - 说明 WebSocket 实时通信的实现
  - _需求: 2.1, 2.2, 2.3_

- [x] 4.4 编写后端架构文档
  - 创建 `docs/content/docs/architecture/backend.md`
  - 说明后端技术栈（Rust、Axum、SQLite、Tower）
  - 说明后端项目结构（biliup、biliup-cli、stream-gears）
  - 说明 REST API 的设计和实现
  - 说明认证和会话管理机制
  - 说明数据库设计和迁移机制
  - _需求: 2.1, 2.2, 2.3_

- [x] 4.5 编写 Python 引擎文档
  - 创建 `docs/content/docs/architecture/python-engine.md`
  - 说明 Python 引擎的职责（下载、上传、任务调度）
  - 说明与 Rust 后端的集成方式（stream-gears）
  - 说明下载器的实现原理
  - 说明上传器的实现原理
  - 说明任务调度和并发控制
  - _需求: 2.1, 2.2, 2.3_

- [x] 4.6 编写数据流设计文档
  - 创建 `docs/content/docs/architecture/data-flow.md`
  - 使用 Mermaid 绘制数据流图
  - 说明录制流程的完整数据流
  - 说明上传流程的完整数据流
  - 说明任务状态的更新流程
  - 说明日志和事件的传递机制
  - _需求: 2.1, 2.3, 2.5_

- [x] 4.7 编写插件系统文档
  - 创建 `docs/content/docs/architecture/plugin-system.md`
  - 说明插件系统的设计原理
  - 说明下载插件的基类和装饰器
  - 说明上传插件的基类和装饰器
  - 说明插件的注册和发现机制
  - 说明事件驱动框架的实现
  - _需求: 2.1, 2.2, 2.4_

- [x] 4.8 编写设计决策文档
  - 创建 `docs/content/docs/architecture/design-decisions.md`
  - 说明为什么选择 Rust + Python 混合架构
  - 说明为什么选择 Zola 作为文档生成器
  - 说明上传线路选择的策略
  - 说明边录边传的设计考虑
  - 说明其他关键技术决策和权衡
  - _需求: 2.1, 2.4_

- [-] 5. 创建开发指南文档
  - 创建开发指南文档，指导开发者参与项目开发
  - _需求: 2.1, 2.2, 2.3, 2.4_

- [x] 5.1 创建开发指南目录结构
  - 创建 `docs/content/docs/development/` 目录
  - 创建 `docs/content/docs/development/_index.md` 索引文件
  - 配置章节元数据
  - _需求: 2.1, 5.1_

- [x] 5.2 编写开发环境搭建文档
  - 创建 `docs/content/docs/development/setup-dev-environment.md`
  - 说明开发环境的系统要求
  - 说明必需的开发工具（Node.js、Rust、Python、uv）
  - 说明如何克隆代码仓库
  - 说明如何安装依赖（前端、后端、Python）
  - 说明如何配置开发环境变量
  - _需求: 2.1, 6.1_

- [x] 5.3 编写项目结构文档
  - 创建 `docs/content/docs/development/project-structure.md`
  - 详细说明项目的目录结构
  - 说明前端代码的组织（pages、components、styles）
  - 说明后端代码的组织（crates、modules）
  - 说明 Python 代码的组织（plugins、engine、common）
  - 说明配置文件和资源文件的位置
  - _需求: 2.1, 2.2_

- [ ] 5.4 编写源码编译文档
  - 创建 `docs/content/docs/development/building-from-source.md`
  - 说明如何编译前端（npm run build）
  - 说明如何编译 Rust 后端（cargo build、maturin dev）
  - 说明如何打包 Python 模块（python -m build）
  - 说明如何运行开发服务器
  - 说明如何构建发布版本
  - _需求: 2.1, 6.1_

- [ ] 5.5 编写插件开发文档
  - 创建 `docs/content/docs/development/plugin-development.md`
  - 说明插件系统的工作原理
  - 提供下载插件开发的完整示例
  - 提供上传插件开发的完整示例
  - 说明插件的测试方法
  - 说明插件的调试技巧
  - _需求: 2.1, 2.4, 6.1, 6.2_

- [ ] 5.6 编写添加平台支持文档
  - 创建 `docs/content/docs/development/adding-platform-support.md`
  - 说明如何分析新平台的直播协议
  - 说明如何实现新平台的下载插件
  - 说明如何处理平台特定的认证和 Cookie
  - 说明如何添加弹幕支持
  - 提供完整的平台添加示例
  - _需求: 2.1, 2.4, 6.1, 6.2_

- [ ] 5.7 编写 API 集成文档
  - 创建 `docs/content/docs/development/api-integration.md`
  - 说明如何添加新的 REST API 端点
  - 说明如何实现 WebSocket 消息处理
  - 说明如何与前端集成
  - 说明 API 的认证和权限控制
  - _需求: 2.1, 2.3, 6.1_

- [ ] 5.8 编写测试指南
  - 创建 `docs/content/docs/development/testing.md`
  - 说明测试框架和工具
  - 说明如何编写单元测试
  - 说明如何编写集成测试
  - 说明如何运行测试套件
  - _需求: 2.1_

- [ ] 5.9 编写调试技巧文档
  - 创建 `docs/content/docs/development/debugging.md`
  - 说明如何调试前端代码（Chrome DevTools）
  - 说明如何调试 Rust 代码（rust-lldb、println!）
  - 说明如何调试 Python 代码（pdb、日志）
  - 说明常见问题的调试方法
  - _需求: 2.1_

- [ ] 6. 创建 API 参考文档
  - 创建完整的 API 参考文档
  - _需求: 1.5, 2.3, 6.1, 6.3_

- [ ] 6.1 创建 API 参考目录结构
  - 创建 `docs/content/docs/api-reference/` 目录
  - 创建 `docs/content/docs/api-reference/_index.md` 索引文件
  - 配置章节元数据
  - _需求: 1.5, 5.1_

- [ ] 6.2 编写 REST API 文档
  - 创建 `docs/content/docs/api-reference/rest-api.md`
  - 列出所有 REST API 端点
  - 详细说明认证 API（登录、登出、会话）
  - 详细说明任务 API（列表、创建、启动、停止、删除）
  - 详细说明配置 API（读取、更新）
  - 详细说明视频 API（列表、详情、上传）
  - 每个 API 提供请求和响应示例
  - _需求: 1.5, 2.3, 6.1, 6.3_

- [ ] 6.3 编写 WebSocket API 文档
  - 创建 `docs/content/docs/api-reference/websocket-api.md`
  - 说明 WebSocket 连接方式
  - 说明实时日志推送的消息格式
  - 说明任务状态推送的消息格式
  - 提供客户端连接示例
  - _需求: 1.5, 2.3, 6.1, 6.3_

- [ ] 6.4 编写 Python API 文档
  - 创建 `docs/content/docs/api-reference/python-api.md`
  - 说明如何将 biliup 作为 Python 库使用
  - 说明上传 API 的使用方法（BiliBili 类）
  - 说明下载 API 的使用方法（download 函数）
  - 提供完整的代码示例
  - _需求: 1.5, 6.1, 6.2_

- [ ] 6.5 编写 CLI 参考文档
  - 创建 `docs/content/docs/api-reference/cli-reference.md`
  - 详细说明所有 CLI 命令和选项
  - 说明 `biliup login` 命令
  - 说明 `biliup upload` 命令及其所有参数
  - 说明 `biliup server` 命令及其所有参数
  - 说明 `biliup download` 命令
  - 说明其他辅助命令（show、list、append 等）
  - 每个命令提供使用示例
  - _需求: 1.5, 6.1, 6.3_

- [ ] 6.6 编写错误码文档
  - 创建 `docs/content/docs/api-reference/error-codes.md`
  - 列出所有可能的错误码
  - 说明每个错误码的含义
  - 说明错误的处理方法
  - 提供常见错误的解决方案
  - _需求: 1.5, 4.4_

- [ ] 7. 更新和完善现有文档
  - 更新现有的帮助和贡献文档
  - _需求: 1.4, 3.1, 3.3, 4.1, 4.4_

- [ ] 7.1 更新 FAQ 文档
  - 修改 `docs/content/docs/help/faq.md`
  - 移除 AdiDoks 相关的内容
  - 添加 biliup 常见问题和解答
  - 添加安装问题、配置问题、录制问题、上传问题的 FAQ
  - 添加性能优化和故障排查的 FAQ
  - _需求: 1.4, 3.1, 4.1_

- [ ] 7.2 更新贡献指南
  - 修改 `docs/content/docs/contributing/how-to-contribute.md`
  - 更新为 biliup 项目的贡献指南
  - 说明如何报告 Bug
  - 说明如何提交功能请求
  - 说明如何提交代码贡献
  - 说明如何提交文档贡献
  - _需求: 3.1, 4.4_

- [ ] 7.3 更新行为准则
  - 修改 `docs/content/docs/contributing/code-of-conduct.md`
  - 更新为 biliup 项目的行为准则
  - 说明社区的价值观和期望
  - _需求: 3.1_

- [ ] 7.4 更新进阶指南
  - 修改 `docs/content/docs/guide/introduction.md`
  - 移除过时的安装说明
  - 更新为进阶使用技巧的索引
  - 链接到相关的详细文档
  - _需求: 1.4, 3.1, 4.1_

- [ ] 8. 优化文档站点配置和导航
  - 优化 Zola 配置和导航结构
  - _需求: 3.1, 3.2, 3.4, 5.1, 5.2, 5.3, 5.4_

- [ ] 8.1 优化 Zola 配置文件
  - 修改 `docs/config.toml`
  - 配置中文语言支持
  - 配置搜索功能
  - 配置代码高亮主题
  - 配置 SEO 相关设置
  - _需求: 3.1, 5.2_

- [ ] 8.2 创建文档导航结构
  - 更新各章节的 `_index.md` 文件
  - 配置章节的权重和排序
  - 确保导航层次清晰
  - 添加章节描述和引导语
  - _需求: 5.1, 5.3, 5.4_

- [ ] 8.3 添加文档交叉引用
  - 在相关文档之间添加链接
  - 在文档底部添加"相关链接"部分
  - 确保所有内部链接有效
  - _需求: 5.4_

- [ ] 8.4 添加文档反馈机制
  - 在文档模板中添加反馈入口
  - 添加"编辑此页面"链接
  - 添加"报告问题"链接
  - _需求: 4.4_

- [ ] 9. 文档质量检查和优化
  - 检查和优化所有文档的质量
  - _需求: 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2_

- [ ] 9.1 检查中文语法和规范
  - 检查所有文档的中文语法
  - 统一标点符号使用
  - 统一术语翻译
  - 检查中英文混排的空格
  - _需求: 3.1, 3.2, 3.3_

- [ ] 9.2 检查代码示例
  - 检查所有代码示例的语法正确性
  - 确保代码示例可以实际运行
  - 添加必要的注释说明
  - 统一代码格式
  - _需求: 3.2, 3.4, 4.1_

- [ ] 9.3 检查文档元数据
  - 检查所有文档的 front matter
  - 确保标题、描述、日期等信息完整
  - 统一权重设置
  - 添加版本信息
  - _需求: 3.1, 3.2, 4.3_

- [ ] 9.4 优化文档可读性
  - 检查文档的段落结构
  - 优化长句和复杂表达
  - 添加必要的列表和表格
  - 确保逻辑清晰流畅
  - _需求: 3.1, 3.2_

- [ ] 9.5 添加图表和截图
  - 为关键功能添加截图
  - 为架构说明添加图表
  - 优化图片质量和大小
  - 添加图片说明
  - _需求: 2.5, 6.1_

- [ ] 10. 构建和测试文档站点
  - 构建文档站点并测试功能
  - _需求: 3.1, 4.1, 5.1, 5.2_

- [ ] 10.1 本地构建测试
  - 运行 `zola build` 构建文档
  - 运行 `zola serve` 启动本地服务器
  - 测试所有页面可以正常访问
  - 测试导航和链接功能
  - _需求: 3.1, 5.1_

- [ ] 10.2 测试搜索功能
  - 测试搜索索引是否正确生成
  - 测试搜索功能是否正常工作
  - 测试中文搜索的准确性
  - _需求: 5.2_

- [ ] 10.3 测试响应式布局
  - 测试桌面端显示效果
  - 测试平板端显示效果
  - 测试移动端显示效果
  - 确保所有设备上可读性良好
  - _需求: 5.1_

- [ ] 10.4 性能优化
  - 优化页面加载速度
  - 压缩图片资源
  - 优化 CSS 和 JavaScript
  - _需求: 5.1_

## 任务执行说明

### 优先级

- **高优先级**: 任务 1-3（快速入门、用户指南、配置参考）
- **中优先级**: 任务 4-6（架构设计、开发指南、API 参考）
- **低优先级**: 任务 7-10（更新现有文档、优化、测试）

### 执行顺序

建议按照任务编号顺序执行，因为后续任务可能依赖前面任务的成果。每完成一个主要任务（如任务 1），应该进行一次文档构建测试，确保没有破坏现有功能。

### 任务完整性

所有任务都是必需的，确保文档系统的完整性和专业性。包括测试、调试文档和视觉优化等任务，这些都是高质量文档不可或缺的部分。

### 验收标准

每个任务完成后，应该满足以下条件：
1. 文档内容完整，覆盖所有必要信息
2. 中文语法规范，表达清晰专业
3. 代码示例正确，可以实际运行
4. 链接有效，没有死链
5. 文档可以正常构建，没有错误
k
