# Description Pattern Library

This reference stores reusable bottom-description patterns for 推特版 AI 信息差 screenshot cards. Use it only when writing the lower explainer copy under the title and screenshot.

## What Competitor Samples Show

The strongest competitor descriptions share the same underlying rhythm:

- They start from a dramatic public issue, not from a neutral product summary.
- They quickly introduce one memorable contrast, usually old vs new, cost vs price, small model vs big model, or past judgment vs later reversal.
- They explain the mechanism in ordinary words, such as budget waste, cost transfer, repetitive work, or market size misjudgment.
- They end by landing on a group of people: employees, consumers, programmers, creators, or ordinary workers.
- They use numbers as proof, but usually only one or two numbers carry the whole paragraph.
- They often sound emotional, but the useful part is the conflict structure, not the noisy hype.

Before writing, clean OCR noise, repeated fragments, and overpacked phrases. Keep the competitive pacing, but make the final copy more readable than the raw sample.

## Sample-To-Pattern Map

- Tencent AI budget cut -> Budget cut / ROI disappointment.
- Apple memory price increase dispute -> Price increase / cost transfer.
- Li Feifei workplace prediction -> Workplace survival prophecy.
- Liang Wenfeng AI coding misjudgment -> Founder misjudgment / market reversal.
- VLX-Go, VLX-Flow, Hyper-Extract examples -> Product mechanism plus landing scenario, but only if the public consequence is clear.

## Pattern 1: Budget Cut / ROI Disappointment

Use when a company first encouraged AI use, then cut budget or restricted usage after measuring output.

Structure:

```text
[Company] 此前放开 AI 工具预算，鼓励员工在更多工作里使用。
但实测后发现，token 消耗和工具支出并没有稳定换来更高业务产出。
预算从 [old amount] 缩到 [new amount]，说明企业开始从尝鲜转向算账。
后面 AI 工具能不能继续用，不只看能力，也要看它能不能真的提升结果。
```

Key ingredients:

- Old budget vs new budget.
- Initial promotion vs later restriction.
- Consumption did not equal productivity.
- Employee may need to pay or ration usage later.

## Pattern 2: Price Increase / Cost Transfer

Use when a company says costs rose, but the final user price rises much more.

Structure:

```text
[Executive/source] 质疑 [company] 把成本压力转嫁给消费者。
据称 [input cost] 只上涨 [number]，但终端价格却上涨 [larger number]。
[Company leader] 将涨价归因于供应紧张或成本变化，市场仍在质疑涨幅是否合理。
消费者看到的是配置升级，真正承担的是更高溢价。
```

Key ingredients:

- Cost increase vs retail price increase.
- Executive criticism or public backlash.
- Company explanation.
- Consumer consequence.

## Pattern 3: Workplace Survival Prophecy

Use when a public figure predicts how AI changes jobs.

Structure:

```text
[Person] 认为未来职场会留下两类人：会驾驭 AI 的人，和能做判断创造的人。
AI 不一定直接取代所有岗位，但会先接走机械执行和重复劳动。
只会照搬指令的人会越来越被动，会提问、决策和创造的人更容易站稳。
这类判断适合落到普通人的学习、转型和工作习惯上。
```

Key ingredients:

- Two types of workers.
- AI replaces repetitive execution before replacing all humans.
- Shift from doing tasks to making decisions.
- Ordinary viewer takeaway.

## Pattern 4: Founder Misjudgment / Market Reversal

Use when an old judgment looks limited after the market changes.

Structure:

```text
[Founder/executive] 曾经判断 [market] 用户规模太小，产品落地价值有限。
当时 [specific group] 只有 [number]，这个判断在当年并不离谱。
但两年后 [tool/category] 快速普及，原来的小众场景变成了高频入口。
这类反转说明 AI 赛道不能只看当下人群规模，还要看工具会不会改变需求本身。
```

Key ingredients:

- Old judgment and reason.
- Old market size.
- New adoption.
- Why the old judgment became limited.

## Pattern 5: Lightweight Model Beats Larger Model

Use when a smaller model beats a larger model or changes an edge-device scenario.

Structure:

```text
[Product/model] 主打轻量化部署，不再单纯依赖更大的参数规模。
它用 [input/mechanism] 完成 [task]，在 [metric] 上达到 [number]，超过更大的 [comparison model]。
这类进展的重点不是参数更大，而是能不能在端侧、机器人或真实场景里跑起来。
巡检、救援、商超等场景看重的是响应和落地，不只是榜单分数。
```

Key ingredients:

- Smaller model vs larger model.
- Concrete metric.
- Edge/on-device deployment.
- Real-world scenario.

## Pattern 6: Product Mechanism Plus Landing Scenario

Use when a product release has technical novelty and clear deployment scenes.

Structure:

```text
[Product] 的重点是让 AI 从单次识别变成持续感知。
它通过 [mechanism] 降低延迟或显存压力，让视频流、记忆和历史画面可以连续处理。
实测 [metric] 达到 [number]，适合 [scenes] 这类需要实时观察的场景。
这类产品要讲清楚机制，但最终要落到它能替谁省时间、降风险或提升反应速度。
```

Key ingredients:

- Single-frame vs continuous perception.
- Mechanism in plain language.
- Latency/speed comparison.
- Landing scenes.

## Pattern 7: Document / Knowledge Tool Upgrade

Use when a tool claims to transform documents, RAG, or knowledge bases.

Structure:

```text
[Tool] 的卖点不是简单切 PDF 或做摘要，而是把杂乱文档变成结构化知识。
它可以生成知识图谱、时空图、数据模型或 Obsidian 知识库，适合论文、财报和私有资料整理。
如果支持本地部署，数据安全会成为一个额外卖点。
这类工具要避免只讲功能堆叠，重点说它把原来人工整理的哪一步自动化了。
```

Key ingredients:

- Not just summary or chunks.
- Structured outputs.
- Scenes such as papers, financial reports, private knowledge bases.
- Local deployment/privacy when relevant.

## Bad Habits To Avoid

- Do not compress too many unrelated facts into one breathless sentence.
- Do not leave OCR noise or repeated phrases in the final description.
- Do not use fake certainty for rumor-like claims.
- Do not write every case as `重磅发布`.
- Do not let technical product names dominate the first sentence when the public issue is more important.
