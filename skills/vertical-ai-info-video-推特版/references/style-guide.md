# Style Guide

## Config Schema

Use a JSON file with these top-level keys:

```json
{
  "duration": 7,
  "fps": 30,
  "output": "renders/output.mp4",
  "contact_sheet": "renders/output-contact-sheet.jpg",
  "header": {
    "brand": "AI 信息差快报",
    "tag": "重磅",
    "category": "法律 · AI 安全",
    "source": "AP News · 2026.06.27"
  },
  "title": [
    {"text": "OpenAI × Anthropic", "y": 126, "size": 88, "color": [236, 255, 255]},
    {"text": "新模型先过白宫安审", "y": 218, "size": 100, "color": [255, 255, 255]},
    {"text": "获批客户才可提前试用", "y": 344, "size": 94, "color": [255, 145, 118]}
  ],
  "info_rows": [
    {"label": "结论", "text": "顶级 AI 发布前，先过安全审查"},
    {"label": "跟你有关", "text": "别只等新模型，先用现有 AI 整理资料、写方案"},
    {"label": "发生", "text": "OpenAI 与 Anthropic 被纳入审查"},
    {"label": "谁先用", "text": "获批客户才可提前试用"},
    {"label": "影响", "text": "最强模型开放节奏会变慢"},
    {"label": "信息差", "text": "发布不等于人人可用，入口才是关键"}
  ],
  "images": [
    "assets/images/event1/event1-01.jpg",
    "assets/images/event1/event1-02-tweet.jpg",
    "assets/images/event1/event1-03.jpg"
  ],
  "tweet_anchor": {
    "url": "https://x.com/example/status/123",
    "author": "Core Person or Official Account",
    "screenshot": "assets/images/event1/event1-02-tweet.jpg",
    "observed_signal": "views / reposts / likes / replies when captured"
  },
  "image_hold_weights": [1, 2, 1, 1, 1],
  "bgm": {
    "path": "assets/audio/bba进行曲.mp3",
    "start": 3,
    "volume": 0.55,
    "fade_in": 0.08,
    "fade_out": 0.35
  }
}
```

All relative paths resolve from `--project-dir`.

## Paper Card Preview Config Schema

Use this schema when the user asks for the approved white-card reference style or wants a rendered image before full video production:

```json
{
  "output": "renders/paper-card-preview.jpg",
  "badge": "AI 信息差快报",
  "date_label": "最新",
  "date": "2026.06.28",
  "title": [
    "SpaceX 开始出租 AI 算力",
    "开源模型公司抢 GPU 入口"
  ],
  "strap": "真正稀缺的不是模型，是算力",
  "image": "assets/images/event/source-screenshot.jpg",
  "body": [
    "重磅！Reflection AI 签下 SpaceX 的计算资源，开源模型公司开始租顶级 GPU。",
    "这说明 AI 竞争不只是谁模型更强，更是谁能拿到更便宜、更稳定的算力。",
    "对普通人来说，AI 服务变贵、变慢、限量开放，背后常常不是产品问题，而是 GPU 不够。",
    "小团队如果能租到巨头机房，就有机会用更低成本挑战闭源大模型。",
    "信息差：未来 AI 入口可能不在 App，而在谁掌握芯片和机房。"
  ]
}
```

Render it with:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

## Request Routing

Use two modes:

1. Specific-topic mode: if the user gives a concrete topic, event, company, URL, or direct instruction, create one video for that event.
2. X/Twitter auto-scout mode: if the user asks for an AI information-gap video but does not provide a concrete topic, search the latest 2-3 days of AI discussion on X/Twitter first, then choose 5 topics that have a strong tweet anchor plus enough real supporting assets.

In auto-scout mode:

- Search current X/Twitter sources because the 2-3 day window is time-sensitive.
- Before choosing topics, review previous generated batches in the workspace, dated export folders, any local `选题记录.md` / `topic-history.md` files, and GitHub-synced history under `records/twitter-ai-info-video/`. Treat these as the duplicate-prevention source of truth.
- Prefer China/US/global AI stories with clear X/Twitter discussion value: model releases, product demos, policy/regulation, safety/security, AI hardware, agent/tools, major company moves, open-source releases, and consumer/workflow impact.
- Start from a candidate pool of roughly 15-30 recent X/Twitter signals when possible, then narrow down to 5. The goal is not "the top 5 posts by engagement"; the goal is "the 5 tweet-anchored stories most suitable for AI 信息差短视频".
- Score candidates by:
  - Normal-viewer relevance: can a casual viewer understand why it matters to work, creation, tools, learning, business, or daily AI use?
  - Information-gap strength: is there a non-obvious takeaway beyond the surface headline?
  - X/Twitter heat and authority: is the post from a core person or official account, and does it show meaningful views, reposts, likes, replies, quotes, or industry spread?
  - Tweet-anchor quality: can a clean screenshot show the author, handle, post text, date/time, and engagement without login walls or distracting UI?
  - Visual asset quality: are there usable real people, company logos, product screenshots, launch images, official pages, media screenshots, and a clean tweet screenshot?
  - Title tension: can it become a strong, honest, click-worthy short-video headline?
  - Topic diversity: does it add a different angle from the other selected stories?
- Select 5 distinct one-event topics. Avoid five variations of the same model launch or the same company.
- Choose topics that can support real images and a people-first or company-recognition cover.
- Avoid exact repeats from previous days. A topic is considered a repeat when the same company/person/product, same event, same source tweet, and same information-gap angle were already rendered, such as "OpenAI makes an AI chip" appearing again with no new development.
- Reusing the same company is allowed only when the event is materially different, the viewer takeaway is different, and the title/rows are not just a rewrite of a previous video.
- Show the 5 selected topics with one-line rationale before rendering if the user has not explicitly approved batch generation.
- Generate 5 separate videos and covers. Do not merge the topics into one compilation video.
- Each topic must still follow the one-event pattern and row order: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.
- Each topic must include `tweet_anchor` metadata, and the screenshot in `tweet_anchor.screenshot` must also be `images[1]`.

Reject candidates when:

- The same event/topic has already been generated in a previous daily batch.
- The source tweet URL and information-gap angle are the same as an item already recorded in GitHub history.
- The story is only a funding amount with weak viewer relevance.
- The item is mostly opinion or prediction without a concrete event.
- The source is unreliable or cannot be verified.
- The only viral signal is a third-party commentary post and no core-person, official, or reputable source can confirm the underlying event.
- A clean tweet screenshot cannot be captured for image 2.
- No real visual assets are available and the video would become a text-card deck.
- It overlaps too much with a stronger selected topic.
- The angle is too technical for a normal viewer to understand in 7 seconds.

Prefer a balanced final set when possible:

- 1 US model/company story.
- 1 China model/company story.
- 1 policy, safety, or regulation story.
- 1 product entry or consumer/workflow tool story.
- 1 AI hardware, agent, infrastructure, or business-model story.

Before rendering, present the proposed list in this format:

```text
01 话题：...
为什么选：普通人能看懂的变化是 ...
核心推文：作者 / 链接 / 看到的热度信号
封面素材：人物 / 公司 logo / 产品截图 / 官方页面
信息差角度：...
```

Daily execution rules:

- If the user gives a topic, tweet URL, company, event, or concrete instruction, use that input and make only that requested topic.
- If the user gives no topic, default to 5 hot X/Twitter AI topics from the latest 2-3 days.
- Before locking the topics, check GitHub-synced history and local history to prevent exact repeats.
- After a successful run, update local export records and GitHub history, then commit and push before reporting completion.

## Tweet Anchor And Image 2

For the 推特版 workflow, the tweet anchor is not optional.

- `images[1]` must be the clean X/Twitter screenshot or Chinese-localized tweet card for the selected topic.
- The tweet anchor should remain a bright source artifact, not a dark explainer slide. Prefer a real tweet screenshot with Chinese overlay, or a white tweet-style localized card that preserves account/date/engagement cues.
- The screenshot should be captured from the public post page or an authenticated browser session when available.
- Crop to the post body. Preserve author, handle, post text, date/time, and visible engagement when possible.
- Hold `images[1]` about twice as long as the other carousel images because it is the proof frame and usually contains readable text. For a 5-image, 7-second video, prefer `image_hold_weights: [1, 2, 1, 1, 1]`; this produces cuts around `[1.17, 3.50, 4.67, 5.83]`.
- Remove or avoid right-side sign-up panels, bottom login banners, unrelated replies, browser chrome, and large blank areas.
- If the page shows login wall, Cloudflare check, blank loading state, `403`, `429`, or "Something went wrong", do not use that screenshot.
- If the anchor post includes a video or image that is central to the story, the screenshot may include that media preview as long as the post text and author remain visible.
- Store the source URL, author, screenshot path, and observed engagement in `tweet_anchor`.

## Chinese Final Output Rule

Final audience-facing output should be Chinese-first.

- If the source tweet is English, keep the raw screenshot in the project as evidence, but make the final visible image a Chinese-localized tweet card or a screenshot with a Chinese translation overlay.
- Preserve source credibility cues: author, handle, date/time, visible engagement, and source URL in the project record.
- Translate or summarize the tweet body into natural Chinese. Keep company/product names such as `Anthropic`, `Claude`, `OpenAI`, `ChatGPT`, and model names in English when they help recognition.
- If the tweet contains a chart, table, or UI image with English labels, add a Chinese caption or localized chart summary so viewers do not need to read the English.
- Do not leave an English tweet screenshot as the only explanation in the final video, cover, paper-card preview, or overview image.
- For paper-card mode, the middle media can be the localized tweet card, while the raw screenshot remains in `assets/raw/` or project notes for traceability.

## Title Defaults

- `title_weight_multiplier`: `0.9`
- `title_oblique`: `-0.075`
- No glow, no black offset shadow, no highlight.
- Keep the title large enough for mobile viewing; reduce text length before shrinking too much.
- Keep the original line-by-line pop animation for the three title lines in video renders.

## Three-Line Animated Title Logic

Normal 推特版 videos use a shared three-line hook. These are the words shown in the opening animation, and the same three lines should also become the main cover headline.

Structure:

1. Line 1 names the protagonist, company, product, source, or concrete event.
2. Line 2 names the direct change: launch, entry, response, new state, or what just happened.
3. Line 3 translates the story into a normal-viewer hook: consequence, contrast, risk, opportunity, or information gap.

Writing rules:

- Do not write a neutral news headline. Write a short-video hook.
- Make the first line instantly identifiable.
- Make the second line explain the change without jargon.
- Make the third line the strongest and most viewer-facing line.
- Use concrete everyday language, not abstract technical terms.
- Keep each line short enough to read on a phone; shorten text before shrinking the font.
- The third line can use stronger color or weight because it carries the information-gap punch.

Examples:

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

Relationship to other title modes:

- Normal videos: use the three-line animated title above.
- Normal covers: reuse the same three lines as the cover headline.
- Paper-card previews: use the separate paper-card title plus purple ribbon logic below.

## Paper Card Title Logic

For the paper-card explainer style, the title area is not the same as the normal three-line video title.

- Use a short, high-impact black headline at the top of the white card.
- Prefer two lines: line 1 names the event or actor, line 2 names the surprising change or conflict.
- Use the purple ribbon for the strongest information-gap sentence, not for a generic category.
- Good pattern: `事件/主角` + `反常识变化` + purple `真正关键点`.
- Examples:
  - Headline: `Anthropic CEO 炮轰开源 AI` / `开放权重也不算真自由`; ribbon: `并不是真正意义上的“免费”`.
  - Headline: `19 岁少年改写 AI 付费` / `零成本接入 ChatGPT`; ribbon: `直接击穿大模型 API 商业模式`.
  - Headline: `SpaceX 开始出租 AI 算力` / `开源模型公司抢 GPU 入口`; ribbon: `真正稀缺的不是模型，是算力`.

## Paper Card Date Rule

- Every paper-card preview should show the latest verified news date on the card itself.
- Use the newest date from the verified source set for that story. If sources disagree, use the newest publication/update date and keep source notes in the project record.
- Preferred display: a small top-right marker such as `最新：2026.06.28`.
- Do not rely only on the embedded screenshot's tiny source date, because it may be cropped or unreadable on mobile.
- Keep the date marker secondary to the headline: visible enough to prove freshness, but smaller than title and purple ribbon.
- When a date marker is present, leave enough top padding so it does not overlap the headline.

## Layout Defaults

- `photo_box`: `[0, 515, 1080, 1235]`
- Use `photo_fit: "contain"` when source images are screenshots, logos, documents, portraits, or mixed aspect ratios that must remain fully visible. This uses a blurred same-image background to fill the photo box, then keeps the original image complete in the center.
- Use `photo_fit: "cover"` only when the source is a spacious photo that can be safely cropped.
- Info rows start at `y=1288`, row height `64`.
- Top brand pill stays at the top-right.
- Do not draw carousel dots, footer labels, or decorative title bands.

## Paper Card Layout Defaults

Use these defaults for static paper-card previews and for future paper-card video variants:

- Canvas: `1080x1920`.
- Background: dark phone-like backdrop.
- Card: one centered rounded white paper card with subtle texture. Keep the card dominant and avoid nested cards.
- Top: black, very bold headline, centered, usually 2 lines.
- Date: small top-right `最新：YYYY.MM.DD` marker when `date` is provided.
- Ribbon: purple rounded bar under the headline, white bold text, one sentence only.
- Media: real image or screenshot in a purple rounded frame. Use `contain` so screenshots and portraits stay complete.
- Copy: bottom paragraph copy with cyan highlight blocks per wrapped line. This replaces the six numbered info rows.
- Label: a small `AI 信息差快报` label can appear in a corner; no footer strips, carousel dots, or decorative divider lines.

## Paper Card Copy Logic

The bottom copy should read like a compact short-video explanation, not a bullet table:

1. Event: what happened, in plain language.
2. Viewer meaning: why a normal viewer should care.
3. Mechanism: what changed in the product, business model, policy, or industry structure.
4. Boundary: risk, dispute, limitation, opportunity, or who is affected first.
5. Information gap: end with `信息差：...`.

Write short paragraphs that can wrap cleanly. Avoid abstract words that a casual viewer cannot immediately picture. The copy should be suitable for cyan highlighted lines and should not require voiceover to understand.

## One News Event Pattern

Use this skill for one event at a time. For example, "GPT-5.6 enters limited preview" is one event. The five images should all support that same event from different angles:

- real person/company/product photo, preferably a recognizable person when the topic has one
- bright core X/Twitter screenshot or Chinese-localized tweet card as image 2
- official evidence screenshot, report, announcement, docs, or release note
- real product/API/app screenshot or reputable media report screenshot
- related person, company, product, office, event, or real-world context scene

The title and `info_rows` explain the event. The images should not be five separate text cards repeating the explanation. If a source page is unusable, replace it with another real image source instead of making an all-text substitute. X/Twitter changes how the topic is discovered and confirmed; it must not change the original real-image carousel into a deck of self-made explainer cards.

## Image Sourcing Priority

Use multiple images for one news event. The middle image carousel should feel like real news footage, not a deck of text cards.

1. Real people/company/product photos: founders, executives, company offices, product launch scenes, real product screenshots, or official brand/product images.
2. Core X/Twitter screenshot or Chinese-localized tweet card: the topic-confirming post by the core person or official account. This must be the second carousel image and should use a bright/white source-like treatment.
3. Official evidence screenshots: announcement pages, Help Center pages, docs, API pages, safety cards, or release notes.
4. Product entry screenshots: ChatGPT, OpenAI Platform, Codex, model selector, API console, pricing page, or developer docs.
5. Media report screenshots: reputable news pages only when official/product imagery is insufficient or useful for news context.
6. Auxiliary context images: developer scenes, data centers, laptops, or abstract tech imagery only as a last supplement.

## Bright Real-Visual Carousel Rule

The middle `photo_box` must feel like bright real news/product footage, not dark slides.

- Prefer bright real photos and screenshots with recognizable subjects.
- Keep at least three of five carousel images as real-source visuals: person/company/product photo, tweet screenshot/card, official page, product UI, report screenshot, media screenshot, or real context photo.
- Use self-made summary cards only as secondary support and only when they still resemble source material. Do not make most images pure text cards.
- The first image should usually be a real person, company/product visual, or official report/product page, not a text explainer.
- The second image is always the tweet anchor and should be bright enough to read quickly.
- If an image is dark, blocked, low contrast, or visually empty, replace it or add a bright readable treatment.

Reject screenshots that show Cloudflare verification, loading spinners, blank pages, cookie walls, or unrelated search results. Replace them with another source before making a video.

Reject X/Twitter screenshots that are mostly login prompts, sign-up panels, unrelated replies, blank post placeholders, or third-party commentary with no primary-source confirmation.

Reject generated fallback/error cards that say `图片源不可用`, `403`, `429`, `Too Many Requests`, `Forbidden`, or similar downloader errors. These cards are only temporary diagnostics. If they appear in assets, configs, contact sheets, or covers, replace them with a real local cached asset, official/product screenshot, usable media screenshot, or a clean source card that summarizes the source without exposing the fetch error.

## Recommended Row Logic

Use this order for news explainers:

1. `结论`: the one-sentence takeaway.
2. `跟你有关`: what this means for a normal viewer right now.
3. `发生`: what happened.
4. `谁先用`: who gets access first, or where the real entry point is.
5. `影响`: the user or industry impact.
6. `信息差`: what most viewers may not have noticed.

Use `跟你有关` as the default second row because it directly answers the viewer's hidden question: "what does this have to do with me?" Use `普通人机会` only when the row is about a concrete personal opportunity, job direction, workflow, or action.

Keep each row short. If a row wraps visually, rewrite it rather than shrinking all rows.

For `跟你有关` / `普通人机会`, avoid abstract phrasing such as "workflow adaptation" or "capability boundary". Make it concrete and actionable for a casual viewer:

- Good: `别等新模型，先用现有 AI 整理资料、写方案`
- Good: `不用等内测，先用现有 AI 整理资料、写方案`
- Good: `先别抢入口，学会判断哪些事该交给 AI`
- Good: `不用等最强模型，先把重复工作交给 AI`
- Good: `会拆任务的人，比会抢内测的人更占便宜`
- Bad: `先看深度推理与工作流适配`

## Viewer-First Example

For a GPT-5.6 limited-preview story, prefer rows like:

```text
01 结论：GPT-5.6 已预览，但普通用户还不能直接用
02 跟你有关：别等新模型，先用现有 AI 整理资料、写方案
03 发生：OpenAI 先测试 Sol、Terra、Luna 三个版本
04 谁先用：先给合作客户、开发者和 Codex/API 场景
05 影响：ChatGPT 里的全面开放，还要再等一段时间
06 信息差：发布不等于人人可用，入口才是关键
```

## Cover Generation Logic

For 小红书 / 抖音 publishing, generate a separate 9:16 cover image when useful. The cover is not a text card; it is a click-entry frame built from real event assets.

Visual priority:

1. Real person or company identity: use a recognizable person connected to the event first; if no person exists, use the clearest company/product identity.
2. Headline impact: reuse the same three animated video title lines as the cover headline and make them the first text layer.
3. Company recognition: add a company or product logo badge as a secondary anchor.
4. One conclusion: show only the first conclusion row as supporting context.

Asset priority for covers:

1. Real person portrait or half-body image: founder, CEO, product lead, government figure, or other event protagonist.
2. Company/product logo: use a clean white-background badge when possible.
3. Product or official screenshot: use only when no relevant person exists.
4. Avoid pure screenshots, pure logos, abstract tech backgrounds, or text-only cards as the main cover.

Layout rules:

- Use `1080x1920`.
- Let the person photo fill the background or main visual area.
- Keep eyes and main facial features unobstructed.
- Put the headline around the lower third when a portrait is used, usually over shirt/background rather than across the eyes, nose, or mouth.
- Make the headline larger and stronger than the person and logo.
- Use the same wording as the video's three animated title lines. The cover may enlarge, stack, or color the lines differently, but should not rewrite them unless the user asks.
- Make the cover headline visually heavy. Use same-color stroke/thickening around the title text when needed; do not add black shadows, glow, or offset effects.
- Put the company logo badge near the headline, commonly lower-right or side-adjacent, with a white or high-contrast background.
- Keep the top `AI 信息差快报` / topic metadata small.
- Show only one bottom conclusion row; do not show all six info rows on the cover.
- Do not add platform play buttons; 小红书/抖音 add those automatically.
- Do not use the core tweet screenshot as the main cover background when a person, avatar, company logo, product visual, or official brand asset can represent the topic. The tweet screenshot belongs as video image 2 and as source evidence.

For a GPT-5.6 limited-preview cover, use:

```text
Person: Sam Altman portrait
Company badge: OpenAI logo, preferably white background and larger than a tiny corner mark
Headline: GPT-5.6 要来了？ / 但普通人 / 还不能直接用
Bottom row: 结论：预览中，普通用户还不能直接用
```

## Verification

After rendering:

```bash
ffprobe -v error -show_entries stream=codec_type,duration -show_entries format=duration -of json renders/output.mp4
```

Confirm:

- format duration is 7 seconds unless the user requested otherwise.
- both video and audio streams exist when BGM is requested.
- contact sheet shows title, image area, and rows without overlap.

## Export Naming

Final 推特版 deliverables should be organized under the dedicated Xiaohongshu video folder:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/
```

Use Chinese names rather than raw English slugs. The dated top-level folder must clearly include `推特版` or `推特专用`, then split videos, covers, overview images, and source notes:

```text
推特专用-AI信息差视频/
  导出-2026年06月28日-推特版AI信息差快报/
  01-视频/
    01-新模型先过安审-OpenAI与Anthropic/
      视频-01-新模型先过安审-OpenAI与Anthropic.mp4
  02-封面/
    01-新模型先过安审-OpenAI与Anthropic/
      封面-01-新模型先过安审-OpenAI与Anthropic.jpg
  03-总览/
    视频总览-2026年06月28日-推特版AI信息差快报.jpg
    封面总览-2026年06月28日-推特版AI信息差快报.jpg
  04-素材与来源/
    01-新模型先过安审-OpenAI与Anthropic/
      核心推文截图.jpg
      来源记录.md
  选题记录.md
```

Rules:

- The top-level export folder should include the date and batch theme.
- The top-level export folder should live under `/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/`.
- The folder name must include `推特版` or `推特专用`.
- Use `01-视频`, `02-封面`, `03-总览`, and `04-素材与来源` as the first split.
- Each topic gets a numbered Chinese topic folder.
- File names should start with `视频-` or `封面-`, then repeat the topic name.
- Keep English product/company names only where they help recognition, such as `OpenAI`, `DeepSeek`, `GLM-5.2`, or `Google`.
- Each topic's `04-素材与来源` folder should preserve the core tweet screenshot or localized tweet card plus a `来源记录.md` with tweet URL, tweet author, observed heat signal, screenshot path, supporting source URLs, and information-gap angle.
- Temporary preview renders may remain in the working project during iteration, but approved final deliverables must be copied or rendered into this dedicated export folder.
- Also create a zip package with the same Chinese top-level name when handing off a batch.

## BGM Selection

Use local BGM for all final videos unless the user asks for silence. The current default pool is:

| Track | Local path | Best fit | Weight |
| --- | --- | --- | --- |
| `bba进行曲.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/bba进行曲.mp3` | heavy, urgent, strategic, big-company, policy, safety, infrastructure | 3 |
| `时尚动感.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/时尚动感.mp3` | stylish tech, product launches, consumer apps, creator tools | 1 |
| `时尚热情绽放.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/时尚热情绽放.mp3` | upbeat launches, opportunity, creator economy, positive momentum | 1 |
| `do it.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/do it.mp3` | action, workflow, practical tools, "what to do now" | 1 |
| `drink.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/drink.mp3` | light consumer topics, lifestyle/service AI, casual app features | 1 |
| `moment.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/moment.mp3` | reflective explainers, business shifts, slower strategic stories | 1 |
| `say no cry.mp3` | `/Users/xieyahao/Desktop/我自己/小红/半奏/say no cry.mp3` | controversy, risk, security, compliance, dispute | 1 |

Selection algorithm:

1. Classify the topic mood: heavy/urgent, controversy/risk, creator/product, consumer/lifestyle, practical/workflow, or reflective/business.
2. Build a candidate set from the mood. Include `bba进行曲.mp3` in serious/high-energy candidate sets with weight `3`; matched alternatives usually use weight `1`.
3. Randomly choose from the candidate set using the weights. This gives the batch variety without ignoring topic fit.
4. In a 5-video batch, do not force all videos to use different tracks, but avoid one track taking every video unless the user asks for a single unified BGM.
5. Copy the selected track into `assets/audio/` in the project and set `bgm.path` to the copied relative path. Keep `bgm.start` around `3` by default, `volume` around `0.55`, and tiny fade-in/out.
6. If the track has a more suitable downbeat later, adjust `bgm.start` while keeping the final video duration at 7 seconds unless the user says otherwise.

## Topic History And GitHub Sync

For recurring daily batches:

- Maintain a per-batch `选题记录.md` in the local export folder and a GitHub-synced history under `records/twitter-ai-info-video/`.
- The recommended GitHub history repository is `/Users/xieyahao/Documents/别人好项目/ai-video-skills/`.
- Recommended GitHub history layout:

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

- Record date, topic title, company/product/person, source tweet URL, source tweet author, observed X/Twitter heat signal, supporting source URLs, selected angle, final export folder, and output filenames.
- Before every auto-scout run, compare candidates against GitHub history, previous local records, and dated export folders.
- Do not repeat the exact same event from a previous day. Prefer a follow-up only when there is a new development, and label it clearly as a follow-up angle.
- After every successful invocation, commit and push the updated history records to GitHub. Do not report full completion until sync succeeds or the sync failure is explicitly reported.
- Sync final deliverable indexes, configs, source notes, and topic history every time. Include final media assets when practical for the target repo; if MP4 files are too large or unsuitable, at minimum sync enough metadata and local export paths to prevent duplicate topics later.
- If the workflow rules, scripts, or skill documentation change, copy the skill into the user's GitHub skill repository and push the commit after validation.
