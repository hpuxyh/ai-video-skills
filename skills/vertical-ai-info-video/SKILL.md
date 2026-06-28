---
name: vertical-ai-info-video
description: "Generate 9:16 Chinese AI information-gap short videos and platform cover images with real news images, people-first cover thumbnails, bold no-glow headline typography, beat-synced multi-photo motion, full-set structured info rows, paper-card explainer previews, no voiceover, and local BGM mixing. Use when the user asks to make, iterate, or standardize vertical AI news/info-gap videos, 抖音/视频号/小红书竖屏快报, 封面图, 最近7天AI热点, 中美AI新闻, or says to use this short-video workflow skill."
---

# Vertical AI Info Video

## Overview

Use this skill to produce the fixed 9:16 AI 信息差短视频 workflow. The current default for daily/news-video production is the confirmed white paper-card video: a white textured 9:16 card, very bold black hook title at the top, one purple horizontal information-gap ribbon under the title, real five-image carousel in the middle, structured thin-line explainer rows at the bottom, no voiceover, and 7-second BGM from a local audio file.

It also preserves the older dark vertical fast-news template: people-first cover image, top positioning label, bold three-line title, real image carousel in the middle, bottom information rows revealed one by one, strong push-pull image motion, no voiceover, and 7-second BGM. Use the older dark template only when the user explicitly asks for the previous dark/normal fast-news style. For daily scheduled production and normal AI news-video output, use the white paper-card video workflow.

This skill is optimized for fast iteration. When the user asks for visual tuning, generate preview screenshots first. Render the full MP4 only after the user confirms the style.

## Workflow

1. Route the request:
   - If the user gives a concrete news topic, company, event, URL, or instruction, generate one video for that event using the confirmed workflow.
   - If the user does not give a concrete topic, search the latest 7 days of AI news, prioritize China/US high-signal stories, choose 5 distinct topics, and generate 5 separate one-event videos.
2. Confirm or infer each video's topic, title lines, info rows, image set, cover, and BGM.
3. Require real topic-matched images. For news videos, start with real people/company/product photos, then add official/news/product screenshots as supporting evidence. Do not use fake UI, abstract placeholders, or pure text cards as primary images.
4. For social publishing, generate a cover preview using the cover rules in `references/style-guide.md`: real person first, headline as the first visual layer, company logo as secondary recognition, and one conclusion row only.
5. Select background music from the local BGM pool using `scripts/select_bgm_for_batch.py`. For a 5-video batch, choose one track per video by theme fit plus weighted randomness, with `bba进行曲.mp3` favored, and validate that the batch is not accidentally inheriting the same BGM for every video.
6. Build a JSON config using the schema in `references/style-guide.md` and the production checklist in `references/paper-card-daily-production.md`. For daily/news-video output, build a white paper-card video JSON by default and render with `scripts/render_paper_card_video.py`; keep the same five-real-image carousel logic inside the middle media frame, keep the title entrance animation, and keep core tweet screenshots at about double hold time. Render a static preview first with `scripts/render_paper_card_preview.py` only when the user asks to see a screenshot. Use `scripts/render_vertical_info_video.py` only when the user explicitly asks for the older dark fast-news template.
   - After writing all batch configs and before rendering, run the BGM selector:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/select_bgm_for_batch.py \
  --project-dir . \
  --configs configs/*-paper-card.json \
  --write-plan renders/bgm-selection-plan.json
```

   - Do not let newly generated daily configs simply inherit an old `bgm` value. The selector must overwrite `bgm.path` for each config and copy the chosen audio into `assets/audio/`.
7. Run the image-sequence preflight before rendering. The first carousel image must identify the protagonist/company/product; source screenshots and auxiliary context images should appear later. If the check fails, reorder or replace the image set before rendering:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/check_image_sequence.py \
  --config configs/video.json \
  --project-dir . \
  --contact-sheet renders/image-sequence-preflight.jpg \
  --strict
```

8. Before rendering, inspect downloaded assets or a contact sheet. If an image source fails and produces an error/fallback card such as `图片源不可用`, `429`, `403`, a blank page, or a blocked page, replace it with a verified real image, local cached asset, official screenshot, or clean source card. Never ship a video with an asset-error card visible.
9. For the default daily/news-video workflow, run `scripts/render_paper_card_video.py` from a project directory:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_video.py \
  --config configs/paper-card-video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

If the user explicitly requests the legacy dark fast-news template, render with `scripts/render_vertical_info_video.py` instead.

10. Validate the MP4 with `ffprobe` and inspect the contact sheet before reporting completion.
11. Export every finished batch into the fixed creator-delivery directory under `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频` using the project-level delivery structure below. Each topic folder must contain only three core publishing files: `视频.mp4`, `封面.jpg`, and `文案.md`.
12. Record the finished topics in both the batch record and `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md`, then sync reusable skill/workflow updates to the user's GitHub repository when the skill or workflow rules changed.

## Delivery Output Contract

All finished news-video deliverables must live under the dedicated 小红书 creator directory:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/
  README.md
  选题历史.md
  导出-YYYY年MM月DD日AI信息差快报/
    01-主题名/
      视频.mp4
      封面.jpg
      文案.md
    02-主题名/
      视频.mp4
      封面.jpg
      文案.md
    ...
    项目总览.md
    _记录/
      视频总览-YYYY年MM月DD日AI信息差快报.jpg
      封面总览-YYYY年MM月DD日AI信息差快报.jpg
      选题记录.md
      渲染校验.md
      bgm-selection-plan.json
      素材与来源/
```

Each topic must include three user-facing outputs before it is considered complete:

- `视频.mp4`: final 9:16 video with BGM unless the user asked for silence.
- `封面.jpg`: 9:16 cover image using the people/company-first cover rules.
- `文案.md`: platform-ready 小红书 and 抖音 title, short description, tags, and one-line posting note.

Do not make the publishing surface category-first (`01-视频`, `02-封面`, `03-发布文案`) for new daily outputs. That older shape is only a temporary legacy/intermediate layout. If a renderer still emits the older layout, run `scripts/package_project_delivery.py` to create the clean project-level delivery folder before reporting completion.

Publishing copy defaults:

- 小红书标题: punchy, specific, 18-28 Chinese characters when possible, with the product/company name near the front.
- 小红书描述: 3-5 short lines. Start with the conclusion, then explain why it matters to a normal viewer, then end with a question or save-worthy takeaway.
- 小红书标签: 8-12 tags, mixing broad tags (`AI`, `人工智能`, `AI工具`) with topic-specific tags (`OpenAI`, `算力`, `大模型`, company/product names).
- 抖音标题: shorter and more direct than 小红书, usually 12-22 Chinese characters.
- 抖音描述: 1-3 compact lines; keep the strongest contrast and the viewer takeaway.
- Do not invent exaggerated claims just for a clickable title. The title can be sharp, but it must be supported by the verified source.

Daily-history rule:

- Before any auto-scout or daily batch, read `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md` plus any current batch `选题记录.md` files.
- Do not repeat the exact same news event, title angle, and viewer takeaway from history.
- A company may repeat only when the event is materially new and the `信息差` angle is different.
- After rendering, append each topic with date, topic name, companies/people, source links, information-gap angle, output paths, and whether it was manually requested or auto-scouted.

Default daily automation:

- The standing daily job is `AI信息差新闻视频-每日8点`.
- It runs every day at 08:00 Asia/Shanghai from `/Users/xieyahao/Documents/别人好项目`.
- The job should use this skill, search the latest 7 days when no concrete topic is provided, avoid historical repeats, generate the final cover/video/publishing-copy package under `小红/视频/新闻视频`, update `选题历史.md`, and sync skill/workflow changes to GitHub when the rules changed.
- Daily scheduled videos must use the confirmed white paper-card video logic by default: bold black title on the white card, purple information-gap ribbon, real five-image carousel, structured thin-line explainer rows, bottom rows visible as a full set, no dark ordinary template unless the user explicitly requests it.

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
- Keep all explanatory text in the template: the top title/ribbon and the bottom structured rows. For the default paper-card workflow, show the bottom rows as a full set.
- Do not create five standalone text cards as the five images. Text cards may only be minor overlays or fallback references, never the primary carousel.
- Use one event-specific row set from the viewer's path. The default paper-card row labels are `事件` / `关键` / `跟你有关` / `机会` or `风险/变化` / `信息差`.
- The target look for daily/news output is the approved white paper-card sample: black hook title, purple information-gap ribbon, real images in the middle, structured text rows below, beat-synced image cuts, no voiceover.

## Paper Card Explainer Mode

Use this mode for daily scheduled news videos and when the user approves or references the white-card examples: a white paper card, strong hook title, real screenshot/photo carousel in the center, and concise explanatory copy below. Treat it as the default creator-delivery video style unless the user explicitly asks for the older dark template.

For the video variant, do not flatten the preview into one static image. The outer paper card, black title, purple information-gap ribbon, bottom copy, and media border become the frame language, while the middle media area still runs the normal one-event five-image carousel with real photos/screenshots and light push-pull motion.

The paper-card video variant must preserve the title entrance rhythm: black title lines pop in one by one, then the purple ribbon expands in with the strongest information-gap sentence. Do not render the title as static text from frame 0 unless the user explicitly asks for a still preview.

Current structured paper-card flow:

- Use `title_on_purple: false` and `show_ribbon: true` for the approved default. Put line 1 and line 2 as very bold black text directly on the white card.
- Title line 1: who/source + a concrete fact, number, product, policy, or event.
- Title line 2: the direct consequence, contrast, or outcome in ordinary language.
- Use `title_color: [0, 0, 0]`, a large `title_size`, and short title lines before shrinking the font. Avoid glow, shadow, or colored title effects in this paper-card style.
- Use `strap` inside the purple horizontal ribbon for the normal-viewer interpretation, action hook, or information-gap sentence. The ribbon should not merely repeat the title.
- Keep the middle media frame bright and legible. It must show real event media, not a pre-rendered full-card image.
- Use exactly one event per video and usually five images: person/company/product recognition, core source/tweet screenshot, official report or evidence, product page, chart or supporting evidence.
- If the second image is the core tweet/X screenshot or localized tweet card, set `image_hold_weights: [1, 2, 1, 1, 1]` so it stays about twice as long as the other images.
- Use `body_rows` for the approved structured bottom area. The default visual style is `editorial_lines`: numbered rows (`01`-`05`), purple labels, thin dividers, and black explanatory text on the white card. Do not use cyan highlight blocks for daily videos unless the user asks to revisit that older preview style.
- Preferred labels: `事件`, `关键`, `跟你有关`, `机会` or `风险/变化`, `信息差`. Keep each bottom row short enough to scan in one glance. The label tells the viewer what kind of information the row contains; the text should be a plain Chinese sentence.

Title logic:

- Use a strong hook structure like the approved reference images, not a neutral news title.
- Top title: black, very bold, high-contrast, usually 1-2 lines. It must first say the concrete thing that happened, then name the biggest surprise or consequence.
- Use viewer-first headline logic: line 1 usually names the actor/source plus a concrete fact, number, product, or event; line 2 says the consequence in plain language. A casual viewer should not need the body copy to understand the basic story.
- Purple horizontal ribbon: carries the information gap, counterintuitive takeaway, or action hook. It should translate the fact into "what should I notice or do?", not repeat the title.
- The headline should make a normal viewer instantly understand "what happened?", "what does this have to do with me?", and "what is the biggest contrast here?"
- Keep titles honest and specific. Avoid vague wording such as "AI 又有大事" unless the next line immediately names the event.
- Avoid abstract summary headlines such as `Claude 用户最怕的事 / 高频用户反而更乐观`: they sound punchy but do not tell a normal viewer what happened. Prefer `超 1/3 Claude 用户说 / AI 一年内能接管大半工作`, with the ribbon `别只问会不会被替代，先学会分配任务`.

Preview card layout:

- Canvas stays `1080x1920`.
- Put one white textured paper card inside the 9:16 canvas, usually on a dark phone-like background.
- Card top: for the current structured default, use 1-2 very bold black hook-title lines, followed by a purple rounded ribbon.
- Show the latest verified news date on the card, preferably as a small top-right `最新：YYYY.MM.DD` marker. Do not rely only on a tiny date inside the embedded screenshot.
- Under the title: show one purple rounded ribbon with the information-gap sentence. Use the older purple title-panel layout only when the user explicitly asks for that old variant.
- Middle area: one real topic-matched news asset inside a thin purple rounded border. Use real news material, screenshots, people, product images, official pages, or company/product visuals. Do not use abstract placeholders as the main media.
- Bottom area: use the structured thin-line rows by default. Each row has a number, short purple label, thin divider, and one concise explanation. Cyan highlight blocks and paragraph-style highlights are older preview styles, not the current daily-video default.
- Add only a small `AI 信息差快报` positioning label. Do not add carousel dots, footer labels, decorative divider lines, or empty title bands.

Paper-card copy logic:

The bottom copy is not a second title and not a list of industry slogans. In the current structured default, it should be `body_rows` with labels and one-sentence explanations. It should explain the story in the order a normal viewer thinks:

1. Fact: start with the verified event in plain language. Include the key actor, source, date/context, number, product, or action when available.
2. Viewer meaning: explain what a normal viewer should understand or care about. Use concrete work, learning, creation, cost, access, or risk language.
3. Mechanism: explain what changed behind the scenes, such as product behavior, business model, policy, access, workflow, or infrastructure.
4. Boundary: name the risk, controversy, limitation, opportunity, or who is affected first.
5. Information gap: end with the `信息差` row as the short takeaway. This line should be a usable conclusion, not a slogan.

Every bottom line should be able to stand alone on screen. Avoid abstract phrasing such as `能力边界变化`, `工作流适配`, or `产业范式迁移` unless immediately translated into a concrete ordinary-life meaning.

The paper-card video mode is now the normal daily scheduled AI news-video template. The ordinary dark vertical template remains available only for explicit style requests.

Use `scripts/render_paper_card_preview.py` for a single static check before video rendering:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

Use `scripts/render_paper_card_video.py` when the approved paper-card style needs an MP4 while preserving the five-image carousel:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_video.py \
  --config configs/paper-card-video.json \
  --project-dir . \
  --output renders/paper-card-video.mp4 \
  --contact-sheet renders/paper-card-video-contact.jpg
```

## Default Creative Rules

- Canvas: `1080x1920`, 30 fps, default duration 7 seconds.
- Default template: white paper-card video. Use the legacy dark fast-news template only when the user explicitly requests it.
- Layout: white textured card on a dark phone-like background; black title and purple ribbon on top, real image carousel in the middle, structured rows in the lower area.
- Title style: 1-2 centered black hook-title lines, very bold, pure fill, no drop shadow, no black offset, no glow, no highlight layer. Keep the approved title entrance animation for MP4 output.
- Ribbon style: one purple horizontal information-gap ribbon under the black title. It should explain the viewer-facing takeaway and must not repeat the title.
- Image motion: strong push-pull plus pan, no fade-flashing at cut points.
- Image count: prefer 5 images for a 7-second video.
- Image sourcing priority: real people/company/product photos first; official announcement/help/docs screenshots second; product entry/API/Codex screenshots third; media report screenshots fourth; auxiliary context images last.
- Image sequence preflight: the first image must be a recognizable protagonist/company/product or official/product evidence image. Media screenshots should usually be slot 4-5, and auxiliary context images should not lead the carousel. Use `scripts/check_image_sequence.py --strict` before rendering.
- Failed image handling: do not leave downloader error cards, `图片源不可用`, `403`, `429`, Cloudflare blocks, or blank screenshots in final assets. Replace failed sources before rendering the final MP4.
- Timing: use beat cuts when known; otherwise use deterministic cuts from the config.
- Text rows: use `body_style: "editorial_lines"` and show all bottom rows as a full set by default. Preferred labels are `事件` / `关键` / `跟你有关` / `机会` or `风险/变化` / `信息差`. Do not animate rows one by one unless the user explicitly asks.
- Audio: no voiceover by default. Use local BGM from the BGM pool, commonly `start=3`, `duration=7`, `volume=0.55`, with tiny fade-in/out.
- Cover: for 小红书/抖音, make the cover from real people/company assets rather than a pure text card. Keep the headline dominant, protect the face, add a company logo badge, and show only one conclusion row.
- Output: one final MP4 plus a contact sheet or preview frame. When publishing to social platforms, also output a cover image.
- Export naming: final deliverables must use Chinese folder and file names. Use project-level topic folders, one folder per video topic, and keep only `视频.mp4`, `封面.jpg`, and `文案.md` in each topic folder. Put validation and source evidence under `_记录`.
- Topic history: after each daily batch, write a Chinese `选题记录.md` or `topic-history.md` with date, topics, sources, and information-gap angles. Future auto-scout runs must review it before selecting topics.
- Legacy dark template note: if explicitly requested, the older dark vertical template may still use three centered title lines and row-by-row reveal. Do not let those legacy rules override the daily white paper-card workflow.

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

- Always run `scripts/select_bgm_for_batch.py` after config generation and before rendering a daily/batch output.
- Choose a short candidate set by topic mood first, then use weighted randomness inside that set. Do not pick purely at random from all tracks.
- Increase the chance of `bba进行曲.mp3` by including it in most serious/high-energy candidate sets with weight `3`; other matched tracks usually have weight `1`.
- For a 5-video daily batch, allow repeats when the theme strongly fits, but do not allow all five videos to inherit or use the same track unless the user explicitly requests one unified BGM.
- Write a BGM selection plan such as `renders/bgm-selection-plan.json` and copy it into the batch's `_记录` folder.
- During validation, inspect final configs and confirm the `bgm.source_track` summary is not accidentally all one track.
- Match examples:
  - `算力 / 芯片 / 大厂战略 / 政策安审`: `bba进行曲.mp3`, `say no cry.mp3`, `moment.mp3`.
  - `争议 / 风险 / 安全 / 合规`: `say no cry.mp3`, `bba进行曲.mp3`, `moment.mp3`.
  - `AI 视频 / 创作者 / 产品发布`: `时尚动感.mp3`, `时尚热情绽放.mp3`, `do it.mp3`.
  - `消费应用 / 本地生活 / 工具入口`: `drink.mp3`, `时尚动感.mp3`, `do it.mp3`.
  - `机会 / 方法 / 工作流`: `do it.mp3`, `时尚热情绽放.mp3`, `moment.mp3`.
- Use the same beat-cut logic as before. If a track has a clearly stronger downbeat later in the file, adjust `bgm.start` rather than changing the 7-second video duration.

## References

- Read `references/style-guide.md` when creating or editing a config.
- Read `references/paper-card-daily-production.md` before daily batches, batch rerenders, or workflow updates. It contains the fixed white-paper-card production logic, copy rules, delivery checklist, validation checklist, and a record of the approved 2026-06-28 second-batch title pattern.
- Use `examples/white-paper-card-batch-manifest.example.json` as the canonical manifest shape when turning selected topics into reusable configs, videos, covers, publishing copy, and source records.
- Patch `scripts/render_vertical_info_video.py` only when the workflow itself needs new reusable behavior.
