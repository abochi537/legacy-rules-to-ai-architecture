# legacy-rules-to-ai-architecture

遗留系统规则抽取与 AI 长期上下文初始化 skill。

它的目标不是直接替你重构代码，而是让 AI 先系统化扫描旧项目，把已经存在的业务规则、架构约束、API 契约、前端一致性规则、测试策略和 Git 流程沉淀成可长期维护的项目上下文。

最终产物通常包括一个短 `AGENTS.md` 和一组 `docs/ai/*` 快速导航文档，用来降低多轮 AI 开发中的架构漂移、实现方式不统一、前端风格不一致和上下文腐烂问题。

## 适用场景

- 想用 AI 从旧系统中捞出已经实现过的功能规则。
- 想基于旧规则重建新架构或迁移系统。
- 多轮 AI 开发后，同一类问题容易出现多套实现方式。
- 前端页面越改越不统一，需要沉淀 layout、组件、tokens、页面模式和视觉检查规则。
- 需要一个短 `AGENTS.md` 作为项目级硬规则入口，而不是把所有规则塞进提示词。

## 生成内容

默认 `core` profile 会生成：

```text
AGENTS.md
docs/ai/00-index.md
docs/ai/tech-baseline.md
docs/ai/architecture.md
docs/ai/git-workflow.md
docs/ai/active-context.md
docs/ai/context-health.md
```

`full` profile 会额外生成：

```text
docs/ai/project-brief.md
docs/ai/domain-rules.md
docs/ai/api-contracts.md
docs/ai/frontend-guidelines.md
docs/ai/testing-strategy.md
docs/ai/migration-map.md
docs/ai/decisions.md
```

## 安装

通过 skills CLI 安装：

```bash
npx skills add abochi537/legacy-rules-to-ai-architecture -g -a cursor -a claude-code -a codex -y
```

或下载 release / 本地分享的压缩包后解压到 Codex skills 目录：

```powershell
Expand-Archive legacy-rules-to-ai-architecture.zip -DestinationPath $env:USERPROFILE\.codex\skills -Force
```

源码仓库不依赖手工维护的 zip。维护者需要分享压缩包时，应从源码重新生成：

```bash
python scripts/package_skill.py --output dist/legacy-rules-to-ai-architecture.zip
```

安装后新开 AI 会话，直接描述目标即可，不需要手动执行脚本：

```text
使用 legacy-rules-to-ai-architecture 分析这个旧项目，自动初始化 AI 上下文，然后按页面和 API 分批抽取规则。
```

Agent 在 skill 触发后会默认自己完成这些动作：

- 识别目标项目根目录。
- 运行 scaffold 脚本创建 `AGENTS.md` 和 `docs/ai/*`，但不覆盖已有文件。
- 分批抽取旧系统规则、架构约束、API 契约和前端一致性规则。
- 运行 lint 脚本检查缺文件、占位符和 `AGENTS.md` 长度。
- 汇报哪些内容已创建、哪些仍缺证据、哪些规则需要人工确认。

## 推荐话术

```text
使用 legacy-rules-to-ai-architecture 初始化当前项目的 AI 长期上下文。
请自动选择合适的 profile，然后按模块分批抽取旧系统规则、架构约束、API 契约和前端一致性规则。
最后自动运行上下文检查，并告诉我哪些地方还缺证据。
```

如果要做完整迁移/重构准备：

```text
使用 legacy-rules-to-ai-architecture 为当前旧项目生成 full profile。
请自动初始化 AGENTS.md 和 docs/ai，上下文目录使用 docs/ai。
然后先建立功能清单，再按页面、API、领域模块分批抽取规则，不要一次性全仓泛读。
```

## 手动 fallback

正常情况下用户不需要执行下面命令。只有当 AI 客户端没有终端权限、Python 不可用、文件系统受限，或你想手动排查时，才需要直接运行脚本。

在目标项目中创建轻量 `core` 上下文：

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root>
```

创建完整上下文：

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root> --profile full
```

自定义 AI 文档目录：

```bash
python <skill-dir>/scripts/scaffold_ai_context.py --project <project-root> --docs-dir .ai/context
```

检查上下文是否缺文件、`AGENTS.md` 是否过长、是否还有明显占位符：

```bash
python <skill-dir>/scripts/lint_ai_context.py --project <project-root>
```

检查 `full` profile：

```bash
python <skill-dir>/scripts/lint_ai_context.py --project <project-root> --profile full
```

## 发布检查

发布或分享前运行：

```bash
python -m unittest discover -s tests
python scripts/package_skill.py --output dist/legacy-rules-to-ai-architecture.zip
```

`package_skill.py` 会只打包正式安装文件，并校验压缩包中不包含 `.git`、`__pycache__`、`.pyc` 或临时目录。

## Git 规范集成

本 skill 已集成 `Links17/csg-git-skill` 作为 Git、版本、分支、commit、tag、提测发布治理入口。

建议配套安装：

```bash
npx skills add Links17/csg-git-skill -g -a cursor -a claude-code -a codex -y
```

`legacy-rules-to-ai-architecture` 负责旧系统规则抽取和长期 AI 上下文；`csg-git-skill` 负责 Git 版本与发布流程治理。

## 设计原则

- `AGENTS.md` 只放项目约束、硬规则和导航，保持短小。
- `docs/ai/*` 存放证据化项目知识，关键规则应能追溯到代码、测试、schema、截图、日志或产品文档。
- workflow skills 只存放可复用流程，不承载整个项目事实。
- 大型代码库必须按 feature、API、page 或 module 分片抽取，不能一次性全仓泛读。
- 缺少证据时写 `Unknown`，不要把推测写成硬规则。

## 边界

这个 skill 不是全自动重构工具。它不会自动保证规则正确，也不会替你完成系统迁移。

它提供的是一套稳定工作流：先抽取证据，再沉淀规则，再用 `AGENTS.md`、`docs/ai/*`、可选 workflow skills 和检查门禁降低 AI 开发漂移。
