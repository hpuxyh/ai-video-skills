---
name: vertical-ai-info-video
description: "Generate 9:16 Chinese AI information-gap short videos and platform cover images with real news images, people-first cover thumbnails, bold no-glow headline typography, beat-synced multi-photo motion, one-by-one info rows, no voiceover, and local BGM mixing. Use when the user asks to make, iterate, or standardize vertical AI news/info-gap videos, 抖音/视频号/小红书竖屏快报, 封面图, 最近7天AI热点, 中美AI新闻, or says to use this short-video workflow skill."
---

# Vertical AI Info Video

## Overview

Use this skill to produce the fixed 9:16 AI 信息差短视频 workflow: people-first cover image, top positioning label, bold three-line title, real image carousel in the middle, bottom information rows revealed one by one, strong push-pull image motion, no voiceover, and 7-second BGM from a local audio file.

This skill is optimized for fast iteration. When the user asks for visual tuning, generate preview screenshots first. Render the full MP4 only after the user confirms the style.

## Workflow

1. Route the request:
   - If the user gives a concrete news topic, company, event, URL, or instruction, generate one video for that event using the confirmed workflow.
   - If the user does not give a concrete topic, search the latest 7 days of AI news, prioritize China/US high-signal stories, choose 5 distinct topics, and generate 5 separate one-event videos.
2. Confirm or infer each video's topic, title lines, info rows, image set, cover, and BGM.
3. Require real topic-matched images. For news videos, start with real people/company/product photos, then add official/news/product screenshots as supporting evidence. Do not use fake UI, abstract placeholders, or pure text cards as primary images.
4. For social publishing, generate a cover preview using the cover rules in `references/style-guide.md`: real person first, headline as the first visual layer, company logo as secondary recognition, and one conclusion row only.
5. Build a JSON config using the schema in `references/style-guide.md`.
6. Run `scripts/render_vertical_info_video.py` from a project directory:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_vertical_info_video.py \
  --config configs/video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

7. Validate the MP4 with `ffprobe` and inspect the contact sheet before reporting completion.

## Topic Selection Modes

- Specific-topic mode: use the user's topic directly. Verify current facts when the topic is recent or time-sensitive, then create one cover and one video.
- Auto-scout mode: when no concrete topic is provided, search the latest 7 days of AI news across US and China, then select 5 topics before rendering.
- Auto-scout selection criteria: do not simply pick the top 5 headlines. Build a candidate pool first, then pick the 5 stories most suitable for AI 信息差短视频: viewer relevance, clear information gap, recognizable people/companies, available real imagery, and platform-friendly tension. Avoid duplicates, low-signal funding-only items, vague opinion pieces, and stories without usable real images.
- Auto-scout output: generate 5 independent videos, not one compilation. Each video keeps the same row logic, image logic, cover logic, and verification steps.
- Before rendering 5 videos, show the chosen 5 topics with one-line rationale, likely cover assets, and the information-gap angle when the user has not already approved the topic list.

## One-Event Video Logic

- Treat each video as one news event, not a multi-card slideshow of separate text panels.
- Attach multiple real images to that single event. Use them as the middle carousel only.
- Keep all explanatory text in the template: the top title and the bottom one-by-one info rows.
- Do not create five standalone text cards as the five images. Text cards may only be minor overlays or fallback references, never the primary carousel.
- Use one event-specific info-row set from the viewer's path: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.
- The target look is the previously approved White House safety-review sample: large top headline, real images in the middle, structured text rows below, beat-synced image cuts, no voiceover.

## Default Creative Rules

- Canvas: `1080x1920`, 30 fps, default duration 7 seconds.
- Layout: title area on top, full-width image area in the middle, text rows in the lower area.
- Title style: 3 centered lines, heavy body weight `0.9`, oblique slant, pure fill colors, no drop shadow, no black offset, no glow, no highlight layer.
- Image motion: strong push-pull plus pan, no fade-flashing at cut points.
- Image count: prefer 5 images for a 7-second video.
- Image sourcing priority: real people/company/product photos first; official announcement/help/docs screenshots second; product entry/API/Codex screenshots third; media report screenshots fourth; auxiliary context images last.
- Timing: use beat cuts when known; otherwise use deterministic cuts from the config.
- Text rows: reveal one row at a time; put `结论` first to lower comprehension cost, then `跟你有关` to answer "what does this mean for me?" from a normal viewer's angle. Use `普通人机会` only when the row is explicitly about a concrete personal opportunity.
- Audio: no voiceover by default. Use local BGM, commonly `start=3`, `duration=7`, `volume=0.55`, with tiny fade-in/out.
- Cover: for 小红书/抖音, make the cover from real people/company assets rather than a pure text card. Keep the headline dominant, protect the face, add a company logo badge, and show only one conclusion row.
- Output: one final MP4 plus a contact sheet or preview frame. When publishing to social platforms, also output a cover image.

## Iteration Rules

- When the user asks “先截图我看看”, render only a preview image.
- When the user confirms a style, preserve that choice in the config or script defaults.
- Do not reintroduce footer labels, carousel dots, decorative divider lines, or empty title bands unless the user asks.
- Keep `AI 信息差快报` as a small top-corner positioning label, not a bottom footer.
- If the user gives no new topic after a confirmed template, reuse the latest working project config and produce a new rendered file with a distinct name.

## References

- Read `references/style-guide.md` when creating or editing a config.
- Patch `scripts/render_vertical_info_video.py` only when the workflow itself needs new reusable behavior.
