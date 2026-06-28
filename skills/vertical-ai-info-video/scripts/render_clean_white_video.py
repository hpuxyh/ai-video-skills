#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat


W, H = 1080, 1920
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"


def font(size):
    return ImageFont.truetype(FONT_BOLD, int(size))


def text_len(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def resolve(project_dir, value):
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_dir / path


def run(cmd):
    subprocess.run(cmd, check=True)


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def add_paper_texture(base):
    draw = ImageDraw.Draw(base, "RGBA")
    for y in range(0, H, 8):
        for x in range(0, W, 8):
            shade = 16 if ((x // 8 + y // 8) % 2 == 0) else 7
            draw.rectangle((x, y, x + 4, y + 4), fill=(0, 0, 0, shade))
    return base.filter(ImageFilter.GaussianBlur(0.15))


def rounded_mask(size, radius):
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255
    )
    return mask


def fit_font(draw, text, start_size, max_width):
    size = start_size
    while size > 32:
        fnt = font(size)
        if text_len(draw, text, fnt) <= max_width:
            return fnt
        size -= 2
    return font(size)


def draw_centered_stroked(draw, text, y, fnt, fill, max_width):
    while text_len(draw, text, fnt) > max_width and fnt.size > 34:
        fnt = font(fnt.size - 2)
    box = draw.textbbox((0, 0), text, font=fnt, stroke_width=2)
    x = (W - (box[2] - box[0])) / 2 - box[0]
    draw.text((x, y), text, font=fnt, fill=fill, stroke_width=2, stroke_fill=fill)
    return y + (box[3] - box[1]) + 14


def pop_state(t, start, duration=0.46):
    p = (t - start) / duration
    if p <= 0:
        return None
    p = min(1.0, p)
    opacity = ease(min(1.0, p / 0.30))
    if p < 0.62:
        scale = 0.76 + 0.34 * ease(p / 0.62)
    else:
        scale = 1.10 - 0.10 * ease((p - 0.62) / 0.38)
    return scale, opacity


def layer_with_opacity(layer, opacity):
    if opacity >= 0.999:
        return layer
    out = layer.copy()
    alpha = out.getchannel("A").point(lambda px: int(px * opacity))
    out.putalpha(alpha)
    return out


def paste_scaled_layer(frame, layer, center, scale, opacity):
    layer = layer_with_opacity(layer, opacity)
    new_w = max(1, int(layer.width * scale + 0.5))
    new_h = max(1, int(layer.height * scale + 0.5))
    scaled = layer.resize((new_w, new_h), Image.Resampling.LANCZOS)
    frame.alpha_composite(
        scaled,
        (int(center[0] - new_w / 2), int(center[1] - new_h / 2)),
    )


def make_title_layer(title_lines, cfg=None):
    cfg = cfg or {}
    probe = ImageDraw.Draw(Image.new("RGBA", (W, H), (0, 0, 0, 0)), "RGBA")
    colors = [(12, 18, 34), (0, 0, 0), (47, 138, 245)]
    max_width = int(cfg.get("title_max_width", 980))
    base_size = int(cfg.get("title_base_size", 72))
    min_size = int(cfg.get("title_min_size", 58))
    line_gap = int(cfg.get("title_line_gap", 30))
    stroke_width = int(cfg.get("title_stroke_width", 2))
    while base_size > min_size:
        fnt = font(base_size)
        if all(text_len(probe, text, fnt) <= max_width for text in title_lines):
            break
        base_size -= 2
    fnt = font(base_size)
    y = int(cfg.get("title_y", 168))
    layers = []
    for i, text in enumerate(title_lines):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, "RGBA")
        box = draw.textbbox((0, 0), text, font=fnt, stroke_width=stroke_width)
        x = (W - (box[2] - box[0])) / 2 - box[0]
        draw.text(
            (x, y),
            text,
            font=fnt,
            fill=colors[min(i, len(colors) - 1)],
            stroke_width=stroke_width,
            stroke_fill=colors[min(i, len(colors) - 1)],
        )
        crop_box = (0, y - 16, W, y + (box[3] - box[1]) + 30)
        layers.append(
            {
                "crop": layer.crop(crop_box),
                "center": (W / 2, (crop_box[1] + crop_box[3]) / 2),
                "start": 0.04 + i * 0.16,
            }
        )
        y += (box[3] - box[1]) + line_gap
    return layers


def fit_contain_motion(img, box_size, progress, idx, preserve_text=False):
    target_w, target_h = box_size
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.02)

    fit_scale = min(target_w / img.width, target_h / img.height) * 0.995
    if preserve_text:
        scale = fit_scale
    else:
        start_scale = fit_scale * 0.94
        scale = start_scale + (fit_scale - start_scale) * ease(progress)
        if idx % 2 == 1:
            scale = fit_scale - (fit_scale - start_scale) * ease(progress)
    resized = img.resize(
        (int(img.width * scale + 0.5), int(img.height * scale + 0.5)),
        Image.Resampling.LANCZOS,
    )
    return resized


def estimate_background_color(img):
    sample_size = 12
    src = img.convert("RGB")
    corners = [
        src.crop((0, 0, sample_size, sample_size)),
        src.crop((src.width - sample_size, 0, src.width, sample_size)),
        src.crop((0, src.height - sample_size, sample_size, src.height)),
        src.crop((src.width - sample_size, src.height - sample_size, src.width, src.height)),
    ]
    merged = Image.new("RGB", (sample_size * 4, sample_size))
    for i, corner in enumerate(corners):
        merged.paste(corner, (i * sample_size, 0))
    stat = ImageStat.Stat(merged)
    return tuple(int(v) for v in stat.mean[:3])


def foreground_bbox(img):
    src = img.convert("RGB")
    bg = Image.new("RGB", src.size, estimate_background_color(src))
    diff = ImageChops.difference(src, bg).convert("L")
    mask = diff.point(lambda px: 255 if px > 38 else 0)
    box = mask.getbbox()
    if not box:
        return (0, 0, src.width, src.height)
    pad_x = int(src.width * 0.015)
    pad_y = int(src.height * 0.03)
    return (
        max(0, box[0] - pad_x),
        max(0, box[1] - pad_y),
        min(src.width, box[2] + pad_x),
        min(src.height, box[3] + pad_y),
    )


def clamp(value, low, high):
    if low > high:
        return (low + high) / 2
    return max(low, min(high, value))


def fit_preserve_fill(img, box_size, idx):
    target_w, target_h = box_size
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.02)

    boxes = getattr(make_media_layer, "foreground_boxes", [])
    fg = boxes[idx] if idx < len(boxes) else foreground_bbox(img)
    fg_w = max(1, fg[2] - fg[0])
    fg_h = max(1, fg[3] - fg[1])
    safe_margin_x = target_w * 0.025
    safe_margin_y = target_h * 0.025

    contain_scale = min(target_w / img.width, target_h / img.height)
    cover_scale = max(target_w / img.width, target_h / img.height)
    max_safe_scale = min(
        (target_w - safe_margin_x * 2) / fg_w,
        (target_h - safe_margin_y * 2) / fg_h,
    )
    scale = max(contain_scale, min(cover_scale, max_safe_scale))
    resized = img.resize(
        (int(img.width * scale + 0.5), int(img.height * scale + 0.5)),
        Image.Resampling.LANCZOS,
    ).convert("RGBA")

    scaled_fg = tuple(v * scale for v in fg)
    fg_cx = (scaled_fg[0] + scaled_fg[2]) / 2
    fg_cy = (scaled_fg[1] + scaled_fg[3]) / 2
    x = target_w / 2 - fg_cx
    y = target_h / 2 - fg_cy

    if resized.width > target_w:
        x = clamp(x, target_w - resized.width, 0)
    else:
        x = (target_w - resized.width) / 2
    if resized.height > target_h:
        y = clamp(y, target_h - resized.height, 0)
    else:
        y = (target_h - resized.height) / 2

    x = clamp(x, safe_margin_x - scaled_fg[0], target_w - safe_margin_x - scaled_fg[2])
    y = clamp(y, safe_margin_y - scaled_fg[1], target_h - safe_margin_y - scaled_fg[3])
    return resized, int(round(x)), int(round(y))


def fit_cover_motion(img, box_size, progress, idx, zoom_extra=0.04):
    target_w, target_h = box_size
    img = img.convert("RGB")
    img = ImageEnhance.Brightness(img).enhance(1.03)
    img = ImageEnhance.Contrast(img).enhance(1.02)

    fit_scale = max(target_w / img.width, target_h / img.height)
    start_scale = fit_scale * (1.0 + zoom_extra)
    end_scale = fit_scale * (1.0 + zoom_extra + 0.045)
    scale = start_scale + (end_scale - start_scale) * ease(progress)
    if idx % 2 == 1:
        scale = end_scale - (end_scale - start_scale) * ease(progress)
    return img.resize(
        (int(img.width * scale + 0.5), int(img.height * scale + 0.5)),
        Image.Resampling.LANCZOS,
    )


def paste_with_crop(base, overlay, xy, opacity=1.0):
    ox, oy = int(xy[0]), int(xy[1])
    src_x0 = max(0, -ox)
    src_y0 = max(0, -oy)
    dst_x0 = max(0, ox)
    dst_y0 = max(0, oy)
    width = min(base.width - dst_x0, overlay.width - src_x0)
    height = min(base.height - dst_y0, overlay.height - src_y0)
    if width <= 0 or height <= 0:
        return
    piece = overlay.crop((src_x0, src_y0, src_x0 + width, src_y0 + height))
    base.alpha_composite(layer_with_opacity(piece, opacity), (dst_x0, dst_y0))


def compose_media_view(
    img,
    idx,
    progress,
    inner,
    view_size,
    pad,
    fit_mode,
    roles,
    qualities,
    preserve_roles,
    focus_x,
    focus_y,
    zoom_extra,
):
    role = roles[idx] if idx < len(roles) else ""
    quality = qualities[idx] if idx < len(qualities) else ""
    preserve_text = role in preserve_roles or quality in preserve_roles
    current_fit_mode = "contain" if preserve_text else fit_mode
    view = Image.new("RGBA", view_size, (255, 255, 255, 255))
    if preserve_text:
        photo, px, py = fit_preserve_fill(img, inner, idx)
        paste_with_crop(view, photo, (pad + px, pad + py), 1.0)
        return view
    if current_fit_mode == "cover":
        photo = fit_cover_motion(img, inner, progress, idx, zoom_extra=zoom_extra).convert("RGBA")
    else:
        photo = fit_contain_motion(img, inner, progress, idx, preserve_text=preserve_text).convert("RGBA")
    spare_x = inner[0] - photo.width
    spare_y = inner[1] - photo.height
    pan_x = 0 if preserve_text else min(24, max(0, spare_x // 3))
    pan_y = 0 if preserve_text else min(16, max(0, spare_y // 3))
    dx = int((ease(progress) - 0.5) * pan_x * (1 if idx % 2 == 0 else -1))
    dy = int((ease(progress) - 0.5) * pan_y * (-1 if idx % 3 == 0 else 1))
    focus_shift_x = 0 if preserve_text else int(inner[0] * focus_x)
    focus_shift_y = 0 if preserve_text else int(inner[1] * focus_y)
    view.alpha_composite(
        photo,
        (pad + spare_x // 2 + dx + focus_shift_x, pad + spare_y // 2 + dy + focus_shift_y),
    )
    return view


def is_preserved_media_index(idx):
    roles = getattr(make_media_layer, "roles", [])
    qualities = getattr(make_media_layer, "qualities", [])
    preserve_roles = getattr(make_media_layer, "preserve_roles", set())
    role = roles[idx] if idx < len(roles) else ""
    quality = qualities[idx] if idx < len(qualities) else ""
    return role in preserve_roles or quality in preserve_roles


def make_media_layer(images, t, duration, beat_cuts, media_box):
    cuts = [float(x) for x in beat_cuts[: len(images) - 1]]
    if len(cuts) < len(images) - 1:
        cuts = [duration * i / len(images) for i in range(1, len(images))]
    starts = [0.0] + cuts
    ends = cuts + [duration]
    idx = 0
    for cut in cuts:
        if t >= cut:
            idx += 1
    idx = min(idx, len(images) - 1)
    progress = (t - starts[idx]) / max(0.001, ends[idx] - starts[idx])

    x0, y0, x1, y1 = media_box
    pad = int(getattr(make_media_layer, "pad", 14))
    fit_mode = getattr(make_media_layer, "fit_mode", "contain")
    roles = getattr(make_media_layer, "roles", [])
    qualities = getattr(make_media_layer, "qualities", [])
    preserve_roles = getattr(make_media_layer, "preserve_roles", set())
    focus_x = float(getattr(make_media_layer, "focus_x", 0.0))
    focus_y = float(getattr(make_media_layer, "focus_y", 0.0))
    zoom_extra = float(getattr(make_media_layer, "zoom_extra", 0.04))
    transition_duration = float(getattr(make_media_layer, "transition_duration", 0.26))
    transition_mode = getattr(make_media_layer, "transition_mode", "fade")
    inner = (x1 - x0 - pad * 2, y1 - y0 - pad * 2)
    view_size = (x1 - x0, y1 - y0)
    view = compose_media_view(
        images[idx],
        idx,
        progress,
        inner,
        view_size,
        pad,
        fit_mode,
        roles,
        qualities,
        preserve_roles,
        focus_x,
        focus_y,
        zoom_extra,
    )
    elapsed_from_cut = t - starts[idx]
    if idx > 0 and 0 <= elapsed_from_cut < transition_duration:
        p = ease(elapsed_from_cut / transition_duration)
        prev_view = compose_media_view(
            images[idx - 1],
            idx - 1,
            1.0,
            inner,
            view_size,
            pad,
            fit_mode,
            roles,
            qualities,
            preserve_roles,
            focus_x,
            focus_y,
            zoom_extra,
        )
        if transition_mode == "fade":
            if is_preserved_media_index(idx) or is_preserved_media_index(idx - 1):
                transition_view = Image.new("RGBA", view_size, (255, 255, 255, 255))
                if p < 0.5:
                    transition_view.alpha_composite(layer_with_opacity(prev_view, 1.0 - p * 2.0))
                else:
                    transition_view.alpha_composite(layer_with_opacity(view, (p - 0.5) * 2.0))
            else:
                transition_view = prev_view.copy()
                transition_view.alpha_composite(layer_with_opacity(view, p))
            view = transition_view
        else:
            direction = -1 if idx % 2 == 0 else 1
            transition_view = prev_view.copy()
            mask = Image.new("L", view_size, 0)
            mask_draw = ImageDraw.Draw(mask)
            reveal_w = int(view_size[0] * p)
            if direction > 0:
                mask_draw.rectangle((view_size[0] - reveal_w, 0, view_size[0], view_size[1]), fill=255)
                edge_x = view_size[0] - reveal_w
            else:
                mask_draw.rectangle((0, 0, reveal_w, view_size[1]), fill=255)
                edge_x = reveal_w
            transition_view.paste(view, (0, 0), mask)
            edge = Image.new("RGBA", (8, view_size[1]), (255, 255, 255, int(130 * (1.0 - p))))
            paste_with_crop(transition_view, edge, (edge_x - 4, 0), 1.0)
            view = transition_view

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    layer.alpha_composite(view, (x0, y0))
    return layer


def draw_header(draw, cfg):
    tag = cfg.get("header_tag", "快报")
    category = cfg.get("header_category", "百度 · AI入口")
    source = cfg.get("header_source", f"最新 · {cfg.get('date', '2026.06')}")
    badge = cfg.get("badge", "AI 信息差快报")

    tag_font = font(31)
    meta_font = font(29)
    badge_font = font(26)

    draw.rounded_rectangle((72, 74, 242, 132), radius=12, fill=(255, 82, 92))
    draw.text((118, 88), tag, font=tag_font, fill=(28, 20, 24))
    draw.text((274, 90), category, font=meta_font, fill=(30, 34, 42))
    draw.text((742, 90), source, font=meta_font, fill=(88, 92, 104))

    bw = int(text_len(draw, badge, badge_font) + 42)
    bx = W - bw - 62
    by = 38
    draw.rounded_rectangle(
        (bx, by, bx + bw, by + 48),
        radius=9,
        fill=(255, 255, 255, 235),
        outline=(73, 158, 205),
        width=2,
    )
    draw.line((bx + 3, by + 47, bx + bw - 3, by + 47), fill=(73, 158, 205), width=4)
    draw.text((bx + 20, by + 10), badge, font=badge_font, fill=(35, 42, 52))


def draw_media_frame(draw, cfg=None):
    cfg = cfg or {}
    media_box = cfg.get("media_box", [52, 622, 1028, 1184])
    outline_width = int(cfg.get("media_outline_width", 3))
    outline = tuple(cfg.get("media_outline", [78, 167, 222]))
    draw.rounded_rectangle(
        tuple(media_box),
        radius=18,
        fill=(255, 255, 255, 255),
        outline=outline if outline_width > 0 else None,
        width=outline_width,
    )


def draw_rows(draw, rows, cfg=None):
    cfg = cfg or {}
    row_x = 52
    row_w = 976
    y = int(cfg.get("body_y", 1308))
    row_h = 58
    gap = 13
    for i, row in enumerate(rows[:5], 1):
        draw_one_row(draw, row, i, y, row_x, row_w, row_h)
        y += row_h + gap


def draw_one_row(draw, row, i, y, row_x=52, row_w=976, row_h=58):
    label_font = font(33)
    text_base_size = 32

    label = row.get("label", "")
    text = row.get("text", "")
    if getattr(draw_one_row, "show_numbers", False):
        num_font = font(24)
        draw.rounded_rectangle((row_x + 12, y + 8, row_x + 58, y + 50), radius=8, fill=(190, 226, 252))
        draw.text((row_x + 20, y + 15), f"{i:02d}", font=num_font, fill=(35, 55, 72))
        label_x = row_x + 80
    else:
        label_x = row_x + 32
    label_text = f"{label}："
    label_w = int(text_len(draw, label_text, label_font))
    text_x = label_x + label_w + 16
    max_w = row_x + row_w - text_x - 18
    text_font = fit_font(draw, text, text_base_size, max_w)
    text_fill = (202, 72, 92) if i in (1, 5) else (18, 22, 30)
    box = draw.textbbox((0, 0), text, font=text_font)
    text_y = y + (row_h - (box[3] - box[1])) / 2 - box[1]
    highlight_fill = tuple(getattr(draw_one_row, "highlight_fill", (53, 214, 226, 232)))
    highlight_pad_x = 8
    highlight_pad_y = 4
    highlight_right = min(row_x + row_w, text_x + (box[2] - box[0]) + highlight_pad_x + 8)
    draw.rounded_rectangle(
        (
            label_x - highlight_pad_x,
            y + 8,
            highlight_right,
            y + row_h - 8,
        ),
        radius=5,
        fill=highlight_fill,
    )
    draw.text((label_x, y + 11), label_text, font=label_font, fill=(12, 18, 26))
    draw.text((text_x, text_y), text, font=text_font, fill=text_fill)


def make_row_layers(rows, cfg=None):
    cfg = cfg or {}
    row_x = 52
    row_w = 976
    y = int(cfg.get("body_y", 1308))
    row_h = 58
    gap = 13
    start = float(cfg.get("body_row_start", 1.05))
    interval = float(cfg.get("body_row_interval", 0.52))
    layers = []
    for i, row in enumerate(rows[:5], 1):
        layer = Image.new("RGBA", (W, row_h + 4), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer, "RGBA")
        draw_one_row(draw, row, i, 2, row_x, row_w, row_h)
        layers.append({"image": layer, "y": y - 2, "start": start + (i - 1) * interval})
        y += row_h + gap
    return layers


def row_reveal_state(t, start, duration=0.42):
    p = (t - start) / duration
    if p <= 0:
        return None
    p = min(1.0, p)
    return ease(p), int((1.0 - ease(p)) * 18)


def make_base(cfg, rows):
    canvas = Image.new("RGB", (W, H), (250, 250, 246))
    add_paper_texture(canvas)
    canvas = canvas.convert("RGBA")
    draw = ImageDraw.Draw(canvas, "RGBA")
    draw_header(draw, cfg)
    draw_media_frame(draw, cfg)
    if not cfg.get("body_rows_animate", False):
        draw_rows(draw, rows, cfg)
    return canvas


def make_title_lines(cfg):
    title = cfg.get("title", [])
    if isinstance(title, str):
        title = [title]
    line1 = title[0] if title else ""
    line2 = title[1] if len(title) > 1 else cfg.get("strap", "")
    strap = cfg.get("strap", "")
    line3 = cfg.get("title_line3")
    if not line3:
        line3 = strap.replace("！", "").replace("!", "")
        if "，" in line3:
            line3 = line3.split("，")[-1]
        if len(line3) > 11:
            line3 = line3[:11]
    return [line1, line2, line3]


def make_frames(cfg, project_dir, frames_dir, output_name):
    duration = float(cfg.get("duration", 7))
    fps = int(cfg.get("fps", 30))
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old in frames_dir.glob("frame-*.jpg"):
        old.unlink()

    images = [Image.open(resolve(project_dir, p)).convert("RGB") for p in cfg["images"][:5]]
    rows = cfg.get("body_rows", [])[:5]
    draw_one_row.show_numbers = bool(cfg.get("body_show_numbers", False))
    draw_one_row.highlight_fill = tuple(cfg.get("body_highlight_fill", [53, 214, 226, 232]))
    base = make_base(cfg, rows)
    title_layers = make_title_layer(make_title_lines(cfg), cfg)
    row_layers = make_row_layers(rows, cfg) if cfg.get("body_rows_animate", False) else []
    media_frame = cfg.get("media_box", [52, 622, 1028, 1184])
    inset = int(cfg.get("media_content_inset", 3 if int(cfg.get("media_outline_width", 3)) > 0 else 0))
    media_box = (
        int(media_frame[0]) + inset,
        int(media_frame[1]) + inset,
        int(media_frame[2]) - inset,
        int(media_frame[3]) - inset,
    )
    beat_cuts = cfg.get("beat_cuts") or [0.9, 1.99, 3.87, 5.83]
    make_media_layer.fit_mode = cfg.get("media_fit", "contain")
    make_media_layer.pad = int(cfg.get("media_pad", 14))
    make_media_layer.focus_x = float(cfg.get("media_focus_x", 0.0))
    make_media_layer.focus_y = float(cfg.get("media_focus_y", 0.0))
    make_media_layer.zoom_extra = float(cfg.get("media_zoom_extra", 0.04))
    make_media_layer.transition_duration = float(cfg.get("media_transition_duration", 0.26))
    make_media_layer.transition_mode = cfg.get("media_transition_mode", "fade")
    make_media_layer.roles = cfg.get("image_roles", [])
    make_media_layer.qualities = cfg.get("image_quality", [])
    make_media_layer.preserve_roles = set(
        cfg.get(
            "media_preserve_roles",
            [
                "media",
                "source-card",
                "official-screenshot",
                "clean-card",
                "product",
                "tweet",
                "screenshot",
            ],
        )
    )
    make_media_layer.foreground_boxes = [foreground_bbox(img) for img in images]

    total_frames = int(round(duration * fps))
    for n in range(total_frames):
        t = n / fps
        frame = base.copy()
        frame.alpha_composite(make_media_layer(images, t, duration, beat_cuts, media_box))
        for item in title_layers:
            state = pop_state(t, item["start"], 0.46)
            if state:
                scale, opacity = state
                paste_scaled_layer(frame, item["crop"], item["center"], scale, opacity)
        for item in row_layers:
            state = row_reveal_state(t, item["start"], float(cfg.get("body_row_duration", 0.42)))
            if state:
                opacity, offset_y = state
                frame.alpha_composite(layer_with_opacity(item["image"], opacity), (0, item["y"] + offset_y))
        frame.convert("RGB").save(frames_dir / f"frame-{n:04d}.jpg", quality=93)

    return duration, fps


def make_video(frames_dir, silent_output, output, bgm_path, duration, fps, bgm_start, volume):
    run(
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
        ]
    )
    if not bgm_path:
        shutil.copyfile(silent_output, output)
        return
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(silent_output),
            "-i",
            str(bgm_path),
            "-filter_complex",
            f"[1:a]atrim=start={bgm_start}:end={bgm_start + duration},asetpts=PTS-STARTPTS,"
            f"afade=t=in:st=0:d=0.08,afade=t=out:st={max(0, duration - 0.35)}:d=0.35,"
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
            str(output),
        ]
    )


def make_contact_sheet(video, contact_sheet):
    run(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(video),
            "-vf",
            "fps=1,scale=270:-1,tile=4x2",
            "-frames:v",
            "1",
            "-update",
            "1",
            str(contact_sheet),
        ]
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--output", required=True)
    parser.add_argument("--contact-sheet", required=True)
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    cfg = json.loads(resolve(project_dir, args.config).read_text(encoding="utf-8"))
    cfg.setdefault("header_tag", "快报")
    cfg.setdefault("header_category", "百度 · 文心入口")
    cfg.setdefault("header_source", f"最新 · {cfg.get('date', '2026.06')}")

    output = resolve(project_dir, args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frames_dir = output.parent / f"{output.stem}-frames"
    duration, fps = make_frames(cfg, project_dir, frames_dir, output.stem)

    bgm = cfg.get("bgm", {})
    bgm_path = resolve(project_dir, bgm.get("path")) if bgm.get("path") else None
    silent = output.with_name(output.stem + ".silent.mp4")
    make_video(
        frames_dir,
        silent,
        output,
        bgm_path,
        duration,
        fps,
        float(bgm.get("start", 3)),
        float(bgm.get("volume", 0.55)),
    )
    make_contact_sheet(output, resolve(project_dir, args.contact_sheet))
    print(output)


if __name__ == "__main__":
    main()
