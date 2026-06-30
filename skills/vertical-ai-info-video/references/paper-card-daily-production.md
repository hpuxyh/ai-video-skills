# White Paper Card Daily Production Workflow

This reference captures the confirmed production logic for the ordinary `vertical-ai-info-video` daily workflow. The ordinary version uses the same controversy-first topic screening, three-line title logic, cover-title logic, dense bottom copy, and delivery structure as the 推特版 workflow. It only differs in final evidence-source choice: the core evidence image can be a media report, official page, data chart, product page, research page, filing, or X/Twitter screenshot, whichever explains the topic most clearly.

## Default Visual Contract

- Format: 9:16, `1080x1920`, 7 seconds, no voiceover, with BGM unless the user asks for silence.
- Card: one white textured paper card on a dark phone-like background.
- Title: very bold three-line headline, usually two black lines plus one blue emphasis line.
- Ribbon: no large purple ribbon by default. Purple ribbon/panel is legacy and only used on explicit request.
- Media: one middle media area containing the original five-image carousel for the same news event.
- Image transition: use short soft fade transitions between carousel images. Normal photos can cross-fade directly, but text-bearing screenshots/source cards/product UI must use split fade-out/fade-in so two text layers never overlap. Avoid hard-only cuts, fast left-right slide switching, white flashes, empty side gaps, or text-on-text overlap.
- Media fit: real people/product images may fill the media area; screenshots, source cards, product UI, tweet cards, and other text-bearing images must use safe-fill behavior. Enlarge them as much as possible and crop only background/empty edges, but preserve the full text and key UI without cropping, hiding, or partial cut-off.
- Bottom: structured unnumbered cyan-highlight reading lines, revealed one by one at a readable pace, then kept visible.
- Date: show the newest verified date on the card as a small top-right marker, such as `最新 2026.06.28`.
- Positioning label: keep `AI 信息差快报` small and secondary.
- Do not add carousel dots, decorative divider lines, empty bands, large footers, or dark-template components.

## Title And Ribbon Logic

The top area must work like the approved reference cases:

```text
黑色标题第 1 行：谁/什么 + 发生了什么具体事
黑色标题第 2 行：这件事造成什么变化、冲突或反差
蓝色第 3 行：最大信息差、普通人该注意什么、或者下一步行动
```

Good title tests:

- A normal viewer can understand the basic story within 3 seconds.
- The title contains a concrete actor, product, policy, number, company, or event.
- The blue third title line does not repeat the title; it translates the event into a viewer-facing takeaway.
- The wording is sharp but still supported by sources.

Avoid:

- Mood-only titles such as `AI 又出大事了`.
- Abstract titles such as `能力边界正在变化`.
- Repeating the same phrase in both the title and blue third line.
- Purple title panels or purple ribbons as the default. The current default is black title plus blue third-line emphasis.

## Language Style

- Use plain, short Chinese that a non-specialist can understand.
- Prefer concrete nouns and verbs: `入口`, `账号`, `算力`, `模型`, `试用`, `下单`, `合规`, `排队`.
- Put the strongest contrast up top, not hidden in the bottom rows.
- The blue third title line should feel like a takeaway, not a news subtitle.
- Do not exaggerate unverifiable claims for clicks.

## Controversy-First Topic Sourcing

The ordinary daily video now uses a 2-3 day, official-first and controversy-first X/Twitter hotspot workflow. It is not a broad news digest and should not soften controversy judgment just because it is the ordinary version.

Scouting sequence:

1. Check major model-company official accounts, product/research official accounts, and founder/CEO/core-person accounts first.
2. For each official or core-person signal, check whether selected AI digest, media, market, and viral accounts amplified or debated the same event.
3. Open the core post in the user's logged-in local Google Chrome X/Twitter session when available. Record visible replies, reposts, likes, views, and quote/spread signals. These are visible-page signals, not API totals.
4. Scroll the core post and collect a small visible comment/reply sample. A practical default is the post first screen plus 2-4 downward scrolls, enough to review roughly 20-50 visible comments/replies when X loads them.
5. Select topics with the same controversy and emotion standard as the 推特版 workflow: visible argument, anxiety, anger, sarcasm, distrust, fairness disputes, fear, job worry, privacy/safety concern, or strong quote/repost disagreement.
6. Confirm the facts with an official page, media report, data chart, product page, filing, or research page before rendering.

The source notes for every selected topic should include:

```text
discovery account/source:
core X/Twitter URL:
visible engagement signal:
typical controversy comment 1:
typical controversy comment 2:
confirmation source:
final screenshot source:
information-gap angle:
duplicate check:
```

Do not describe comment sentiment as full-platform sentiment. Use wording such as `可见评论样本显示`. Do not select only generic praise such as `wow`, `cool`, or `amazing` as controversy evidence.

## Bottom Row Structure

Use unnumbered cyan-highlight reading lines and 6 rows by default for daily controversy-first batches:

```text
01 事件：verified event in plain language
02 关键：what changed behind the surface headline
03 跟你有关：normal-viewer meaning
04 机会 / 风险 / 变化：who benefits, who is affected, or what boundary changed
05 信息差：final usable conclusion
06 结论：one memorable ordinary-viewer takeaway when the story needs it
```

Rules:

- Each row should be readable as a standalone screen sentence.
- The structure names above are writer-side checks only. Do not render labels such as `事件`, `关键`, `冲突`, `影响`, `信息差`, or `结论`.
- Use `跟你有关` as a writing test unless the line is truly a concrete personal opportunity; then `普通人机会` or `机会` is acceptable internally.
- Keep rows short enough to fit one line when possible.
- Bottom rows reveal one by one by default in MP4 output. Recommended timing: start around `1.05s`, interval around `0.52s`, duration around `0.42s`, so all rows are stable by about `3.5s`.

## Image Sourcing And Sequence

Each video is one news event with multiple real images, not five text cards.

Image priority:

1. Real person, company, or product image.
2. Core evidence screenshot: the clearest official page, media report, data chart, product page, filing, research page, or X/Twitter post for the event.
3. Official page, announcement, docs, product entry, API, or app screenshot.
4. Media report screenshot or data/chart screenshot.
5. Clean explanatory source card only when it supports the story.
6. Auxiliary context image last.

Sequence rules:

- First image must identify the protagonist/company/product whenever possible.
- The second image should usually be the core evidence screenshot. It does not have to be a tweet. For ordinary videos, prefer the screenshot that explains the fact most clearly to a normal Chinese viewer: media page, official page, data chart, product page, research page, filing, or tweet/X screenshot.
- Core source screenshots can stay longer with `image_hold_weights`, commonly `[1, 2, 1, 1, 1]`.
- Use `image_roles` and `image_quality` to mark screenshots/cards/products so the renderer can preserve them with safe-fill. Roles/qualities such as `media`, `source-card`, `official-screenshot`, `clean-card`, `product`, `tweet`, and `screenshot` should be enlarged as much as possible but must not crop text or key UI.
- Use `media_transition_mode: "fade"` and `media_transition_duration` around `0.30`-`0.36` for readable image transitions. The renderer must avoid direct overlap between two text-bearing media frames.
- Do not use blocked pages, blank screenshots, download-error cards, `403`, `429`, or `图片源不可用`.
- Run `scripts/check_image_sequence.py --strict` before rendering.
- Inspect the contact sheet before final delivery.

## Cover Logic

Cover images are for 小红书/抖音 recognition:

- Prefer real people or company/product images first.
- The title must be more visually important than the face, but should not destroy the face.
- Use a company badge or logo as secondary recognition.
- Use one conclusion row only; do not turn the cover into a full explainer.
- Reuse the same three-line title as the video and 推特版 cover logic by default. Only shorten or rewrite the cover title when the user explicitly asks or when the exact title cannot fit after reasonable layout adjustments.

## BGM Logic

- Use local BGM assets from the skill BGM pool.
- Daily and batch scripts must run `scripts/select_bgm_for_batch.py` after generating configs and before rendering. Do not rely on inherited `bgm` fields from older configs.
- For serious company, policy, infrastructure, or safety topics, include `bba进行曲.mp3` in the candidate set with higher weight.
- Match topic mood before randomness.
- For 5-video batches, repeats are allowed when they fit the topic, but all five videos must not use the same track unless the user explicitly asks for a single unified soundtrack.
- Save a BGM plan such as `renders/bgm-selection-plan.json` and include it in the delivery evidence.
- Keep final duration at 7 seconds unless the user says otherwise.
- Do not upload user music files to GitHub.

## Delivery Contract

Every finished batch goes under:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/
  导出-YYYY年MM月DD日AI信息差快报/
    01-主题名/
      视频.mp4
      封面.jpg
    02-主题名/
      视频.mp4
      封面.jpg
    ...
    整体描述.md
    _记录/
      视频总览.jpg
      封面总览.jpg
      渲染校验.md
      选题记录.md
      bgm-selection-plan.json
      素材与来源/
```

Each topic folder must include:

- `视频.mp4`
- `封面.jpg`

The batch root must include `整体描述.md`, matching the 推特版 delivery style. It should merge all topics' cover/video paths, 抖音 titles, video-bottom copy, tags, source summaries, and posting notes. If a compatibility `文案.md` is generated, keep it under `_记录/` or mention it from `整体描述.md`; do not mix it into the core topic folders by default.

The project folder should be organized by topic/video first, not by asset type. Do not make the user jump between separate `视频`, `封面`, and `文案` category folders to assemble one post.

Keep validation, overview, source material, and debug evidence under `_记录/` so the delivery surface stays clean.

If an older renderer or batch script still creates the legacy category-first structure (`01-视频`, `02-封面`, `03-发布文案`, `04-总览与记录`, `05-素材与来源`), run:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/package_project_delivery.py \
  --legacy-batch-dir /path/to/legacy-batch \
  --output-dir /path/to/clean-project-delivery \
  --overwrite
```

## Validation Checklist

Before reporting completion:

- Confirm each MP4 is 7 seconds.
- Confirm each MP4 contains video and audio streams.
- Confirm each config has a selected `bgm.path` and `bgm.source_track`.
- For multi-video batches, confirm the BGM plan did not assign one inherited track to every video.
- Confirm the final delivery folder is topic-first: each video topic has exactly the two core files `视频.mp4` and `封面.jpg`.
- Confirm root `整体描述.md` contains every topic's video path, cover path, 抖音 title, bottom copy, tags, and source summary.
- Confirm each contact sheet shows the red metadata tag, black/blue three-line title, middle carousel, and bottom cyan-highlight reading lines without `01`-`05` number pills.
- Confirm images occupy the media area as fully as possible, text-bearing images are not cropped or partially cut, and images are not leaking off-screen.
- Confirm carousel image transitions have soft fade motion without white flashes, empty side gaps, distracting rapid left-right slides, or overlapping text from two screenshots.
- Confirm there are no carousel dots or old dark-template remnants.
- Confirm publishing copy exists for 小红书 and 抖音.
- Confirm `选题记录.md` includes discovery source, visible engagement signal, two typical controversy/comment samples or paraphrases, confirmation source, final screenshot source, and duplicate check for every selected topic.
- Update `选题历史.md` so future daily runs avoid exact repeats.

## GitHub Sync Rule

Push reusable workflow changes to `hpuxyh/ai-video-skills`.

Push:

- skill docs
- style guide updates
- scripts
- reusable examples or manifests
- successful daily `records/ai-info-video/YYYY-MM-DD/final-delivery/` archives, including final MP4/JPG deliverables, `整体描述.md`, configs, validation records, contact sheets, selected source screenshots, and source notes

Do not push:

- user-owned music files
- browser caches
- failed downloads
- temporary render caches
- duplicate intermediate files unrelated to the final published package

## Approved 2026-06-28 Second-Batch Title Pattern

Use this batch as the canonical example for the white paper-card title pattern:

| Topic | Black title | Blue third title line |
| --- | --- | --- |
| SpaceX 出租算力 | `SpaceX 开始出租 AI 算力` / `开源模型公司抢 GPU 入口` | `真正稀缺的不是模型，是算力！` |
| Anthropic 指控阿里 | `Anthropic 指控阿里蒸馏 Claude` / `2.5 万假账号狂刷模型` | `也防能力被偷学` |
| 阿里 HappyHorse | `阿里视频模型 HappyHorse 升级` / `AI 视频开始抢创作者` | `会写分镜的人先吃红利` |
| 豆包内测打车 | `豆包开始内测打车` / `AI 应用不只会聊天` | `聊天框变成下单入口` |
| 百度文心入口合并 | `百度合并文心 AI 入口` / `普通人别再找错入口` | `先找对官方入口` |
