---
name: twitter-ai-viral-title-writing
description: "Twitter-version AI video viral title-writing workflow. Use when turning approved X/Twitter-version AI video topics into Chinese three-line short-video titles for Douyin/Xiaohongshu screenshot-card layouts with top three-line headline, middle screenshot, and lower explainer copy; especially after controversy-first topic screening, with rules for public familiarity, emotional hooks, familiar issue first, obscure protagonist later, numbers/contrast/reversal, and honest information-gap packaging."
---

# Twitter AI Viral Title Writing

## Overview

Use this skill to write Chinese titles for **推特版 AI 信息差视频** after topics have been screened. It is optimized for Douyin/Xiaohongshu screenshot-card layouts: a top three-line large headline, a middle source screenshot, and lower explainer copy.

The title is not a neutral news headline. It is the large hook that makes ordinary viewers stop, understand the public conflict in one second, then see the event and consequence.

## Precondition Gate

Write titles only for topics that have passed `twitter-ai-viral-topic-selection`. Do not use a sharper title to rescue a weak or duplicate topic.

- If the topic has no score, decision band, controversy evidence, or duplicate check, pause title writing and request or create the topic-quality audit first.
- If the topic is below 80 in a daily batch, label it as backup-only instead of polishing it into a final headline unless the user explicitly accepts the weakness.
- If the topic is developer-only, a narrow tool fix, a minor product update, pure benchmark, pure funding, or low-emotion news, say that the topic should be replaced before writing final titles.
- If the topic repeats an already-produced event and viewer takeaway, reject it even when a different title could make it feel new.
- A title can sharpen a passed topic; it cannot make an unpassed topic production-ready.

## Title Structure

Use exactly three short lines. Each line should usually be about 8-16 Chinese characters when possible:

```text
Line 1: public conflict or familiar protagonist
Line 2: concrete event/change
Line 3: ordinary-viewer consequence/information gap
```

Line 1 must have conflict. Line 2 must have change. Line 3 must have consequence.

Prefer numbers, comparison, and reversal when the source supports them. Avoid long lines that only work as body copy.

The three-line title should align with the first carousel image and cover subject. If the title leads with OpenAI, Meta, Google, Apple, Microsoft, Anthropic, xAI, Elon Musk, or another familiar protagonist, the first image and cover should also make that protagonist or parent-company identity immediately visible rather than leading with a text card or obscure product screenshot.

## Familiarity Rule

Do not lead with obscure names.

Lead with the protagonist only when it is broadly recognizable: OpenAI, ChatGPT, Google, Meta, Apple, Microsoft, Anthropic/Claude, xAI/Grok, Elon Musk, NVIDIA, Tencent, ByteDance, TikTok, major celebrities, major schools, government, courts, or famous media brands.

When the protagonist is obscure, lead with the familiar public issue:

- Not: `Notion 关掉 Notion Mail`
- Better: `以后邮箱不用你回了`

- Not: `Backstreet Boys 注册声音商标`
- Better: `AI 翻唱越像本人`

- Not: `AWS CEO 反驳 AI 抢新人饭碗`
- Better: `AI 真抢新人饭碗吗`

If both protagonist and issue are obscure, the topic should usually be deleted instead of titled.

## Emotional Hooks

Pick one dominant hook per title:

- Fairness: `凭什么不给钱`, `内容被拿去训练`, `声音也要注册`.
- Anxiety: `普通人不能随便用`, `新人门票变了`, `以后谁先被替代`.
- Fear/privacy: `聊天可能上法庭`, `你的声音可能被克隆`, `AI 记录不只是隐私`.
- Power/control: `巨头也开始抢入口`, `谁能先用被卡住`, `大厂怕被偷师`.
- Money/market: `市场已经开始押注`, `AI 影响的不只是产品`, `资本先动了`.
- Children/education: `孩子作业先变了`, `老师开始抢规则`, `作弊边界被重写`.

## Writing Rules

- Write like a short-video hook, not a neutral news headline.
- Use exactly three lines for screenshot-card titles.
- Keep each line roughly 8-16 Chinese characters when possible.
- Make line 1 feel like conflict, line 2 like change, and line 3 like consequence.
- Use Chinese-first wording; keep English product names only when recognition helps.
- Prefer concrete words over abstractions such as `范式`, `生态`, `能力边界`, `产业迁移`.
- Prefer numbers, comparison, contrast, and reversal when they are true.
- Do not exaggerate beyond the verified source.
- Do not hide the real event: the viewer should understand what happened from the three lines alone.
- If the title needs a long explanation to make sense, rewrite or reject the topic.

## Common Templates

Use these templates as starting points, then rewrite them into natural Chinese:

```text
[familiar protagonist] 这次被骂惨了
[cost/ability/rule] 只变了 [number]
普通人却要多付 [cost]
```

```text
[public issue] 开始变了
[concrete change] 正在发生
普通人可能还没意识到
```

```text
[work/privacy/content/money] 出问题了
[AI/big tech/platform] 正在改规则
以后不能再这么用了
```

```text
[old belief] 可能错了
[new fact] 直接反转
AI 不是越大越强
```

```text
[big tech company] 开始算账了
AI 预算被直接砍掉
会用 AI 不等于有产出
```

## Strong Patterns

Use these patterns when they fit:

```text
400 家报纸起诉 AI
内容被拿去训练
凭什么不给钱
```

```text
你和 ChatGPT 的聊天
可能被拿上法庭
AI 记录不只是隐私
```

```text
连 Meta 都被限制
Google 不让随便用 Gemini
AI 巨头也抢入口
```

```text
GPT-5.6 来了
但普通人不能随便用
AI 入口被卡住
```

```text
AI 翻唱越像本人
明星开始抢回声音
以后嗓子也要注册
```

```text
机器人不用听指令了
看一眼就能自己走
小模型开始挑战大模型
```

```text
苹果这次被骂惨了
成本涨 45 却加价 250
消费者成了转嫁对象
```

## Rewrite Checklist

Before finalizing, check:

- Does line 1 use a familiar conflict or recognizable protagonist?
- Does line 2 state a concrete event?
- Does line 3 create consequence, tension, or information gap?
- Is each line short enough to sit as a top screenshot-card headline?
- Is there a number, contrast, or reversal when the source supports one?
- Could a non-AI viewer understand the issue without prior context?
- Is the emotional hook supported by the source?
- Are obscure names moved out of line 1 unless they are necessary?

## Final Upload Review

Use this review again immediately before video upload or GitHub sync. The title is not final just because it rendered once.

- Confirm the rendered video title, cover title, and `整体描述.md` three-line title use the same words and the same angle unless the user explicitly approved a platform-specific rewrite.
- Confirm the paste-ready 抖音标题 is a compressed version of the three-line title, not a different story angle.
- Confirm line 1 still creates public conflict or uses a familiar protagonist, line 2 still states the concrete event/change, and line 3 still lands on the ordinary-viewer consequence or information gap.
- If a screenshot, source, or bottom description changed during production, re-check whether the title still matches the evidence. If not, rewrite the title before uploading.
- Reject titles that became neutral news summaries, obscure product-name leads, unsupported exaggeration, or vague hooks such as `AI 又有大事`.

Return 2-4 title options when the topic is promising but the best emotional angle is not obvious. Mark the recommended title first.
