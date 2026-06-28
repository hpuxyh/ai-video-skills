---
name: vertical-ai-info-video-推特版
description: "Generate 9:16 Chinese AI information-gap short videos from recent X/Twitter AI hotspots, with the second carousel image fixed as a verified core tweet screenshot, plus real news/product images, people-first covers, bold no-glow headline typography, beat-synced motion, paper-card previews, no voiceover, and local BGM mixing. Use when the user asks for 推特版 AI 信息差短视频, X/Twitter AI 热点, 近2-3天 AI 热点, or a tweet-anchored vertical AI news video."
---

# Vertical AI Info Video - 推特版

## Overview

Use this skill to produce the X/Twitter-first version of the fixed 9:16 AI 信息差短视频 workflow: find recent AI hotspots on X/Twitter, confirm the topic with a core tweet from the relevant person or official account, place that tweet screenshot as the second carousel image, then keep the original video system: people-first cover image, top positioning label, bold three-line title, real image carousel in the middle, bottom information rows revealed one by one, strong push-pull image motion, no voiceover, and 7-second BGM from a local audio file.

The defining rule of this version is: every auto-scouted topic must have a verified tweet anchor. The second image in the video carousel must be a clean screenshot of the core tweet that confirms why this topic exists. Because viewers need time to read it, image 2 should hold for roughly twice as long as the other carousel images.

The final audience-facing output must be Chinese-first. If the source tweet, chart, UI, or screenshot is in English, keep the original asset for traceability, then create a Chinese-localized tweet card or overlay so the final image/video can be understood without reading English. Product names, company names, handles, and short technical terms may remain in English when they help recognition.

This version must preserve the original real-visual carousel logic. X/Twitter changes the topic discovery and proof chain only; it must not turn the video into a deck of self-made explainer cards. The middle image area should stay bright, real, and evidence-like: people, company/product photos, official pages, product UI, news screenshots, and one tweet anchor.

It also supports the confirmed paper-card explainer mode: a white textured 9:16 card with a strong black headline, purple information-gap ribbon, real news media in the middle, and cyan-highlighted explanatory copy at the bottom. Use this mode when the user references the white card examples, asks for "参考这种图文卡样式", or wants a static rendered image before video production.

This skill is optimized for fast iteration. When the user asks for visual tuning, generate preview screenshots first. Render the full MP4 only after the user confirms the style.

## Workflow

1. Route the request:
   - If the user gives a concrete news topic, company, event, URL, tweet URL, or instruction, use the given topic directly and generate one video for that event using the confirmed workflow.
   - If the user does not give a concrete topic, default to daily auto-scout: search X/Twitter for AI-related hotspots from the latest 2-3 days, build a candidate pool, verify the strongest candidates with official/news sources when needed, and generate 5 one-event videos.
2. Confirm or infer each video's topic, three-line animated title, info rows, image set, cover, BGM, and tweet anchor.
3. Before choosing or rendering topics, check the GitHub-synced history records and local `选题记录.md` / `topic-history.md`. Do not produce a duplicate, identical topic that has already been successfully rendered. A topic is duplicate if the same company/person/product, same event, same source tweet, and same information-gap angle already exist in history.
4. Require one verified tweet anchor for every topic. Prefer the direct X/Twitter post from the core person involved in the event; if no person tweet exists, use an official company/product/research account. If only third-party commentary exists, use it only as a discovery signal, not as the anchor.
5. Require bright, real, topic-matched images. For news videos, image 1 should be a real person/company/product visual, image 2 must be the verified core tweet screenshot or Chinese-localized tweet card derived from it, and later images should add official/news/product evidence. Do not use fake UI, abstract placeholders, dark information cards, or pure text cards as primary carousel images.
6. For social publishing, generate a cover preview using the cover rules in `references/style-guide.md`: real person first, company/product identity second, the same three animated title lines as the main cover headline, and one conclusion row only. If the visible product is backed by a larger parent company, trace that lineage before choosing the cover visual; do not stop at a narrow product-page screenshot when a stronger parent-company person or identity is available.
7. Select background music from the local BGM pool using the BGM rules below. For a 5-video batch, choose one track per video by theme fit plus weighted randomness, with `bba进行曲.mp3` favored.
8. Build a JSON config using the schema in `references/style-guide.md`. For paper-card explainer mode, build a paper-card JSON and render a static preview first with `scripts/render_paper_card_preview.py`.
9. Before rendering, inspect downloaded assets or a contact sheet. If the tweet screenshot, image source, or fallback card shows `图片源不可用`, `429`, `403`, login wall, a blank page, a blocked page, or unrelated search results, replace it before rendering. Never ship a video with an asset-error card visible.
10. Run `scripts/render_vertical_info_video.py` from a project directory:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/render_vertical_info_video.py \
  --config configs/video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

11. Validate the MP4 with `ffprobe` and inspect the contact sheet before reporting completion.
12. After validation, organize final deliverables under the dedicated Xiaohongshu video export folder. The user-facing handoff should be project-first: each topic gets one folder with only the final MP4 and cover image, and the batch root gets one overall copy file:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/
  导出-YYYY年MM月DD日-推特版AI信息差快报/
    01-中文话题名/
      视频.mp4
      封面.jpg
    02-中文话题名/
      视频.mp4
      封面.jpg
    整体描述.md
```

The folder name must clearly include `推特版` or `推特专用` so it is not confused with ordinary AI 信息差 videos.
13. Record the finished topics, source tweet URL, source tweet author, observed engagement signal, source URLs, information-gap angle, and final export folder in `整体描述.md`, local history records, and the GitHub-synced history records. Keep detailed source screenshots/configs in the working project or GitHub records, not mixed into the user-facing project folders unless the user asks for them.
14. Every successful invocation must sync to GitHub before reporting completion. Commit and push the history records, source notes, configs, and deliverable index. Include final media assets when practical for the target repo; at minimum, the GitHub history must contain enough metadata to prevent future duplicate topics and trace each output.

## Topic Selection Modes

- Specific-topic mode: use the user's topic directly. Verify current facts when the topic is recent or time-sensitive, then create one cover and one video.
- X/Twitter auto-scout mode: when no concrete topic is provided, search the latest 2-3 days of AI discussion on X/Twitter first, then select 5 topics with strong AI 信息差信号.
- X/Twitter selection criteria: do not simply pick posts with the largest number. Build a candidate pool first, then pick the stories most suitable for AI 信息差短视频: viewer relevance, clear information gap, recognizable people/companies, available real imagery, platform-friendly tension, and a clean tweet anchor.
- Heat judgment: treat X/Twitter engagement as a signal, not the only proof. Consider views, reposts, likes, replies, account authority, quote-post spread, whether AI builders are discussing it, and whether official/news sources can verify the underlying event.
- Daily freshness: before selecting auto-scout topics, check previous generated batches, local topic-history files, and the GitHub-synced history records. Do not choose the exact same event/topic as an earlier successful batch unless the user explicitly asks for a follow-up angle. If a company repeats, the event and information-gap angle must be materially different.
- Auto-scout output: generate 5 independent videos, not one compilation. Each video keeps the same row logic, image logic, cover logic, and verification steps.
- Before rendering 5 videos, show the chosen 5 topics with one-line rationale, tweet anchor, likely cover assets, and the information-gap angle when the user has not already approved the topic list.

## Daily Execution Logic

- If the user provides a topic, tweet URL, company, event, or concrete instruction, do not auto-scout a new batch. Produce the requested topic only.
- If the user does not provide a topic, default to finding 5 hot X/Twitter AI topics from the latest 2-3 days.
- "Hot" does not mean likes-only. Rank candidates by tweet heat, account authority, quote/reply spread, source credibility, viewer relevance, information-gap strength, and available real assets.
- Before finalizing the 5 topics, check GitHub-synced history and local topic history. Reject exact repeats.
- A non-duplicate follow-up is allowed only when there is a materially new development, a new source tweet, or a different information-gap angle.
- After each successful run, update the history records and sync them to GitHub before telling the user the run is complete.

## Tweet Anchor Rules

- The second carousel image must be the topic-confirming X/Twitter screenshot.
- The tweet anchor should look like a bright, source-like artifact. The preferred default is the previously approved proof-card layout: a cleaned real tweet screenshot on the left, a Chinese interpretation block on the right, and source metadata at the bottom-left. Do not show internal timing notes such as "第二张图停留加长" in the final audience-facing card.
- For this proof-card layout, do not turn the frame into a new headline card. Use `中文释义` as the small purple label, then 3-5 cyan highlighted Chinese lines that summarize the tweet's core fact and viewer meaning. For daily batch videos, prefer 5 lines: concrete fact, direct change, normal-viewer meaning, mechanism/boundary, and `信息差：...`. Keep the original tweet visible for credibility.
- The typography should be tidy and consistent: at 1600x1000 source-card size, use roughly 34-40px bold Chinese for cyan highlighted lines, 29-34px for small labels, 23-26px for URL/source metadata, with even line height and aligned left edges. Prefer uniform full-width cyan highlight bars on the right side for cleaner video readability. If a line wraps into a single character or orphan word, rewrite the sentence shorter before shrinking below the normal font range.
- Prefer direct posts by the core person in the story: founder, CEO, product lead, researcher, government official, creator of the tool, or other primary actor.
- If no core-person post exists, use the official account for the company, product, lab, open-source project, or conference.
- If the topic is discovered through a third-party viral post, use that post for discovery only; then find a primary-source tweet, official page, or reputable report before making the final topic.
- The screenshot should show the author, handle, post text, timestamp/date, and visible engagement when available.
- Crop the screenshot to the tweet body or post card. Preserve the author/avatar, handle, key tweet text, timestamp or visible engagement when available, and the main attached image/video/logo. Avoid narrow crops that cut off faces, avatars, company logos, product names, or the main media. Avoid showing right-side sign-up panels, bottom login banners, unrelated replies, blank loading areas, or browser chrome unless they are unavoidable and do not distract.
- In a 5-image, 7-second video, give the tweet-anchor image about twice the hold time of other images. Prefer `image_hold_weights: [1, 2, 1, 1, 1]`, which yields cuts around `[1.17, 3.50, 4.67, 5.83]`.
- If the tweet is not in Chinese, produce a Chinese-localized final card: preserve author, handle, date, visible engagement, and source URL in notes; translate/summarize the tweet body in Chinese; translate important chart labels or add a Chinese caption explaining the chart. The raw English screenshot can be stored as evidence, but it should not be the only audience-facing explanation.
- Do not use screenshots that show login walls, Cloudflare checks, cookie walls, `403`, `429`, "Something went wrong", blank pages, or unrelated search results.
- If a clean tweet screenshot cannot be captured, choose another tweet or another topic.
- Store the source tweet URL next to the image path in the working notes or topic history so the screenshot can be traced.
- Use `scripts/render_tweet_proof_card.py` when turning a raw tweet screenshot into the preferred Chinese proof card:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/render_tweet_proof_card.py \
  --config configs/tweet-proof-card.json \
  --project-dir . \
  --output assets/images/event/02-核心推文中文卡.jpg
```

## One-Event Video Logic

- Treat each video as one news event, not a multi-card slideshow of separate text panels.
- Attach multiple real images to that single event. Use them as the middle carousel only. The carousel should not become a sequence of self-made explanation cards.
- Keep image 2 as the tweet anchor. The rest of the image order can vary only if the user explicitly asks, but the default is:
  1. Real person/company/product/event visual, preferably a recognizable person when the topic has one.
  2. Bright core tweet screenshot or Chinese-localized tweet card derived from it.
  3. Official announcement, product page, docs, report, or release note screenshot.
  4. Real product/API/app screenshot or reputable media report screenshot.
  5. Related person, company, product, office, event, or real-world context image.
- Keep all explanatory text in the template: the top title and the bottom one-by-one info rows.
- Do not create five standalone text cards as the five images. Text cards may only be minor overlays or fallback references, never the primary carousel.
- Use one event-specific info-row set from the viewer's path: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.
- The target look is the previously approved White House safety-review sample, with one important change: the second image is always the clean X/Twitter source screenshot or Chinese-localized tweet card that confirms the topic.

## Animated Title And Cover Text Logic

Use one shared three-line hook as the main title system for normal 推特版 videos. The video shows these lines with the original line-by-line pop animation; the cover reuses the same three lines as its large headline. Do not invent a separate cover headline unless the user explicitly asks for a different cover copy.

Three-line structure:

1. Line 1: protagonist, company, product, source, or core event. Name the concrete actor first so the viewer immediately knows who the story is about.
2. Line 2: the direct change, action, launch, entry, response, or new state. This line explains what just changed.
3. Line 3: the normal-viewer hook: the consequence, contrast, information gap, risk, or useful takeaway. This is usually the strongest line and can use heavier color/emphasis.

Language style:

- Write like a short-video hook, not a neutral news headline.
- Prefer concrete, ordinary language over technical abstraction.
- Make the third line translate the event into "what this means" for normal viewers.
- Keep each line short enough for mobile reading. Shorten wording before shrinking the title too much.
- Keep the line-by-line title animation in final videos.

Current batch examples:

```text
GPT-5.6 要来了？
但普通人
还不能直接用

Google Finance
接入 AI 研究工具
看盘变成投资助理

Seedance 2.0
直接冲到 4K
AI 视频更像实拍

Claude 进入 Slack
不只是聊天助手
还会记住公司

A24 回应 Google AI
电影圈开始抢规则
创作者要争边界
```

Cover and card text rule:

- Normal 小红书/抖音 covers use the same three lines above as the cover headline.
- The cover should not switch to a separate paper-card title or a tweet-screenshot title.
- The cover headline can be larger, heavier, and arranged around the real person/company/product visual, but the words should remain the same as the video title unless the user asks to rewrite them.
- Cover headline typography should be clean, bright, and heavy: use a large white first line, flat topic-accent colors for the second/third lines, and a white stroke/rim only to keep the text readable on photos. A very soft translucent gray lift is allowed, but do not use black thick outlines, black offset shadows, neon colors, glow layers, or glowing edges.
- The company/product badge on the cover should use the company's classic logo or wordmark when available, not a plain typed company name. For combined stories, use paired logos such as `A24 × Google`.
- Do not draw large standalone topic serial numbers such as `01`, `02`, `03`, or `04` on the cover background or cover overview tiles. In the approved full-bleed quick-report cover style, the bottom conclusion strip may include a small left-side `01`-style badge as a visual anchor.
- Cover visuals should prefer event people first, then representative company people, then company identity/mascot/logo, then product screenshots. For example, Google-related covers can use Sundar Pichai or a strong Google identity image; Claude/Anthropic covers can use Dario Amodei or a strong Anthropic/Claude identity image before falling back to product UI.
- For subsidiary or product-line stories, identify the backing company and use that recognition layer when it helps normal viewers. Example: Coze, BytePlus, Seedance, and Doubao are ByteDance-family topics; if no direct product lead is more suitable, consider Zhang Yiming as ByteDance founder/representative figure, or use ByteDance/Doubao/BytePlus/Coze brand visuals before falling back to a generic product screenshot.
- Do not force the tweet proof card or middle carousel source cards to repeat the full three-line hook. The three-line hook belongs to the animated title and cover; the middle carousel should remain evidence-like.
- Image 2 should use the tweet proof-card layout above: left real tweet screenshot, right Chinese cyan-highlight interpretation, and bottom source metadata. Do not show timing or production notes on the card.
- Other middle carousel cards should stay visually simple: one real visual focus plus at most 1-2 short Chinese caption lines. Avoid stuffing the top title, bottom rows, and long explanation into the image itself because those layers already exist in the video template.
- Never expose internal production instructions in final images, covers, contact sheets, or videos. Remove phrases such as `第二张图停留加长，方便读推文`, `人物优先`, `脸部完整`, `真实素材优先`, `只保留一句说明`, `先看背后公司是谁`, crop notes, hold-time notes, asset-selection rationale, and other operator-facing text. Replace them with viewer-facing facts such as the person name, company name, product name, source label, or one concrete event caption.

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
- Show the latest verified news date on the card, preferably as a small top-right `最新：YYYY.MM.DD` marker. Do not rely only on a tiny date inside the embedded screenshot.
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
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

## Default Creative Rules

- Canvas: `1080x1920`, 30 fps, default duration 7 seconds.
- Layout: title area on top, full-width image area in the middle, text rows in the lower area.
- Title style: 3 centered animated lines, heavy body weight `0.9`, oblique slant, pure fill colors, no drop shadow, no black offset, no glow, no highlight layer. Keep the original line-by-line pop animation.
- Image motion: strong push-pull plus pan, no fade-flashing at cut points.
- Image count: prefer 5 images for a 7-second video.
- Middle image brightness: the carousel images should be bright and legible. Avoid dark cards, black backgrounds, low-contrast screenshots, or heavy overlays in the photo box. If a real source is dark, use `photo_fit: "contain"` with a bright blurred/background treatment or choose a brighter asset.
- Image sourcing priority: real people/company/product photos first; the bright verified core tweet screenshot second; official announcement/help/docs screenshots third; product entry/API/Codex screenshots fourth; media report screenshots fifth; auxiliary context images last.
- Real-visual crop safety: before rendering, inspect each carousel panel or contact sheet. Person images must preserve the full face and recognizable body/gesture when possible. Company/product screenshots must preserve the logo, product name, and central UI/visual; do not crop away the first word, logo, face, or main object.
- Horizontal page handling: for wide official pages, product pages, and news pages, do not force a cover-fill crop when it cuts off important text or visuals. Prefer `contain` inside a bright rounded card, with only the blurred background filling the frame.
- Carousel copy limit: real images may carry one short Chinese caption or at most two simple lines. Do not rebuild images 1/3/4/5 as dense text cards; the title and bottom rows already carry the explanation.
- Text-card boundary: self-made explainer cards are allowed only as minor support assets when no better real image exists. They must not replace the person/product/official-page logic, and they must not dominate a 5-image carousel.
- Failed image handling: do not leave downloader error cards, `图片源不可用`, `403`, `429`, Cloudflare blocks, or blank screenshots in final assets. Replace failed sources before rendering the final MP4.
- Language handling: final visible titles, labels, rows, captions, chart explanations, and tweet-summary text should be Chinese. Do not leave an English tweet screenshot as the only readable explanation in the final artifact.
- Timing: for tweet-anchored videos, keep total duration at 7 seconds but hold image 2 for about 2x the other images by setting `image_hold_weights: [1, 2, 1, 1, 1]`. Use manual `beat_cuts` only when the user asks for a music-specific exception.
- Text rows: reveal one row at a time; put `结论` first to lower comprehension cost, then `跟你有关` to answer "what does this mean for me?" from a normal viewer's angle. Use `普通人机会` only when the row is explicitly about a concrete personal opportunity.
- Audio: no voiceover by default. Use local BGM from the BGM pool, commonly `start=3`, `duration=7`, `volume=0.55`, with tiny fade-in/out.
- Cover: for 小红书/抖音, make the cover from real people/company assets rather than a pure text card. Use the approved full-bleed quick-report style by default: bright full-screen person/company visual, top-left `重磅` tag, top-right `AI 信息差快报` pill, white classic-logo badge near the title, the same three animated title lines as a large lower-third headline, and one bottom conclusion strip. The cover title should use clean heavy typography: white first line, flat accent-color second/third lines, white stroke/rim for readability, and no black thick outline or glow. Protect the face and full representative subject. The conclusion strip may use a small `01`-style badge, but do not add big standalone topic numbers. If there is no suitable product/event person, check the parent company or backing company for a more recognizable representative person or brand asset before using a product page screenshot. If no person is suitable, use the company's logo/product page/official visual and preserve the complete brand/product identity.
- Output: one final MP4 plus a contact sheet or preview frame. When publishing to social platforms, also output a cover image.
- Export destination: final 推特版 deliverables must be organized under `/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/`. Temporary render files can stay in the project folder during iteration, but the handoff-ready batch must be copied or rendered into this dedicated folder.
- Export naming: final user-facing deliverables must use Chinese folder and file names. The top-level batch folder should include `推特版` or `推特专用`; inside it, create one numbered topic folder per project. Each topic folder contains only `视频.mp4` and `封面.jpg`. Put the batch title/copy/description for all topics in one root `整体描述.md`. Keep source screenshots, configs, overviews, and detailed history in the working project or GitHub records.
- Topic history: after each daily batch, write a Chinese `选题记录.md` or `topic-history.md` with date, topics, sources, and information-gap angles. Future auto-scout runs must review it before selecting topics.

## Iteration Rules

- When the user asks “先截图我看看”, render only a preview image.
- When the user confirms a style, preserve that choice in the config or script defaults.
- Do not reintroduce footer labels, carousel dots, decorative divider lines, or empty title bands unless the user asks.
- Keep `AI 信息差快报` as a small top-corner positioning label, not a bottom footer.
- If the user gives no new topic after a confirmed template, reuse the latest working project config only when its tweet anchor is still relevant. Otherwise scout a fresh X/Twitter topic.

## Export Destination

All handoff-ready videos produced by this 推特版 skill should be placed under:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/
```

Use this batch structure:

```text
导出-YYYY年MM月DD日-推特版AI信息差快报/
  01-中文话题名/
    视频.mp4
    封面.jpg
  02-中文话题名/
    视频.mp4
    封面.jpg
  03-中文话题名/
    视频.mp4
    封面.jpg
  整体描述.md
```

Rules:

- Do not leave final deliverables only inside a temporary project `renders/` directory.
- Do not split the user-facing export into `01-视频`, `02-封面`, `03-总览`, and `04-素材与来源` unless the user explicitly requests the old structure.
- Keep iteration previews, contact sheets, overviews, configs, and detailed source notes in the working project while tuning; copy only the approved MP4, cover, and one root `整体描述.md` into the handoff-ready Xiaohongshu export folder.
- GitHub/local source records should include the source tweet URL, tweet author, observed heat signal, screenshot filename, supporting source URLs, and why this topic is suitable for a 推特版 AI 信息差 video.
- The folder or file name must clearly say `推特版` or `推特专用`.

## GitHub Sync And History

Every successful invocation must be synced to GitHub.

Sync target:

```text
/Users/xieyahao/Documents/别人好项目/ai-video-skills/
```

Recommended GitHub history location:

```text
records/twitter-ai-info-video/
  topic-history.md
  YYYY-MM-DD/
    batch-summary.md
    01-中文话题名/
      来源记录.md
      config.json
      output-index.md
```

Sync rules:

- Before selecting topics, read the GitHub-synced `records/twitter-ai-info-video/topic-history.md` when present, plus local batch histories.
- After a successful run, append the selected topics to `topic-history.md`.
- Record enough fields to block duplicates later: date, topic title, company/product/person, source tweet URL, source tweet author, observed heat signal, supporting source URLs, information-gap angle, final export folder, and output filenames.
- Commit and push after each successful invocation. Do not report the run as fully complete until the GitHub sync succeeds or the sync failure is clearly reported.
- If final MP4 files are too large or unsuitable for the skill repository, still sync topic history, source records, configs, output index, and local export paths so future runs can avoid duplicate topics.

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
