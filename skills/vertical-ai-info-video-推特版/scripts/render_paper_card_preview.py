#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


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


def text_len(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def wrap_text(draw, text, fnt, max_width):
    lines = []
    current = ""
    for ch in text:
        trial = current + ch
        if text_len(draw, trial, fnt) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, lines, y, fnt, fill, max_width, canvas_width=W, line_gap=12):
    wrapped = []
    for raw in lines:
        wrapped.extend(wrap_text(draw, raw, fnt, max_width))
    for line in wrapped:
        box = draw.textbbox((0, 0), line, font=fnt)
        h = box[3] - box[1]
        x = (canvas_width - text_len(draw, line, fnt)) / 2
        draw.text((x, y), line, font=fnt, fill=fill)
        y += h + line_gap
    return y


def fit_contain(img, size, bg=(255, 255, 255)):
    img = img.convert("RGB")
    target_w, target_h = size
    scale = min(target_w / img.width, target_h / img.height)
    new_w = int(img.width * scale)
    new_h = int(img.height * scale)
    resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", size, bg)
    canvas.paste(resized, ((target_w - new_w) // 2, (target_h - new_h) // 2))
    return canvas


def add_paper_texture(base):
    width, height = base.size
    draw = ImageDraw.Draw(base, "RGBA")
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            shade = 18 if ((x // 8 + y // 8) % 2 == 0) else 8
            draw.rectangle((x, y, x + 4, y + 4), fill=(0, 0, 0, shade))
    return base.filter(ImageFilter.GaussianBlur(0.15))


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def render_card(cfg, project_dir, output):
    canvas = Image.new("RGB", (W, H), (19, 20, 22))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark_draw = ImageDraw.Draw(dark, "RGBA")
    for i in range(90):
        dark_draw.line((0, i * 24, W, i * 24 + 7), fill=(255, 255, 255, 5))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), dark).convert("RGB")

    card_x = int(cfg.get("card_x", 36))
    card_y = int(cfg.get("card_y", 44))
    card_w = int(cfg.get("card_w", W - 72))
    card_h = int(cfg.get("card_h", H - 88))
    card = Image.new("RGB", (card_w, card_h), tuple(cfg.get("paper_color", [248, 248, 244])))
    add_paper_texture(card)
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_layer.paste(card.convert("RGBA"), (card_x, card_y), rounded_mask((card_w, card_h), 18))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), card_layer)
    draw = ImageDraw.Draw(canvas, "RGBA")

    date_text = cfg.get("date")
    if date_text:
        label = cfg.get("date_label", "最新")
        date_font = font(int(cfg.get("date_size", 27)), True)
        label_font = font(int(cfg.get("date_label_size", 24)), True)
        label_w = int(text_len(draw, label, label_font))
        date_w = int(text_len(draw, date_text, date_font))
        pill_h = 42
        pill_w = label_w + date_w + 58
        pill_x = card_x + card_w - pill_w - 28
        pill_y = card_y + 26
        draw.rounded_rectangle(
            (pill_x, pill_y, pill_x + pill_w, pill_y + pill_h),
            radius=12,
            fill=tuple(cfg.get("date_bg", [238, 238, 232, 235])),
            outline=tuple(cfg.get("date_outline", [0, 0, 0, 26])),
            width=1,
        )
        draw.rounded_rectangle(
            (pill_x + 8, pill_y + 7, pill_x + 8 + label_w + 20, pill_y + pill_h - 7),
            radius=8,
            fill=tuple(cfg.get("date_label_bg", [255, 126, 104, 245])),
        )
        draw.text((pill_x + 18, pill_y + 9), label, font=label_font, fill=(13, 16, 24))
        draw.text((pill_x + label_w + 40, pill_y + 7), date_text, font=date_font, fill=(45, 48, 55))

    title = cfg.get("title", [])
    if isinstance(title, str):
        title = [title]
    title_font = font(int(cfg.get("title_size", 62)), True)
    default_title_y_offset = 96 if date_text else 62
    y = card_y + int(cfg.get("title_y_offset", default_title_y_offset))
    y = draw_centered(draw, title, y, title_font, tuple(cfg.get("title_color", [0, 0, 0])), card_w - 90)

    ribbon_y = y + int(cfg.get("ribbon_gap", 22))
    ribbon_x = card_x + 30
    ribbon_w = card_w - 60
    ribbon_h = int(cfg.get("ribbon_h", 92))
    purple = tuple(cfg.get("ribbon_color", [180, 59, 205]))
    draw.rounded_rectangle(
        (ribbon_x, ribbon_y, ribbon_x + ribbon_w, ribbon_y + ribbon_h),
        radius=42,
        fill=purple,
    )
    draw.rectangle((ribbon_x, ribbon_y, ribbon_x + 58, ribbon_y + ribbon_h), fill=purple)
    strap = cfg.get("strap", "")
    strap_font = font(int(cfg.get("strap_size", 54)), True)
    while text_len(draw, strap, strap_font) > ribbon_w - 70 and strap_font.size > 24:
        strap_font = font(strap_font.size - 2, True)
    draw.text(
        (ribbon_x + (ribbon_w - text_len(draw, strap, strap_font)) / 2, ribbon_y + 17),
        strap,
        font=strap_font,
        fill=tuple(cfg.get("strap_color", [255, 255, 255])),
    )

    media_x = card_x + 28
    media_y = ribbon_y + ribbon_h + int(cfg.get("media_gap", 34))
    media_w = card_w - 56
    media_h = int(cfg.get("media_h", 640))
    draw.rounded_rectangle(
        (media_x, media_y, media_x + media_w, media_y + media_h),
        radius=16,
        fill=(255, 255, 255),
        outline=purple,
        width=5,
    )
    img = Image.open(resolve_path(project_dir, cfg["image"]))
    fitted = fit_contain(img, (media_w - 18, media_h - 18), bg=(255, 255, 255))
    canvas.paste(fitted, (media_x + 9, media_y + 9))

    if cfg.get("play_marker", True):
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay, "RGBA")
        cx = media_x + media_w // 2
        cy = media_y + media_h // 2
        overlay_draw.polygon(
            [(cx - 52, cy - 70), (cx - 52, cy + 70), (cx + 72, cy)],
            fill=(255, 255, 255, int(cfg.get("play_marker_alpha", 92))),
        )
        canvas = Image.alpha_composite(canvas, overlay)
        draw = ImageDraw.Draw(canvas, "RGBA")

    text_y = media_y + media_h + int(cfg.get("body_gap", 54))
    body_font = font(int(cfg.get("body_size", 37)), True)
    max_w = card_w - 86
    line_h = int(cfg.get("body_line_h", 48))
    highlight = tuple(cfg.get("highlight_color", [52, 211, 226, 218]))
    for para in cfg.get("body", []):
        for line in wrap_text(draw, para, body_font, max_w):
            if text_y > card_y + card_h - 62:
                break
            line_w = text_len(draw, line, body_font)
            draw.rounded_rectangle(
                (card_x + 30, text_y - 4, card_x + 42 + line_w, text_y + line_h - 4),
                radius=6,
                fill=highlight,
            )
            draw.text((card_x + 38, text_y), line, font=body_font, fill=(0, 0, 0))
            text_y += line_h + 5
        text_y += 6

    badge = cfg.get("badge", "AI 信息差快报")
    if badge:
        badge_font = font(int(cfg.get("badge_size", 24)), True)
        draw.text(
            (card_x + card_w - 238, card_y + card_h - 44),
            badge,
            font=badge_font,
            fill=(76, 76, 76, 210),
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output, quality=int(cfg.get("quality", 94)))
    return output


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    config_path = resolve_path(project_dir, args.config)
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    output = resolve_path(project_dir, args.output or cfg.get("output", "renders/paper-card-preview.jpg"))
    print(render_card(cfg, project_dir, output))


if __name__ == "__main__":
    main()
