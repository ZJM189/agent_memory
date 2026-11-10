# Presentations Skill 分发包

本目录复制自 OpenAI Codex 内置 Presentations 插件，版本 `26.1105.12137`。保留上游 Skill、文档、脚本、图标及插件元数据；不包含本机生成文件、缓存、凭据或运行时二进制。

## 安装与使用

将整个 `presentations` 目录放到接收者的 `~/.codex/skills/`（Windows 为 `%USERPROFILE%\.codex\skills\`），重新开启会话后使用 `$presentations`。如已有同名内置 Skill，优先使用内置版本，避免重复安装。

**这是一份依赖宿主运行时的 Skill，不是独立 PPT 生成程序。** 完整创作功能需要兼容的 Codex 环境提供 `@oai/artifact-tool`、Node.js、Python 及相关依赖。Skill 本身不会安装这些依赖。先使用 `load_workspace_dependencies` 获取运行时路径；无该工具时，只能使用接收者已经合法安装的兼容运行时，通过 `RUNTIME_NODE_MODULES` 指定依赖目录，不能照搬分发者机器上的路径。Google Slides、实时画布等功能也需要对应的连接器或工具。

当前上游包引用了一些未随本缓存提供的可选模板、领域文档。引用不存在时应使用接收者安装的原版插件补齐，或说明该功能不可用，不要假定模板已安装。本包适合在已有兼容运行时的 Codex 中复用；其他 Agent 仅安装本目录不能保证正常生成 PPT。

## 来源与许可

上游作者：OpenAI。上游插件清单声明许可为 `MIT`，原始声明保留在 [upstream-plugin.json](upstream-plugin.json)。上游标识的仓库为 `https://github.com/openai/openai`，此处不将其视为已验证的公开源码下载地址。

上游文件保留原内容，仅将 `SKILL.md` 的 `name: Presentations` 改为符合独立 Skill 命名规范的 `name: presentations`，已通过 Skill 格式校验。本说明及分发排除规则由本仓库补充。该缓存包未附单独的 LICENSE 文件；未替上游补造版权年份或许可正文。上游声明不代表 `@oai/artifact-tool`、宿主服务、字体、模板或其他依赖也允许再分发；它们均未打包在本目录中。继续分发时请保留上游署名、插件元数据及本说明。
