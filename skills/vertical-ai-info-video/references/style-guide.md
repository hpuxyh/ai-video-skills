# Style Guide

## Legacy Dark Video Config Schema

This schema is for the older dark vertical fast-news renderer only. Do not use it for daily scheduled news videos unless the user explicitly requests the legacy dark template. The current default daily/news-video schema is `Paper Card Video Config Schema` below.

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
    "assets/images/event1/event1-02.jpg"
  ],
  "image_roles": [
    "hero",
    "official"
  ],
  "image_quality": [
    "real",
    "real"
  ],
  "beat_cuts": [0.90, 1.99, 3.87, 5.83],
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

## Clean White Paper Card Video Config Schema

Use this schema for the current default daily/news-video MP4 output. It uses the approved no-purple white-card style: red metadata tag, three-line title with blue third line, five-image carousel, and label-free cyan-highlight bottom lines.

```json
{
  "duration": 7,
  "fps": 30,
  "badge": "AI 信息差快报",
  "date": "2026.06.27",
  "header_tag": "重磅",
  "header_category": "模型安全 · 访问限制",
  "header_source": "最新 · 2026.06.27",
  "title": [
    "Anthropic 发布 Fable 5",
    "美国限制外籍用户访问"
  ],
  "title_line3": "普通人还不能直接用",
  "images": [
    "assets/images/event/01-hero.jpg",
    "assets/images/event/02-official.png",
    "assets/images/event/03-source.png",
    "assets/images/event/04-product.jpg",
    "assets/images/event/05-latest-card.png"
  ],
  "image_roles": ["hero", "official", "media", "product", "source-card"],
  "image_quality": ["real", "official-screenshot", "source-card", "product", "source-card"],
  "media_box": [0, 492, 1080, 1262],
  "media_outline_width": 0,
  "media_fit": "cover",
  "media_pad": 0,
  "media_transition_mode": "fade",
  "media_transition_duration": 0.34,
  "body_y": 1298,
  "body_show_numbers": false,
  "body_show_labels": false,
  "body_max_rows": 6,
  "body_highlight_fill": [53, 214, 226, 232],
  "body_rows_animate": true,
  "body_row_start": 1.05,
  "body_row_interval": 0.52,
  "body_row_duration": 0.42,
  "body_rows": [
    {"text": "用一句话说清楚发生了什么"},
    {"text": "补一个最强数字、事实或直接变化"},
    {"text": "解释为什么这件事会引发争议"},
    {"text": "落到普通用户、员工或创作者会遇到的影响"},
    {"text": "最后给一个能直接带走的判断"}
  ],
  "bgm": {
    "path": "assets/audio/bba进行曲.mp3",
    "start": 3,
    "volume": 0.55,
    "fade_in": 0.08,
    "fade_out": 0.35
  }
}
```

Render it with:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_clean_white_video.py \
  --config configs/clean-white-video.json \
  --project-dir . \
  --output renders/clean-white-video.mp4 \
  --contact-sheet renders/clean-white-video-contact.jpg
```

## Legacy Paper Card Preview Config Schema

The following preview/video schemas are for older purple-ribbon paper-card variants. Do not use them for default daily output unless the user explicitly asks for the purple-ribbon style.

## Paper Card Preview Config Schema

Use this schema when the user asks for the approved white-card reference style or wants a rendered image before full video production:

```json
{
  "output": "renders/paper-card-preview.jpg",
  "badge": "AI 信息差快报",
  "date_label": "最新",
  "date": "2026.06.28",
  "title_on_purple": false,
  "show_ribbon": true,
  "title": [
    "超 1/3 Claude 用户说",
    "AI 一年内能接管大半工作"
  ],
  "title_color": [0, 0, 0],
  "title_size": 58,
  "strap": "别只问会不会被替代，先学会分配任务",
  "strap_color": [255, 255, 255],
  "image": "assets/images/event/tweet-anchor-cn.png",
      "body_style": "editorial_lines",
      "body_show_labels": false,
      "body_show_numbers": false,
      "body_max_rows": 6,
      "body_rows": [
        {"text": "官方报告称，超 1/3 Claude 用户预计 AI 一年内能完成多数任务"},
        {"text": "Claude 正从聊天助手，变成能长期接任务的工具"},
        {"text": "别只问会不会被替代，先练习把工作拆给 AI"},
        {"text": "会拆任务、会验收的人会更早升级"},
        {"text": "拉开差距的不是有没有 AI，而是谁先会指挥 AI"}
      ]
}
```

Render it with:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

## Paper Card Video Config Schema

Use this schema for the current default daily/news-video MP4 output. This keeps the paper-card frame language while preserving the one-event five-real-image carousel inside the middle media frame. Use the older dark vertical video schema only when the user explicitly asks for that style.

```json
{
  "duration": 7,
  "fps": 30,
  "output": "renders/paper-card-video.mp4",
  "contact_sheet": "renders/paper-card-video-contact.jpg",
  "badge": "AI 信息差快报",
  "date_label": "最新",
  "date": "2026.06.28",
  "title_on_purple": false,
  "show_ribbon": true,
  "title": [
    "超 1/3 Claude 用户说",
    "AI 一年内能接管大半工作"
  ],
  "title_color": [0, 0, 0],
  "title_size": 58,
  "strap": "别只问会不会被替代，先学会分配任务",
  "strap_color": [255, 255, 255],
  "images": [
    "assets/images/event/person.png",
    "assets/images/event/tweet-anchor-cn.png",
    "assets/images/event/official-report.png",
    "assets/images/event/product.png",
    "assets/images/event/chart.png"
  ],
  "image_roles": ["hero", "tweet", "official", "product", "media"],
  "image_quality": ["real", "tweet", "official-screenshot", "product", "source-card"],
  "image_hold_weights": [1, 2, 1, 1, 1],
  "media_h": 720,
  "media_outline_width": 0,
  "media_fit": "cover",
  "media_transition_mode": "fade",
  "media_transition_duration": 0.34,
  "media_preserve_roles": [
    "media",
    "source-card",
    "official-screenshot",
    "clean-card",
    "product",
    "tweet",
    "screenshot"
  ],
  "body_style": "editorial_lines",
  "body_show_labels": false,
  "body_show_numbers": false,
  "body_max_rows": 6,
  "animate_body_rows": true,
  "body_anim_start": 1.05,
  "body_anim_step": 0.52,
  "body_anim_duration": 0.42,
  "body_rows": [
    {"text": "官方报告称，超 1/3 Claude 用户预计 AI 一年内能完成多数任务"},
    {"text": "Claude 正从聊天助手，变成能长期接任务的工具"},
    {"text": "别只问会不会被替代，先练习把工作拆给 AI"},
    {"text": "会拆任务、会验收的人会更早升级"},
    {"text": "拉开差距的不是有没有 AI，而是谁先会指挥 AI"}
  ],
  "bgm": {
    "path": "assets/audio/moment.mp3",
    "start": 3,
    "volume": 0.55,
    "fade_in": 0.08,
    "fade_out": 0.35
  }
}
```

Render it with:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_video.py \
  --config configs/paper-card-video.json \
  --project-dir . \
  --output renders/paper-card-video.mp4 \
  --contact-sheet renders/paper-card-video-contact.jpg
```

Paper-card video rules:

- `images` must contain the same real one-event media set used by the normal video, usually 5 images.
- Do not pass the already-rendered paper-card JPG as the only image.
- Preserve the title entrance rhythm: three title lines pop in one by one, with the third line in blue as the information-gap sentence. The title should not be static from the first frame in MP4 output.
- In the current structured paper-card style, use `scripts/render_clean_white_video.py`, `title_line3`, `body_rows`, `body_rows_animate: true`, and no purple ribbon.
- If the middle carousel's second image is a core tweet screenshot or localized tweet card, hold it about twice as long as the other images. Prefer `image_hold_weights: [1, 2, 1, 1, 1]` for a 5-image, 7-second video.
- Keep screenshots bright and legible; avoid dark overlays in the middle media frame.
- Default to `media_outline_width: 0` for the current clean white-card variant. Use a visible purple border only when a specific style asks for it. Do not add carousel dots or extra footer strips.
- Use `media_fit: "cover"` for real people/product images, but preserve text-bearing screenshots/cards via `image_roles`, `image_quality`, and `media_preserve_roles` so their text is not cropped.
- Use `media_transition_mode: "fade"` and `media_transition_duration` around `0.30`-`0.36` so image changes have a soft cross-fade without white flashing or fast left-right slide motion.
- Daily scheduled videos default to the white paper-card video style. The bottom copy should reveal row by row at a readable pace, then remain visible. Use 4-6 pure content lines, usually 5; keep internal labels out of the rendered video by setting `body_show_labels: false`.

## Request Routing

Use two modes:

1. Specific-topic mode: if the user gives a concrete topic, event, company, URL, or direct instruction, create one video for that event.
2. Auto-scout mode: if the user asks for an AI information-gap video but does not provide a concrete topic, search the latest 7 days of AI news and choose 5 topics across China and the US.

In auto-scout mode:

- Search current sources because the 7-day window is time-sensitive.
- Before choosing topics, review previous generated batches in the workspace, dated export folders, `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md`, and the GitHub-synced 推特版 `topic-history.md` when available. Treat both ordinary news-video history and 推特版 history as duplicate-prevention sources.
- Prefer China/US AI stories with clear platform appeal: model releases, policy/regulation, major product launches, safety/security, AI hardware, agent/tools, major company moves, and consumer/workflow impact.
- Start from a candidate pool of roughly 15-30 recent stories when possible, then narrow down to 5. The goal is not "news ranking top 5"; the goal is "the 5 stories most suitable for AI 信息差短视频".
- Score candidates by:
  - Normal-viewer relevance: can a casual viewer understand why it matters to work, creation, tools, learning, business, or daily AI use?
  - Information-gap strength: is there a non-obvious takeaway beyond the surface headline?
  - Heat and authority: is it from an official source, reputable media, or clearly discussed by the industry?
  - Visual asset quality: are there usable real people, company logos, product screenshots, launch images, official pages, or media screenshots?
  - Title tension: can it become a strong, honest, click-worthy short-video headline?
  - Topic diversity: does it add a different angle from the other selected stories?
- Select 5 distinct one-event topics. Avoid five variations of the same model launch or the same company.
- Choose topics that can support real images and a people-first or company-recognition cover. Favor familiar companies, people, products, and public issues; obscure companies/products should only survive when the public conflict is extremely clear.
- Avoid exact repeats from previous days across both ordinary AI 信息差 videos and 推特版 videos. A topic is considered a repeat when the same company/person/product and the same event angle were already rendered, such as "OpenAI makes an AI chip" appearing again with no new development.
- Reusing the same company is allowed only when the event is materially different, the viewer takeaway is different, and the title/rows are not just a rewrite of a previous video.
- Show the 5 selected topics with one-line rationale before rendering if the user has not explicitly approved batch generation.
- Generate 5 separate videos and covers. Do not merge the topics into one compilation video.
- Each topic must still follow the one-event pattern and use 4-6 bottom description lines, usually 5. The internal writing order is event, key fact, conflict/mechanism, affected group, and final takeaway, but final text must not show labels such as `事件`, `关键`, `冲突`, `影响`, or `信息差`.

Reject candidates when:

- The same event/topic has already been generated in a previous daily batch.
- The story is only a funding amount with weak viewer relevance.
- The item is mostly opinion or prediction without a concrete event.
- The source is unreliable or cannot be verified.
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
封面素材：人物 / 公司 logo / 产品截图 / 官方页面
信息差角度：...
```

## Title Defaults

- `title_weight_multiplier`: `0.9`
- `title_oblique`: `-0.075`
- No glow, no black offset shadow, no highlight.
- Keep the title large enough for mobile viewing; reduce text length before shrinking too much.

## Paper Card Title Logic

For the paper-card explainer style, the title area is not the same as the normal three-line video title. This paper-card style is the current default for daily scheduled AI news videos.

- In the current structured default, use a bold three-line headline on the white card: first two lines black, third line blue. Purple title/ribbon layouts are only for explicit fallback requests.
- Prefer two black title lines: line 1 gives the actor/source plus a concrete fact, number, product, policy, or event; line 2 gives the plain-language consequence, surprise, or conflict.
- Use `title_line3` for the strongest information-gap sentence, action hook, or counterintuitive takeaway. It should tell the viewer what to notice or do, not merely restate the title.
- Good pattern: `谁/什么来源 + 发生了什么具体事` + `这件事造成什么变化` + blue third line `普通人该注意的关键点`.
- Run the 3-second comprehension test before rendering: after reading only the three title lines, a normal viewer should know the basic story, why it matters, and the main contrast. If they still need the bottom copy to decode the title, rewrite it.
- Do not use abstract mood-only titles. They may sound dramatic but fail as a social-video entry point.
- Examples:
  - Title: `Anthropic CEO 炮轰开源 AI` / `开放权重也不算真自由` / `别只看“开源”`.
  - Title: `19 岁少年改写 AI 付费` / `零成本接入 ChatGPT` / `API 收费入口被冲击`.
  - Title: `SpaceX 开始出租 AI 算力` / `开源模型公司抢 GPU 入口` / `稀缺的是算力`.
  - Title: `超 1/3 Claude 用户说` / `AI 一年内能接管大半工作` / `先学会分配任务`.
- Avoid:
  - Headline: `Claude 用户最怕的事` / `高频用户反而更乐观`; why: it does not say what happened.
  - Headline: `AI 工作方式巨变` / `普通人必须重视`; why: it has no source, number, product, or concrete event.

## Paper Card Date Rule

- Every paper-card preview should show the latest verified news date on the card itself.
- Use the newest date from the verified source set for that story. If sources disagree, use the newest publication/update date and keep source notes in the project record.
- Preferred display: a small top-right marker such as `最新：2026.06.28`.
- Do not rely only on the embedded screenshot's tiny source date, because it may be cropped or unreadable on mobile.
- Keep the date marker secondary to the headline: visible enough to prove freshness, but smaller than title.
- When a date marker is present, leave enough top padding so it does not overlap the headline.

## Layout Defaults

- `photo_box`: `[0, 515, 1080, 1235]`
- Use `photo_fit: "contain"` when source images are screenshots, logos, documents, portraits, or mixed aspect ratios that must remain fully visible. This uses a blurred same-image background to fill the photo box, then keeps the original image complete in the center.
- Use `photo_fit: "cover"` only when the source is a spacious photo that can be safely cropped.
- Info rows start at `y=1288`, row height `64`.
- Top brand pill stays at the top-right.
- Do not draw carousel dots, footer labels, or decorative title bands.

## Paper Card Layout Defaults

Use these defaults for static paper-card previews and for the current daily paper-card video variant:

- Canvas: `1080x1920`.
- Background: dark phone-like backdrop.
- Card: one centered rounded white paper card with subtle texture. Keep the card dominant and avoid nested cards.
- Top: current default is a very bold three-line headline, centered. The first two lines are black and the third line is blue emphasis.
- Date: small top-right `最新：YYYY.MM.DD` marker when `date` is provided.
- No purple ribbon by default: use the blue third title line for the viewer takeaway, information gap, or action hook.
- Media: real image or screenshot in a clean full-width frame. Use bright, legible media. For video, this frame must contain the five-image carousel.
- Copy: bottom structured cyan-highlight reading lines by default. Use 4-6 pure content sentences, usually 5, with no visible labels and no `01`-`05` number pills. Keep the internal event/key/conflict/impact/takeaway logic for writing only.
- Label: a small `AI 信息差快报` label can appear in a corner; no footer strips, carousel dots, or decorative divider lines.

## Paper Card Copy Logic

The bottom copy should read like a compact short-video explanation, not a loose paragraph dump. The current preferred form is `body_rows` rendered as unnumbered, label-free cyan-highlight reading lines:

```json
[
  {"text": "官方报告称，超 1/3 Claude 用户预计 AI 一年内能完成多数任务"},
  {"text": "Claude 正从聊天助手，变成能长期接任务的工具"},
  {"text": "别只问会不会被替代，先练习把工作拆给 AI"},
  {"text": "会拆任务、会验收的人会更早升级"},
  {"text": "拉开差距的不是有没有 AI，而是谁先会指挥 AI"}
]
```

Write rows in this order:

1. Fact: what happened, in plain language. Include the source, actor, number, product, date/context, or action when available.
2. Viewer meaning: why a normal viewer should care. Translate it into work, learning, creation, cost, access, opportunity, or risk.
3. Mechanism: what changed in the product, business model, policy, workflow, access path, or industry structure.
4. Boundary or opportunity: risk, dispute, limitation, opportunity, or who is affected first.
5. Information gap: end with a natural short takeaway. Do not render an `信息差` label unless the user explicitly asks for visible labels.

Write short rows that can wrap cleanly. Avoid abstract words that a casual viewer cannot immediately picture. The copy should not require voiceover to understand.

Bottom copy quality rules:

- Each line should add new information. Do not repeat the title in different words.
- Start concrete, then explain. Avoid opening with conclusions such as `AI 正在重构工作方式` before stating the actual event.
- Use everyday verbs: `接走`, `分配`, `验收`, `变贵`, `变慢`, `先开放`, `先用上`, `拿不到`, `抢入口`.
- Prefer `普通人...`, `对你来说...`, or direct action language when the line is about viewer meaning.
- Avoid jargon-only phrasing such as `能力边界变化`, `工作流适配`, `产业范式迁移`, `组织效率重构`, unless immediately translated into a concrete consequence.
- The final line should be a sharp conclusion the viewer can remember, for example `拉开差距的不是有没有 AI，而是谁先学会指挥 AI`. Do not write `这个选题的信息差是...`.

## One News Event Pattern

Use this skill for one event at a time. For example, "GPT-5.6 enters limited preview" is one event. The five images should all support that same event from different angles:

- person/company/product photo
- official evidence screenshot
- product/API/Codex entry screenshot
- media report screenshot
- related company or product scene

The title and `body_rows` explain the event in the default clean white workflow. The images should not be five separate text cards repeating the explanation. If a source page is unusable, replace it with another real image source instead of making an all-text substitute.

## Image Sourcing Priority

Use multiple images for one news event. The middle image carousel should feel like real news footage, not a deck of text cards.

1. Real people/company/product photos: founders, executives, company offices, product launch scenes, real product screenshots, or official brand/product images.
2. Official evidence screenshots: announcement pages, Help Center pages, docs, API pages, safety cards, or release notes.
3. Product entry screenshots: ChatGPT, OpenAI Platform, Codex, model selector, API console, pricing page, or developer docs.
4. Media report screenshots: reputable news pages only when official/product imagery is insufficient or useful for news context.
5. Auxiliary context images: developer scenes, data centers, laptops, or abstract tech imagery only as a last supplement.

Reject screenshots that show Cloudflare verification, loading spinners, blank pages, cookie walls, or unrelated search results. Replace them with another source before making a video.

Reject generated fallback/error cards that say `图片源不可用`, `403`, `429`, `Too Many Requests`, `Forbidden`, or similar downloader errors. These cards are only temporary diagnostics. If they appear in assets, configs, contact sheets, or covers, replace them with a real local cached asset, official/product screenshot, usable media screenshot, or a clean source card that summarizes the source without exposing the fetch error.

## Image Sequence Preflight

Before rendering, run the preflight checker against every final video config:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/check_image_sequence.py \
  --config configs/video.json \
  --project-dir . \
  --contact-sheet renders/image-sequence-preflight.jpg \
  --strict
```

The checker is a guardrail, not a replacement for human review. It catches obvious ordering and asset-quality mistakes before rendering:

- Slot 1 should be a protagonist/company/product recognition image, or at least an official/product evidence image when no person/company photo exists.
- The first two slots should include a `hero` image whenever the story has a recognizable person, company, product, or place.
- Media/source screenshots should normally appear after the recognition and evidence images, usually slot 4-5.
- Auxiliary context images such as chips, data centers, laptops, local/generated context cards, and generic compute scenes should not lead the carousel.
- Error/fallback assets such as `403`, `429`, Cloudflare pages, loading screens, and unavailable-image cards are hard failures.
- If the filename is ambiguous, add explicit `image_roles` to the config so the checker can evaluate the intended order.
- If the asset quality is known, add `image_quality` values such as `real`, `source-card`, `clean-card`, `fallback`, or `error`. `fallback` and `error` are hard failures.
- The checker can also produce a contact sheet. Always inspect it when a source was downloaded from the web, because filename-only checks cannot reliably read every embedded error message.

Recommended 5-image order:

```text
01 hero: real person / company / product / recognizable place
02 official: announcement, docs, release notes, official page, or direct evidence
03 product: app, API, model selector, Codex, console, or product-entry screenshot
04 media: reputable news/source screenshot
05 auxiliary: related context scene, hardware, infrastructure, or supporting background
```

Allowed `image_roles` values:

```text
hero, official, product, media, auxiliary
```

Recommended `image_quality` values:

```text
real, official-screenshot, product-screenshot, source-card, clean-card, fallback, error
```

If the checker fails, do not weaken the rule just to pass. Reorder the images, replace weak assets, rename assets descriptively, or add explicit roles only when the visual source truly matches that role.

## Default Paper-Card Row Logic

Use this 5-line logic for the default white paper-card news explainers. These are writing roles only; do not render the role names on screen:

1. Event: what happened, stated plainly with the actor/source/product/date when possible.
2. Key fact: what changed behind the surface headline.
3. Conflict/mechanism: why this is controversial or what changed behind the scenes.
4. Affected group: who benefits, who is affected, or what boundary changed.
5. Takeaway: the final usable conclusion most viewers may not have noticed.

Land one of the lines on normal viewers because it directly answers the hidden question: "what does this have to do with me?" Use concrete personal opportunity, risk, job direction, workflow, or action language when relevant.

Keep each row short. If a row wraps visually, rewrite it rather than shrinking all rows.

The older visible-label orders such as `事件` / `关键` / `跟你有关` / `信息差` and `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差` belong to legacy templates. Do not use visible labels for daily scheduled white paper-card videos unless the user explicitly asks for that style.

For viewer-impact lines, avoid abstract phrasing such as "workflow adaptation" or "capability boundary". Make it concrete and actionable for a casual viewer:

- Good: `别等新模型，先用现有 AI 整理资料、写方案`
- Good: `不用等内测，先用现有 AI 整理资料、写方案`
- Good: `先别抢入口，学会判断哪些事该交给 AI`
- Good: `不用等最强模型，先把重复工作交给 AI`
- Good: `会拆任务的人，比会抢内测的人更占便宜`
- Bad: `先看深度推理与工作流适配`

## Viewer-First Example

For a GPT-5.6 limited-preview story, prefer rows like:

```text
GPT-5.6 已经预览，但普通用户还不能直接用
入口先给合作客户、开发者和 Codex/API 场景
别等新模型，先用现有 AI 整理资料、写方案
ChatGPT 里的全面开放，还要再等一段时间
发布不等于人人可用，入口才是关键
```

## Cover Generation Logic

For 小红书 / 抖音 publishing, generate a separate 9:16 cover image when useful. The cover is not a text card; it is a click-entry frame built from real event assets.

Visual priority:

1. Headline impact: the headline must be the first visual layer.
2. Real person: use a recognizable person connected to the event for trust and stopping power.
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
- Make the cover headline visually heavy. Use same-color stroke/thickening around the title text when needed; do not add black shadows, glow, or offset effects.
- Put the company logo badge near the headline, commonly lower-right or side-adjacent, with a white or high-contrast background.
- Keep the top `AI 信息差快报` / topic metadata small.
- Show only one bottom conclusion row; do not show all six info rows on the cover.
- Do not add platform play buttons; 小红书/抖音 add those automatically.

For a GPT-5.6 limited-preview cover, use:

```text
Person: Sam Altman portrait
Company badge: OpenAI logo, preferably white background and larger than a tiny corner mark
Headline: GPT-5.6 要来了？ / 但普通人 / 还不能直接用
Bottom row: 预览中，普通用户还不能直接用
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

Final deliverables should be organized with Chinese names rather than raw English slugs. The canonical creator handoff root is:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/
```

Use a dated top-level project folder under this `新闻视频` category. The folder is project-level, not asset-type-level: one batch/project contains five video topics, and each topic folder contains the three publishing files for that topic.

```text
新闻视频/
  README.md
  选题历史.md
  导出-2026年06月28日AI信息差快报/
    01-新模型先过安审-OpenAI与Anthropic/
      视频.mp4
      封面.jpg
      文案.md
    02-另一个AI新闻主题/
      视频.mp4
      封面.jpg
      文案.md
    ...
    项目总览.md
    _记录/
      视频总览-2026年06月28日AI信息差快报.jpg
      封面总览-2026年06月28日AI信息差快报.jpg
      选题记录.md
      渲染校验.md
      bgm-selection-plan.json
      素材与来源/
```

Rules:

- The top-level export folder should include the date and batch theme, and must sit under `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频`.
- Each topic gets a numbered Chinese topic folder directly under the project folder.
- Each topic folder should contain exactly three core publishing files: `视频.mp4`, `封面.jpg`, and `文案.md`.
- `文案.md` merges 小红书 and 抖音 titles, descriptions, tags, and posting notes.
- Overview images, validation files, source records, contact sheets, preflight images, configs, and BGM plans must go under `_记录/`, not in the publishing surface.
- If a legacy renderer still emits category-first folders, run `scripts/package_project_delivery.py` to create the topic-first delivery folder before reporting completion.
- Keep English product/company names only where they help recognition, such as `OpenAI`, `DeepSeek`, `GLM-5.2`, or `Google`.
- Update `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md` after each batch so the next run can avoid repeats.

## Platform Publishing Copy

Each completed topic should include platform-ready copy, not just rendered media.

For 小红书:

```text
# 小红书标题
...

# 内容描述
...

# 标签
#AI #人工智能 #AI工具 ...

# 发布备注
封面使用：...
视频使用：...
```

For 抖音:

```text
# 抖音标题
...

# 内容描述
...

# 标签
#AI #大模型 ...
```

Copy rules:

- Title must name the actual topic or product; avoid only saying `AI又变天了`.
- Description should explain the conclusion and the viewer meaning in plain Chinese.
- Tags should mix broad AI traffic tags and exact company/product/event tags.
- Keep platform copy concise enough to paste directly.

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

1. After generating all batch configs, run `scripts/select_bgm_for_batch.py`. Do not let batch scripts inherit old `bgm` values.
2. Classify the topic mood: heavy/urgent, controversy/risk, creator/product, consumer/lifestyle, practical/workflow, or reflective/business.
3. Build a candidate set from the mood. Include `bba进行曲.mp3` in serious/high-energy candidate sets with weight `3`; matched alternatives usually use weight `1`.
4. Randomly choose from the candidate set using deterministic weighted randomness. This gives the batch variety without ignoring topic fit.
5. In a 5-video batch, do not force all videos to use different tracks, but reject accidental all-same output unless the user asks for a single unified BGM.
6. Copy the selected track into `assets/audio/` in the project and set `bgm.path` to the copied relative path. Also set `bgm.source_track` and `bgm.mood` so validation can inspect the assignment.
7. Keep `bgm.start` around `3` by default, `volume` around `0.55`, and tiny fade-in/out. If the track has a more suitable downbeat later, adjust `bgm.start` while keeping the final video duration at 7 seconds unless the user says otherwise.

Run:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/select_bgm_for_batch.py \
  --project-dir . \
  --configs configs/*-paper-card.json \
  --write-plan renders/bgm-selection-plan.json
```

Validation:

- The plan must list one `track`, `mood`, and `reason` per config.
- The final configs must include `bgm.path`, `bgm.source_track`, and `bgm.mood`.
- For a 5-video batch, do not accept `summary` with only one track unless the user explicitly asked for one BGM across all videos.

## Topic History And GitHub Sync

For recurring daily batches:

- Use the clean white paper-card video style by default: red metadata tag, black/blue three-line headline, five-image carousel with soft cross-fade transitions, structured clean bottom rows, and body rows revealing one by one at a readable pace.
- Maintain a per-batch `选题记录.md` in the project folder, or update an existing `topic-history.md` when the project already has one.
- Record date, topic title, company/product, source URLs, selected angle, and final output folder.
- Before every auto-scout run, compare candidates against previous records and dated export folders.
- Do not repeat the exact same event from a previous day. Prefer a follow-up only when there is a new development, and label it clearly as a follow-up angle.
- If the workflow rules, scripts, or skill documentation change, copy the skill into the user's GitHub skill repository and push the commit after validation.
- Generated video assets do not need to be pushed to the skill repository unless the user explicitly asks; only reusable skill/workflow updates should be pushed.
