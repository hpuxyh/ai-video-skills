---
name: vertical-ai-info-video
description: "Generate 9:16 Chinese AI information-gap short videos and platform cover images with real news images, people-first cover thumbnails, bold no-glow headline typography, beat-synced multi-photo motion, one-by-one info rows, paper-card explainer previews, no voiceover, and local BGM mixing. Use when the user asks to make, iterate, or standardize vertical AI news/info-gap videos, 抖音/视频号/小红书竖屏快报, 封面图, 最近7天AI热点, 中美AI新闻, or says to use this short-video workflow skill."
---

# Vertical AI Info Video

## Overview

Use this skill to produce the fixed 9:16 AI 信息差短视频 workflow: people-first cover image, top positioning label, bold three-line title, real image carousel in the middle, bottom information rows revealed one by one, strong push-pull image motion, no voiceover, and 7-second BGM from a local audio file.

It also supports the confirmed paper-card explainer mode: a white textured 9:16 card with a strong black headline, purple information-gap ribbon, real news media in the middle, and cyan-highlighted explanatory copy at the bottom. Use this mode when the user references the white card examples, asks for "参考这种图文卡样式", or wants a static rendered image before video production.

This skill is optimized for fast iteration. When the user asks for visual tuning, generate preview screenshots first. Render the full MP4 only after the user confirms the style.

## Workflow

1. Route the request:
   - If the user gives a concrete news topic, company, event, URL, or instruction, generate one video for that event using the confirmed workflow.
   - If the user does not give a concrete topic, search the latest 7 days of AI news, prioritize China/US high-signal stories, choose 5 distinct topics, and generate 5 separate one-event videos.
2. Confirm or infer each video's topic, title lines, info rows, image set, cover, and BGM.
3. Require real topic-matched images. For news videos, start with real people/company/product photos, then add official/news/product screenshots as supporting evidence. Do not use fake UI, abstract placeholders, or pure text cards as primary images.
4. For social publishing, generate a cover preview using the cover rules in `references/style-guide.md`: real person first, headline as the first visual layer, company logo as secondary recognition, and one conclusion row only.
5. Select background music from the local BGM pool using the BGM rules below. For a 5-video batch, choose one track per video by theme fit plus weighted randomness, with `bba进行曲.mp3` favored.
6. Build a JSON config using the schema in `references/style-guide.md`. For paper-card explainer mode, build a paper-card JSON and render a static preview first with `scripts/render_paper_card_preview.py`.
7. Before rendering, inspect downloaded assets or a contact sheet. If an image source fails and produces an error/fallback card such as `图片源不可用`, `429`, `403`, a blank page, or a blocked page, replace it with a verified real image, local cached asset, official screenshot, or clean source card. Never ship a video with an asset-error card visible.
8. Run `scripts/render_vertical_info_video.py` from a project directory:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_vertical_info_video.py \
  --config configs/video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

9. Validate the MP4 with `ffprobe` and inspect the contact sheet before reporting completion.
10. Record the finished topics in the project history file, then sync reusable skill/workflow updates to the user's GitHub repository when the skill or workflow rules changed.

## Topic Selection Modes

- Specific-topic mode: use the user's topic directly. Verify current facts when the topic is recent or time-sensitive, then create one cover and one video.
- Auto-scout mode: when no concrete topic is provided, search the latest 7 days of AI news across US and China, then select 5 topics before rendering.
- Auto-scout selection criteria: do not simply pick the top 5 headlines. Build a candidate pool first, then pick the 5 stories most suitable for AI 信息差短视频: viewer relevance, clear information gap, recognizable people/companies, available real imagery, and platform-friendly tension. Avoid duplicates, low-signal funding-only items, vague opinion pieces, and stories without usable real images.
- Daily freshness: before selecting auto-scout topics, check previous generated batches and topic-history files. Do not choose the exact same event/topic as an earlier batch unless the user explicitly asks for a follow-up angle. If a company repeats, the event and information-gap angle must be materially different.
- Auto-scout output: generate 5 independent videos, not one compilation. Each video keeps the same row logic, image logic, cover logic, and verification steps.
- Before rendering 5 videos, show the chosen 5 topics with one-line rationale, likely cover assets, and the information-gap angle when the user has not already approved the topic list.

## One-Event Video Logic

- Treat each video as one news event, not a multi-card slideshow of separate text panels.
- Attach multiple real images to that single event. Use them as the middle carousel only.
- Keep all explanatory text in the template: the top title and the bottom one-by-one info rows.
- Do not create five standalone text cards as the five images. Text cards may only be minor overlays or fallback references, never the primary carousel.
- Use one event-specific info-row set from the viewer's path: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.
- The target look is the previously approved White House safety-review sample: large top headline, real images in the middle, structured text rows below, beat-synced image cuts, no voiceover.

## Paper Card Explainer Mode

Use this mode when the user approves or references the white-card examples: bold black headline, purple ribbon, a real screenshot/photo in the center, and cyan-highlighted explanatory copy below.

Title logic:

- Use a strong two-part hook instead of a neutral news title.
- Line 1-2: black, heavy, high-contrast headline that names the surprising event or actor.
- Purple ribbon: the sharp conclusion, information gap, or counterintuitive takeaway.
- The headline should answer why a normal viewer should stop and watch: "what changed", "why it matters", or "what most people missed".
- Keep titles honest and specific. Avoid vague wording such as "AI 又有大事" unless the next line immediately names the event.

Preview card layout:

- Canvas stays `1080x1920`.
- Put one rounded white textured paper card inside a dark phone-like background.
- Top area: bold black title, usually 2 lines.
- Under the title: a purple rounded ribbon with white bold text.
- Middle area: one real topic-matched screenshot/photo/product image, inside a thin purple rounded border. Prefer a source/report screenshot, official page, real person, product screenshot, or company/product image over an abstract placeholder.
- Bottom area: paragraph-style explanatory copy, each wrapped line highlighted with cyan blocks. This is not the six-row info table.
- Add only a small `AI 信息差快报` positioning label. Do not add carousel dots, footer labels, decorative divider lines, or empty title bands.

Paper-card copy logic:

1. Start with the event in plain language.
2. Explain what a normal viewer should understand.
3. Explain the mechanism or business change behind it.
4. Name the risk, controversy, limitation, or opportunity.
5. End with `信息差：...` as the short takeaway.

Use `scripts/render_paper_card_preview.py` for a single static check before video rendering:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

## Default Creative Rules

- Canvas: `1080x1920`, 30 fps, default duration 7 seconds.
- Layout: title area on top, full-width image area in the middle, text rows in the lower area.
- Title style: 3 centered lines, heavy body weight `0.9`, oblique slant, pure fill colors, no drop shadow, no black offset, no glow, no highlight layer.
- Image motion: strong push-pull plus pan, no fade-flashing at cut points.
- Image count: prefer 5 images for a 7-second video.
- Image sourcing priority: real people/company/product photos first; official announcement/help/docs screenshots second; product entry/API/Codex screenshots third; media report screenshots fourth; auxiliary context images last.
- Failed image handling: do not leave downloader error cards, `图片源不可用`, `403`, `429`, Cloudflare blocks, or blank screenshots in final assets. Replace failed sources before rendering the final MP4.
- Timing: use beat cuts when known; otherwise use deterministic cuts from the config.
- Text rows: reveal one row at a time; put `结论` first to lower comprehension cost, then `跟你有关` to answer "what does this mean for me?" from a normal viewer's angle. Use `普通人机会` only when the row is explicitly about a concrete personal opportunity.
- Audio: no voiceover by default. Use local BGM from the BGM pool, commonly `start=3`, `duration=7`, `volume=0.55`, with tiny fade-in/out.
- Cover: for 小红书/抖音, make the cover from real people/company assets rather than a pure text card. Keep the headline dominant, protect the face, add a company logo badge, and show only one conclusion row.
- Output: one final MP4 plus a contact sheet or preview frame. When publishing to social platforms, also output a cover image.
- Export naming: final deliverables must use Chinese folder and file names. Separate `01-视频`, `02-封面`, and `03-总览`; include the topic in each folder/file name so the user can distinguish video, cover, and theme at a glance.
- Topic history: after each daily batch, write a Chinese `选题记录.md` or `topic-history.md` with date, topics, sources, and information-gap angles. Future auto-scout runs must review it before selecting topics.

## Iteration Rules

- When the user asks “先截图我看看”, render only a preview image.
- When the user confirms a style, preserve that choice in the config or script defaults.
- Do not reintroduce footer labels, carousel dots, decorative divider lines, or empty title bands unless the user asks.
- Keep `AI 信息差快报` as a small top-corner positioning label, not a bottom footer.
- If the user gives no new topic after a confirmed template, reuse the latest working project config and produce a new rendered file with a distinct name.

## BGM Pool And Selection

Use these local tracks as the default accompaniment pool for this skill. They are local user assets; do not upload the mp3 files to GitHub unless the user explicitly asks for that. For reproducible project builds, copy the selected track into the project's `assets/audio/` folder and point `bgm.path` at the copied relative path.

| Track | Local path | Best fit | Weight |
| --- | --- | --- | --- |
| `bba进行曲.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/bba进行曲.mp3` | major company moves, policy, infrastructure, safety, heavy/urgent topics | 3 |
| `时尚动感.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/时尚动感.mp3` | product launches, consumer apps, creator tools, stylish/tech topics | 1 |
| `时尚热情绽放.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/时尚热情绽放.mp3` | upbeat releases, creator economy, growth and opportunity angles | 1 |
| `do it.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/do it.mp3` | action-oriented tools, workflow tips, "what to do now" topics | 1 |
| `drink.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/drink.mp3` | lighter consumer stories, lifestyle/service AI, casual app updates | 1 |
| `moment.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/moment.mp3` | reflective business shifts, slower strategic topics, explainers | 1 |
| `say no cry.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/say no cry.mp3` | controversy, risk, tension, dispute, security and compliance topics | 1 |

BGM selection rules:

- Choose a short candidate set by topic mood first, then use weighted randomness inside that set. Do not pick purely at random from all tracks.
- Increase the chance of `bba进行曲.mp3` by including it in most serious/high-energy candidate sets with weight `3`; other matched tracks usually have weight `1`.
- For a 5-video daily batch, allow repeats when the theme strongly fits, but avoid using the same track for all five videos.
- Match examples:
  - `算力 / 芯片 / 大厂战略 / 政策安审`: `bba进行曲.mp3`, `say no cry.mp3`, `moment.mp3`.
  - `争议 / 风险 / 安全 / 合规`: `say no cry.mp3`, `bba进行曲.mp3`, `moment.mp3`.
  - `AI 视频 / 创作者 / 产品发布`: `时尚动感.mp3`, `时尚热情绽放.mp3`, `do it.mp3`.
  - `消费应用 / 本地生活 / 工具入口`: `drink.mp3`, `时尚动感.mp3`, `do it.mp3`.
  - `机会 / 方法 / 工作流`: `do it.mp3`, `时尚热情绽放.mp3`, `moment.mp3`.
- Use the same beat-cut logic as before. If a track has a clearly stronger downbeat later in the file, adjust `bgm.start` rather than changing the 7-second video duration.

## References

- Read `references/style-guide.md` when creating or editing a config.
- Patch `scripts/render_vertical_info_video.py` only when the workflow itself needs new reusable behavior.
