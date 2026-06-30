---
name: vertical-ai-info-video-推特版
description: "Generate 9:16 Chinese AI information-gap short videos from recent X/Twitter AI hotspots, with the second carousel image fixed as a verified core tweet screenshot, plus real news/product images, people-first covers, bold no-glow headline typography, beat-synced motion, paper-card previews, no voiceover, and local BGM mixing. Use when the user asks for 推特版 AI 信息差短视频, X/Twitter AI 热点, 近2-3天 AI 热点, or a tweet-anchored vertical AI news video."
---

# Vertical AI Info Video - 推特版

## Overview

Use this skill to produce the X/Twitter-first version of the fixed 9:16 AI 信息差短视频 workflow: find recent AI hotspots on X/Twitter, filter them through the GitHub-synced viral topic screening project, confirm the topic with a core tweet from the relevant person or official account, place that tweet screenshot as the second carousel image, then keep the original video system: people-first cover image, top positioning label, bold three-line title, real image carousel in the middle, label-free bottom description lines revealed one by one, strong push-pull image motion, no voiceover, and 7-second BGM from a local audio file.

The defining rule of this version is: every auto-scouted topic must have a verified tweet anchor and a viral-topic rationale. The second image in the video carousel must be a clean screenshot of the core tweet that confirms why this topic exists. Because viewers need time to read it, image 2 should hold for roughly twice as long as the other carousel images.

The final audience-facing output must be Chinese-first. If the source tweet, chart, UI, or screenshot is in English, keep the original asset for traceability, then create a Chinese-localized tweet card or overlay so the final image/video can be understood without reading English. If the source screenshot is already mainly Chinese and readable, do not add a redundant `中文释义` block; use a clean crop or a lightly framed source card instead. Product names, company names, handles, and short technical terms may remain in English when they help recognition.

When selecting topics, writing the three-line title, and writing the bottom description, use the GitHub-synced writing skills as hard gates: `twitter-ai-viral-topic-selection`, `twitter-ai-viral-title-writing`, and `twitter-ai-viral-description-writing`. Do not start image capture or rendering until the topic, title, and bottom description pass those three skills.

This version must preserve the original real-visual carousel logic. X/Twitter changes the topic discovery and proof chain only; it must not turn the video into a deck of self-made explainer cards. The middle image area should stay bright, real, and evidence-like: people, company/product photos, official pages, product UI, news screenshots, and one tweet anchor.

It also supports the confirmed clean white paper-card explainer mode: a white textured 9:16 card with a red `重磅` tag, small `AI 信息差快报` positioning label, three oversized black/blue title lines, real news media in the middle, and label-free cyan-highlighted explanatory lines at the bottom. Do not use the older purple title/ribbon style unless the user explicitly asks for that legacy variant.

This skill is optimized for fast iteration. When the user asks for visual tuning, generate preview screenshots first. Render the full MP4 only after the user confirms the style.

## Recent Run Failure Guardrails

These hard gates come from the 2026-06-30 manual Twitter batch failure. Treat them as production rules, not optional notes.

- Freshness audit first: when the request says latest, today, daily, or latest 2-3 days, do not reuse an old manual batch or an old topic list as the source of truth. Start by writing or updating a freshness audit that lists every candidate, the real source date, the visible X/Twitter date, the source URL, and the pass/fail decision.
- Real date beats config date: never trust only local `date`, `header_source`, folder names, or `06.30` labels in previous configs. Verify freshness from the source article/page timestamp or the visible X/Twitter timestamp captured in Chrome. If a source page is older than the 2-3 day window, reject it even if the local config says today's date.
- Re-scout stale batches: if any topic in a 5-video batch fails freshness or duplicate checks, re-run candidate selection for the whole batch, then present the replacement 5 topics with rationale, anchor, cover direction, and information-gap angle before rendering unless the user has already explicitly approved the replacements.
- Do not patch stale topics with better assets: better screenshots, covers, or descriptions do not fix an old topic. Replace the topic first, then rebuild screenshots, cover, config, publishing copy, records, and history for the new topic.
- Chrome capture is the screenshot authority: public oEmbed, search snippets, or remembered links are discovery aids only. A final tweet anchor must have a local Chrome screenshot plus metadata. For X/Twitter final assets, the raw screenshot must be from `--tweet-only` / `article[data-testid="tweet"]` or have an explicit reviewed `crop_box`.
- Inspect pixels, not just files: after source capture and again after rendering a preview/contact sheet, visually inspect the images. Reject screenshots with left navigation, right sidebar, browser chrome, unrelated replies, blank margins, half-visible cards, cropped avatars/faces/logos, blurry text, blocked pages, or source-error placeholders.
- Text review is mandatory: before export, check that title, middle media, and bottom rows do not overlap; rows are aligned; no row is hidden, clipped, or squeezed into one-character wraps; bottom copy is 4-6 viewer-facing Chinese lines with no visible labels such as `信息差是`, `发生了什么`, `关键事实`, `结论`, or internal production notes.
- Cover source must be revalidated: a cover cannot be a video first frame, tweet card, paper-card screenshot, old topic cover, or generic webpage crop. Re-check the cover logic before export, prefer recognizable people/company/product identity, record `cover_source_type` and source asset, archive the cover background, and run cover review.
- Confirm skill provenance: before a production run, compare the active local skill under `~/.codex/skills` with the GitHub/repo copy under `skills/vertical-ai-info-video-推特版/`. If they differ, sync or clearly report the mismatch before running. Do not claim to be using the GitHub-synced skill without checking the actual file being executed.
- Use the correct renderer for the approved style: clean white paper-card MP4s should be rendered with the clean white renderer (for example `/Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_clean_white_video.py` when available). Use the older `render_vertical_info_video.py` only for the non-paper-card/legacy template or when the user explicitly requests that style.

## Topic Quality Hard Gate

This gate must run before title writing, bottom-description writing, screenshot cleanup, cover generation, or MP4 rendering. The most common failure is treating a recent, visually fixable story as an approved topic. Do not do that.

- A freshness audit only says a topic is recent enough to consider. It is not a topic-selection pass.
- Run the `twitter-ai-viral-topic-selection` score for every candidate. Record controversy strength, emotional spread, source priority, public familiarity, information gap, comment/spread signal, visual assets, total score, and decision band.
- Do not render a 5-topic daily batch with any topic below 80 unless the user explicitly approves a backup topic after seeing the score and weakness.
- Reject developer-only, narrow tool-fix, minor product-update, pure benchmark, pure funding, or weakly emotional topics even when they have a clean X screenshot and a strong company name.
- Reject exact or near duplicates across 推特版 and ordinary AI 信息差 histories before rendering. Same event/development plus same source or same viewer takeaway is a hard fail, even if the cover or tweet anchor is new.
- Treat the candidate list, freshness audit, and source-capture table as separate stages. A row appearing in the candidate pool must not be copied into final configs until it has passed scoring and duplicate checks.
- Visual review cannot approve topic quality. Contact sheets, cover review, MP4 specs, and screenshot cleanliness only validate assets; they do not make a weak topic acceptable.
- If topic quality fails after rendering, replace the topic and rebuild screenshots, title, bottom copy, cover, records, and history. Do not patch the old topic with better visuals.
- The final review must include a topic-quality audit alongside the visual audit. If the final response cannot say which topics passed, which were deleted, and why, the run is not complete.

## Mandatory Execution Order

Every production run must begin by reading the current local requirements, workflow, quality standards, and purpose before taking action. Do not rely on remembered workflow details from an older run.

1. Read this `SKILL.md` completely, then read `references/style-guide.md`.
2. Read `twitter-ai-viral-topic-selection`, `twitter-ai-viral-title-writing`, and `twitter-ai-viral-description-writing`; these are hard gates for topic selection, title writing, and bottom description writing.
3. Read `projects/twitter-viral-topic-screening/source-accounts.md` and `candidate-template.md` when scouting topics.
4. Read 推特版 and ordinary-version history records before selecting topics, then remove exact duplicates and near-duplicates.
5. In auto-scout mode, build a default pool of 30 candidate topics from the latest 2-3 days whenever source availability allows. If fewer than 30 credible candidates can be found, record the reason in `选题记录.md`.
6. Score the candidate pool with the controversy-first model, rank it, and select the final 5 topics only after scoring. Do not jump directly from a few discovered posts to the final 5.
7. For each selected topic, confirm the core tweet anchor, write the three-line title, then write the 4-6 line bottom description. The title and description must pass the title and description skills before screenshots or rendering begin.
8. Capture the core X/Twitter screenshot from local Chrome with `--tweet-only` or an explicitly reviewed crop, then capture only the best supporting comment/reply screenshot when useful. Keep the final video to a small number of X screenshots, normally the core tweet plus one comment/reply.
9. Prepare real people/company/product/source visuals, build configs, choose BGM, render videos and covers, run `ffprobe`, inspect contact sheets, and package the final delivery.
10. Before any GitHub upload, commit, push, or success report, run the final pre-upload quality gate below. If it finds a problem, fix that stage and rerun the relevant checks before uploading.

## Workflow

1. Route the request:
   - If the user gives a concrete news topic, company, event, URL, tweet URL, or instruction, use the given topic directly and generate one video for that event using the confirmed workflow.
   - If the user does not give a concrete topic, default to daily auto-scout: search X/Twitter for AI-related hotspots from the latest 2-3 days, build a default 30-topic candidate pool from viral/media/source accounts when possible, score and rank candidates with the viral topic screening logic, verify the strongest candidates with official/news sources when needed, and generate 5 one-event videos.
2. Confirm or infer each video's topic, three-line animated title, bottom description lines, image set, cover, BGM, and tweet anchor.
3. Before choosing or rendering topics, read the GitHub-synced screening project under `projects/twitter-viral-topic-screening/`, plus history records and local `选题记录.md` / `topic-history.md`. Also read the ordinary AI 信息差 news-video history under `/Users/xieyahao/Desktop/我自己/小红/视频/新闻视频/选题历史.md`. Do not produce an already-rendered exact duplicate across either workflow. Exact duplicate means the same company/person/product, the same event/development, the same core source tweet or factual source, and the same information-gap angle/viewer takeaway. Similar company/theme is allowed; reuse the company only when there is a new event, new development, new source tweet, or clearly different information-gap angle.
4. Require one verified tweet anchor for every topic. Prefer the direct X/Twitter post from the core person involved in the event; if no person tweet exists, use an official company/product/research account. If only third-party commentary or viral-media amplification exists, use it only as a discovery signal, not as the anchor.
5. Capture source material in the user's local Google Chrome first. Open the chosen X/Twitter post and supporting official/news/product pages in the user's Chrome profile, using its existing login/session state, then save raw browser screenshots under the working project's `assets/raw/chrome/` directory. The tweet proof card and source evidence images should be derived from these Chrome screenshots by default. Do not replace Chrome capture with web search thumbnails, generated source cards, or guessed screenshots unless Chrome capture fails; if it fails, record the exact blocked URL and reason in the source notes before using any fallback. Use the provided Chrome capture command:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/capture_chrome_source.py \
  --url "https://x.com/example/status/123" \
  --output assets/raw/chrome/topic-tweet.png \
  --wait 8 \
  --tweet-only
```

For X/Twitter anchors, `--tweet-only` is the default requirement. It captures the visible `article[data-testid="tweet"]` card instead of the whole page, so the final proof image does not include the left navigation, right sidebar, empty browser area, unrelated replies, or half-visible surrounding posts. Use full-page screenshots only as raw evidence or when debugging, not as final carousel assets.

6. Require bright, real, topic-matched images. For news videos, image 1 should be a real person/company/product visual, preferably the most recognizable person in the story when there is one. Image 2 must be the verified core tweet screenshot or Chinese-localized tweet card derived from the local Chrome capture, and later images should add official/news/product evidence from Chrome-captured pages when possible. Do not use fake UI, abstract placeholders, dark information cards, or pure text cards as primary carousel images.
7. For each X/Twitter topic, capture more than the single core tweet when useful: after saving the core tweet screenshot, scroll the same Chrome thread and capture raw lower-thread evidence using `--scroll-y`, then derive one or two compact crops from the best replies, official follow-up comments, quote/repost embeds, or related posts. The normal final video should use two X screenshots total: one core tweet screenshot and one best supporting/comment screenshot. A second compact reply crop can be kept as backup or used only when the story genuinely needs it. Save final compact crops as `assets/raw/chrome/<topic-id>-reply-01-compact.png` and `assets/raw/chrome/<topic-id>-reply-02-compact.png`; keep any third raw screenshot only as backup unless the user asks for more. Run Chrome captures sequentially because they control the same visible browser window. These screenshots are supporting context only; they do not replace the primary tweet anchor. If the visible text is English, translate the key opinion or add a short Chinese caption/overlay before using it in final video frames; if the screenshot is already mainly Chinese and readable, do not add redundant Chinese interpretation.
8. For social publishing, generate a separate cover preview using the cover rules in `references/style-guide.md`: recognizable person first, company/product identity second, the same three animated title lines as the main cover headline, and one conclusion row only. If the visible product is backed by a larger parent company, trace that lineage before choosing the cover visual; do not stop at a narrow product-page screenshot when a stronger parent-company person or identity is available. Use `scripts/render_full_bleed_cover.py` or an equivalent dedicated cover renderer. Never create the final `封面.jpg` by extracting the first frame of the MP4. Cover configs must declare `cover_source_type` or `background_role`, plus `cover_source` / `cover_source_asset` / `cover_source_url`; screenshot-like values such as tweet, source-card, paper-card, webpage screenshot, video frame, or first frame are invalid cover backgrounds unless an official/product screenshot is explicitly documented as a last-resort fallback with `cover_fallback_reason`.
9. Select background music from the local BGM pool using the BGM rules below. For a 5-video batch, choose one track per video by theme fit plus weighted randomness, with `bba进行曲.mp3` favored.
10. Build a JSON config using the schema in `references/style-guide.md`. For paper-card explainer mode, build a paper-card JSON and render a static preview first with `scripts/render_paper_card_preview.py`.
11. Before rendering, run the visual review gate on every topic config, then inspect the generated report/contact sheet. The review target is strict:
   - Image quality: screenshots are clear enough, high-resolution, not blank, not over-smoothed, and cropped to the useful source area.
   - Screenshot space: tweet screenshots show the core post card only; no side navigation, right sidebar, unrelated replies, bottom login bars, huge blank margins, or browser chrome unless explicitly kept as evidence outside the final video.
   - Text layout: title, middle image, and bottom description do not overlap; bottom rows stay inside the safe area; text lines are aligned, readable, and not squeezed into awkward one-character wraps.
   - Description discipline: bottom copy must follow `twitter-ai-viral-description-writing`: 4-6 pure viewer-facing Chinese lines, no visible labels such as `发生了什么`, `关键事实`, `背后冲突`, `影响谁`, `结论`, or `信息差`.

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/review_visual_quality.py \
  --config configs/video.json \
  --project-dir . \
  --report renders/video-review.json \
  --contact-sheet renders/video-review-contact-sheet.jpg \
  --strict
```

If the review fails or the contact sheet shows `图片源不可用`, `429`, `403`, login wall, a blank page, a blocked page, unrelated search results, sidebars around the tweet, awkward crop, text overlap, or uneven/blocked typography, stop. Reopen the source in Chrome, recapture with `--tweet-only` or a tighter element/crop, rewrite long bottom rows, and rerun the review. Never ship a video with an asset-error card, cluttered tweet screenshot, or visibly messy text layout.
12. Run the renderer that matches the approved style. For the current clean white paper-card mode, use the shared clean white renderer:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video/scripts/render_clean_white_video.py \
  --config configs/video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

Use `scripts/render_vertical_info_video.py` only for the non-paper-card/legacy vertical template or when the user explicitly asks for that style:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/render_vertical_info_video.py \
  --config configs/video.json \
  --project-dir . \
  --output renders/output.mp4 \
  --contact-sheet renders/output-contact-sheet.jpg
```

13. Validate the MP4 with `ffprobe` and inspect the contact sheet before reporting completion.
14. Validate each cover before export. The cover must be a standalone 9:16 image generated from a cover config or explicit cover asset, not `ffmpeg -frames:v 1`, not the video first frame, not the tweet proof card, and not a paper-card screenshot. Reject a cover if it does not visibly follow the people/company-first logic. Run the same strict visual review gate on every cover config before rendering/exporting:

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/review_visual_quality.py \
  --config configs/cover.json \
  --project-dir . \
  --report renders/cover-review.json \
  --contact-sheet renders/cover-review-contact-sheet.jpg \
  --strict
```

The cover review must fail if the config lacks source provenance, lacks a recognized people/company/brand/product source type, or tries to use the core tweet/source card/webpage/video frame as the main cover background.
15. Run the final pre-upload quality gate below. Do this after rendering and packaging, but before GitHub archive, commit, push, or success report.
16. After validation, organize final deliverables under the dedicated Xiaohongshu video export folder. The user-facing handoff should be project-first and minimal: each topic gets one folder with only the final MP4 and cover image; the batch root gets one `整体描述.md` containing all five topics' cover/video paths, 抖音标题, video-bottom copy, and tags:

```text
/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/
  导出-YYYY年MM月DD日-HH点MM分-推特版AI信息差快报/
    01-中文话题名/
      视频.mp4
      封面.jpg
    02-中文话题名/
      视频.mp4
      封面.jpg
    整体描述.md
```

The folder name must clearly include `推特版` or `推特专用` so it is not confused with ordinary AI 信息差 videos.
17. Record the finished topics, 抖音标题, video-bottom copy, tags, source tweet URL, source tweet author, observed engagement signal, Chrome screenshot paths, source URLs, cover source asset, cover source type, cover config path, cover review report/contact sheet, information-gap angle, and final export folder in `整体描述.md`, local history records, and the GitHub-synced history records. Archive each selected cover background as `封面背景.jpg` under that topic's source folder so the cover-selection logic can be reviewed later. Keep Chrome/source screenshots, configs, contact sheets, source records, and detailed production notes in the working project or GitHub records, not mixed into the user-facing project folders unless the user asks for them.
18. Every successful invocation must sync to GitHub before reporting completion. Commit and push the history records, source notes, configs, cover configs, deliverable index, final media assets, and final source-review materials. The user's current rule is to upload the final exported package after each daily run; do not treat MP4/JPG deliverables as optional unless GitHub rejects the push or the user explicitly changes the rule. Never upload local BGM original files, browser caches, failed downloads, temporary render caches, or duplicate intermediate files.

## Final Pre-Upload Quality Gate

Run this gate after the final MP4s, covers, `整体描述.md`, and `_记录` package are assembled, and before uploading or pushing anything to GitHub. Create or update `_记录/最终上传前质量检查.md` with pass/fail notes for each topic.

If any item fails, do not upload and do not report the run as successful. Fix the specific problem, regenerate the affected screenshot/config/video/cover/copy, rerun the visual/contact-sheet review, and only then continue.

Required checks:

1. Screenshot quality:
   - X/Twitter screenshots must be complete, readable, and cropped to the useful post/comment area.
   - The core tweet screenshot should come from `--tweet-only` or an explicitly reviewed crop. It must not include left navigation, right sidebar, browser chrome, bottom login bars, unrelated replies, excessive blank space, or half-visible surrounding posts.
   - Comment/reply screenshots must be compact, ordinary-browser-readable blocks that show the author row and complete key text. Do not use a tall timeline column when a tight comment crop is enough.
   - Official/news/product/data screenshots must preserve the title, source identity, key chart/text/UI, and any logo or date needed to understand the source.
   - Reject screenshots with 403/429/Cloudflare/login-wall/blank/error states, blurred text, cropped faces/logos, or dark/gray overlays that make the image look broken.
2. Description and title correctness:
   - Re-check the three-line title against `twitter-ai-viral-title-writing`: line 1 has public conflict or familiar protagonist, line 2 has concrete event/change, and line 3 has ordinary-viewer consequence or information gap.
   - Re-check bottom copy against `twitter-ai-viral-description-writing`: 4-6 pure Chinese lines, default 6 for daily batches, no visible labels, no structure names, no exaggerated claims, and no angle drift away from the title.
   - Confirm `整体描述.md` contains the 抖音 title, video-bottom content, tags, and core tweet/source summary for every topic.
3. Visual quality:
   - Inspect every video contact sheet and cover overview. Title, screenshots, and bottom rows must not overlap, clip, squeeze into awkward wraps, or run outside the safe area.
   - Covers must be separately rendered people/company-first assets, not MP4 first frames, tweet cards, paper-card screenshots, or ordinary video frames.
   - Check cover brightness, face/logo protection, company/product recognition, title readability, and consistency with the three-line title.
   - Confirm final MP4s have video stream, audio stream, expected 1080x1920 resolution, and about 7 seconds duration unless the user requested otherwise.

## Topic Selection Modes

- Specific-topic mode: use the user's topic directly. Verify current facts when the topic is recent or time-sensitive, then create one cover and one video.
- X/Twitter auto-scout mode: when no concrete topic is provided, search the latest 2-3 days of AI discussion on X/Twitter first, build a default 30-topic candidate pool when possible, then select 5 topics with strong AI 信息差信号 and strong viral-topic scores.
- X/Twitter selection criteria: do not simply pick posts with the largest number. Build a candidate pool first from viral/media/source accounts, then pick the stories most suitable for AI 信息差短视频: public emotion trigger, viral source signal, information-gap strength, normal-viewer relevance, credible anchor, recognizable people/companies, available real imagery, platform-friendly tension, and a clean tweet anchor. Familiar protagonists and familiar public issues are preferred; obscure companies/products must have a very clear public conflict to survive.
- Heat judgment: treat X/Twitter engagement as a signal, not the only proof. Consider views, reposts, likes, replies, account authority, quote-post spread, whether AI builders are discussing it, whether viral media or prediction-market accounts have amplified it, and whether official/news sources can verify the underlying event.
- Daily freshness: before selecting auto-scout topics, check previous generated batches, local topic-history files, the GitHub-synced 推特版 history records, and the ordinary AI 信息差 news-video history. Do not choose an exact duplicate from either workflow: same company/person/product, same event/development, same core source tweet or factual source, and same information-gap angle/viewer takeaway. Similar company/theme is acceptable when the event, development, source, or information-gap angle is materially different.
- Auto-scout output: generate 5 independent videos, not one compilation. Each video keeps the same row logic, image logic, cover logic, and verification steps.
- Before rendering 5 videos, show the chosen 5 topics with one-line rationale, tweet anchor, likely cover assets, and the information-gap angle when the user has not already approved the topic list.

## Daily Execution Logic

- If the user provides a topic, tweet URL, company, event, or concrete instruction, do not auto-scout a new batch. Produce the requested topic only.
- If the user does not provide a topic, default to building and scoring a 30-topic X/Twitter AI candidate pool from the latest 2-3 days using the viral topic screening project, then select the top 5 that pass quality and duplicate checks.
- "Hot" does not mean likes-only. Rank candidates by public emotion trigger, viral account signal, tweet heat, account authority, quote/reply spread, source credibility, viewer relevance, information-gap strength, and available real assets.
- Use the scoring model from `twitter-ai-viral-topic-selection`: controversy strength, emotional spread, source priority, public familiarity, information gap, comment/spread signal, and visual assets. Do not select topics below 70 unless the user explicitly asks; prefer 80+ for a daily batch and 90+ for priority output.
- Before finalizing the 5 topics, check GitHub-synced 推特版 history, local topic history, and ordinary AI 信息差 news-video history. Reject exact duplicates across both ordinary and 推特版 workflows, using the same-company/person/product + same-event/development + same-source + same-information-gap-angle definition.
- A non-duplicate follow-up is allowed only when there is a materially new development, a new source tweet, or a different information-gap angle.
- After each successful run, update the history records and sync them to GitHub before telling the user the run is complete.

## Viral Topic Screening Logic

For auto-scouted 推特版 videos, AI relevance is only the entry gate. The strongest topics should look like:

```text
viral/media account signal + public emotion theme + clear information gap + credible source anchor + real visual assets
```

Source-account roles:

- Viral radar: `@Polymarket`, `@Kalshi`, `@ManifoldMarkets`, `@unusual_whales`, `@WatcherGuru`.
- AI digest/packaging: `@TheRundownAI`, `@rowancheung`, `@ArtificialAnlys`, `@AiBreakfast`, `@tldrnewsletter`.
- Credible media: `@ReutersTech`, `@technology`, `@theinformation`, `@TechCrunch`, `@verge`, `@WIRED`, `@VentureBeat`.
- Official/source anchor: the company, product, founder, CEO, product lead, researcher, creator, government official, or other primary actor.

Use viral/media accounts as discovery and packaging signals, not final proof. If a topic starts from a third-party viral account, find a primary-source tweet, official page, or reputable report before selecting it.

Prioritize public themes in this order:

1. 饭碗变化: replacement, layoffs, skill devaluation, work automation.
2. 钱和市场: prediction-market movement, stock reaction, chip orders, AI investment direction.
3. 造假和安全: deepfakes, scams, fake videos, voice cloning, data leaks, model misuse.
4. 版权和创作者冲突: film, music, writing, illustration, gaming, short-video creators.
5. 大厂战争: OpenAI, Google, Meta, Anthropic, xAI, Apple, Microsoft competition.
6. 普通人马上能用的新工具: slides, video, spreadsheets, websites, apps, investment research, office automation.
7. 孩子和教育: homework, cheating, tutoring, teacher replacement, child development.
8. 规则变化: regulation, courts, government procurement, safety reviews, platform bans.

Low-priority topics are pure benchmark posts, pure fundraising, pure papers, or pure developer tools unless they can be translated into a normal-viewer change in cost, access, risk, work, money, creativity, or daily tools.

Before rendering 5 videos, show the chosen 5 topics with one-line rationale, tweet anchor, likely cover assets, information-gap angle, public theme, viral-source signal, and score when the user has not already approved the topic list.

## Tweet Anchor Rules

- The second carousel image must be the topic-confirming X/Twitter screenshot.
- The tweet anchor should look like a bright, source-like artifact. The preferred default is the previously approved proof-card layout: a cleaned real tweet screenshot on the left, a Chinese interpretation block on the right, and source metadata at the bottom-left. Do not show internal timing notes such as "第二张图停留加长" in the final audience-facing card.
- For this proof-card layout, do not turn the frame into a new headline card. Use `中文释义` only when the source tweet, chart, or UI is not already Chinese-readable and needs localization. For English/non-Chinese sources, use `中文释义` as the small source-localization label, then 3-5 cyan highlighted Chinese lines that summarize the tweet's core fact and viewer meaning. For daily batch videos, prefer 5 lines: concrete fact, direct change, normal-viewer meaning, mechanism/boundary, and final takeaway. Do not write visible internal labels such as `事件：`, `关键：`, `冲突：`, `影响：`, or `信息差：` in those lines. If the source screenshot is mainly Chinese, skip the right-side interpretation block and keep the clean Chrome crop as the proof image unless extra context is truly needed.
- The typography should be tidy and consistent: at 1600x1000 source-card size, use roughly 34-40px bold Chinese for cyan highlighted lines, 29-34px for small labels, 23-26px for URL/source metadata, with even line height and aligned left edges. Prefer uniform full-width cyan highlight bars on the right side for cleaner video readability. If a line wraps into a single character or orphan word, rewrite the sentence shorter before shrinking below the normal font range.
- Prefer direct posts by the core person in the story: founder, CEO, product lead, researcher, government official, creator of the tool, or other primary actor.
- If no core-person post exists, use the official account for the company, product, lab, open-source project, or conference.
- If the topic is discovered through a third-party viral post, use that post for discovery only; then find a primary-source tweet, official page, or reputable report before making the final topic.
- Capture the raw tweet screenshot from the user's local Google Chrome first. Use Chrome because it carries the user's actual X/Twitter login state, cookies, locale, and extensions; this is more reliable than unauthenticated fetches, web search previews, or guessed screenshots. Save the raw capture as evidence before rendering the Chinese proof card.
- The screenshot should show the author, handle, post text, timestamp/date, and visible engagement when available.
- Crop the screenshot to the tweet body or post card. Preserve the author/avatar, handle, key tweet text, timestamp or visible engagement when available, and the main attached image/video/logo. Avoid narrow crops that cut off faces, avatars, company logos, product names, or the main media. Avoid showing right-side sign-up panels, bottom login banners, unrelated replies, blank loading areas, or browser chrome unless they are unavoidable and do not distract.
- Lower-thread support screenshots should be compact blocks, not full-height timeline columns. Crop each block like a single X post card: author row, readable text, and either one complete key image/chart or no media at all. Do not leave half-visible media at the bottom, and do not use a 900px-tall full column when a 350-620px block explains the point. For one topic, choose two compact blocks by default.
- In a 5-image, 7-second video, give the tweet-anchor image about twice the hold time of other images. Prefer `image_hold_weights: [1, 2, 1, 1, 1]`, which yields cuts around `[1.17, 3.50, 4.67, 5.83]`.
- If the tweet is not in Chinese, produce a Chinese-localized final card: preserve author, handle, date, visible engagement, and source URL in notes; translate/summarize the tweet body in Chinese; translate important chart labels or add a Chinese caption explaining the chart. The raw English screenshot can be stored as evidence, but it should not be the only audience-facing explanation.
- If the tweet is mainly Chinese, do not create a separate Chinese interpretation just to fill the template. Prefer the direct Chrome crop, with only minimal source framing, title, or bottom metadata when needed.
- Chrome screenshots may remain in English as trace evidence, but the final audience-facing crop must be Chinese-first. If the embedded tweet media, official page, chart, or product UI is English, add a Chinese overlay title/caption inside that image area using `source_media_cn_title` / `source_media_cn_subtitle` or an equivalent localized caption. A normal viewer should understand the source image without reading English.
- Do not use screenshots that show login walls, Cloudflare checks, cookie walls, `403`, `429`, "Something went wrong", blank pages, or unrelated search results.
- If the tweet screenshot itself is valid but the embedded media/link preview is blank or not rendered, do not ship the blank white box. Capture the linked official/source page in Chrome and fill that preview area via `render_tweet_proof_card.py` using `source_media_image`, `source_media_box`, and optional `source_media_crop_box`, while preserving the original tweet author, text, time, and engagement.
- If a clean tweet screenshot cannot be captured in Chrome, choose another tweet or another topic. Only use a non-Chrome fallback when the user explicitly accepts it or when the fallback is an official page screenshot that still verifies the event; record that exception in `来源记录.md`.
- Store the source tweet URL next to the Chrome screenshot path and derived proof-card path in the working notes or topic history so the screenshot can be traced.
- Before rendering the proof card, run the visual review gate against the proof-card config. This catches the specific failure mode where a full X/Twitter page screenshot gets embedded inside the card instead of the core post. The raw screenshot must either come from `capture_chrome_source.py --tweet-only` metadata or have an explicit `crop_box`.

```bash
python3 /Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版/scripts/review_visual_quality.py \
  --config configs/tweet-proof-card.json \
  --project-dir . \
  --report renders/tweet-proof-card-review.json \
  --strict
```

- Use `scripts/render_tweet_proof_card.py` when turning a reviewed raw tweet screenshot into the preferred Chinese proof card:

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
- Use one event-specific bottom-description set from the viewer's path. Use 4-6 pure content lines, defaulting to 6 for daily 推特版 videos. Do not present or output a labeled structure. The lines should read naturally as short Chinese sentences and must not show labels such as `发生了什么`, `关键事实`, `背后冲突`, `影响谁`, `结论`, `跟你有关`, or `信息差`.
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

Cover generation guardrail:

- `封面.jpg` is a separate publishing asset. It must be rendered from a dedicated cover config or a deliberate cover design asset.
- Do not use `ffmpeg -ss ... -frames:v 1`, `sips`, screenshot capture, or any other first-frame extraction as the default way to create `封面.jpg`.
- Do not reuse the video opening frame when it is a paper-card, tweet-card, or ordinary video frame. Even if it is 1080x1920, it is not a valid cover unless it was specifically designed with the cover rules.
- Before copying to the user-facing export folder, check the cover source: it should have a cover config, cover renderer output, or documented manual cover asset. If the only source is `视频.mp4`, regenerate the cover.
- The cover must visibly show the people/company-first hierarchy: recognizable person or strong company identity, classic logo/wordmark badge, same three-line title, and one bottom conclusion row.

## Paper Card Explainer Mode

Use this mode when the user approves or references the white-card examples: red `重磅` metadata, bold black/blue three-line headline, a real screenshot/photo in the center, and label-free cyan-highlighted explanatory copy below. The older purple ribbon version is legacy-only.

Title logic:

- Use a strong three-line hook instead of a neutral news title.
- Line 1-2: black, heavy, high-contrast headline that names the familiar protagonist, public conflict, and concrete event/change.
- Line 3: the sharp conclusion, information gap, or counterintuitive takeaway, usually in blue emphasis.
- The headline should answer why a normal viewer should stop and watch: "what changed", "why it matters", or "what most people missed".
- Keep titles honest and specific. Avoid vague wording such as "AI 又有大事" unless the next line immediately names the event.

Preview card layout:

- Canvas stays `1080x1920`.
- Put one rounded white textured paper card inside a dark phone-like background.
- Top area: bold black title, usually 2 lines.
- Show the latest verified news date on the card, preferably as a small top-right `最新：YYYY.MM.DD` marker. Do not rely only on a tiny date inside the embedded screenshot.
- Under the title: do not use a purple rounded ribbon in the current default. Use the blue third title line for the information-gap sentence.
- Middle area: one real topic-matched screenshot/photo/product image, with clean no-color-border handling by default. Prefer a source/report screenshot, official page, real person, product screenshot, or company/product image over an abstract placeholder.
- Spacing: keep the title, middle media area, and bottom description visually tight like the approved reference. Avoid large blank gaps above or below the media. As a practical default, keep only about half-to-one line of text height between the media and nearby text blocks after readability is protected.
- Media fill: fill the middle image area horizontally whenever safe. People/company/product photos can cover the full media area; screenshots, tweet cards, report pages, and product UI should use safe-fill/contain behavior that enlarges the asset as much as possible while preserving all important text and UI.
- Bottom area: 4-6 pure content sentences, defaulting to 6 for daily 推特版 videos, each line highlighted with cyan blocks. Do not show internal labels.
- Add only a small `AI 信息差快报` positioning label. Do not add carousel dots, footer labels, decorative divider lines, or empty title bands.

Paper-card copy logic:

1. Start with the event in plain language.
2. Explain what a normal viewer should understand.
3. Explain the mechanism or business change behind it.
4. Name the risk, controversy, limitation, or opportunity.
5. End with a natural short takeaway. Do not render `信息差：...` or other internal labels unless the user explicitly asks for visible labels.

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
- Text rows: reveal one row at a time. Default to 6 pure content lines with no visible labels or numbers; use 4-5 lines only when the story is very simple or the screen would become crowded. Do not expose any structure names such as `发生了什么`, `关键事实`, `背后冲突`, `影响谁`, or `信息差判断`.
- Audio: no voiceover by default. Use local BGM from the BGM pool, commonly `start=3`, `duration=7`, `volume=0.55`, with tiny fade-in/out.
- Cover: for 小红书/抖音, make the cover from real people/company assets rather than a pure text card. Use the approved full-bleed quick-report style by default: bright full-screen person/company visual, top-left `重磅` tag, top-right `AI 信息差快报` pill, white classic-logo badge near the title, the same three animated title lines as a large lower-third headline, and one bottom conclusion strip. The cover title should use clean heavy typography: white first line, flat accent-color second/third lines, white stroke/rim for readability, and no black thick outline or glow. Protect the face and full representative subject. The conclusion strip may use a small `01`-style badge, but do not add big standalone topic numbers. If there is no suitable product/event person, check the parent company or backing company for a more recognizable representative person or brand asset before using a product page screenshot. If no person is suitable, use the company's logo/product page/official visual and preserve the complete brand/product identity.
- Cover rendering: build a cover config and run `scripts/render_full_bleed_cover.py`. A video frame, paper-card frame, or tweet screenshot cannot substitute for the cover.
- Output: one final MP4 plus a contact sheet or preview frame. When publishing to social platforms, also output a cover image.
- Export destination: final 推特版 deliverables must be organized under `/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/`. Temporary render files can stay in the project folder during iteration, but the handoff-ready batch must be copied or rendered into this dedicated folder.
- Export naming: final user-facing deliverables must use Chinese folder and file names. The top-level batch folder should include date, run time, and `推特版` or `推特专用`; inside it, create one numbered topic folder per project. Each topic folder contains only `视频.mp4` and `封面.jpg`. Put the batch-level summary, five video/cover paths, five 抖音 titles, five video-bottom descriptions, and tags in one root `整体描述.md`. Keep source screenshots, configs, contact sheets, and detailed history in the working project or GitHub records. Contact sheets or `渲染总览.jpg` may be copied only when the user is reviewing visual quality.
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
导出-YYYY年MM月DD日-HH点MM分-推特版AI信息差快报/
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
- Keep iteration previews, contact sheets, configs, and detailed source notes in the working project while tuning. For the handoff-ready Xiaohongshu export folder, copy only the approved MP4 and cover into each topic folder, plus one root `整体描述.md` containing the publishing copy for all topics; include visual overview images only when the user asks to inspect them.
- GitHub/local source records should include the source tweet URL, tweet author, observed heat signal, screenshot filename, supporting source URLs, and why this topic is suitable for a 推特版 AI 信息差 video.
- The folder or file name must clearly say `推特版` or `推特专用`.

## GitHub Sync And History

Every successful invocation must be synced to GitHub.

Scheduling boundary:

- The recurring daily runner for this skill is the local Codex Automation `ai-9` named `推特版AI信息差视频-每日9点`, scheduled for 09:00 Asia/Shanghai.
- GitHub is the sync and history surface for the skill, configs, source notes, and duplicate-prevention records. It is not the default video-rendering runtime.
- Do not replace the local Codex Automation with GitHub Actions unless the user explicitly asks for a cloud-only version. This workflow depends on local BGM files, local export folders, possible logged-in X/Twitter browser state, and local media inspection.

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
    final-delivery/
      01-中文话题名/
        视频.mp4
        封面.jpg
        文案.md
      整体描述.md
      _记录/
        contact sheets
        渲染校验*.md
        素材与来源/
```

Sync rules:

- Before selecting topics, read the GitHub-synced `records/twitter-ai-info-video/topic-history.md` when present, plus local batch histories.
- After a successful run, append the selected topics to `topic-history.md`.
- Record enough fields to block duplicates later: date, topic title, company/product/person, source tweet URL, source tweet author, observed heat signal, supporting source URLs, information-gap angle, final export folder, and output filenames.
- Commit and push after each successful invocation. Do not report the run as fully complete until the GitHub sync succeeds or the sync failure is clearly reported.
- For daily runs, upload the final exported videos, covers, publishing copy, overall document, validation/contact-sheet records, configs, source notes, and final material-review package into `records/twitter-ai-info-video/YYYY-MM-DD/final-delivery/`. Do not upload local BGM original files, failed screenshots, browser caches, temporary render caches, or duplicated intermediate assets. If GitHub rejects the media upload, keep a local commit or clearly explain the blocked file size/path and the recovery step.

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
