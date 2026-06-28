#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


FONT_REG = "/Library/Fonts/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def resolve_path(project_dir, value):
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_dir / path


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(size))


def text_len(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def tokenize(text):
    pieces = re.findall(r"[A-Za-z0-9_.:/@#+-]+|\s+|[\u4e00-\u9fff]|[^\s]", text)
    return pieces or list(text)


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


def wrap_lines(draw, lines, fnt, max_width):
    wrapped = []
    for line in lines:
        wrapped.extend(wrap_text(draw, line, fnt, max_width))
    return wrapped


def fit_contain(img, box):
    box_w, box_h = box
    scale = min(box_w / img.width, box_h / img.height)
    new_size = (int(img.width * scale + 0.5), int(img.height * scale + 0.5))
    return img.resize(new_size, Image.Resampling.LANCZOS)


def rounded_paste(canvas, img, xy, radius=24):
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, img.width, img.height), radius=radius, fill=255)
    canvas.paste(img.convert("RGBA"), xy, mask)


def draw_wrapped_text(draw, xy, text, fnt, fill, max_width, line_gap=6):
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def render_card(cfg, project_dir, output):
    width = int(cfg.get("width", 1600))
    height = int(cfg.get("height", 1000))
    canvas = Image.new("RGBA", (width, height), (249, 251, 253, 255))
    draw = ImageDraw.Draw(canvas, "RGBA")

    margin = 50
    draw.rounded_rectangle(
        (margin, 48, width - margin, height - 48),
        radius=30,
        fill=(255, 255, 255, 255),
        outline=(206, 216, 228, 255),
        width=3,
    )

    raw_path = resolve_path(project_dir, cfg["raw_screenshot"])
    raw = Image.open(raw_path).convert("RGB")
    crop_box = cfg.get("crop_box")
    if crop_box:
        raw = raw.crop(tuple(int(v) for v in crop_box))

    left_box = cfg.get("left_box", [120, 82, 760, 682])
    lx, ly, lw, lh = [int(v) for v in left_box]
    tweet = fit_contain(raw, (lw, lh))
    tx = lx + (lw - tweet.width) // 2
    ty = ly + (lh - tweet.height) // 2
    draw.rounded_rectangle(
        (tx - 8, ty - 8, tx + tweet.width + 8, ty + tweet.height + 8),
        radius=26,
        fill=(255, 255, 255, 255),
        outline=(226, 232, 240, 255),
        width=2,
    )
    rounded_paste(canvas, tweet, (tx, ty), radius=22)

    right_x = int(cfg.get("right_x", 980))
    right_w = int(cfg.get("right_w", 520))
    y = int(cfg.get("right_y", 102))

    label = cfg.get("label", "中文释义")
    label_font = font(int(cfg.get("label_font_size", 34)), True)
    label_pad_x = 22
    label_h = int(cfg.get("label_height", 62))
    label_w = int(text_len(draw, label, label_font) + label_pad_x * 2)
    draw.rounded_rectangle((right_x, y, right_x + label_w, y + label_h), radius=14, fill=(139, 78, 229, 255))
    draw.text((right_x + label_pad_x, y + 10), label, font=label_font, fill=(255, 255, 255, 255))
    y += label_h + 14

    summary_lines = cfg.get("summary_lines", [])
    summary_font_size = int(cfg.get("summary_font_size", 39))
    min_summary_size = int(cfg.get("min_summary_font_size", 34))
    highlight_pad_x = int(cfg.get("highlight_pad_x", 12))
    highlight_pad_y = int(cfg.get("highlight_pad_y", 7))
    highlight_gap = int(cfg.get("highlight_gap", 10))
    max_summary_lines = int(cfg.get("max_summary_lines", 6))
    highlight_full_width = bool(cfg.get("highlight_full_width", False))

    while True:
        summary_font = font(summary_font_size, True)
        wrapped = wrap_lines(draw, summary_lines, summary_font, right_w - highlight_pad_x * 2)
        line_h = summary_font_size + highlight_pad_y * 2
        total_h = len(wrapped) * line_h + max(0, len(wrapped) - 1) * highlight_gap
        if (len(wrapped) <= max_summary_lines and total_h <= 360) or summary_font_size <= min_summary_size:
            break
        summary_font_size -= 2

    summary_font = font(summary_font_size, True)
    wrapped = wrap_lines(draw, summary_lines, summary_font, right_w - highlight_pad_x * 2)
    line_h = summary_font_size + highlight_pad_y * 2
    for line in wrapped[:max_summary_lines]:
        line_w = int(text_len(draw, line, summary_font))
        rect_w = right_w if highlight_full_width else min(right_w, line_w + highlight_pad_x * 2)
        draw.rounded_rectangle((right_x, y, right_x + rect_w, y + line_h), radius=8, fill=(32, 213, 222, 255))
        draw.text((right_x + highlight_pad_x, y + highlight_pad_y - 1), line, font=summary_font, fill=(10, 18, 24, 255))
        y += line_h + highlight_gap

    y += 30
    link_title = cfg.get("link_title", "核心链接")
    draw.text((right_x, y), link_title, font=font(31, True), fill=(31, 37, 47, 255))
    y += 48
    source_url = cfg.get("source_url", "")
    draw_wrapped_text(draw, (right_x, y), source_url, font(24), (76, 86, 101, 255), right_w, line_gap=3)

    source_box = cfg.get("source_box", [86, 810, 850, 88])
    sx, sy, sw, sh = [int(v) for v in source_box]
    draw.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=16, fill=(244, 248, 252, 255), outline=(217, 226, 237, 255), width=2)
    draw.text((sx + 34, sy + 16), cfg.get("source_title", "来源"), font=font(33, True), fill=(29, 35, 44, 255))
    source_meta = cfg.get("source_meta", "")
    if source_meta:
        draw.text((sx + 34, sy + 53), source_meta, font=font(24), fill=(94, 104, 118, 255))

    note = cfg.get("hold_note", "")
    if note:
        nx = int(cfg.get("note_x", 1000))
        ny = int(cfg.get("note_y", 810))
        nw = int(cfg.get("note_w", 515))
        nh = int(cfg.get("note_h", 78))
        note_font = font(int(cfg.get("note_font_size", 29)), True)
        draw.rounded_rectangle((nx, ny, nx + nw, ny + nh), radius=14, fill=(139, 78, 229, 255))
        wrapped_note = wrap_text(draw, note, note_font, nw - 46)
        note_y = ny + (nh - len(wrapped_note) * (note_font.size + 3)) // 2 - 1
        for line in wrapped_note:
            draw.text((nx + 25, note_y), line, font=note_font, fill=(255, 255, 255, 255))
            note_y += note_font.size + 3

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=int(cfg.get("quality", 95)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    config_path = resolve_path(project_dir, args.config)
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    output_value = args.output or cfg.get("output")
    if not output_value:
        raise SystemExit("Missing --output or config.output")
    output = resolve_path(project_dir, output_value)
    render_card(cfg, project_dir, output)
    print(output)


if __name__ == "__main__":
    main()
