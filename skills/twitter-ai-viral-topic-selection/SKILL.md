---
name: twitter-ai-viral-topic-selection
description: "Twitter-version AI video viral topic screening workflow. Use when selecting X/Twitter-version AI news/video topics, ranking candidate AI stories for short videos, removing weak or obscure topics, scoring controversy/emotion/comment spread, or choosing 5 daily AI topics from Polymarket, OpenAI/Anthropic official updates, AI news accounts, trusted tech media, and viral media."
---

# Twitter AI Viral Topic Selection

## Overview

Use this skill to select **推特版 AI 信息差视频** topics. The goal is not to find the newest AI news; it is to find AI stories from approved sources that can trigger public controversy, emotion, comments, and sharing.

## Source Priority

Use this source order when scouting topics:

1. **Top priority**: `@Polymarket`, OpenAI official site/account, Anthropic/Claude official site/account.
2. **AI signal amplifiers**: `@TheRundownAI`, `@rowancheung`, `@ArtificialAnlys`, `@AiBreakfast`, `@tldrnewsletter`.
3. **Trusted tech media**: `@TechCrunch`, `@verge`, `@WIRED`, `@ReutersTech`, `@technology`, `@theinformation`, `@VentureBeat`.
4. **Viral spread media**: `@unusual_whales`, `@WatcherGuru`, `@MorningBrew`, `@Dexerto`.

Prefer candidates first seen in the sources above. Viral spread media can prove heat, but should not be the only factual source for a controversial claim.

## Hard Delete Rules

Delete or downgrade candidates when any of these are true:

- The protagonist is obscure and the public issue is also obscure.
- The story only matters to AI insiders, developers, or productivity-tool fans.
- The first line of a potential title would require explaining a niche product, person, or benchmark.
- There is no visible controversy, comment debate, quote-post spread, or obvious public emotion.
- The story is pure funding, pure benchmark, pure paper, or minor product update.
- The claim cannot be verified by an official source or trusted media.
- The topic repeats or nearly repeats an already-produced event and information-gap angle in either `records/twitter-ai-info-video/topic-history.md` or the ordinary AI 信息差 news-video history at `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md`.

If the protagonist is obscure but the public issue is familiar, keep it only when the title can lead with the familiar issue instead of the obscure name.

## Production Hard Gate

Do not let freshness, screenshot quality, a clean cover, or a good rewrite substitute for topic quality. A topic is not approved until it has passed the scoring model below and duplicate checks. Treat this as a hard gate before screenshot capture, cover generation, title writing, description writing, or rendering.

- Candidate pool is not the final list. A freshness audit or source table only proves that stories are recent enough to consider; it does not approve them for production.
- Score before assets. Do not move a candidate into rendering just because it has a clean X screenshot, a strong visual, or a familiar company name.
- Fresh is not enough. A latest 2-3 day story can still fail if it is a minor tool fix, a narrow developer issue, a weak product update, or has no public emotion.
- No visual rescue. If a topic is weak or duplicate, do not try to save it with better screenshots, a stronger cover, sharper title, or denser bottom copy. Replace the topic.
- Duplicates are hard fails. If the same event/development and information-gap angle already appeared in 推特版 or ordinary AI 信息差 history, delete it even if a new tweet, new media account, or better asset is available.
- A daily 5-topic batch should not contain backup-only topics unless the user explicitly accepts them. Prefer 80+ topics; if fewer than five pass, keep scouting.
- Before reporting the selected 5 topics, include the score and decision band for each topic plus a short note for any deleted near-miss. If this audit is missing, the batch is not ready to render.

## Selection Workflow

1. Read recent topic history when available and remove exact repeats.
2. Read both 推特版 history and ordinary AI 信息差 news-video history. Remove exact repeats and near-duplicates across both workflows before scoring. Similar company/theme is allowed, but if the event object, factual anchor/source tweet, title hook, and ordinary-viewer takeaway are almost the same, treat it as a duplicate and delete it.
3. Build a default candidate pool of 30 topics from the approved sources, with Polymarket and official OpenAI/Anthropic updates checked first. If fewer than 30 credible candidates are available inside the requested time window, record the smaller number and why.
4. For each candidate, capture the factual anchor: official post/page, trusted media story, or source tweet.
5. Judge controversy with replies, quote-posts, comment count, and visible disagreement. Likes alone are not enough.
6. Score the remaining candidates using the table below before any visual work, then sort by total score and decision band.
7. Keep the strongest 5, but avoid choosing five stories with the same company, theme, or emotional hook. If one of the strongest 5 is backup-only or duplicate, replace it before rendering.
8. Before rendering or screenshot capture, keep a record of the full candidate pool, deleted candidates, final top 5, scores, and reasons.

Familiarity is a practical priority, not a decorative score. Prefer stories led by familiar companies, people, products, or public issues. Cold protagonists such as niche enterprise suppliers, component vendors, or unknown startups should be downgraded unless the public conflict is so clear that the title can lead with the familiar issue instead of the obscure name.

## Default 30-To-5 Daily Mode

For daily auto-scouting, the default logic is:

```text
collect 30 candidates -> remove duplicates/weak sources -> score every candidate -> rank -> select final 5
```

Do not directly choose the first 5 high-like or easy-to-screenshot posts. The 30-candidate pool is part of the quality control: it forces comparison across official sources, media amplification, public familiarity, controversy, emotional comments, visual assets, and duplicate risk.

If source access, login state, or the time window prevents finding 30 credible candidates, continue with the largest credible pool and explicitly record:

- candidate count found
- candidate count deleted
- final selected count
- why the pool was smaller than 30
- whether any selected topic is below 80 and why the user accepted it

## Scoring

Score each candidate out of 100:

| Dimension | Points | What To Check |
| --- | ---: | --- |
| Controversy strength | 30 | Can ordinary viewers argue, take sides, or object? |
| Emotional spread | 25 | Does it trigger anxiety, anger, fear, excitement, curiosity, or fairness instincts? |
| Source priority | 15 | Does it come from Polymarket, official OpenAI/Anthropic, AI signal accounts, or trusted tech media? |
| Public familiarity | 10 | Is the protagonist known, or is the issue immediately familiar? |
| Information gap | 10 | Is there a clear "people think A, but actually B" angle? |
| Comment/spread signal | 5 | Are replies, quotes, or comment debates visibly active? |
| Visual assets | 5 | Are there usable people, product, chart, article, tweet, or official-page visuals? |

Decision bands:

- `90+`: lead topic for the day.
- `80-89`: good daily candidate.
- `70-79`: backup only.
- `<70`: delete.

## Public Themes

Prioritize themes ordinary viewers already understand:

- AI and jobs: newcomers, white-collar workers, creators, support, design, coding.
- AI and money: prediction markets, stocks, IPOs, chips, company control.
- AI and rights: copyright, publishers, music, film, creator compensation.
- AI and privacy: chat logs, court evidence, data use, surveillance.
- AI and safety: deepfakes, scams, voice cloning, model misuse.
- AI and children/education: cheating, tutoring, school rules, ability decline.
- Big-tech power: OpenAI, Google, Meta, Apple, Microsoft, Anthropic, xAI controlling access, rules, or compute.
- Government/regulation: safety review, release limits, lawsuits, bans, procurement.

## Output Format

When presenting selected topics, include:

```text
topic:
source:
link:
candidate rank:
candidate pool size:
public theme:
controversy:
emotion:
public familiarity:
information gap:
comment/spread signal:
score:
decision:
title direction:
```

Also mention deleted candidates briefly when they were removed for being too obscure, too niche, not from approved sources, weakly controversial, or already repeated.
