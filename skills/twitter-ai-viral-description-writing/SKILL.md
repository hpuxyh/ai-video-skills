---
name: twitter-ai-viral-description-writing
description: "Twitter-version AI video screenshot-card description writing workflow. Use when writing the bottom explainer copy under a Douyin/Xiaohongshu AI news screenshot card after viral topic selection and three-line title writing; covers what facts to extract, how to compress news into 3-5 short Chinese sentences, how to mirror the title, and how to use competitor-style patterns without overhyping."
---

# Twitter AI Viral Description Writing

## Overview

Use this skill to write the **bottom description copy** for 推特版 AI 信息差 screenshot-card videos. The card has three layers:

```text
Top: three-line title, for stopping the viewer
Middle: source screenshot, for proof
Bottom: description, for explaining the news
```

The description is not a press release, long article, or source transcript. It should explain the title in 3-5 short Chinese sentences.

## What To Extract

Extract only the facts that help viewers understand the conflict:

- **Core event**: who did what, such as sued, cut budget, limited access, launched, reversed, rehired, raised price, or banned usage.
- **Numbers and comparison**: money, percentage, model size, speed, parameter count, budget cut, cost increase, price increase, people count, time window.
- **Conflict parties**: company vs users, media vs AI company, employee vs AI budget, creator vs platform, big tech vs big tech.
- **Cause or mechanism**: why it happened, such as cost control, data risk, copyright, low ROI, model inefficiency, regulation, or competitive leakage.
- **Affected group**: ordinary users, consumers, creators, employees, developers, students, publishers, companies, or platform operators.
- **Scene or consequence**: where it lands, such as workplace survival, pricing, training data, privacy, internal AI rules, or real-world deployment.

Do not copy all details from the source. Prefer one sharp number and one clear conflict over many technical facts.

## Description Structure

Use 3-5 short sentences:

```text
Sentence 1: Say what happened directly.
Sentence 2: Add the strongest number, comparison, or concrete fact.
Sentence 3: Explain the cause, conflict, or mechanism.
Sentence 4: Say who is affected and how.
Sentence 5: Optional natural closing judgment.
```

Do not end with a fixed phrase such as `真正的信息差是...`. Say the conclusion directly.

## Match The Title

Mirror the three-line title:

- Title line 1 has conflict -> description sentence 1 explains the event.
- Title line 2 has change -> description sentence 2 gives the fact or number.
- Title line 3 has consequence -> description sentence 3-5 explains the affected people and outcome.

If the description introduces a totally different angle from the title, rewrite one of them.

## Style Rules

- Write like a person explaining news, not like an official announcement.
- Keep the copy dense but readable; avoid long paragraph walls.
- Use concrete Chinese and avoid empty hype such as `重磅炸场`, `彻底颠覆`, `重新定义` unless the requested style is intentionally exaggerated.
- Translate technical terms into ordinary meaning.
- Keep important numbers, but avoid stacking too many numbers in one sentence.
- For negative company stories, use careful wording such as `据报道`, `被曝`, `引发争议`, `可能`, or `外界质疑` when appropriate.
- Do not repeat the screenshot text verbatim; explain what the screenshot proves.
- Do not overstate legal, financial, medical, or safety claims beyond the source.

## Competitor Pattern Library

When you need more pattern guidance, read `references/description-pattern-library.md`. It contains reusable structures derived from competitor examples, including:

- Budget cut / ROI disappointment.
- Price increase / cost transfer.
- Workplace survival prophecy.
- Founder misjudgment / market reversal.
- Lightweight model beats larger model.
- Product mechanism plus landing scenario.

## Output Format

Return:

```text
topic:
three-line title:
bottom description:
source facts used:
notes:
```

When asked for multiple options, keep the same topic and title, then vary the description angle: factual, sharper, more ordinary-viewer, or more business-focused.
