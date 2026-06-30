# 2026-06-30 22:26 Twitter Batch Freshness Audit

审核时间：2026-06-30

硬门槛：只保留 2026-06-28 至 2026-06-30 发布或明显发酵的 AI 选题；不能只看本地配置里的 `date: 2026.06.30`。

## 旧手动批次结论

| 原序号 | 话题 | 原记录日期 | 当前结论 | 原因 |
| --- | --- | --- | --- | --- |
| 01 | Meta伪装青少年测试AI | WIRED / X 06.29-06.30 | 保留 | WIRED 原文发布时间为 Jun 29, 2026 5:49 PM，X 传播在 06.30，仍在 2-3 天窗口内。 |
| 02 | Anthropic回应政府模型限制 | 误记为 Anthropic X 06.30 | 淘汰 | Anthropic 官方声明为 Jun 12, 2026，核心 X 状态也显示 2 weeks ago，不属于近 2-3 天。 |
| 03 | Gemini上线学习笔记 | Google X 06.25 | 淘汰 | 超出 2026-06-28 至 2026-06-30 窗口。 |
| 04 | OpenAI研究有益特质 | OpenAI X 06.19 | 淘汰 | 超出 2026-06-28 至 2026-06-30 窗口。 |
| 05 | OpenAI生命科学基准 | OpenAI X 06.18 | 淘汰 | 超出 2026-06-28 至 2026-06-30 窗口。 |

## 替换规则

- 先查 `records/twitter-ai-info-video/topic-history.md` 和普通版 `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md`。
- 淘汰与普通版 06.30 已产出同事件同角度的题，例如 TIDAL AI 音乐、Google AI 价值观、NVIDIA 中国芯片、AI 数据中心社区争议等。
- 每条新题必须带可截图的 X 状态或清晰可信媒体/官方页面。
- 后续截图阶段必须用 `--tweet-only` 或明确 crop，不能把 X 左导航、右栏、空白、回复区带入最终图。

## Fresh Candidate Pool

| 候选 | 来源日期 | 核心锚点 | 去重判断 | 方向 |
| --- | --- | --- | --- | --- |
| Meta contractors posed as teens | WIRED Jun 29, 2026 / X 06.30 | https://x.com/WIRED/status/2071719798749446528 | 不重复 | 儿童安全 / 竞品测试 / 平台责任 |
| OpenAI Codex usage-limit fix | BI Jun 30, 2026 / X Jun 29-30 | https://x.com/thsottiaux/status/2071740419030053227 | 不重复 | AI 工具成本 / 算力额度 / 付费体验 |
| Ford rehires veteran engineers after AI falls short | TechCrunch Jun 28, 2026 / X 06.28 | https://x.com/TechCrunch/status/2071310226167578673 | 不重复 | AI 替代失败 / 老经验回流 / 质量控制 |
| AI jobs debate just got messier | TechCrunch Jun 29, 2026 / X 06.30 | https://x.com/TechCrunch/status/2071807338328272949 | 不重复，但与 Ford 同属就业主题，二选一优先 Ford | 就业焦虑 / 初级岗位 / AI 投入与扩张 |
| Lumo privacy-focused AI chatbot upgrade | TechCrunch Jun 30, 2026 / X 06.30 | https://x.com/TechCrunch/status/2071957323304804748 | 不重复 | 隐私 AI / 记忆功能 / 数据训练边界 |
| OKX AI agent marketplace | TechCrunch Jun 30, 2026 / X 06.30 | https://x.com/TechCrunch/status/2071882039868150040 | 不重复 | AI agent 交易 / 钱包身份 / 自动支付 |
| X hosted MCP server | TechCrunch Jun 30, 2026 | TechCrunch / X official developer source pending capture | 不重复 | AI 工具接入社交平台 / 实时数据 / 自动化风险 |
| Amazon $1B FDE org | TechCrunch Jun 30, 2026 | TechCrunch / Amazon official source pending capture | 不重复 | 大厂下场做 AI 落地服务 / 企业部署 |

## Chrome Capture Review

公开 oEmbed 接口在本机多次超时，不能作为可用性或日期依据；最终以本机 Chrome 实际打开后的 `--tweet-only` 截图为准。

已通过本机 Chrome 抓到的核心帖：

| 文件 | 截图结果 | 质量判断 |
| --- | --- | --- |
| `assets/raw/chrome/fresh-01-meta-teen-test-tweet.png` | WIRED 核心帖，显示 2026年6月30日 | 合格：核心帖卡片，无左右栏，正文和主图可读。 |
| `assets/raw/chrome/fresh-02-codex-limits-tweet.png` | Tibo / Codex 用量说明帖，显示 2026年6月30日 | 合格：核心帖卡片，无左右栏；内容较长，后续证据卡需提炼中文释义。 |
| `assets/raw/chrome/fresh-03-ford-rehire-tweet.png` | TechCrunch / Ford 重新雇回工程师，显示 2026年6月29日 | 合格：核心帖卡片，无左右栏，主图和标题完整。 |
| `assets/raw/chrome/fresh-04-lumo-privacy-tweet.png` | TechCrunch / Lumo 隐私 AI 升级，显示 2026年6月30日 | 合格：核心帖卡片，无左右栏，主图完整；互动较弱但主题多样性好。 |
| `assets/raw/chrome/fresh-05-okx-agents-tweet.png` | TechCrunch / OKX AI agents 互相雇佣和支付，显示 2026年6月30日 | 合格：核心帖卡片，无左右栏，主图完整。 |
| `assets/raw/chrome/fresh-backup-ai-jobs-tweet.png` | TechCrunch / AI jobs debate，显示 2026年6月30日 | 合格，作为备选；与 Ford 同属就业主题，避免同批过度重复。 |

本次替换拟采用：

1. Meta伪装青少年测试AI
2. OpenAI Codex用量限制修复
3. Ford重新雇回老工程师
4. Lumo隐私AI升级
5. OKX让AI代理互相雇佣支付

备选：AI jobs debate just got messier。
