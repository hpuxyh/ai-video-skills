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


def draw_centered_lines(draw, lines, y, fnt, fills, max_width, canvas_width=W, line_gap=12):
    wrapped = []
    line_fills = []
    for index, raw in enumerate(lines):
        raw_fill = fills[min(index, len(fills) - 1)] if fills else (255, 255, 255)
        raw_lines = wrap_text(draw, raw, fnt, max_width)
        wrapped.extend(raw_lines)
        line_fills.extend([raw_fill] * len(raw_lines))
    total_h = 0
    line_boxes = []
    for line in wrapped:
        box = draw.textbbox((0, 0), line, font=fnt)
        h = box[3] - box[1]
        line_boxes.append((line, h))
        total_h += h
    total_h += max(0, len(wrapped) - 1) * line_gap
    current_y = y
    for i, (line, h) in enumerate(line_boxes):
        x = (canvas_width - text_len(draw, line, fnt)) / 2
        draw.text((x, current_y), line, font=fnt, fill=tuple(line_fills[i]))
        current_y += h + line_gap
    return total_h


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


def draw_structured_body(draw, cfg, card_x, card_y, card_w, card_h, text_y):
    rows = cfg.get("body_rows", [])[: int(cfg.get("body_max_rows", 6))]
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
    show_labels = bool(cfg.get("body_show_labels", True))

    for row in rows:
        if isinstance(row, str):
            label = ""
            text = row
        else:
            label = row.get("label", "")
            text = row.get("text", "")
        use_label = show_labels and bool(label)
        text_x = row_x + (label_w + row_pad_x + 14 if use_label else row_pad_x + 14)
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
        if use_label:
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
    show_title = cfg.get("show_title", True)
    purple = tuple(cfg.get("ribbon_color", [180, 59, 205]))
    title_on_purple = cfg.get("title_on_purple", False)
    if show_title and title_on_purple:
        panel_x = card_x + int(cfg.get("title_panel_x_offset", 30))
        panel_y = y
        panel_w = card_w - int(cfg.get("title_panel_x_offset", 30)) * 2
        panel_h = int(cfg.get("title_panel_h", 206))
        draw.rounded_rectangle(
            (panel_x, panel_y, panel_x + panel_w, panel_y + panel_h),
            radius=int(cfg.get("title_panel_radius", 30)),
            fill=purple,
        )
        draw.rectangle((panel_x, panel_y, panel_x + 58, panel_y + panel_h), fill=purple)
        title_fills = cfg.get("title_line_colors", [[255, 255, 255], [255, 235, 120]])
        probe_lines = []
        for raw in title:
            probe_lines.extend(wrap_text(draw, raw, title_font, panel_w - 78))
        total_h = 0
        for line in probe_lines:
            box = draw.textbbox((0, 0), line, font=title_font)
            total_h += box[3] - box[1]
        total_h += max(0, len(probe_lines) - 1) * int(cfg.get("title_panel_line_gap", 14))
        title_y = panel_y + max(16, int((panel_h - total_h) / 2) - 1)
        draw_centered_lines(
            draw,
            title,
            title_y,
            title_font,
            [tuple(c) for c in title_fills],
            panel_w - 78,
            canvas_width=W,
            line_gap=int(cfg.get("title_panel_line_gap", 14)),
        )
        action_text = cfg.get("action_text") or cfg.get("strap", "")
        action_font = font(int(cfg.get("action_size", 36)), bool(cfg.get("action_bold", False)))
        action_max_w = card_w - 96
        action_y = panel_y + panel_h + int(cfg.get("action_gap", 22))
        for line in wrap_text(draw, action_text, action_font, action_max_w):
            x = (W - text_len(draw, line, action_font)) / 2
            draw.text((x, action_y), line, font=action_font, fill=tuple(cfg.get("action_color", [22, 24, 30])))
            box = draw.textbbox((0, 0), line, font=action_font)
            action_y += (box[3] - box[1]) + 10
        y = action_y
    elif show_title:
        y = draw_centered(draw, title, y, title_font, tuple(cfg.get("title_color", [0, 0, 0])), card_w - 90)
    else:
        probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
        wrapped = []
        for raw in title:
            wrapped.extend(wrap_text(probe, raw, title_font, card_w - 90))
        for line in wrapped:
            box = probe.textbbox((0, 0), line, font=title_font)
            y += box[3] - box[1] + 12

    ribbon_y = y + int(cfg.get("ribbon_gap", 22))
    ribbon_x = card_x + 30
    ribbon_w = card_w - 60
    ribbon_h = int(cfg.get("ribbon_h", 92))
    strap = cfg.get("strap", "")
    if cfg.get("show_ribbon", True) and not title_on_purple:
        draw.rounded_rectangle(
            (ribbon_x, ribbon_y, ribbon_x + ribbon_w, ribbon_y + ribbon_h),
            radius=42,
            fill=purple,
        )
        draw.rectangle((ribbon_x, ribbon_y, ribbon_x + 58, ribbon_y + ribbon_h), fill=purple)
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
    show_media_content = cfg.get("show_media_content", True)
    if show_media_content:
        img = Image.open(resolve_path(project_dir, cfg["image"]))
        fitted = fit_contain(img, (media_w - 18, media_h - 18), bg=(255, 255, 255))
        canvas.paste(fitted, (media_x + 9, media_y + 9))

    if show_media_content and cfg.get("play_marker", True):
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
    label_font = font(int(cfg.get("body_label_size", max(24, int(cfg.get("body_size", 37)) - 7))), True)
    max_w = card_w - 86
    line_h = int(cfg.get("body_line_h", 48))
    highlight = tuple(cfg.get("highlight_color", [52, 211, 226, 218]))
    body_items = cfg.get("body_items")
    body_style = cfg.get("body_style", "highlight")
    if cfg.get("body_rows") or body_style == "structured":
        draw_structured_body(draw, cfg, card_x, card_y, card_w, card_h, text_y)
    elif body_items and body_style == "editorial_lines":
        show_labels = bool(cfg.get("body_show_labels", True))
        show_numbers = bool(cfg.get("body_show_numbers", True))
        row_x = card_x + int(cfg.get("body_row_x_offset", 54))
        row_w = card_w - int(cfg.get("body_row_x_offset", 54)) * 2
        label_fill = tuple(cfg.get("body_label_color", [126, 51, 163]))
        text_fill = tuple(cfg.get("body_text_color", [18, 22, 28]))
        number_fill = tuple(cfg.get("body_number_fill", [180, 59, 205, 230]))
        divider = tuple(cfg.get("body_divider", [30, 36, 46, 42]))
        row_gap = int(cfg.get("body_item_gap", 5))
        label_w = int(cfg.get("body_editorial_label_w", 112))
        body_font = font(int(cfg.get("body_size", 31)), True)
        label_font = font(int(cfg.get("body_label_size", 24)), True)
        number_font = font(int(cfg.get("body_number_size", 24)), True)
        for index, item in enumerate(body_items, start=1):
            label = item.get("label", "")
            text = item.get("text", "")
            left_extra = (52 if show_numbers else 0) + (label_w if show_labels and label else 0)
            text_x = row_x + left_extra + 40
            text_max_w = row_x + row_w - text_x
            lines = wrap_text(draw, text, body_font, text_max_w)
            use_body_font = body_font
            if len(lines) > 1:
                use_body_font = font(max(24, body_font.size - 3), True)
                lines = wrap_text(draw, text, use_body_font, text_max_w)
            row_h = max(int(cfg.get("body_editorial_row_h", 58)), len(lines) * line_h + 16)
            if text_y + row_h > card_y + card_h - 62:
                break
            num = f"{index:02d}"
            if show_numbers:
                draw.text((row_x, text_y + 12), num, font=number_font, fill=number_fill)
            if show_labels and label:
                draw.text((row_x + (52 if show_numbers else 0), text_y + 14), label, font=label_font, fill=label_fill)
            current_y = text_y + max(10, (row_h - len(lines) * line_h) // 2 - 1)
            for line in lines:
                draw.text((text_x, current_y), line, font=use_body_font, fill=text_fill)
                current_y += line_h
            if index < len(body_items):
                draw.line((row_x, text_y + row_h, row_x + row_w, text_y + row_h), fill=divider, width=1)
            text_y += row_h + row_gap
    elif body_items and body_style == "clean_rows":
        show_labels = bool(cfg.get("body_show_labels", True))
        show_numbers = bool(cfg.get("body_show_numbers", True))
        row_x = card_x + int(cfg.get("body_row_x_offset", 38))
        row_w = card_w - int(cfg.get("body_row_x_offset", 38)) * 2
        row_fill = tuple(cfg.get("body_row_fill", [239, 253, 254, 188]))
        row_outline = tuple(cfg.get("body_row_outline", [42, 185, 201, 68]))
        label_fill = tuple(cfg.get("body_label_color", [126, 51, 163]))
        text_fill = tuple(cfg.get("body_text_color", [18, 22, 28]))
        number_fill = tuple(cfg.get("body_number_fill", [179, 59, 205, 235]))
        row_gap = int(cfg.get("body_item_gap", 10))
        label_w = int(cfg.get("body_clean_label_w", 112))
        body_font = font(int(cfg.get("body_size", 31)), True)
        label_font = font(int(cfg.get("body_label_size", 25)), True)
        number_font = font(int(cfg.get("body_number_size", 20)), True)
        for index, item in enumerate(body_items, start=1):
            label = item.get("label", "")
            text = item.get("text", "")
            left_extra = (58 if show_numbers else 0) + (label_w if show_labels and label else 0)
            text_x = row_x + left_extra + 22
            text_max_w = row_x + row_w - text_x - 24
            lines = wrap_text(draw, text, body_font, text_max_w)
            if len(lines) > 1:
                compact_text = text.replace("，", "，")
                lines = wrap_text(draw, compact_text, font(max(24, body_font.size - 3), True), text_max_w)
                use_body_font = font(max(24, body_font.size - 3), True)
            else:
                use_body_font = body_font
            row_h = max(int(cfg.get("body_clean_row_h", 58)), len(lines) * line_h + 18)
            if text_y + row_h > card_y + card_h - 62:
                break
            draw.rounded_rectangle(
                (row_x, text_y, row_x + row_w, text_y + row_h),
                radius=12,
                fill=row_fill,
                outline=row_outline,
                width=1,
            )
            if show_numbers:
                draw.rounded_rectangle(
                    (row_x + 13, text_y + 13, row_x + 45, text_y + 45),
                    radius=8,
                    fill=number_fill,
                )
                number = f"{index:02d}"
                num_w = text_len(draw, number, number_font)
                draw.text((row_x + 29 - num_w / 2, text_y + 18), number, font=number_font, fill=(255, 255, 255))
            if show_labels and label:
                draw.text((row_x + (58 if show_numbers else 0), text_y + 15), label, font=label_font, fill=label_fill)
            current_y = text_y + max(11, (row_h - len(lines) * line_h) // 2 - 1)
            for line in lines:
                draw.text((text_x, current_y), line, font=use_body_font, fill=text_fill)
                current_y += line_h
            text_y += row_h + row_gap
    elif body_items:
        show_labels = bool(cfg.get("body_show_labels", True))
        label_bg = tuple(cfg.get("body_label_bg", [180, 59, 205, 238]))
        label_fill = tuple(cfg.get("body_label_color", [255, 255, 255]))
        text_fill = tuple(cfg.get("body_text_color", [0, 0, 0]))
        row_gap = int(cfg.get("body_item_gap", 10))
        for item in body_items:
            if text_y > card_y + card_h - 62:
                break
            label = item.get("label", "")
            text = item.get("text", "")
            use_label = show_labels and bool(label)
            label_w = int(text_len(draw, label, label_font)) + 30 if use_label else 0
            label_h = max(34, int(cfg.get("body_label_h", line_h - 8)))
            label_x = card_x + 30
            label_y = text_y + max(0, (line_h - label_h) // 2) - 2
            first_text_x = label_x + label_w + (12 if use_label else 0)
            first_max_w = card_x + 30 + max_w - first_text_x - 8
            first_lines = wrap_text(draw, text, body_font, max(120, first_max_w))
            if first_lines:
                line = first_lines[0]
                line_w = text_len(draw, line, body_font)
                if use_label:
                    draw.rounded_rectangle(
                        (label_x, label_y, label_x + label_w, label_y + label_h),
                        radius=8,
                        fill=label_bg,
                    )
                    draw.text((label_x + 15, label_y + 4), label, font=label_font, fill=label_fill)
                draw.rounded_rectangle(
                    (first_text_x - 8, text_y - 4, first_text_x + line_w + 10, text_y + line_h - 4),
                    radius=6,
                    fill=highlight,
                )
                draw.text((first_text_x, text_y), line, font=body_font, fill=text_fill)
                text_y += line_h + 5
                rest_text = text[len(line) :]
            else:
                rest_text = ""
            for line in wrap_text(draw, rest_text, body_font, max_w - 10):
                if text_y > card_y + card_h - 62:
                    break
                line_w = text_len(draw, line, body_font)
                draw.rounded_rectangle(
                    (card_x + 30, text_y - 4, card_x + 42 + line_w, text_y + line_h - 4),
                    radius=6,
                    fill=highlight,
                )
                draw.text((card_x + 38, text_y), line, font=body_font, fill=text_fill)
                text_y += line_h + 5
            text_y += row_gap
    else:
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
