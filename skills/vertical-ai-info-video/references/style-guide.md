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
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_paper_card_preview.py \
  --config configs/paper-card.json \
  --project-dir . \
  --output renders/paper-card-preview.jpg
```

## Paper Card Video Config Schema

Use this schema only after the paper-card preview style is approved and the user asks for MP4 output. This keeps the paper-card frame language while preserving the one-event five-real-image carousel inside the middle media frame.

```json
{
  "duration": 7,
  "fps": 30,
  "output": "renders/paper-card-video.mp4",
  "contact_sheet": "renders/paper-card-video-contact.jpg",
  "badge": "AI 信息差快报",
  "date_label": "最新",
  "date": "2026.06.28",
  "title": [
    "超 1/3 Claude 用户说",
    "AI 一年内能接管大半工作"
  ],
  "strap": "别只问会不会被替代，先学会分配任务",
  "images": [
    "assets/images/event/person.png",
    "assets/images/event/tweet-anchor-cn.png",
    "assets/images/event/official-report.png",
    "assets/images/event/product.png",
    "assets/images/event/chart.png"
  ],
  "beat_cuts": [0.90, 1.99, 3.87, 5.83],
  "media_h": 660,
  "body": [
    "Anthropic 调查 Claude 用户：超 1/3 的人认为，一年内 AI 能完成自己大部分工作",
    "普通人别只看“会不会被替代”，更该看谁先学会把工作拆给 AI",
    "背后机制是：AI 正从聊天助手变成长期执行任务的工具",
    "风险是只等答案的人更被动；机会是会拆任务、会验收结果的人先升级",
    "信息差：拉开差距的不是有没有 AI，而是谁先学会指挥 AI"
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
- Preserve the original title entrance rhythm: headline lines pop in one by one, then the purple ribbon expands in. The title/ribbon should not be static from the first frame in MP4 output.
- Keep screenshots bright and legible; avoid dark overlays in the middle media frame.
- Use the purple border only as a media frame. Do not add carousel dots or extra footer strips.

## Request Routing

Use two modes:

1. Specific-topic mode: if the user gives a concrete topic, event, company, URL, or direct instruction, create one video for that event.
2. Auto-scout mode: if the user asks for an AI information-gap video but does not provide a concrete topic, search the latest 7 days of AI news and choose 5 topics across China and the US.

In auto-scout mode:

- Search current sources because the 7-day window is time-sensitive.
- Before choosing topics, review previous generated batches in the workspace, dated export folders, and any `选题记录.md` / `topic-history.md` files. Treat these as a local topic history.
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
- Choose topics that can support real images and a people-first or company-recognition cover.
- Avoid exact repeats from previous days. A topic is considered a repeat when the same company/person/product and the same event angle were already rendered, such as "OpenAI makes an AI chip" appearing again with no new development.
- Reusing the same company is allowed only when the event is materially different, the viewer takeaway is different, and the title/rows are not just a rewrite of a previous video.
- Show the 5 selected topics with one-line rationale before rendering if the user has not explicitly approved batch generation.
- Generate 5 separate videos and covers. Do not merge the topics into one compilation video.
- Each topic must still follow the one-event pattern and row order: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.

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

For the paper-card explainer style, the title area is not the same as the normal three-line video title.

- Use a short, high-impact black headline at the top of the white card.
- Prefer two lines: line 1 gives the actor/source plus a concrete fact, number, product, policy, or event; line 2 gives the plain-language consequence, surprise, or conflict.
- Use the purple ribbon for the strongest information-gap sentence, action hook, or counterintuitive takeaway. The ribbon should tell the viewer what to notice or do, not merely restate the headline.
- Good pattern: `谁/什么来源 + 发生了什么具体事` + `这件事造成什么变化` + purple `普通人该注意的关键点`.
- Run the 3-second comprehension test before rendering: after reading only the title and purple ribbon, a normal viewer should know the basic story, why it matters, and the main contrast. If they still need the bottom copy to decode the title, rewrite it.
- Do not use abstract mood-only titles. They may sound dramatic but fail as a social-video entry point.
- Examples:
  - Headline: `Anthropic CEO 炮轰开源 AI` / `开放权重也不算真自由`; ribbon: `并不是真正意义上的“免费”`.
  - Headline: `19 岁少年改写 AI 付费` / `零成本接入 ChatGPT`; ribbon: `直接击穿大模型 API 商业模式`.
  - Headline: `SpaceX 开始出租 AI 算力` / `开源模型公司抢 GPU 入口`; ribbon: `真正稀缺的不是模型，是算力`.
  - Headline: `超 1/3 Claude 用户说` / `AI 一年内能接管大半工作`; ribbon: `别只问会不会被替代，先学会分配任务`.
- Avoid:
  - Headline: `Claude 用户最怕的事` / `高频用户反而更乐观`; why: it does not say what happened.
  - Headline: `AI 工作方式巨变` / `普通人必须重视`; why: it has no source, number, product, or concrete event.

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

1. Fact: what happened, in plain language. Include the source, actor, number, product, date/context, or action when available.
2. Viewer meaning: why a normal viewer should care. Translate it into work, learning, creation, cost, access, opportunity, or risk.
3. Mechanism: what changed in the product, business model, policy, workflow, access path, or industry structure.
4. Boundary: risk, dispute, limitation, opportunity, or who is affected first.
5. Information gap: end with `信息差：...`.

Write short paragraphs that can wrap cleanly. Avoid abstract words that a casual viewer cannot immediately picture. The copy should be suitable for cyan highlighted lines and should not require voiceover to understand.

Bottom copy quality rules:

- Each line should add new information. Do not repeat the title in different words.
- Start concrete, then explain. Avoid opening with conclusions such as `AI 正在重构工作方式` before stating the actual event.
- Use everyday verbs: `接走`, `分配`, `验收`, `变贵`, `变慢`, `先开放`, `先用上`, `拿不到`, `抢入口`.
- Prefer `普通人...`, `对你来说...`, or direct action language when the line is about viewer meaning.
- Avoid jargon-only phrasing such as `能力边界变化`, `工作流适配`, `产业范式迁移`, `组织效率重构`, unless immediately translated into a concrete consequence.
- The final `信息差：...` line should be a sharp conclusion the viewer can remember, for example `信息差：拉开差距的不是有没有 AI，而是谁先学会指挥 AI`.

## One News Event Pattern

Use this skill for one event at a time. For example, "GPT-5.6 enters limited preview" is one event. The five images should all support that same event from different angles:

- person/company/product photo
- official evidence screenshot
- product/API/Codex entry screenshot
- media report screenshot
- related company or product scene

The title and `info_rows` explain the event. The images should not be five separate text cards repeating the explanation. If a source page is unusable, replace it with another real image source instead of making an all-text substitute.

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

Final deliverables should be organized with Chinese names rather than raw English slugs. Use a dated top-level folder and split videos, covers, and overview images:

```text
导出-2026年06月28日AI信息差快报/
  01-视频/
    01-新模型先过安审-OpenAI与Anthropic/
      视频-01-新模型先过安审-OpenAI与Anthropic.mp4
  02-封面/
    01-新模型先过安审-OpenAI与Anthropic/
      封面-01-新模型先过安审-OpenAI与Anthropic.jpg
  03-总览/
    视频总览-2026年06月28日AI信息差快报.jpg
    封面总览-2026年06月28日AI信息差快报.jpg
```

Rules:

- The top-level export folder should include the date and batch theme.
- Use `01-视频`, `02-封面`, and `03-总览` as the first split.
- Each topic gets a numbered Chinese topic folder.
- File names should start with `视频-` or `封面-`, then repeat the topic name.
- Keep English product/company names only where they help recognition, such as `OpenAI`, `DeepSeek`, `GLM-5.2`, or `Google`.
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

- Maintain a per-batch `选题记录.md` in the project folder, or update an existing `topic-history.md` when the project already has one.
- Record date, topic title, company/product, source URLs, selected angle, and final output folder.
- Before every auto-scout run, compare candidates against previous records and dated export folders.
- Do not repeat the exact same event from a previous day. Prefer a follow-up only when there is a new development, and label it clearly as a follow-up angle.
- If the workflow rules, scripts, or skill documentation change, copy the skill into the user's GitHub skill repository and push the commit after validation.
- Generated video assets do not need to be pushed to the skill repository unless the user explicitly asks; only reusable skill/workflow updates should be pushed.
