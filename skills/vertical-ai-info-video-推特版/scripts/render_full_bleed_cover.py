#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


W, H = 1080, 1920
FONT_REG = "/Library/Fonts/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def resolve_path(project_dir, value):
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_dir / path


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(size))


def rgb(value, fallback):
    if not value:
        return fallback
    return tuple(int(x) for x in value[:3])


def text_len(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def tokenize(text):
    return re.findall(r"[A-Za-z0-9_.:/@#+-]+|\s+|[\u4e00-\u9fff]|[^\s]", text) or list(text)


def fit_cover(img, size, focus=None):
    target_w, target_h = size
    img = img.convert("RGB")
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)
    fx, fy = focus or (0.5, 0.42)
    left = int((resized.width - target_w) * max(0, min(1, fx)))
    top = int((resized.height - target_h) * max(0, min(1, fy)))
    left = max(0, min(left, resized.width - target_w))
    top = max(0, min(top, resized.height - target_h))
    return resized.crop((left, top, left + target_w, top + target_h))


def fit_contain(img, size):
    target_w, target_h = size
    img = img.convert("RGBA")
    scale = min(target_w / img.width, target_h / img.height)
    return img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)


def wrap_text(draw, text, fnt, max_width):
    lines = []
    current = ""
    for piece in tokenize(text):
        probe = current + piece
        if current and text_len(draw, probe, fnt) > max_width:
            lines.append(current.rstrip())
            current = piece.lstrip()
        else:
            current = probe
    if current:
        lines.append(current.strip())
    return lines


def title_texts(cfg):
    raw = cfg.get("title") or cfg.get("title_lines") or []
    lines = []
    for item in raw:
        if isinstance(item, dict):
            lines.append(str(item.get("text", "")).strip())
        else:
            lines.append(str(item).strip())
    if cfg.get("title_line3") and len(lines) < 3:
        lines.append(str(cfg["title_line3"]).strip())
    return [line for line in lines if line][:3]


def title_colors(cfg):
    raw = cfg.get("title") or []
    defaults = [
        (255, 255, 255),
        tuple(cfg.get("line2_color", [255, 255, 255])),
        tuple(cfg.get("line3_color", [255, 145, 118])),
    ]
    colors = []
    for idx in range(3):
        if idx < len(raw) and isinstance(raw[idx], dict) and raw[idx].get("color"):
            colors.append(rgb(raw[idx].get("color"), defaults[idx]))
        else:
            colors.append(defaults[idx])
    return colors


def rounded_panel(draw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def draw_top_meta(draw, cfg):
    tag = cfg.get("tag", "重磅")
    brand = cfg.get("brand", "AI 信息差快报")
    tag_font = font(int(cfg.get("tag_font_size", 30)), True)
    brand_font = font(int(cfg.get("brand_font_size", 24)), True)

    rounded_panel(draw, (58, 54, 190, 104), 13, (255, 92, 92, 245))
    draw.text((84, 64), tag, font=tag_font, fill=(15, 18, 26, 255))

    bw = int(text_len(draw, brand, brand_font)) + 44
    x0 = W - 58 - bw
    rounded_panel(draw, (x0, 54, W - 58, 104), 14, (8, 20, 36, 210), (120, 210, 255, 120), 1)
    draw.text((x0 + 22, 66), brand, font=brand_font, fill=(232, 250, 255, 255))


def draw_logo_badge(canvas, cfg, project_dir):
    logo_path = cfg.get("logo_image")
    badge_text = cfg.get("badge_text") or cfg.get("company") or cfg.get("source")
    if not logo_path and not badge_text:
        return

    badge_w = int(cfg.get("logo_badge_w", 360))
    badge_h = int(cfg.get("logo_badge_h", 104))
    x = int(cfg.get("logo_badge_x", W - badge_w - 68))
    y = int(cfg.get("logo_badge_y", 930))
    layer = Image.new("RGBA", (badge_w, badge_h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    rounded_panel(d, (0, 0, badge_w, badge_h), 26, (255, 255, 255, 238), (255, 255, 255, 150), 2)

    if logo_path:
        logo = Image.open(resolve_path(project_dir, logo_path)).convert("RGBA")
        fitted = fit_contain(logo, (badge_w - 50, badge_h - 36))
        layer.alpha_composite(fitted, ((badge_w - fitted.width) // 2, (badge_h - fitted.height) // 2))
    else:
        size = int(cfg.get("badge_font_size", 38))
        while size > 20:
            fnt = font(size, True)
            if text_len(d, badge_text, fnt) <= badge_w - 44:
                break
            size -= 2
        tw = int(text_len(d, badge_text, fnt))
        d.text(((badge_w - tw) // 2, (badge_h - size) // 2 - 2), badge_text, font=fnt, fill=(12, 18, 30, 255))

    canvas.alpha_composite(layer, (x, y))


def fit_font_size(draw, text, max_width, start_size, min_size=42):
    size = start_size
    while size > min_size:
        fnt = font(size, True)
        if text_len(draw, text, fnt) <= max_width:
            return size, fnt
        size -= 2
    return size, font(size, True)


def draw_title_block(draw, cfg):
    lines = title_texts(cfg)
    if not lines:
        raise SystemExit("Cover config requires title lines.")
    colors = title_colors(cfg)
    max_width = int(cfg.get("title_max_width", 950))
    y = int(cfg.get("title_y", 1075))
    line_gap = int(cfg.get("title_line_gap", 18))
    default_sizes = cfg.get("title_sizes", [92, 98, 90])

    for idx, line in enumerate(lines):
        start_size = int(default_sizes[min(idx, len(default_sizes) - 1)])
        size, fnt = fit_font_size(draw, line, max_width, start_size)
        tw = int(text_len(draw, line, fnt))
        x = (W - tw) // 2
        fill = colors[idx]
        stroke_w = int(cfg.get("title_stroke_width", 3))
        stroke_fill = tuple(cfg.get("title_stroke_fill", [255, 255, 255, 230]))
        if idx == 0 and fill == (255, 255, 255):
            stroke_fill = tuple(cfg.get("title_line1_stroke_fill", [255, 255, 255, 180]))
            stroke_w = int(cfg.get("title_line1_stroke_width", 1))
        draw.text((x, y), line, font=fnt, fill=(*fill, 255), stroke_width=stroke_w, stroke_fill=stroke_fill)
        y += size + line_gap


def draw_bottom_conclusion(draw, cfg):
    text = cfg.get("bottom_text") or cfg.get("conclusion")
    if not text:
        rows = cfg.get("bottom_description") or cfg.get("info_rows") or []
        if rows:
            last = rows[-1]
            text = last.get("text") if isinstance(last, dict) else str(last)
    if not text:
        return

    x0 = int(cfg.get("bottom_x", 58))
    y0 = int(cfg.get("bottom_y", 1645))
    x1 = int(cfg.get("bottom_x2", W - 58))
    y1 = int(cfg.get("bottom_y2", 1812))
    rounded_panel(draw, (x0, y0, x1, y1), 30, (8, 14, 26, 218), (255, 255, 255, 36), 1)

    badge = cfg.get("index_badge")
    text_x = x0 + 34
    if badge:
        badge_font = font(30, True)
        rounded_panel(draw, (x0 + 24, y0 + 36, x0 + 98, y0 + 104), 19, (235, 242, 248, 238))
        draw.text((x0 + 43, y0 + 52), str(badge), font=badge_font, fill=(14, 22, 34, 255))
        text_x = x0 + 122

    max_width = x1 - text_x - 32
    size = int(cfg.get("bottom_font_size", 38))
    while size > 24:
        fnt = font(size, True)
        wrapped = wrap_text(draw, text, fnt, max_width)
        if len(wrapped) <= 2:
            break
        size -= 2
    fnt = font(size, True)
    wrapped = wrap_text(draw, text, fnt, max_width)[:2]
    total_h = len(wrapped) * size + (len(wrapped) - 1) * 8
    ty = y0 + (y1 - y0 - total_h) // 2 - 2
    for line in wrapped:
        draw.text((text_x, ty), line, font=fnt, fill=(255, 255, 255, 255))
        ty += size + 8


def render_cover(cfg, project_dir, output):
    bg_key = cfg.get("background_image") or cfg.get("person_image") or cfg.get("cover_image")
    if not bg_key:
        raise SystemExit("Cover config requires background_image/person_image/cover_image.")

    bg = Image.open(resolve_path(project_dir, bg_key)).convert("RGB")
    focus = cfg.get("focus")
    focus = tuple(float(x) for x in focus[:2]) if focus else None
    cover = fit_cover(bg, (W, H), focus=focus)
    cover = ImageEnhance.Brightness(cover).enhance(float(cfg.get("background_brightness", 0.88)))
    cover = ImageEnhance.Contrast(cover).enhance(float(cfg.get("background_contrast", 1.08)))
    canvas = cover.convert("RGBA")

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay, "RGBA")
    od.rectangle((0, 0, W, 270), fill=(5, 12, 24, 104))
    for i in range(820):
        alpha = int(8 + (i / 819) ** 1.7 * 190)
        od.line((0, H - 820 + i, W, H - 820 + i), fill=(5, 8, 18, alpha))
    canvas.alpha_composite(overlay)
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw_top_meta(draw, cfg)
    draw_logo_badge(canvas, cfg, project_dir)
    draw_title_block(draw, cfg)
    draw_bottom_conclusion(draw, cfg)

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=94)
    return output


def main():
    parser = argparse.ArgumentParser(description="Render a full-bleed people/company-first cover for 推特版 AI videos.")
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).resolve()
    cfg_path = resolve_path(project_dir, args.config)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    output = Path(args.output) if args.output else resolve_path(project_dir, cfg.get("output", "renders/cover.jpg"))
    if not output.is_absolute():
        output = project_dir / output
    print(render_cover(cfg, project_dir, output))


if __name__ == "__main__":
    main()
