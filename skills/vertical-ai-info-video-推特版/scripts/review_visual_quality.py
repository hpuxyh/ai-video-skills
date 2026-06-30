#!/usr/bin/env python3
import argparse
import json
import math
import statistics
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont, ImageStat


W, H = 1080, 1920
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
STRUCTURE_LABELS = [
    "发生了什么",
    "关键事实",
    "背后冲突",
    "影响谁",
    "信息差判断",
    "事件：",
    "关键：",
    "冲突：",
    "影响：",
    "结论：",
    "跟你有关：",
    "信息差：",
]
COVER_IMAGE_KEYS = ("background_image", "person_image", "cover_image")
COVER_ALLOWED_SOURCE_TYPES = {
    "event_person",
    "company_person",
    "representative_person",
    "founder",
    "ceo",
    "product_lead",
    "government_figure",
    "parent_company_identity",
    "company_identity",
    "brand_identity",
    "logo_identity",
    "product_identity",
    "product_visual",
    "official_product_visual",
}
COVER_SCREENSHOT_FALLBACK_TYPES = {
    "product_screenshot",
    "official_screenshot",
    "official_page_screenshot",
}
COVER_FORBIDDEN_SOURCE_TYPES = {
    "tweet",
    "tweet_screenshot",
    "core_tweet",
    "x_screenshot",
    "twitter_screenshot",
    "tweet_proof_card",
    "proof_card",
    "source_card",
    "paper_card",
    "video_frame",
    "first_frame",
    "webpage",
    "webpage_screenshot",
    "browser_screenshot",
    "search_result",
    "error_card",
}
COVER_PATH_FORBIDDEN_HINTS = (
    "tweet",
    "twitter",
    "x-screenshot",
    "proof-card",
    "source-card",
    "paper-card",
    "first-frame",
    "video-frame",
    "screenshot",
    "截图",
    "来源截图",
    "核心来源",
)


def resolve(project_dir, value):
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_dir / path


def resolve_existing(project_dir, value):
    path = resolve(project_dir, value)
    if path.exists():
        return path
    name = Path(value).name
    topic = Path(value).parent.name
    candidates = list(project_dir.rglob(name))
    if topic:
        topic_matches = [candidate for candidate in candidates if topic in str(candidate)]
        if topic_matches:
            return topic_matches[0]
    if candidates:
        return candidates[0]
    return path


def font(size):
    return ImageFont.truetype(FONT_BOLD, int(size))


def text_width(draw, text, size):
    return draw.textlength(str(text), font=font(size))


def corner_background(img):
    src = img.convert("RGB")
    sample = max(6, min(src.width, src.height) // 60)
    regions = [
        src.crop((0, 0, sample, sample)),
        src.crop((src.width - sample, 0, src.width, sample)),
        src.crop((0, src.height - sample, sample, src.height)),
        src.crop((src.width - sample, src.height - sample, src.width, src.height)),
    ]
    values = []
    for region in regions:
        values.extend(region.getdata())
    return tuple(int(statistics.median(channel)) for channel in zip(*values))


def foreground_bbox(img):
    src = img.convert("RGB")
    bg = Image.new("RGB", src.size, corner_background(src))
    diff = ImageChops.difference(src, bg).convert("L")
    mask = diff.point(lambda px: 255 if px > 34 else 0)
    return mask.getbbox()


def edge_variance(img):
    gray = img.convert("L")
    scale = min(1.0, 480 / max(gray.width, gray.height))
    if scale < 1:
        gray = gray.resize((max(1, int(gray.width * scale)), max(1, int(gray.height * scale))), Image.Resampling.LANCZOS)
    edges = gray.filter(ImageFilter.FIND_EDGES)
    return ImageStat.Stat(edges).var[0]


def inspect_image(path):
    with Image.open(path) as img:
        width, height = img.size
        thumb = img.convert("RGB").resize((160, max(1, int(160 * height / width))), Image.Resampling.LANCZOS)
        stat = ImageStat.Stat(thumb)
        mean = sum(stat.mean[:3]) / 3
        extrema = thumb.convert("L").getextrema()
        bbox = foreground_bbox(thumb)
        sharpness = edge_variance(img)

    if bbox:
        left = bbox[0] / thumb.width
        top = bbox[1] / thumb.height
        right = (thumb.width - bbox[2]) / thumb.width
        bottom = (thumb.height - bbox[3]) / thumb.height
        content_ratio = ((bbox[2] - bbox[0]) * (bbox[3] - bbox[1])) / (thumb.width * thumb.height)
    else:
        left = top = right = bottom = 1.0
        content_ratio = 0.0

    return {
        "width": width,
        "height": height,
        "mean_luma": round(mean, 1),
        "luma_range": int(extrema[1] - extrema[0]),
        "sharpness": round(sharpness, 1),
        "content_ratio": round(content_ratio, 3),
        "margins": {
            "left": round(left, 3),
            "top": round(top, 3),
            "right": round(right, 3),
            "bottom": round(bottom, 3),
        },
    }


def normalize_role(value):
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def is_cover_config(cfg):
    return any(cfg.get(key) for key in COVER_IMAGE_KEYS)


def cover_background_ref(cfg):
    for key in COVER_IMAGE_KEYS:
        if cfg.get(key):
            return key, cfg.get(key)
    return None, None


def cover_source_value(cfg):
    for key in ("cover_source", "cover_source_asset", "cover_source_url", "source_url", "source_note"):
        if cfg.get(key):
            return cfg.get(key)
    return None


def cover_fallback_reason(cfg):
    for key in ("cover_fallback_reason", "fallback_reason", "no_person_reason", "selection_reason"):
        if cfg.get(key):
            return str(cfg.get(key)).strip()
    return ""


def review_cover_config(cfg, project_dir):
    key, bg_ref = cover_background_ref(cfg)
    if not bg_ref:
        return {}, [], []

    errors = []
    warnings = []
    source_type = normalize_role(
        cfg.get("cover_source_type")
        or cfg.get("background_role")
        or cfg.get("source_type")
        or cfg.get("asset_role")
    )
    source_value = cover_source_value(cfg)
    result = {
        "background_key": key,
        "background_image": bg_ref,
        "cover_source_type": source_type or None,
        "cover_source": source_value,
        "logo_image": cfg.get("logo_image"),
        "badge_text": cfg.get("badge_text") or cfg.get("company") or cfg.get("source"),
    }

    bg_path = resolve_existing(project_dir, bg_ref)
    result["exists"] = bg_path.exists()
    if not bg_path.exists():
        errors.append(f"cover background missing: {bg_ref}")
    else:
        metrics = inspect_image(bg_path)
        result.update(metrics)
        if max(metrics["width"], metrics["height"]) < 1200 or min(metrics["width"], metrics["height"]) < 700:
            warnings.append(f"cover background is low-resolution for 9:16 full-bleed use: {metrics['width']}x{metrics['height']} {bg_ref}")
        if metrics["sharpness"] < 38:
            warnings.append(f"cover background may be blurry or over-smoothed: sharpness={metrics['sharpness']} {bg_ref}")
        if metrics["luma_range"] < 38 or metrics["content_ratio"] < 0.08:
            errors.append(f"cover background looks blank/low-information: {bg_ref}")

    if not source_type:
        errors.append("cover config must declare cover_source_type/background_role before rendering")
    elif source_type in COVER_FORBIDDEN_SOURCE_TYPES:
        errors.append(f"cover background source type is forbidden for covers: {source_type}")
    elif source_type in COVER_SCREENSHOT_FALLBACK_TYPES:
        if not cover_fallback_reason(cfg):
            errors.append(
                "cover uses a screenshot fallback; add cover_fallback_reason/no_person_reason "
                "explaining why no person/company identity asset is available"
            )
    elif source_type not in COVER_ALLOWED_SOURCE_TYPES:
        warnings.append(f"cover_source_type is not in the approved cover taxonomy: {source_type}")

    bg_hint = str(bg_ref).lower()
    if source_type not in COVER_SCREENSHOT_FALLBACK_TYPES and any(hint in bg_hint for hint in COVER_PATH_FORBIDDEN_HINTS):
        errors.append(f"cover background path looks like a tweet/source/video screenshot, not a cover asset: {bg_ref}")

    if not source_value:
        errors.append("cover config must record cover_source/cover_source_asset/cover_source_url for provenance")

    if not (cfg.get("logo_image") or cfg.get("badge_text") or cfg.get("company") or cfg.get("source")):
        warnings.append("cover has no logo_image or badge_text; add a company/product recognition anchor")

    lines = title_lines(cfg)
    if len(lines) != 3:
        warnings.append(f"cover headline should reuse exactly the three video title lines, got {len(lines)}")
    if not (cfg.get("bottom_text") or cfg.get("conclusion")):
        errors.append("cover needs one bottom_text/conclusion row")

    return result, errors, warnings


def review_images(cfg, project_dir):
    errors = []
    warnings = []
    items = []
    images = cfg.get("images") or []
    qualities = cfg.get("image_quality") or []
    roles = cfg.get("image_roles") or []

    for index, image_ref in enumerate(images):
        path = resolve_existing(project_dir, image_ref)
        role = roles[index] if isinstance(roles, list) and index < len(roles) else ""
        quality = qualities[index] if isinstance(qualities, list) and index < len(qualities) else ""
        item = {"index": index + 1, "path": image_ref, "role": role, "quality": quality}
        if not path.exists():
            errors.append(f"image {index + 1} missing: {image_ref}")
            item["exists"] = False
            items.append(item)
            continue

        metrics = inspect_image(path)
        item.update({"exists": True, **metrics})
        items.append(item)

        if metrics["width"] < 900 or metrics["height"] < 560:
            errors.append(f"image {index + 1} resolution is too low: {metrics['width']}x{metrics['height']} {image_ref}")
        elif metrics["width"] < 1200 or metrics["height"] < 720:
            warnings.append(f"image {index + 1} is usable but not very high-res: {metrics['width']}x{metrics['height']} {image_ref}")

        if metrics["sharpness"] < 45:
            warnings.append(f"image {index + 1} may be blurry or over-smoothed: sharpness={metrics['sharpness']} {image_ref}")
        if metrics["luma_range"] < 42 or metrics["content_ratio"] < 0.08:
            errors.append(f"image {index + 1} looks blank/low-information: {image_ref}")

        margins = metrics["margins"]
        max_margin = max(margins.values())
        if max_margin > 0.42:
            warnings.append(f"image {index + 1} has too much empty margin; recrop tighter: margins={margins} {image_ref}")
        if index == 1 or role in {"core-evidence", "tweet"} or quality in {"source-card", "tweet"}:
            if margins["left"] > 0.25 or margins["right"] > 0.25:
                warnings.append(f"core tweet image {index + 1} may include sidebars/blank space; crop to the tweet card: {image_ref}")

    if images and len(images) != 5:
        warnings.append(f"expected 5 carousel images for the 7-second format, got {len(images)}")
    return items, errors, warnings


def normalize_media_box(raw):
    if not raw:
        return (52, 622, 1028, 1184)
    values = [int(v) for v in raw]
    if len(values) != 4:
        return (52, 622, 1028, 1184)
    return tuple(values)


def title_lines(cfg):
    title = cfg.get("title") or []
    if isinstance(title, str):
        title = [title]
    if title and isinstance(title[0], dict):
        return [str(line.get("text", "")).strip() for line in title if str(line.get("text", "")).strip()]
    lines = [str(line).strip() for line in title if str(line).strip()]
    line3 = str(cfg.get("title_line3", "")).strip()
    if line3:
        lines.append(line3)
    return lines


def review_cover_text_layout(cfg):
    errors = []
    warnings = []
    draw = ImageDraw.Draw(Image.new("RGB", (W, H)))
    lines = title_lines(cfg)
    title_y = int(cfg.get("title_y", 1075))
    line_gap = int(cfg.get("title_line_gap", 18))
    sizes = cfg.get("title_sizes", [92, 98, 90])
    max_width = int(cfg.get("title_max_width", 950))
    y = title_y
    fitted = []
    for index, line in enumerate(lines[:3]):
        start_size = int(sizes[min(index, len(sizes) - 1)]) if isinstance(sizes, list) and sizes else 92
        size = start_size
        while size > 42 and text_width(draw, line, size) > max_width:
            size -= 2
        fitted.append({"text": line, "size": size, "width": round(text_width(draw, line, size), 1)})
        y += size + line_gap

    bottom_y = int(cfg.get("bottom_y", 1645))
    bottom_y2 = int(cfg.get("bottom_y2", 1812))
    if fitted and y > bottom_y - 24:
        errors.append(f"cover headline overlaps or crowds bottom conclusion: title_bottom={y}, bottom_y={bottom_y}")
    if bottom_y2 > 1850:
        warnings.append(f"cover bottom strip is close to platform safe area: bottom_y2={bottom_y2}")

    bottom_text = cfg.get("bottom_text") or cfg.get("conclusion") or ""
    if bottom_text:
        badge_extra = 98 if cfg.get("index_badge") else 0
        max_bottom_width = int(cfg.get("bottom_x2", W - 58)) - int(cfg.get("bottom_x", 58)) - 66 - badge_extra
        if text_width(draw, bottom_text, int(cfg.get("bottom_font_size", 38))) > max_bottom_width * 1.9:
            warnings.append(f"cover bottom_text is too long for a clean two-line strip: {bottom_text}")

    return {
        "cover_only": True,
        "title_lines": lines,
        "fitted_title": fitted,
        "title_bottom": y if fitted else None,
        "bottom_box": [int(cfg.get("bottom_x", 58)), bottom_y, int(cfg.get("bottom_x2", W - 58)), bottom_y2],
    }, errors, warnings


def review_text_layout(cfg):
    errors = []
    warnings = []
    draw = ImageDraw.Draw(Image.new("RGB", (W, H)))
    is_proof_card_only = bool(cfg.get("raw_screenshot")) and not (cfg.get("images") or cfg.get("title") or cfg.get("body_rows"))
    if is_proof_card_only:
        return {"proof_card_only": True}, [], []
    if is_cover_config(cfg) and not cfg.get("images"):
        return review_cover_text_layout(cfg)
    media = normalize_media_box(cfg.get("media_box") or cfg.get("photo_box"))
    media_top = media[1]
    media_bottom = media[3]

    lines = title_lines(cfg)
    title_size = int(cfg.get("title_base_size", cfg.get("title_size", 72)))
    min_title_size = int(cfg.get("title_min_size", 50))
    title_width = int(cfg.get("title_max_width", 980))
    while title_size > min_title_size and any(text_width(draw, line, title_size) > title_width for line in lines):
        title_size -= 2
    title_y = int(cfg.get("title_y", 168))
    line_gap = int(cfg.get("title_line_gap", 30))
    title_bottom = title_y + len(lines) * title_size + max(0, len(lines) - 1) * line_gap
    if title_bottom > media_top - 20:
        errors.append(f"title block overlaps or crowds media area: title_bottom={title_bottom}, media_top={media_top}")

    rows = cfg.get("body_rows") or cfg.get("bottom_description") or cfg.get("info_rows") or []
    if isinstance(rows, str):
        rows = [line.strip() for line in rows.splitlines() if line.strip()]
    clean_rows = []
    for row in rows:
        text = row.get("text", "") if isinstance(row, dict) else row
        text = str(text).strip()
        if text:
            clean_rows.append(text)
    max_rows = int(cfg.get("body_max_rows", cfg.get("max_lines", 6)))
    if not 4 <= len(clean_rows[:max_rows]) <= 6:
        warnings.append(f"bottom description should usually be 4-6 visible lines, got {len(clean_rows[:max_rows])}")
    for row in clean_rows:
        for label in STRUCTURE_LABELS:
            if label in row:
                errors.append(f"bottom description exposes structure label '{label}': {row}")

    body_y = int(cfg.get("body_y", cfg.get("description_y", 1308)))
    row_h = int(cfg.get("body_row_h", 58))
    gap = int(cfg.get("body_row_gap", 13))
    row_bottom = body_y + len(clean_rows[:max_rows]) * row_h + max(0, len(clean_rows[:max_rows]) - 1) * gap
    if clean_rows and body_y < media_bottom + 18:
        errors.append(f"bottom description overlaps or crowds media area: body_y={body_y}, media_bottom={media_bottom}")
    if row_bottom > int(cfg.get("safe_bottom", 1810)):
        errors.append(f"bottom description runs into lower safe area: row_bottom={row_bottom}")

    row_w = int(cfg.get("body_row_w", 976))
    text_limit = row_w - 64
    for row in clean_rows[:max_rows]:
        if text_width(draw, row, 32) > text_limit and text_width(draw, row, 26) > text_limit:
            warnings.append(f"bottom row is too long and may shrink/crowd: {row}")

    return {
        "title_lines": lines,
        "effective_title_size": title_size,
        "title_bottom": title_bottom,
        "media_box": media,
        "body_line_count": len(clean_rows[:max_rows]),
        "body_bottom": row_bottom if clean_rows else None,
    }, errors, warnings


def load_capture_metadata(raw_path):
    candidates = [
        raw_path.with_suffix(raw_path.suffix + ".json"),
        raw_path.with_suffix(".json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            try:
                return json.loads(candidate.read_text(encoding="utf-8")), str(candidate)
            except Exception:
                return None, str(candidate)
    return None, None


def review_source_capture(cfg, project_dir):
    raw_ref = cfg.get("raw_screenshot")
    if not raw_ref:
        return {}, [], []
    errors = []
    warnings = []
    raw_path = resolve_existing(project_dir, raw_ref)
    result = {"raw_screenshot": raw_ref, "exists": raw_path.exists()}
    if not raw_path.exists():
        errors.append(f"raw screenshot missing: {raw_ref}")
        return result, errors, warnings

    metrics = inspect_image(raw_path)
    result.update(metrics)
    metadata, metadata_path = load_capture_metadata(raw_path)
    result["metadata_path"] = metadata_path
    result["element_selector"] = metadata.get("element_selector") if isinstance(metadata, dict) else None
    has_manual_crop = bool(cfg.get("crop_box"))
    has_tweet_only = bool(result["element_selector"] and 'article[data-testid="tweet"]' in result["element_selector"])
    aspect = metrics["width"] / max(1, metrics["height"])

    if not has_manual_crop and not has_tweet_only:
        errors.append(
            "tweet proof card raw screenshot is not confirmed as a core tweet crop; "
            "recapture with --tweet-only or set an explicit crop_box"
        )
    if aspect > 1.45 and not has_manual_crop and not has_tweet_only:
        warnings.append(f"raw screenshot is wide like a full browser page, not a tweet card: aspect={aspect:.2f}")
    if metrics["margins"]["left"] > 0.20 or metrics["margins"]["right"] > 0.20:
        warnings.append(f"raw screenshot has large side margins; verify it is not carrying X navigation/sidebar: {metrics['margins']}")
    return result, errors, warnings


def make_contact_sheet(items, project_dir, output):
    thumbs = []
    for item in items:
        if not item.get("exists"):
            continue
        with Image.open(resolve_existing(project_dir, item["path"])).convert("RGB") as img:
            img.thumbnail((320, 200), Image.Resampling.LANCZOS)
            tile = Image.new("RGB", (340, 240), (246, 248, 250))
            tile.paste(img, ((340 - img.width) // 2, 12))
            d = ImageDraw.Draw(tile)
            d.text((12, 216), f"{item['index']}. {Path(item['path']).name[:36]}", fill=(20, 24, 32))
            thumbs.append(tile)
    if not thumbs:
        return
    cols = 3
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 340, rows * 240), (255, 255, 255))
    for i, tile in enumerate(thumbs):
        sheet.paste(tile, ((i % cols) * 340, (i // cols) * 240))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main():
    parser = argparse.ArgumentParser(description="Review AI info video images and text layout before rendering.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--report", help="Optional JSON report path.")
    parser.add_argument("--contact-sheet", help="Optional image contact sheet path.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors.")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    cfg_path = resolve(project_dir, args.config)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    cover, cover_errors, cover_warnings = review_cover_config(cfg, project_dir)
    source_capture, source_errors, source_warnings = review_source_capture(cfg, project_dir)
    image_items, image_errors, image_warnings = review_images(cfg, project_dir)
    layout, layout_errors, layout_warnings = review_text_layout(cfg)
    errors = cover_errors + source_errors + image_errors + layout_errors
    warnings = cover_warnings + source_warnings + image_warnings + layout_warnings
    report = {
        "config": str(cfg_path),
        "status": "fail" if errors else ("warn" if warnings else "pass"),
        "errors": errors,
        "warnings": warnings,
        "cover": cover,
        "source_capture": source_capture,
        "images": image_items,
        "layout": layout,
    }

    if args.report:
        report_path = resolve(project_dir, args.report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    if args.contact_sheet:
        sheet_items = image_items[:]
        if cover.get("exists") and cover.get("background_image"):
            sheet_items.insert(0, {"index": "cover-bg", "path": cover["background_image"], "exists": True})
        make_contact_sheet(sheet_items, project_dir, resolve(project_dir, args.contact_sheet))

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if errors or (args.strict and warnings):
        sys.exit(1)


if __name__ == "__main__":
    main()
