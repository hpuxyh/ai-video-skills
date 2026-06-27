#!/usr/bin/env python3
import argparse
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageStat


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


def rgb(value, fallback):
    if not value:
        return fallback
    return tuple(int(x) for x in value[:3])


def ease(t):
    t = max(0.0, min(1.0, t))
    return t * t * (3 - 2 * t)


def cover_crop(img, size):
    target_w, target_h = size
    img = img.convert("RGB")
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def grade_image(img, idx, total):
    img = img.convert("RGB")
    mean_luma = sum(ImageStat.Stat(img.resize((1, 1))).mean) / 3
    if idx == total - 1 or mean_luma < 45:
        img = ImageEnhance.Brightness(img).enhance(1.70)
        img = ImageEnhance.Contrast(img).enhance(1.22)
        img = ImageEnhance.Color(img).enhance(1.06)
    elif mean_luma < 85:
        img = ImageEnhance.Brightness(img).enhance(1.12)
        img = ImageEnhance.Contrast(img).enhance(1.04)
    elif mean_luma > 210:
        img = ImageEnhance.Brightness(img).enhance(0.72)
        img = ImageEnhance.Contrast(img).enhance(0.96)
    else:
        img = ImageEnhance.Brightness(img).enhance(0.94)
        img = ImageEnhance.Contrast(img).enhance(0.98)
    return img


def fit_cover(img, size, idx, total, zoom=1.0):
    target_w, target_h = size
    img = grade_image(img, idx, total)
    scale = max(target_w / img.width, target_h / img.height) * zoom
    return img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)


def fit_contain(img, size, idx, total, zoom_amount, progress, is_pull=False):
    target_w, target_h = size
    img = grade_image(img, idx, total)
    eased = ease(progress)
    peak = max(0.0, float(zoom_amount))
    contain_scale = min(target_w / img.width, target_h / img.height) * 0.992
    base_scale = contain_scale / (1.0 + peak)
    zoom = 1.0 + peak * (1.0 - eased if is_pull else eased)
    scale = base_scale * zoom
    return img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)


def paste_clipped(dst, src, xy):
    x, y = xy
    src_left = max(0, -x)
    src_top = max(0, -y)
    dst_left = max(0, x)
    dst_top = max(0, y)
    src_right = min(src.width, dst.width - x)
    src_bottom = min(src.height, dst.height - y)
    if src_right <= src_left or src_bottom <= src_top:
        return
    crop = src.crop((src_left, src_top, src_right, src_bottom))
    dst.alpha_composite(crop, (dst_left, dst_top))


def make_static_base(bg_src, cfg):
    bg = cover_crop(bg_src.filter(ImageFilter.GaussianBlur(18)), (W, H))
    bg = ImageEnhance.Brightness(bg).enhance(0.20).convert("RGBA")
    canvas = Image.alpha_composite(bg, Image.new("RGBA", (W, H), (7, 10, 18, 142)))
    d = ImageDraw.Draw(canvas, "RGBA")
    margin = 72
    header = cfg.get("header", {})

    panel = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    pd = ImageDraw.Draw(panel, "RGBA")
    pd.rounded_rectangle((44, 54, W - 44, 472), radius=26, fill=(6, 8, 18, 118), outline=(255, 255, 255, 26), width=1)
    canvas.alpha_composite(panel)

    brand_text = header.get("brand", "AI 信息差快报")
    brand_font = font(23, True)
    brand_w = int(d.textlength(brand_text, font=brand_font))
    brand_x = W - margin - brand_w - 34
    d.rounded_rectangle((brand_x - 16, 18, W - margin, 52), radius=11, fill=(8, 18, 34, 190), outline=(110, 205, 255, 95), width=1)
    d.rectangle((brand_x - 16, 47, W - margin, 52), fill=(80, 190, 255, 130))
    d.text((brand_x, 22), brand_text, font=brand_font, fill=(232, 250, 255))

    tag = header.get("tag", "重磅")
    category = header.get("category", "AI")
    source = header.get("source", "")
    d.rounded_rectangle((margin, 70, margin + 174, 122), radius=12, fill=(255, 93, 93, 242))
    d.text((margin + 24, 80), tag, font=font(29, True), fill=(13, 16, 24))
    d.text((margin + 198, 82), category, font=font(28, True), fill=(223, 235, 255))
    if source:
        d.text((W - margin - 245, 83), source, font=font(25), fill=(156, 174, 209))

    return canvas


def alpha_composite_with_opacity(canvas, layer, opacity):
    if opacity >= 1:
        canvas.alpha_composite(layer)
        return
    alpha = layer.getchannel("A").point(lambda p: int(p * opacity))
    layer = layer.copy()
    layer.putalpha(alpha)
    canvas.alpha_composite(layer)


def draw_centered_heavy_text(canvas, text, y, size, fill, weight_multiplier=0.9, stroke_width=12, oblique=-0.075):
    size = int(size)
    body_grow = max(1, int(round(stroke_width * 0.24 * weight_multiplier)))
    while size > 12:
        fnt = font(size, True)
        probe = ImageDraw.Draw(Image.new("L", (1, 1)))
        bbox = probe.textbbox((0, 0), text, font=fnt)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        pad_x = max(40, body_grow * 8 + 24)
        pad_y = max(30, body_grow * 7 + 18)
        local_w = text_w + pad_x * 2 + int(abs(oblique) * (text_h + pad_y * 2)) + 24
        if local_w <= W - 18:
            break
        size -= 2

    local_h = text_h + pad_y * 2 + 18
    x = pad_x - bbox[0]
    ty = pad_y - bbox[1]

    mask = Image.new("L", (local_w, local_h), 0)
    md = ImageDraw.Draw(mask)
    md.text((x, ty), text, font=fnt, fill=255)
    body_mask = mask.filter(ImageFilter.MaxFilter(body_grow * 2 + 1))
    local = Image.new("RGBA", (local_w, local_h), (0, 0, 0, 0))
    body_layer = Image.new("RGBA", (local_w, local_h), (*fill, 255))
    body_layer.putalpha(body_mask)
    local.alpha_composite(body_layer)

    if oblique:
        shift = max(0, -oblique * local_h)
        skewed_w = int(local_w + abs(oblique) * local_h + 4)
        local = local.transform(
            (skewed_w, local_h),
            Image.Transform.AFFINE,
            (1, -oblique, -shift, 0, 1, 0),
            resample=Image.Resampling.BICUBIC,
        )

    paste_x = int((W - local.width) / 2)
    paste_y = int(y - pad_y)
    canvas.alpha_composite(local, (paste_x, paste_y))


def pop_scale_opacity(t, start, duration=0.48):
    p = (t - start) / duration
    if p <= 0:
        return None
    p = min(1.0, p)
    opacity = ease(min(1.0, p / 0.28))
    if p < 0.62:
        scale = 0.72 + 0.43 * ease(p / 0.62)
    else:
        scale = 1.15 - 0.15 * ease((p - 0.62) / 0.38)
    return scale, opacity


def draw_title_popup(canvas, t, cfg):
    title = cfg.get("title", [])
    weight = float(cfg.get("title_weight_multiplier", 0.9))
    oblique = float(cfg.get("title_oblique", -0.075))
    starts = cfg.get("title_starts", [0.02, 0.18, 0.36])
    for i, line in enumerate(title):
        text = line["text"]
        y = int(line.get("y", 126 + i * 100))
        size = int(line.get("size", 90))
        fill = rgb(line.get("color"), (255, 255, 255))
        stroke_width = int(line.get("stroke_width", 12))
        start = float(line.get("start", starts[min(i, len(starts) - 1)]))
        state = pop_scale_opacity(t, start)
        if state is None:
            continue
        scale, opacity = state
        scaled_size = max(10, int(size * scale + 0.5))
        scaled_y = int(y - (scaled_size - size) * 0.46)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        draw_centered_heavy_text(layer, text, scaled_y, scaled_size, fill, weight, stroke_width, oblique)
        alpha_composite_with_opacity(canvas, layer, opacity)


def draw_info_rows(canvas, t, cfg):
    rows = cfg.get("info_rows", [])
    style = cfg.get("info_style", {})
    margin = int(style.get("margin", 38))
    y0 = int(style.get("y", 1288))
    row_h = int(style.get("row_h", 64))
    start = float(style.get("start", 0.52))
    step = float(style.get("step", 0.58))
    reveal = float(style.get("reveal", 0.22))
    max_width = W - margin * 2
    hot_labels = set(style.get("hot_labels", ["普通人机会", "结论", "变化", "信息差"]))

    for i, row_data in enumerate(rows):
        p = (t - (start + i * step)) / reveal
        if p <= 0:
            continue
        a = ease(p)
        row = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        rd = ImageDraw.Draw(row, "RGBA")
        y = y0 + i * row_h + int((1 - a) * 18)
        num = row_data.get("num", f"{i + 1:02d}")
        label = row_data["label"]
        text = row_data["text"]
        rd.rounded_rectangle((margin, y, margin + max_width, y + 52), radius=12, fill=(9, 14, 28, 148), outline=(255, 255, 255, 28), width=1)
        rd.rounded_rectangle((margin + 10, y + 10, margin + 48, y + 42), radius=8, fill=(166, 203, 238, 235))
        rd.text((margin + 17, y + 10), num, font=font(21, True), fill=(12, 18, 30))
        x = margin + 68
        label_font = font(34, True)
        rd.text((x, y + 8), f"{label}：", font=label_font, fill=(243, 248, 255))
        x += int(rd.textlength(f"{label}：", font=label_font))
        color = rgb(row_data.get("color"), (255, 101, 101) if label in hot_labels else (235, 242, 255))
        text_font_size = 33 if rd.textlength(text, font=font(34, True)) < W - x - margin else 29
        rd.text((x, y + 8), text, font=font(text_font_size, True), fill=color)
        alpha_composite_with_opacity(canvas, row, min(1.0, a))


def photo_layer(img, progress, idx, total, cfg):
    box = tuple(cfg.get("photo_box", [0, 515, W, 1235]))
    motion = cfg.get("motion", {"zoom": 0.13, "pan_x": 54, "pan_y": 46})
    photo_fit = cfg.get("photo_fit", "cover")
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    eased = ease(progress)
    is_pull = idx % 2 == 1
    view_w = box[2] - box[0]
    view_h = box[3] - box[1]
    view_size = (view_w, view_h)
    view = Image.new("RGBA", view_size, (0, 0, 0, 0))

    if photo_fit == "contain":
        bg = cover_crop(grade_image(img, idx, total).filter(ImageFilter.GaussianBlur(18)), view_size)
        bg = ImageEnhance.Brightness(bg).enhance(0.45)
        bg = ImageEnhance.Contrast(bg).enhance(1.08).convert("RGBA")
        overlay = Image.new("RGBA", view_size, (4, 6, 12, 76))
        view.alpha_composite(Image.alpha_composite(bg, overlay))
        photo = fit_contain(
            img,
            view_size,
            idx,
            total,
            float(motion.get("zoom", 0.08)),
            progress,
            is_pull=is_pull,
        ).convert("RGBA")
    else:
        zoom = 1.0 + float(motion.get("zoom", 0.13)) * (1.0 - eased if is_pull else eased)
        photo = fit_cover(img, view_size, idx, total, zoom=zoom).convert("RGBA")

    x_dir = -1 if idx % 2 else 1
    y_dir = -1 if idx % 3 == 0 else 1
    spare_x = max(0, view_w - photo.width)
    spare_y = max(0, view_h - photo.height)
    pan_x = float(motion.get("pan_x", 54))
    pan_y = float(motion.get("pan_y", 46))
    if photo_fit == "contain":
        pan_x = min(pan_x, spare_x * 0.42)
        pan_y = min(pan_y, spare_y * 0.42)
    px = spare_x // 2 + int(pan_x * (eased - 0.5) * x_dir)
    py = spare_y // 2 + int(pan_y * (eased - 0.5) * y_dir)

    paste_clipped(view, photo, (px, py))
    layer.alpha_composite(view, (box[0], box[1]))
    return layer


def frame_timing(t, total_photos, cfg):
    cuts = cfg.get("beat_cuts")
    duration = float(cfg.get("duration", 7))
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
    output = resolve_path(project_dir, args.output or cfg.get("output", "renders/vertical-ai-info-video.mp4"))
    output.parent.mkdir(parents=True, exist_ok=True)
    silent_output = output.with_name(output.stem + ".silent.mp4")

    image_paths = [resolve_path(project_dir, p) for p in cfg["images"]]
    images = [Image.open(path).convert("RGB") for path in image_paths]
    if not images:
        raise ValueError("Config must include at least one image")

    base = make_static_base(images[0], cfg)
    frames_dir = output.parent / f"{output.stem}-frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for old_frame in frames_dir.glob("frame-*.jpg"):
        old_frame.unlink()

    for n in range(total_frames):
        t = n / fps
        idx, progress = frame_timing(t, len(images), cfg)
        canvas = base.copy()
        draw_title_popup(canvas, t, cfg)
        canvas.alpha_composite(photo_layer(images[idx], progress, idx, len(images), cfg))
        draw_info_rows(canvas, t, cfg)
        canvas.convert("RGB").save(frames_dir / f"frame-{n:04d}.jpg", quality=92)

    run_ffmpeg_frames(frames_dir, fps, silent_output)
    mix_bgm(silent_output, output, project_dir, cfg)

    contact_sheet = args.contact_sheet or cfg.get("contact_sheet")
    if contact_sheet:
        make_contact_sheet(output, resolve_path(project_dir, contact_sheet))

    print(output)


if __name__ == "__main__":
    main()
