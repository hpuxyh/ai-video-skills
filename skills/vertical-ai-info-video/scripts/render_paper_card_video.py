#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


W, H = 1080, 1920
DEFAULT_FPS = 30
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


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


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


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def add_paper_texture(base):
    width, height = base.size
    draw = ImageDraw.Draw(base, "RGBA")
    for y in range(0, height, 8):
        for x in range(0, width, 8):
            shade = 16 if ((x // 8 + y // 8) % 2 == 0) else 7
            draw.rectangle((x, y, x + 4, y + 4), fill=(0, 0, 0, shade))
    return base.filter(ImageFilter.GaussianBlur(0.15))


def fit_cover(img, size):
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def brighten(img, cfg):
    grade = cfg.get("image_grade", {})
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(float(grade.get("brightness", 1.08)))
    img = ImageEnhance.Contrast(img).enhance(float(grade.get("contrast", 1.03)))
    img = ImageEnhance.Color(img).enhance(float(grade.get("color", 1.03)))
    return img


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


def centered_line_layout(draw, lines, y, fnt, max_width, canvas_width=W, line_gap=12):
    wrapped = []
    for raw in lines:
        wrapped.extend(wrap_text(draw, raw, fnt, max_width))
    layout = []
    for line in wrapped:
        box = draw.textbbox((0, 0), line, font=fnt)
        h = box[3] - box[1]
        w = text_len(draw, line, fnt)
        layout.append({"text": line, "x": (canvas_width - w) / 2, "y": y, "w": w, "h": h})
        y += h + line_gap
    return layout, y


def centered_colored_line_layout(draw, lines, y, fnt, fills, max_width, center_x=W / 2, line_gap=12):
    wrapped = []
    for index, raw in enumerate(lines):
        fill = tuple(fills[min(index, len(fills) - 1)]) if fills else (255, 255, 255)
        for line in wrap_text(draw, raw, fnt, max_width):
            wrapped.append((line, fill))
    layout = []
    for line, fill in wrapped:
        box = draw.textbbox((0, 0), line, font=fnt)
        h = box[3] - box[1]
        w = text_len(draw, line, fnt)
        layout.append({"text": line, "x": center_x - w / 2, "y": y, "w": w, "h": h, "fill": fill})
        y += h + line_gap
    return layout, y


def total_layout_height(draw, lines, fnt, max_width, line_gap=12):
    total = 0
    count = 0
    for raw in lines:
        for line in wrap_text(draw, raw, fnt, max_width):
            box = draw.textbbox((0, 0), line, font=fnt)
            total += box[3] - box[1]
            count += 1
    return total + max(0, count - 1) * line_gap


def alpha_composite_with_opacity(canvas, layer, opacity):
    opacity = max(0.0, min(1.0, opacity))
    if opacity >= 1:
        canvas.alpha_composite(layer)
        return
    alpha = layer.getchannel("A").point(lambda p: int(p * opacity))
    layer = layer.copy()
    layer.putalpha(alpha)
    canvas.alpha_composite(layer)


def pop_state(t, start, duration=0.42):
    p = (t - start) / duration
    if p <= 0:
        return None
    p = min(1.0, p)
    opacity = ease(min(1.0, p / 0.32))
    if p < 0.62:
        scale = 0.76 + 0.34 * ease(p / 0.62)
    else:
        scale = 1.10 - 0.10 * ease((p - 0.62) / 0.38)
    return scale, opacity


def draw_line_popup(canvas, text, center_y, base_size, fill, start, t, center_x=None, bold=True):
    state = pop_state(t, start)
    if state is None:
        return
    scale, opacity = state
    size = max(12, int(base_size * scale + 0.5))
    fnt = font(size, bold)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    box = d.textbbox((0, 0), text, font=fnt)
    text_w = box[2] - box[0]
    text_h = box[3] - box[1]
    if center_x is None:
        center_x = W / 2
    x = center_x - text_w / 2 - box[0]
    y = center_y - text_h / 2 - box[1]
    d.text((x, y), text, font=fnt, fill=fill)
    alpha_composite_with_opacity(canvas, layer, opacity)


def draw_panel_popup(canvas, layout, t):
    start = float(layout.get("title_panel_start", 0.0))
    p = (t - start) / float(layout.get("title_panel_duration", 0.30))
    if p <= 0:
        return
    p = min(1.0, p)
    eased = ease(p)
    opacity = ease(min(1.0, p / 0.36))
    panel_x, panel_y, panel_w, panel_h = layout["title_panel_rect"]
    current_w = panel_w * (0.18 + 0.82 * eased)
    cx = panel_x + panel_w / 2
    left = cx - current_w / 2
    right = cx + current_w / 2

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    purple = layout["purple"]
    d.rounded_rectangle(
        (left, panel_y, right, panel_y + panel_h),
        radius=int(layout.get("title_panel_radius", 30)),
        fill=purple,
    )
    d.rectangle((left, panel_y, min(left + 58, right), panel_y + panel_h), fill=purple)
    alpha_composite_with_opacity(canvas, layer, opacity)


def draw_action_fade(canvas, layout, t):
    start = float(layout.get("action_start", 0.72))
    p = (t - start) / float(layout.get("action_duration", 0.36))
    if p <= 0:
        return
    p = min(1.0, p)
    opacity = ease(p)
    shift = int(10 * (1 - opacity))
    fnt = font(int(layout.get("action_size", 36)), bool(layout.get("action_bold", False)))
    fill = tuple(layout.get("action_fill", [18, 20, 28]))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    for item in layout.get("action_lines", []):
        d.text((item["x"], item["y"] + shift), item["text"], font=fnt, fill=fill)
    alpha_composite_with_opacity(canvas, layer, opacity)


def draw_ribbon_popup(canvas, layout, t):
    start = float(layout.get("ribbon_start", 0.46))
    p = (t - start) / float(layout.get("ribbon_duration", 0.34))
    if p <= 0:
        return
    p = min(1.0, p)
    eased = ease(p)
    opacity = ease(min(1.0, p / 0.36))
    ribbon_x, ribbon_y, ribbon_w, ribbon_h = layout["ribbon_rect"]
    purple = layout["purple"]
    current_w = ribbon_w * (0.20 + 0.80 * eased)
    cx = ribbon_x + ribbon_w / 2
    left = cx - current_w / 2
    right = cx + current_w / 2

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle((left, ribbon_y, right, ribbon_y + ribbon_h), radius=40, fill=purple)
    d.rectangle((left, ribbon_y, min(left + 58, right), ribbon_y + ribbon_h), fill=purple)

    strap = layout["strap"]
    strap_font = layout["strap_font"]
    strap_fill = layout["strap_fill"]
    text_alpha = ease(max(0.0, min(1.0, (t - start - 0.10) / 0.22)))
    if text_alpha > 0:
        text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        td = ImageDraw.Draw(text_layer, "RGBA")
        strap_w = text_len(td, strap, strap_font)
        td.text(
            (ribbon_x + (ribbon_w - strap_w) / 2, ribbon_y + (ribbon_h - strap_font.size) / 2 - 3),
            strap,
            font=strap_font,
            fill=strap_fill,
        )
        alpha_composite_with_opacity(layer, text_layer, text_alpha)
    alpha_composite_with_opacity(canvas, layer, opacity)


def draw_dynamic_header(canvas, t, cfg, layout):
    if not cfg.get("animate_title", True):
        return
    if layout.get("title_on_purple"):
        draw_panel_popup(canvas, layout, t)
        title_start = float(cfg.get("title_start", 0.08))
        title_step = float(cfg.get("title_step", 0.18))
        title_size = int(cfg.get("title_size", 58))
        panel_x, _, panel_w, _ = layout["title_panel_rect"]
        center_x = panel_x + panel_w / 2
        for i, item in enumerate(layout["title_lines"]):
            center_y = item["y"] + item["h"] / 2
            draw_line_popup(
                canvas,
                item["text"],
                center_y,
                title_size,
                tuple(item.get("fill", [255, 255, 255])),
                title_start + i * title_step,
                t,
                center_x=center_x,
                bold=True,
            )
        draw_action_fade(canvas, layout, t)
        return
    title_start = float(cfg.get("title_start", 0.04))
    title_step = float(cfg.get("title_step", 0.18))
    title_size = int(cfg.get("title_size", 58))
    fill = tuple(cfg.get("title_color", [0, 0, 0]))
    for i, item in enumerate(layout["title_lines"]):
        center_y = item["y"] + item["h"] / 2
        draw_line_popup(canvas, item["text"], center_y, title_size, fill, title_start + i * title_step, t)
    if layout.get("show_ribbon", True):
        draw_ribbon_popup(canvas, layout, t)


def draw_structured_body(draw, cfg, card_x, card_y, card_w, card_h, text_y):
    rows = cfg.get("body_rows", [])
    body_font = font(int(cfg.get("body_size", 29)), True)
    label_font = font(int(cfg.get("body_label_size", 25)), True)
    row_x = card_x + int(cfg.get("body_row_x_offset", 30))
    row_w = card_w - int(cfg.get("body_row_x_offset", 30)) * 2
    label_w = int(cfg.get("body_label_w", 132))
    row_gap = int(cfg.get("body_row_gap", 10))
    row_pad_x = int(cfg.get("body_row_pad_x", 14))
    row_pad_y = int(cfg.get("body_row_pad_y", 12))
    line_h = int(cfg.get("body_line_h", 38))
    min_h = int(cfg.get("body_row_min_h", 66))
    row_bg = tuple(cfg.get("body_row_bg", [203, 247, 252, 230]))
    label_bg = tuple(cfg.get("body_label_bg", [52, 211, 226, 245]))
    row_outline = tuple(cfg.get("body_row_outline", [52, 211, 226, 105]))
    text_fill = tuple(cfg.get("body_text_color", [0, 0, 0]))
    label_fill = tuple(cfg.get("body_label_color", [8, 14, 18]))
    bottom_limit = card_y + card_h - int(cfg.get("body_bottom_margin", 78))

    for row in rows:
        label = row.get("label", "")
        text = row.get("text", "")
        text_x = row_x + label_w + row_pad_x + 14
        text_max_w = row_x + row_w - text_x - row_pad_x
        lines = wrap_text(draw, text, body_font, text_max_w)
        row_h = max(min_h, len(lines) * line_h + row_pad_y * 2)
        if text_y + row_h > bottom_limit:
            break

        draw.rounded_rectangle(
            (row_x, text_y, row_x + row_w, text_y + row_h),
            radius=9,
            fill=row_bg,
            outline=row_outline,
            width=1,
        )
        label_y = text_y + 9
        draw.rounded_rectangle(
            (row_x + 10, label_y, row_x + label_w, text_y + row_h - 9),
            radius=8,
            fill=label_bg,
        )
        label_box = draw.textbbox((0, 0), label, font=label_font)
        label_text_h = label_box[3] - label_box[1]
        label_text_w = text_len(draw, label, label_font)
        draw.text(
            (
                row_x + 10 + (label_w - 10 - label_text_w) / 2,
                text_y + (row_h - label_text_h) / 2 - label_box[1],
            ),
            label,
            font=label_font,
            fill=label_fill,
        )

        line_y = text_y + row_pad_y + 1
        if len(lines) == 1:
            text_box = draw.textbbox((0, 0), lines[0], font=body_font)
            line_y = text_y + (row_h - (text_box[3] - text_box[1])) / 2 - text_box[1]
        for line in lines:
            draw.text((text_x, line_y), line, font=body_font, fill=text_fill)
            line_y += line_h
        text_y += row_h + row_gap
    return text_y


def draw_editorial_body(draw, cfg, card_x, card_y, card_w, card_h, text_y):
    rows = cfg.get("body_rows") or cfg.get("body_items", [])
    body_font = font(int(cfg.get("body_size", 31)), True)
    label_font = font(int(cfg.get("body_label_size", 24)), True)
    number_font = font(int(cfg.get("body_number_size", 24)), True)
    row_x = card_x + int(cfg.get("body_row_x_offset", 54))
    row_w = card_w - int(cfg.get("body_row_x_offset", 54)) * 2
    label_w = int(cfg.get("body_editorial_label_w", 112))
    row_gap = int(cfg.get("body_item_gap", 5))
    line_h = int(cfg.get("body_line_h", 38))
    row_min_h = int(cfg.get("body_editorial_row_h", 58))
    label_fill = tuple(cfg.get("body_label_color", [126, 51, 163]))
    text_fill = tuple(cfg.get("body_text_color", [18, 22, 28]))
    number_fill = tuple(cfg.get("body_number_fill", [180, 59, 205, 230]))
    divider = tuple(cfg.get("body_divider", [30, 36, 46, 42]))
    bottom_limit = card_y + card_h - int(cfg.get("body_bottom_margin", 78))

    for index, row in enumerate(rows, start=1):
        label = row.get("label", "")
        text = row.get("text", "")
        text_x = row_x + label_w + 40
        text_max_w = row_x + row_w - text_x
        lines = wrap_text(draw, text, body_font, text_max_w)
        use_body_font = body_font
        if len(lines) > 1:
            use_body_font = font(max(24, body_font.size - 3), True)
            lines = wrap_text(draw, text, use_body_font, text_max_w)
        row_h = max(row_min_h, len(lines) * line_h + 16)
        if text_y + row_h > bottom_limit:
            break

        number = f"{index:02d}"
        draw.text((row_x, text_y + 12), number, font=number_font, fill=number_fill)
        draw.text((row_x + 52, text_y + 14), label, font=label_font, fill=label_fill)
        current_y = text_y + max(10, (row_h - len(lines) * line_h) // 2 - 1)
        for line in lines:
            draw.text((text_x, current_y), line, font=use_body_font, fill=text_fill)
            current_y += line_h
        if index < len(rows):
            draw.line((row_x, text_y + row_h, row_x + row_w, text_y + row_h), fill=divider, width=1)
        text_y += row_h + row_gap
    return text_y


def draw_static_base(cfg):
    canvas = Image.new("RGB", (W, H), tuple(cfg.get("background", [19, 20, 22])))
    dark = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dark_draw = ImageDraw.Draw(dark, "RGBA")
    for i in range(90):
        dark_draw.line((0, i * 24, W, i * 24 + 7), fill=(255, 255, 255, 5))
    canvas = Image.alpha_composite(canvas.convert("RGBA"), dark).convert("RGBA")

    card_x = int(cfg.get("card_x", 36))
    card_y = int(cfg.get("card_y", 44))
    card_w = int(cfg.get("card_w", W - 72))
    card_h = int(cfg.get("card_h", H - 88))
    card = Image.new("RGB", (card_w, card_h), tuple(cfg.get("paper_color", [248, 248, 244])))
    add_paper_texture(card)
    card_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_layer.paste(card.convert("RGBA"), (card_x, card_y), rounded_mask((card_w, card_h), 18))
    canvas = Image.alpha_composite(canvas, card_layer)
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
    title_font = font(int(cfg.get("title_size", 58)), True)
    default_title_y_offset = 96 if date_text else 62
    y = card_y + int(cfg.get("title_y_offset", default_title_y_offset))
    purple = tuple(cfg.get("ribbon_color", [180, 59, 205]))
    show_title = cfg.get("show_title", True)
    title_on_purple = cfg.get("title_on_purple", False)

    if title_on_purple and show_title:
        panel_x_offset = int(cfg.get("title_panel_x_offset", 30))
        panel_x = card_x + panel_x_offset
        panel_y = y
        panel_w = card_w - panel_x_offset * 2
        panel_h = int(cfg.get("title_panel_h", 206))
        panel_radius = int(cfg.get("title_panel_radius", 30))
        title_gap = int(cfg.get("title_panel_line_gap", 14))
        title_fills = cfg.get("title_line_colors", [[255, 255, 255], [255, 238, 118]])
        title_max_w = panel_w - 78
        title_total_h = total_layout_height(draw, title, title_font, title_max_w, title_gap)
        title_y = panel_y + max(16, int((panel_h - title_total_h) / 2) - 1)
        title_layout, _ = centered_colored_line_layout(
            draw,
            title,
            title_y,
            title_font,
            title_fills,
            title_max_w,
            center_x=panel_x + panel_w / 2,
            line_gap=title_gap,
        )

        if not cfg.get("animate_title", True):
            draw.rounded_rectangle(
                (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
                radius=panel_radius,
                fill=purple,
            )
            draw.rectangle((panel_x, panel_y, panel_x + 58, panel_y + panel_h), fill=purple)
            for item in title_layout:
                draw.text((item["x"], item["y"]), item["text"], font=title_font, fill=tuple(item["fill"]))

        action_text = cfg.get("action_text") or cfg.get("strap", "")
        action_font = font(int(cfg.get("action_size", 36)), bool(cfg.get("action_bold", False)))
        action_y = panel_y + panel_h + int(cfg.get("action_gap", 22))
        action_layout, action_end_y = centered_line_layout(
            draw,
            wrap_text(draw, action_text, action_font, card_w - 96) if action_text else [],
            action_y,
            action_font,
            card_w - 96,
            line_gap=int(cfg.get("action_line_gap", 10)),
        )
        action_fill = tuple(cfg.get("action_color", [18, 20, 28]))
        if not cfg.get("animate_title", True):
            for item in action_layout:
                draw.text((item["x"], item["y"]), item["text"], font=action_font, fill=action_fill)

        title_start = float(cfg.get("title_start", 0.08))
        title_step = float(cfg.get("title_step", 0.18))
        action_start_default = title_start + max(1, len(title_layout)) * title_step + 0.18
        header_layout = {
            "title_on_purple": True,
            "title_lines": title_layout,
            "title_panel_rect": (panel_x, panel_y, panel_w, panel_h),
            "title_panel_radius": panel_radius,
            "title_panel_start": float(cfg.get("title_panel_start", 0.0)),
            "title_panel_duration": float(cfg.get("title_panel_duration", 0.30)),
            "purple": purple,
            "action_lines": action_layout,
            "action_start": float(cfg.get("action_start", action_start_default)),
            "action_duration": float(cfg.get("action_duration", 0.36)),
            "action_size": int(cfg.get("action_size", 36)),
            "action_bold": bool(cfg.get("action_bold", False)),
            "action_fill": action_fill,
        }
        media_anchor_y = action_end_y + int(cfg.get("ribbon_gap", 0)) + int(cfg.get("ribbon_h", 0))
    else:
        title_layout, y = centered_line_layout(draw, title, y, title_font, card_w - 90)
        if not cfg.get("animate_title", True) and show_title:
            for item in title_layout:
                draw.text((item["x"], item["y"]), item["text"], font=title_font, fill=tuple(cfg.get("title_color", [0, 0, 0])))

        ribbon_y = y + int(cfg.get("ribbon_gap", 22))
        ribbon_x = card_x + 30
        ribbon_w = card_w - 60
        ribbon_h = int(cfg.get("ribbon_h", 86))
        show_ribbon = cfg.get("show_ribbon", True)
        strap = cfg.get("strap", "")
        strap_font = font(int(cfg.get("strap_size", 44)), True)
        while text_len(draw, strap, strap_font) > ribbon_w - 70 and strap_font.size > 24:
            strap_font = font(strap_font.size - 2, True)
        if not cfg.get("animate_title", True) and show_ribbon:
            draw.rounded_rectangle((ribbon_x, ribbon_y, ribbon_x + ribbon_w, ribbon_y + ribbon_h), radius=40, fill=purple)
            draw.rectangle((ribbon_x, ribbon_y, ribbon_x + 58, ribbon_y + ribbon_h), fill=purple)
            draw.text(
                (ribbon_x + (ribbon_w - text_len(draw, strap, strap_font)) / 2, ribbon_y + (ribbon_h - strap_font.size) / 2 - 3),
                strap,
                font=strap_font,
                fill=tuple(cfg.get("strap_color", [255, 255, 255])),
            )

        ribbon_start_default = float(cfg.get("title_start", 0.04)) + max(1, len(title_layout)) * float(cfg.get("title_step", 0.18)) + 0.08
        header_layout = {
            "title_on_purple": False,
            "title_lines": title_layout if show_title else [],
            "ribbon_rect": (ribbon_x, ribbon_y, ribbon_w, ribbon_h),
            "ribbon_start": float(cfg.get("ribbon_start", ribbon_start_default)),
            "ribbon_duration": float(cfg.get("ribbon_duration", 0.34)),
            "purple": purple,
            "strap": strap,
            "strap_font": strap_font,
            "strap_fill": tuple(cfg.get("strap_color", [255, 255, 255])),
            "show_ribbon": show_ribbon,
        }
        media_anchor_y = ribbon_y + (ribbon_h if show_ribbon else 0)

    media_x = card_x + int(cfg.get("media_x_offset", 28))
    media_y = media_anchor_y + int(cfg.get("media_gap", 32))
    media_w = card_w - int(cfg.get("media_x_offset", 28)) * 2
    media_h = int(cfg.get("media_h", 660))

    text_y = media_y + media_h + int(cfg.get("body_gap", 46))
    if cfg.get("body_style") == "editorial_lines":
        draw_editorial_body(draw, cfg, card_x, card_y, card_w, card_h, text_y)
    elif cfg.get("body_rows") or cfg.get("body_style") == "structured":
        draw_structured_body(draw, cfg, card_x, card_y, card_w, card_h, text_y)
    else:
        body_font = font(int(cfg.get("body_size", 31)), True)
        max_w = card_w - 86
        line_h = int(cfg.get("body_line_h", 40))
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

    return canvas, (media_x, media_y, media_w, media_h), purple, header_layout


def frame_timing(t, total_photos, cfg):
    duration = float(cfg.get("duration", 7))
    weights = cfg.get("image_hold_weights") or cfg.get("image_weights")
    if weights:
        weights = [float(x) for x in weights[:total_photos]]
        if len(weights) < total_photos:
            weights.extend([1.0] * (total_photos - len(weights)))
        weights = [max(0.01, x) for x in weights]
        unit = duration / sum(weights)
        cuts = []
        elapsed = 0.0
        for weight in weights[:-1]:
            elapsed += weight * unit
            cuts.append(round(elapsed, 4))
    else:
        cuts = cfg.get("beat_cuts")
    if cuts is None:
        cuts = [round(duration * i / total_photos, 2) for i in range(1, total_photos)]
    cuts = [float(x) for x in cuts[: total_photos - 1]]
    starts = [0.0] + cuts
    ends = cuts + [duration]
    idx = 0
    for cut in cuts:
        if t >= cut:
            idx += 1
    idx = min(idx, total_photos - 1)
    start = starts[idx]
    end = ends[idx]
    progress = (t - start) / max(1 / float(cfg.get("fps", DEFAULT_FPS)), end - start)
    return idx, progress


def media_layer(img, media_rect, idx, total, progress, cfg, purple):
    media_x, media_y, media_w, media_h = media_rect
    frame_pad = int(cfg.get("media_pad", 9))
    inner_w = media_w - frame_pad * 2
    inner_h = media_h - frame_pad * 2
    motion = cfg.get("motion", {})
    zoom_amount = float(motion.get("zoom", 0.025))
    pan_x = float(motion.get("pan_x", 10))
    pan_y = float(motion.get("pan_y", 7))

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    d.rounded_rectangle(
        (media_x, media_y, media_x + media_w, media_y + media_h),
        radius=16,
        fill=(255, 255, 255),
        outline=purple,
        width=5,
    )

    src = brighten(img, cfg)
    bg = fit_cover(src.filter(ImageFilter.GaussianBlur(18)), (inner_w, inner_h))
    bg = ImageEnhance.Brightness(bg).enhance(1.12)
    bg = ImageEnhance.Contrast(bg).enhance(0.96).convert("RGBA")
    wash = Image.new("RGBA", (inner_w, inner_h), (255, 255, 255, 112))
    view = Image.alpha_composite(bg, wash)

    eased = ease(progress)
    scale = min(inner_w / src.width, inner_h / src.height) * (1 + zoom_amount * eased)
    photo = src.resize((int(src.width * scale + 0.5), int(src.height * scale + 0.5)), Image.Resampling.LANCZOS).convert("RGBA")
    spare_x = inner_w - photo.width
    spare_y = inner_h - photo.height
    x_dir = -1 if idx % 2 else 1
    y_dir = -1 if idx % 3 == 0 else 1
    px = spare_x // 2 + int(pan_x * (eased - 0.5) * x_dir)
    py = spare_y // 2 + int(pan_y * (eased - 0.5) * y_dir)

    clipped = Image.new("RGBA", (inner_w, inner_h), (0, 0, 0, 0))
    clipped.alpha_composite(view)
    clipped.alpha_composite(photo, (px, py))
    layer.paste(clipped, (media_x + frame_pad, media_y + frame_pad), rounded_mask((inner_w, inner_h), 12))
    return layer


def run_ffmpeg_frames(frames_dir, fps, silent_output):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(frames_dir / "frame-%04d.jpg"),
            "-vf",
            "format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-movflags",
            "+faststart",
            str(silent_output),
        ],
        check=True,
    )


def mix_bgm(silent_output, final_output, project_dir, cfg):
    bgm = cfg.get("bgm")
    if not bgm or not bgm.get("path"):
        if silent_output != final_output:
            shutil.copyfile(silent_output, final_output)
        return

    duration = float(cfg.get("duration", 7))
    start = float(bgm.get("start", 0))
    volume = float(bgm.get("volume", 0.55))
    fade_in = float(bgm.get("fade_in", 0.08))
    fade_out = float(bgm.get("fade_out", 0.35))
    bgm_path = resolve_path(project_dir, bgm["path"])
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(silent_output),
            "-i",
            str(bgm_path),
            "-filter_complex",
            f"[1:a]atrim=start={start}:end={start + duration},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d={fade_in},afade=t=out:st={max(0, duration - fade_out)}:d={fade_out},"
            f"volume={volume}[a]",
            "-map",
            "0:v:0",
            "-map",
            "[a]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            "-movflags",
            "+faststart",
            str(final_output),
        ],
        check=True,
    )


def make_contact_sheet(output, contact_sheet):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(output),
            "-vf",
            "fps=1,scale=270:-1,tile=4x2",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(contact_sheet),
        ],
        check=True,
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output")
    parser.add_argument("--contact-sheet")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    config_path = resolve_path(project_dir, args.config)
    cfg = json.loads(config_path.read_text(encoding="utf-8"))

    fps = int(cfg.get("fps", DEFAULT_FPS))
    duration = float(cfg.get("duration", 7))
    total_frames = int(round(fps * duration))
    output = resolve_path(project_dir, args.output or cfg.get("output", "renders/paper-card-video.mp4"))
    output.parent.mkdir(parents=True, exist_ok=True)
    silent_output = output.with_name(output.stem + ".silent.mp4")

    images = [Image.open(resolve_path(project_dir, p)).convert("RGB") for p in cfg["images"]]
    if not images:
        raise ValueError("Config must include at least one image")

    base, media_rect, purple, header_layout = draw_static_base(cfg)
    frames_dir = output.parent / f"{output.stem}-frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old_frame in frames_dir.glob("frame-*.jpg"):
        old_frame.unlink()

    for n in range(total_frames):
        t = n / fps
        idx, progress = frame_timing(t, len(images), cfg)
        canvas = base.copy()
        draw_dynamic_header(canvas, t, cfg, header_layout)
        canvas.alpha_composite(media_layer(images[idx], media_rect, idx, len(images), progress, cfg, purple))
        canvas.convert("RGB").save(frames_dir / f"frame-{n:04d}.jpg", quality=int(cfg.get("frame_quality", 92)))

    run_ffmpeg_frames(frames_dir, fps, silent_output)
    mix_bgm(silent_output, output, project_dir, cfg)

    contact_sheet = args.contact_sheet or cfg.get("contact_sheet")
    if contact_sheet:
        make_contact_sheet(output, resolve_path(project_dir, contact_sheet))

    print(output)


if __name__ == "__main__":
    main()
