# Presentations · PptxGenJS

独立、可离线执行的可编辑 PPT 生成 Skill。使用公开 npm 包 `pptxgenjs@4.0.1`，不包含、不依赖 `@oai/artifact-tool`。这是本仓库新写的适配版，与保留的上游 `skills/presentations` 分开。

把整个目录放到 `~/.codex/skills/presentations-pptxgenjs/`，新会话中调用 `$presentations-pptxgenjs`。其他支持 SKILL.md 的 Agent 也可加载，但需自行提供 Node.js 和必要的工具权限。

- 联网安装：在本目录执行 `npm ci --ignore-scripts --no-audit --no-fund`。
- 自检：`node scripts/doctor.mjs`。
- 生成示例：`node scripts/build.mjs examples/demo.json demo.pptx`。
- 离线迁移：复制整个已安装目录，**包含 node_modules**。单独下载 GitHub 源码不含依赖。配套离线 ZIP 已包含依赖，但未包含 Node.js、字体、Office 或 AI 模型。
- Windows PowerPoint 预览：`powershell -File scripts/render.ps1 -PptxPath demo.pptx -OutputDir preview`。
- 结构检查：`python scripts/inspect_pptx.py demo.pptx`。

可编辑：文本、原生图形、连接线、表格、图表及其数据。PNG 仅作为独立可移动素材，不可编辑图片内部文字。任意已有 PPTX 的保真导入编辑不由 PptxGenJS 提供。

完整步骤见 [SKILL.md](SKILL.md) 和 [离线安装说明](references/portable.md)。本适配代码采用 MIT，依赖保留各自许可。生图服务、密钥及本机专有运行时均不打包。
