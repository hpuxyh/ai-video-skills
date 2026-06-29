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
- The topic repeats an already-produced event and information-gap angle in `records/twitter-ai-info-video/topic-history.md`.

If the protagonist is obscure but the public issue is familiar, keep it only when the title can lead with the familiar issue instead of the obscure name.

## Selection Workflow

1. Read recent topic history when available and remove exact repeats.
2. Build a candidate pool from the approved sources, with Polymarket and official OpenAI/Anthropic updates checked first.
3. For each candidate, capture the factual anchor: official post/page, trusted media story, or source tweet.
4. Judge controversy with replies, quote-posts, comment count, and visible disagreement. Likes alone are not enough.
5. Score the remaining candidates using the table below.
6. Keep the strongest 5, but avoid choosing five stories with the same company, theme, or emotional hook.

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
