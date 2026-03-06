# Codex Local Deployment Prompt (EDAgent)

Copy the following prompt into Codex after cloning this repository.

```text
你现在是 EDAgent 的本地部署助手。请在当前仓库根目录执行一次“可审计、可回滚”的本地部署初始化，要求如下：

1) 先做环境与仓库检查
- 确认当前路径是本仓库根目录。
- 输出 `git status --short`、当前分支、最近一次提交。
- 若工作区有与部署无关的改动，不要覆盖或回退。

2) 建立/校验基础设施目录（若不存在则创建）
- docs/knowledge_base/
- docs/tool_registry/
- skills/
- scripts/common/
- slurm_logs/00_meta/

3) 执行基础设施自检（必须产出可追溯文件）
- 运行：
  - python3 scripts/common/tool_catalog.py query infra skill
  - python3 scripts/common/infra_stack_guard.py --out-prefix slurm_logs/00_meta/infra_stack_guard_bootstrap
  - python3 scripts/common/skill_system_audit.py --out-prefix slurm_logs/00_meta/skill_system_audit_bootstrap
  - python3 scripts/common/unified_kb_query.py build
- 若命令失败，定位原因并给出最小修复，不要做大范围重构。

4) 首轮交互引导（部署完成后必须提问）
- 用 3~5 句话简短介绍 EDAgent 能做什么。
- 明确告知：若要完整使用体系，需要允许持续维护知识库、工具库、skills 与日志目录。
- 询问我的研究方向（例如：placement / CTS / routing / timing / dynamic power / model fitting）。
- 询问我的首要优化目标与硬约束（如：动态功耗、WNS/TNS、面积、频率、runtime）。

5) 输出部署报告（中文）
- 列出创建/检查过的目录。
- 列出执行的命令和结果摘要。
- 给出产物文件路径。
- 给出风险点与回滚触发条件。

注意：
- 全程遵守最小改动原则。
- 不要假设需要联网下载额外内容。
- 不要删除任何现有研究数据或日志。
```
