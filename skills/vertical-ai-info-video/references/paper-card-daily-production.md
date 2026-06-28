# White Paper Card Daily Production Workflow

This reference captures the confirmed production logic for the normal `vertical-ai-info-video` daily/news-video workflow. Use it for daily 08:00 batches, manual rerenders, and any request that asks to standardize or update the skill.

## Default Visual Contract

- Format: 9:16, `1080x1920`, 7 seconds, no voiceover, with BGM unless the user asks for silence.
- Card: one white textured paper card on a dark phone-like background.
- Title: very bold black headline, usually two centered lines.
- Ribbon: one purple horizontal rounded ribbon directly under the headline.
- Media: one middle media frame containing the original five-image carousel for the same news event.
- Bottom: structured thin-line rows, shown as a full set by default.
- Date: show the newest verified date on the card as a small top-right marker, such as `最新 2026.06.28`.
- Positioning label: keep `AI 信息差快报` small and secondary.
- Do not add carousel dots, decorative divider lines, empty bands, large footers, or dark-template components.

## Title And Ribbon Logic

The top area must work like the approved reference cases:

```text
黑色标题第 1 行：谁/什么 + 发生了什么具体事
黑色标题第 2 行：这件事造成什么变化、冲突或反差
紫色条：最大信息差、普通人该注意什么、或者下一步行动
```

Good title tests:

- A normal viewer can understand the basic story within 3 seconds.
- The title contains a concrete actor, product, policy, number, company, or event.
- The ribbon does not repeat the title; it translates the event into a viewer-facing takeaway.
- The wording is sharp but still supported by sources.

Avoid:

- Mood-only titles such as `AI 又出大事了`.
- Abstract titles such as `能力边界正在变化`.
- Repeating the same phrase in both the title and purple ribbon.
- Purple title panels as the default. The current default is black title plus purple ribbon.

## Language Style

- Use plain, short Chinese that a non-specialist can understand.
- Prefer concrete nouns and verbs: `入口`, `账号`, `算力`, `模型`, `试用`, `下单`, `合规`, `排队`.
- Put the strongest contrast up top, not hidden in the bottom rows.
- The purple ribbon should feel like a takeaway, not a news subtitle.
- Do not exaggerate unverifiable claims for clicks.

## Bottom Row Structure

Use `body_style: "editorial_lines"` and 5 rows by default:

```text
01 事件：verified event in plain language
02 关键：what changed behind the surface headline
03 跟你有关：normal-viewer meaning
04 机会 / 风险 / 变化：who benefits, who is affected, or what boundary changed
05 信息差：final usable conclusion
```

Rules:

- Each row should be readable as a standalone screen sentence.
- Use `跟你有关` unless the line is truly a concrete personal opportunity; then `普通人机会` or `机会` is acceptable.
- Keep rows short enough to fit one line when possible.
- Bottom rows appear as a full set by default. Do not animate them row by row unless explicitly requested.

## Image Sourcing And Sequence

Each video is one news event with multiple real images, not five text cards.

Image priority:

1. Real person, company, or product image.
2. Official page, announcement, docs, product entry, API, or app screenshot.
3. Media report screenshot.
4. Clean explanatory source card only when it supports the story.
5. Auxiliary context image last.

Sequence rules:

- First image must identify the protagonist/company/product whenever possible.
- Core source screenshots can stay longer with `image_hold_weights`, commonly `[1, 2, 1, 1, 1]`.
- Do not use blocked pages, blank screenshots, download-error cards, `403`, `429`, or `图片源不可用`.
- Run `scripts/check_image_sequence.py --strict` before rendering.
- Inspect the contact sheet before final delivery.

## Cover Logic

Cover images are for 小红书/抖音 recognition:

- Prefer real people or company/product images first.
- The title must be more visually important than the face, but should not destroy the face.
- Use a company badge or logo as secondary recognition.
- Use one conclusion row only; do not turn the cover into a full explainer.
- Reuse the same title/ribbon logic as the video, but shorten for cover readability.

## BGM Logic

- Use local BGM assets from the skill BGM pool.
- For serious company, policy, infrastructure, or safety topics, include `bba进行曲.mp3` in the candidate set with higher weight.
- Match topic mood before randomness.
- Keep final duration at 7 seconds unless the user says otherwise.
- Do not upload user music files to GitHub.

## Delivery Contract

Every finished batch goes under:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/
  导出-YYYY年MM月DD日AI信息差快报/
    01-视频/
    02-封面/
    03-发布文案/
    04-总览与记录/
    05-素材与来源/
```

Each topic must include:

- final mp4 in `01-视频`
- cover jpg in `02-封面`
- 小红书 and 抖音 publishing markdown in `03-发布文案`
- video overview, cover overview, render validation, and topic record in `04-总览与记录`
- configs, preflight image, contact sheet, and source images in `05-素材与来源`

## Validation Checklist

Before reporting completion:

- Confirm each MP4 is 7 seconds.
- Confirm each MP4 contains video and audio streams.
- Confirm each contact sheet shows black title, purple ribbon, middle carousel, and bottom rows.
- Confirm images are complete inside the media frame and not leaking off-screen.
- Confirm there are no carousel dots or old dark-template remnants.
- Confirm publishing copy exists for 小红书 and 抖音.
- Update `选题历史.md` so future daily runs avoid exact repeats.

## GitHub Sync Rule

Push reusable workflow changes to `hpuxyh/ai-video-skills`.

Push:

- skill docs
- style guide updates
- scripts
- reusable examples or manifests

Do not push by default:

- generated MP4 files
- generated cover JPG files
- downloaded third-party news images
- user-owned music files

## Approved 2026-06-28 Second-Batch Title Pattern

Use this batch as the canonical example for the white paper-card title pattern:

| Topic | Black title | Purple ribbon |
| --- | --- | --- |
| SpaceX 出租算力 | `SpaceX 开始出租 AI 算力` / `开源模型公司抢 GPU 入口` | `真正稀缺的不是模型，是算力！` |
| Anthropic 指控阿里 | `Anthropic 指控阿里蒸馏 Claude` / `2.5 万假账号狂刷模型` | `AI 公司不只防黑客，也防能力被偷学！` |
| 阿里 HappyHorse | `阿里视频模型 HappyHorse 升级` / `AI 视频开始抢创作者` | `会写分镜的人，先吃到 AI 视频红利！` |
| 豆包内测打车 | `豆包开始内测打车` / `AI 应用不只会聊天` | `聊天框正在变成新的下单入口！` |
| 百度文心入口合并 | `百度合并文心 AI 入口` / `普通人别再找错入口` | `别只追新模型，先找对官方入口！` |

