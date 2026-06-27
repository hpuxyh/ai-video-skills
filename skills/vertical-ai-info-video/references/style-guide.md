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
  "beat_cuts": [0.90, 1.99, 3.87, 5.83],
  "bgm": {
    "path": "assets/audio/bgm.mp3",
    "start": 3,
    "volume": 0.55
  }
}
```

All relative paths resolve from `--project-dir`.

## Request Routing

Use two modes:

1. Specific-topic mode: if the user gives a concrete topic, event, company, URL, or direct instruction, create one video for that event.
2. Auto-scout mode: if the user asks for an AI information-gap video but does not provide a concrete topic, search the latest 7 days of AI news and choose 5 topics across China and the US.

In auto-scout mode:

- Search current sources because the 7-day window is time-sensitive.
- Prefer China/US AI stories with clear platform appeal: model releases, policy/regulation, major product launches, safety/security, AI hardware, agent/tools, major company moves, and consumer/workflow impact.
- Select 5 distinct one-event topics. Avoid five variations of the same model launch or the same company.
- Choose topics that can support real images and a people-first or company-recognition cover.
- Show the 5 selected topics with one-line rationale before rendering if the user has not explicitly approved batch generation.
- Generate 5 separate videos and covers. Do not merge the topics into one compilation video.
- Each topic must still follow the one-event pattern and row order: `结论` / `跟你有关` / `发生` / `谁先用` / `影响` / `信息差`.

## Title Defaults

- `title_weight_multiplier`: `0.9`
- `title_oblique`: `-0.075`
- No glow, no black offset shadow, no highlight.
- Keep the title large enough for mobile viewing; reduce text length before shrinking too much.

## Layout Defaults

- `photo_box`: `[0, 515, 1080, 1235]`
- Info rows start at `y=1288`, row height `64`.
- Top brand pill stays at the top-right.
- Do not draw carousel dots, footer labels, or decorative title bands.

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
