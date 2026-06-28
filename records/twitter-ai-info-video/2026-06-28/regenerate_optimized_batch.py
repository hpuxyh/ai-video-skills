#!/usr/bin/env python3
import json
import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/Users/xieyahao/.codex/skills/vertical-ai-info-video-推特版")
EXPORT = Path("/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/导出-2026年06月28日-推特版AI信息差快报-背后公司逻辑版")
RECORDS = Path("/Users/xieyahao/Documents/别人好项目/ai-video-skills/records/twitter-ai-info-video/2026-06-28")
LOGOS = ROOT / "assets/logos"

FONT_REG = "/Library/Fonts/Arial Unicode.ttf"
FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_ARIAL_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_ARIAL_BLACK = "/System/Library/Fonts/Supplemental/Arial Black.ttf"
WIDE = (1600, 1000)
COVER = (1080, 1920)


TOPICS = [
    {
        "id": "01-GPT-56-Sol限量预览",
        "label": "OpenAI",
        "badge": "模型发布",
        "accent": (255, 112, 92),
        "raw_person": "sam-altman-ted.jpg",
        "raw_tweet": "openai-tweet.png",
        "tweet_crop": [110, 0, 710, 740],
        "visuals": [
            ("01-真实视觉.jpg", "sam-altman-ted.jpg", "OpenAI", "Sam Altman", "photo", None),
            ("03-来源截图.jpg", "openai-tweet.png", "官方推文素材", "Sol / Terra / Luna 分层模型", "crop", [126, 210, 692, 532]),
            ("04-信息差解释.jpg", "openai-tweet.png", "模型分层信号", "发布不等于人人可用", "crop", [126, 118, 692, 620]),
            ("05-补充素材.jpg", "sam-altman-ted.jpg", "OpenAI 入口变化", "会拆任务的人先受益", "photo", None),
        ],
        "summary_lines": [
            "OpenAI 限量预览 GPT-5.6 Sol",
            "同时给出 Terra、Luna 两个分层模型",
            "普通用户看到发布，不代表马上能用",
            "真正变化是模型开始按场景分配入口",
            "信息差：先看谁能用，再看模型多强",
        ],
        "source_title": "来源：OpenAI @OpenAI",
        "source_meta": "2026年6月26日 · 约1610.1万 Views · 3.3K回复 / 5.5K转发",
        "source_url": "https://x.com/OpenAI/status/2070555272230384038",
        "cover_focus": (0.50, 0.32),
        "cover_visual_mode": "person",
        "title_lines": ["GPT-5.6 要来了？", "但普通人", "还不能直接用"],
        "bottom": "结论：预览中，普通用户还不能直接用",
    },
    {
        "id": "02-Google-Finance-AI研究工具",
        "label": "Google",
        "badge": "工具入口",
        "accent": (66, 133, 244),
        "raw_person": "sundar-pichai-wikimedia-2023.jpg",
        "raw_tweet": "google-finance-tweet.png",
        "tweet_crop": [110, 0, 710, 760],
        "visuals": [
            ("01-真实视觉.jpg", "sundar-pichai-wikimedia-2023.jpg", "Google", "Sundar Pichai", "photo", None),
            ("03-来源截图.jpg", "google-finance-page.png", "官方页面", "Google Finance 新 App", "screenshot", None),
            ("04-信息差解释.jpg", "google-finance-page.png", "产品入口", "AI 先改变信息收集", "crop", [113, 258, 855, 760]),
            ("05-补充素材.jpg", "sundar-pichai-google-official.webp", "Google AI 入口", "财经信息变成研究助手", "photo", None),
        ],
        "summary_lines": [
            "Google Finance 接入 AI 研究",
            "新 App 先从 Android 开始",
            "AI 会先帮你整理财经信息",
            "它不是替你下注，而是改研究流程",
            "信息差：会提问的人先看懂市场",
        ],
        "source_title": "来源：Google @Google",
        "source_meta": "2026年6月25日 · 约3.2万 Views · 4回复 / 8转发",
        "source_url": "https://x.com/Google/status/2070203169309602115",
        "cover_focus": (0.50, 0.22),
        "cover_visual_mode": "person",
        "title_lines": ["Google Finance", "接入 AI 研究工具", "看盘变成投资助理"],
        "bottom": "结论：AI 先改变信息收集，不是替你下注",
    },
    {
        "id": "03-BytePlus-Seedance-20-4K",
        "label": "BytePlus",
        "badge": "AI视频",
        "accent": (255, 132, 55),
        "raw_person": "zhang-yiming-yicai-2024.jpg",
        "raw_tweet": "byteplus-seedance-tweet.png",
        "tweet_crop": [110, 0, 710, 780],
        "visuals": [
            ("01-真实视觉.jpg", "zhang-yiming-yicai-2024.jpg", "字节系", "张一鸣", "photo", None),
            ("03-来源截图.jpg", "byteplus-page.png", "官方页面", "4K 与视频生成能力", "crop", [0, 40, 1080, 900]),
            ("04-信息差解释.jpg", "byteplus-seedance-tweet.png", "推文视频素材", "清晰度只是表面变化", "crop", [126, 220, 692, 600]),
            ("05-补充素材.jpg", "byteplus-page.png", "创作者入口", "先做样片和分镜", "crop", [0, 40, 1080, 900]),
        ],
        "summary_lines": [
            "BytePlus 发布 Seedance 2.0",
            "AI 视频生成能力直接冲到 4K",
            "清晰度提升只是表面变化",
            "创作者会先用它做分镜和样片",
            "信息差：镜头参考更关键",
        ],
        "source_title": "来源：BytePlus @BytePlusGlobal",
        "source_meta": "2026年6月23日 · 约1144.1万 Views · 262回复 / 316转发",
        "source_url": "https://x.com/BytePlusGlobal/status/2069228410422079665",
        "cover_focus": (0.45, 0.34),
        "cover_visual_mode": "person",
        "title_lines": ["Seedance 2.0", "直接冲到 4K", "AI 视频更像实拍"],
        "bottom": "结论：短视频和广告样片成本继续下降",
    },
    {
        "id": "04-Claude-Tag进入Slack",
        "label": "Anthropic",
        "badge": "企业Agent",
        "accent": (216, 97, 67),
        "raw_person": "dario-amodei-techcrunch-2023.jpg",
        "raw_tweet": "claude-tag-tweet.png",
        "tweet_crop": [110, 0, 710, 900],
        "visuals": [
            ("01-真实视觉.jpg", "dario-amodei-techcrunch-2023.jpg", "Anthropic", "Dario Amodei", "photo", None),
            ("03-来源截图.jpg", "claude-tag-tweet.png", "Slack 场景", "Claude 进入协作线程", "crop", [126, 640, 692, 984]),
            ("04-信息差解释.jpg", "dario-amodei-official-index-card.png", "Anthropic 身份", "公司记忆比模型更难搬", "photo", None),
            ("05-补充素材.jpg", "anthropic-ai-summit-image.png", "企业 AI 风险", "方便背后是锁定成本", "photo", None),
        ],
        "summary_lines": [
            "Claude Tag 开始进入 Slack 线程",
            "AI 不只是在旁边回答问题",
            "它会跟随团队讨论和上下文",
            "真正沉淀的是公司的协作记忆",
            "信息差：公司记忆最难搬",
        ],
        "source_title": "来源：Ashwin Gopinath @ashwingop",
        "source_meta": "推文讨论 Claude Tag 与 Slack 工作流锁定风险",
        "source_url": "https://x.com/ashwingop/status/2069814177624121469",
        "cover_focus": (0.42, 0.30),
        "cover_visual_mode": "person",
        "title_lines": ["Claude 进入 Slack", "不只是聊天助手", "还会记住公司"],
        "bottom": "结论：公司记忆一旦绑定，最难搬走",
    },
    {
        "id": "05-A24回应Google-AI合作",
        "label": "A24 × Google",
        "badge": "创作争议",
        "accent": (220, 38, 92),
        "raw_person": "a24-google-tweet.png",
        "raw_tweet": "a24-google-tweet.png",
        "tweet_crop": [0, 188, 940, 1010],
        "visuals": [
            ("01-真实视觉.jpg", "a24-google-tweet.png", "A24 公司身份", "创作者开始争规则", "crop", [126, 160, 692, 690]),
            ("03-来源截图.jpg", "wired-a24-page.png", "媒体来源", "争议来自 Google AI 合作", "screenshot", None),
            ("04-信息差解释.jpg", "a24-google-tweet.png", "公司标识", "关键是工具规则权", "crop", [126, 235, 692, 800]),
            ("05-补充素材.jpg", "wired-a24-page.png", "创作边界", "版权和流程会被重新谈判", "crop", [118, 250, 920, 980]),
        ],
        "summary_lines": [
            "A24 回应与 Google AI 的合作争议",
            "电影圈争的不是一句用不用 AI",
            "关键是训练、授权和创作边界",
            "创作者开始要求参与工具规则",
            "信息差：真正竞争是工具怎么被建造",
        ],
        "source_title": "来源：DiscussingFilm @DiscussingFilm",
        "source_meta": "争议声明指向 WIRED 2026年6月24日报道",
        "source_url": "https://x.com/DiscussingFilm/status/2070601640642801704",
        "cover_focus": (0.50, 0.42),
        "cover_visual_mode": "brand",
        "title_lines": ["A24 回应 Google AI", "电影圈开始抢规则", "创作者要争边界"],
        "bottom": "结论：真正竞争是工具怎么被建造",
    },
]


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, int(size))


def cover_crop_focus(img, size, focus=(0.5, 0.35), target=(0.5, 0.35)):
    tw, th = size
    img = img.convert("RGB")
    scale = max(tw / img.width, th / img.height)
    resized = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)
    fx, fy = focus[0] * resized.width, focus[1] * resized.height
    left = int(fx - target[0] * tw)
    top = int(fy - target[1] * th)
    left = max(0, min(left, resized.width - tw))
    top = max(0, min(top, resized.height - th))
    return resized.crop((left, top, left + tw, top + th))


def fit_contain(img, size):
    tw, th = size
    scale = min(tw / img.width, th / img.height)
    resized = img.resize((int(img.width * scale + 0.5), int(img.height * scale + 0.5)), Image.Resampling.LANCZOS)
    return resized


def rounded_rect_mask(size, radius):
    mask = Image.new("L", size, 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    return mask


def paste_round(canvas, img, box, radius=24):
    x, y, w, h = box
    fitted = fit_contain(img, (w, h)).convert("RGB")
    bg = Image.new("RGB", (w, h), (250, 252, 255))
    bg.paste(fitted, ((w - fitted.width) // 2, (h - fitted.height) // 2))
    canvas.paste(bg, (x, y), rounded_rect_mask((w, h), radius))
    ImageDraw.Draw(canvas).rounded_rectangle((x, y, x + w, y + h), radius=radius, outline=(232, 236, 242), width=3)


def draw_label(draw, x, y, text, fill):
    f = font(27, True)
    pad_x = 18
    w = int(draw.textlength(text, font=f)) + pad_x * 2
    draw.rounded_rectangle((x, y, x + w, y + 46), radius=12, fill=fill)
    draw.text((x + pad_x, y + 7), text, font=f, fill=(255, 255, 255))
    return x + w


def draw_centered_lines(draw, lines, y, colors, sizes):
    for i, line in enumerate(lines):
        f = font(sizes[i], True)
        w = draw.textlength(line, font=f)
        draw.text(((COVER[0] - w) / 2, y), line, font=f, fill=colors[i])
        y += sizes[i] + 18
    return y


def fitted_font(draw, text, size, max_width, min_size=42):
    size = int(size)
    while size > min_size:
        f = font(size, True)
        if draw.textlength(text, font=f) <= max_width:
            return f, size
        size -= 2
    return font(min_size, True), min_size


def draw_centered_stroke_text(draw, text, y, size, fill, max_width=930, stroke_width=5):
    f, actual_size = fitted_font(draw, text, size, max_width)
    w = draw.textlength(text, font=f)
    x = (COVER[0] - w) / 2

    # Clean cover title: flat fill, white rim, no neon glow or heavy black outline.
    is_light_fill = min(fill[:3]) > 230
    draw.text(
        (x + 3, y + 3),
        text,
        font=f,
        fill=(24, 32, 44, 86),
    )
    if is_light_fill:
        draw.text((x, y), text, font=f, fill=fill)
    else:
        draw.text(
            (x, y),
            text,
            font=f,
            fill=fill,
            stroke_width=6,
            stroke_fill=(255, 255, 255, 245),
        )
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (0, 0)):
        draw.text((x + dx, y + dy), text, font=f, fill=fill)
    return y + actual_size + 18


def bright_cover_color(color):
    r, g, b = color
    if b > r and b > g:
        return (76, 142, 245)
    if r > 200 and b > 80:
        return (224, 58, 118)
    if r > 220 and g > 95:
        return (242, 124, 72)
    return (
        min(255, int(r * 1.02 + 8)),
        min(255, int(g * 1.02 + 8)),
        min(255, int(b * 1.02 + 8)),
    )


def draw_bottom_row(draw, topic, index):
    x0, y0, x1, y1 = 40, 1716, 1040, 1796
    draw.rounded_rectangle((x0, y0, x1, y1), radius=18, fill=(5, 12, 28, 235), outline=(255, 255, 255, 220), width=3)
    draw.rounded_rectangle((x0 + 22, y0 + 18, x0 + 92, y1 - 18), radius=10, fill=(213, 238, 255, 245))
    idx = f"{index:02d}"
    idx_f = font(27, True)
    idx_w = draw.textlength(idx, font=idx_f)
    draw.text((x0 + 57 - idx_w / 2, y0 + 24), idx, font=idx_f, fill=(12, 28, 44))

    text = topic["bottom"].replace("结论：", "", 1)
    prefix = "结论："
    prefix_f = font(36, True)
    text_f, _ = fitted_font(draw, text, 35, x1 - x0 - 250, min_size=28)
    px = x0 + 122
    py = y0 + 22
    draw.text((px, py), prefix, font=prefix_f, fill=(250, 253, 255))
    draw.text((px + draw.textlength(prefix, font=prefix_f), py), text, font=text_f, fill=bright_cover_color(topic["accent"]))


def trim_logo(im, threshold=245, pad=8):
    im = im.convert("RGBA")
    alpha = im.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        rgb = im.convert("RGB")
        mask = Image.new("L", im.size, 0)
        pix = rgb.load()
        mpix = mask.load()
        for y in range(im.height):
            for x in range(im.width):
                r, g, b = pix[x, y]
                if min(r, g, b) < threshold:
                    mpix[x, y] = 255
        bbox = mask.getbbox()
    if not bbox:
        return im
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(im.width, bbox[2] + pad)
    bottom = min(im.height, bbox[3] + pad)
    return im.crop((left, top, right, bottom))


def white_to_alpha(im, threshold=248):
    im = im.convert("RGBA")
    out = Image.new("RGBA", im.size, (255, 255, 255, 0))
    src = im.load()
    dst = out.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = src[x, y]
            if min(r, g, b) < threshold and a:
                dst[x, y] = (r, g, b, a)
    return trim_logo(out)


def make_google_logo(path):
    f = ImageFont.truetype(FONT_ARIAL_BOLD, 84)
    letters = [("G", (66, 133, 244)), ("o", (234, 67, 53)), ("o", (251, 188, 5)), ("g", (66, 133, 244)), ("l", (52, 168, 83)), ("e", (234, 67, 53))]
    widths = [int(ImageDraw.Draw(Image.new("RGB", (1, 1))).textlength(ch, font=f)) for ch, _ in letters]
    canvas = Image.new("RGBA", (sum(widths) + 20, 112), (255, 255, 255, 0))
    d = ImageDraw.Draw(canvas)
    x = 8
    for ch, color in letters:
        d.text((x, 4), ch, font=f, fill=color + (255,))
        x += int(d.textlength(ch, font=f))
    trim_logo(canvas).save(path)


def make_word_logo(path, text, size=72, fill=(20, 20, 20), font_path=FONT_ARIAL_BLACK):
    f = ImageFont.truetype(font_path, size)
    dummy = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    w = int(dummy.textlength(text, font=f)) + 24
    canvas = Image.new("RGBA", (w, size + 36), (255, 255, 255, 0))
    ImageDraw.Draw(canvas).text((12, 8), text, font=f, fill=fill + (255,))
    trim_logo(canvas).save(path)


def make_a24_logo(path):
    raw = Image.open(ROOT / "assets/raw/a24-google-tweet.png").convert("RGB")
    crop = raw.crop((120, 720, 900, 1060))
    crop = ImageEnhance.Contrast(crop).enhance(1.12)
    gray = crop.convert("L")
    out = Image.new("RGBA", crop.size, (0, 0, 0, 0))
    gp = gray.load()
    op = out.load()
    for y in range(crop.height):
        for x in range(crop.width):
            if gp[x, y] > 155:
                op[x, y] = (10, 10, 10, 255)
    trim_logo(out, pad=12).save(path)


def make_byteplus_logo(path):
    raw = Image.open(ROOT / "assets/raw/byteplus-page.png").convert("RGB")
    crop = raw.crop((18, 55, 165, 88))
    crop = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.LANCZOS)
    white_to_alpha(crop).save(path)


def prepare_logo_assets():
    LOGOS.mkdir(parents=True, exist_ok=True)
    src_openai = Path("/Users/xieyahao/Documents/别人好项目/anthropic-alibaba-representative-backgrounds/logos/openai_logo.png")
    if src_openai.exists():
        trim_logo(Image.open(src_openai)).save(LOGOS / "openai-logo.png")
    else:
        make_word_logo(LOGOS / "openai-logo.png", "OpenAI", size=78, font_path=FONT_ARIAL_BOLD)

    make_google_logo(LOGOS / "google-logo.png")
    make_byteplus_logo(LOGOS / "byteplus-logo.png")
    make_word_logo(LOGOS / "anthropic-logo.png", "ANTHROPIC", size=64, font_path=FONT_ARIAL_BLACK)
    make_a24_logo(LOGOS / "a24-logo.png")


def logo_files_for(topic):
    if topic["id"] == "01-GPT-56-Sol限量预览":
        return ["openai-logo.png"]
    if topic["id"] == "02-Google-Finance-AI研究工具":
        return ["google-logo.png"]
    if topic["id"] == "03-BytePlus-Seedance-20-4K":
        return ["byteplus-logo.png"]
    if topic["id"] == "04-Claude-Tag进入Slack":
        return ["anthropic-logo.png"]
    if topic["id"] == "05-A24回应Google-AI合作":
        return ["a24-logo.png", "google-logo.png"]
    return []


def resized_logo(path, max_w, max_h):
    logo = Image.open(LOGOS / path).convert("RGBA")
    scale = min(max_w / logo.width, max_h / logo.height)
    return logo.resize((max(1, int(logo.width * scale)), max(1, int(logo.height * scale))), Image.Resampling.LANCZOS)


def draw_logo_badge(canvas, draw, topic):
    prepare_logo_assets()
    files = logo_files_for(topic)
    if not files:
        return
    if len(files) == 1:
        logo = resized_logo(files[0], 250, 52)
        bw, bh = logo.width + 84, 84
        px2, py0 = 1080 - 118, 1074
        px1, py1 = px2 - bw, py0 + bh
        draw.rounded_rectangle((px1, py0, px2, py1), radius=24, fill=(255, 255, 255, 248))
        canvas.paste(logo, (px1 + (bw - logo.width) // 2, py0 + (bh - logo.height) // 2), logo)
        return

    left_logo = resized_logo(files[0], 130, 48)
    right_logo = resized_logo(files[1], 150, 46)
    x_f = font(32, True)
    x_w = int(draw.textlength("×", font=x_f))
    bw = left_logo.width + x_w + right_logo.width + 92
    bh = 84
    px2, py0 = 1080 - 118, 1074
    px1, py1 = px2 - bw, py0 + bh
    draw.rounded_rectangle((px1, py0, px2, py1), radius=24, fill=(255, 255, 255, 248))
    x = px1 + 34
    canvas.paste(left_logo, (x, py0 + (bh - left_logo.height) // 2), left_logo)
    x += left_logo.width + 22
    draw.text((x, py0 + 24), "×", font=x_f, fill=(22, 28, 38))
    x += x_w + 22
    canvas.paste(right_logo, (x, py0 + (bh - right_logo.height) // 2), right_logo)


def make_panel(topic, filename, raw_name, label, caption, mode, crop_box):
    raw = Image.open(ROOT / "assets/raw" / raw_name).convert("RGB")
    if crop_box:
        raw = raw.crop(tuple(crop_box))
    accent = topic["accent"]
    bg_src = raw if raw.width > 50 else Image.new("RGB", WIDE, (245, 245, 245))
    bg = cover_crop_focus(bg_src.filter(ImageFilter.GaussianBlur(22)), WIDE)
    bg = ImageEnhance.Brightness(bg).enhance(1.10 if mode != "photo" else 0.82)
    bg = ImageEnhance.Contrast(bg).enhance(1.04)
    canvas = bg.convert("RGB")
    overlay = Image.new("RGB", WIDE, (246, 248, 252))
    canvas = Image.blend(canvas, overlay, 0.20 if mode == "photo" else 0.54)
    draw = ImageDraw.Draw(canvas)

    if mode == "screenshot":
        box = (172, 92, 1256, 708)
    elif mode == "photo":
        box = (160, 86, 1280, 716)
    else:
        box = (170, 112, 1260, 654)
    paste_round(canvas, raw, box, radius=30)

    draw_label(draw, 82, 72, label, accent)
    cap_f = font(40, True)
    cap_w = draw.textlength(caption, font=cap_f)
    draw.rounded_rectangle((82, 820, 82 + int(cap_w) + 42, 888), radius=18, fill=(255, 255, 255))
    draw.text((103, 834), caption, font=cap_f, fill=(20, 28, 38))
    out = ROOT / "assets/images" / topic["id"] / filename
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=94)


def make_cover(topic):
    raw = Image.open(ROOT / "assets/raw" / topic["raw_person"]).convert("RGB")
    focus_target = (0.40, 0.31) if topic["cover_visual_mode"] == "person" else (0.50, 0.45)
    if topic["id"] == "05-A24回应Google-AI合作":
        raw = raw.crop((0, 500, 910, 1330))
        focus_target = (0.50, 0.45)
    bg = cover_crop_focus(raw, COVER, focus=topic["cover_focus"], target=focus_target)
    bg = ImageEnhance.Brightness(bg).enhance(1.22)
    bg = ImageEnhance.Contrast(bg).enhance(1.03)
    bg = ImageEnhance.Color(bg).enhance(1.08)
    canvas = bg.convert("RGB")
    draw = ImageDraw.Draw(canvas, "RGBA")

    draw.rectangle((0, 0, 1080, 1920), fill=(255, 255, 255, 10))
    draw.rectangle((0, 940, 1080, 1398), fill=(0, 0, 0, 36))
    draw.rectangle((0, 1540, 1080, 1920), fill=(0, 0, 0, 58))

    hot_f = font(31, True)
    draw.rounded_rectangle((60, 92, 230, 154), radius=16, fill=(255, 92, 92, 255))
    draw.text((60 + (170 - draw.textlength("重磅", font=hot_f)) / 2, 108), "重磅", font=hot_f, fill=(15, 20, 28))

    brand = "AI 信息差快报"
    bf = font(31, True)
    bw = int(draw.textlength(brand, font=bf)) + 64
    bx1, by0, bx2, by1 = 1080 - bw - 70, 48, 1018, 104
    draw.rounded_rectangle((bx1, by0, bx2, by1), radius=17, fill=(8, 18, 34, 232), outline=(116, 209, 255, 135), width=2)
    draw.text((bx1 + 32, by0 + 10), brand, font=bf, fill=(246, 253, 255))

    draw_logo_badge(canvas, draw, topic)

    title_y = 1188
    cover_accent = bright_cover_color(topic["accent"])
    title_y = draw_centered_stroke_text(draw, topic["title_lines"][0], title_y, 94, (252, 254, 255), max_width=970, stroke_width=8)
    title_y = draw_centered_stroke_text(draw, topic["title_lines"][1], title_y, 98, cover_accent, max_width=970, stroke_width=8)
    draw_centered_stroke_text(draw, topic["title_lines"][2], title_y, 98, cover_accent, max_width=970, stroke_width=8)

    draw_bottom_row(draw, topic, TOPICS.index(topic) + 1)

    out = ROOT / "covers" / f"封面-{topic['id']}.jpg"
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, quality=94)
    return out


def render_tweet_card(topic):
    cfg = {
        "raw_screenshot": f"assets/raw/{topic['raw_tweet']}",
        "crop_box": topic["tweet_crop"],
        "output": f"assets/images/{topic['id']}/02-核心推文中文卡.jpg",
        "left_box": [120, 82, 640, 600],
        "right_x": 960,
        "right_y": 104,
        "right_w": 560,
        "label_font_size": 34,
        "summary_font_size": 36,
        "min_summary_font_size": 32,
        "highlight_pad_x": 18,
        "highlight_pad_y": 8,
        "highlight_gap": 12,
        "highlight_full_width": True,
        "max_summary_lines": 6,
        "summary_lines": topic["summary_lines"],
        "link_title": "核心链接",
        "source_title": topic["source_title"],
        "source_meta": topic["source_meta"],
        "source_url": topic["source_url"],
        "source_box": [86, 810, 850, 88],
    }
    cfg_path = ROOT / "configs" / f"{topic['id']}-tweet-proof-card.json"
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    subprocess.run(
        [
            "python3",
            str(SKILL / "scripts/render_tweet_proof_card.py"),
            "--config",
            str(cfg_path.relative_to(ROOT)),
            "--project-dir",
            str(ROOT),
        ],
        check=True,
    )


def update_video_configs():
    grade = {
        "high_luma_brightness": 0.95,
        "high_luma_contrast": 1.0,
        "normal_brightness": 1.02,
        "normal_contrast": 1.02,
        "low_brightness": 1.18,
        "dark_brightness": 1.45,
        "dark_contrast": 1.12,
    }
    for topic in TOPICS:
        cfg_path = ROOT / "configs" / f"{topic['id']}.json"
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        cfg["photo_fit"] = "contain"
        cfg["image_hold_weights"] = [1, 2, 1, 1, 1]
        cfg["image_grade"] = grade
        cfg["motion"] = {"zoom": 0.06, "pan_x": 26, "pan_y": 22}
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")


def render_videos():
    for topic in TOPICS:
        cfg = f"configs/{topic['id']}.json"
        subprocess.run(
            [
                "python3",
                str(SKILL / "scripts/render_vertical_info_video.py"),
                "--config",
                cfg,
                "--project-dir",
                str(ROOT),
            ],
            check=True,
        )


def copy_exports(covers):
    if EXPORT.exists():
        shutil.rmtree(EXPORT)
    EXPORT.mkdir(parents=True, exist_ok=True)
    for topic in TOPICS:
        project_dir = EXPORT / topic["id"]
        project_dir.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "renders" / f"{topic['id']}.mp4", project_dir / "视频.mp4")
        shutil.copyfile(covers[topic["id"]], project_dir / "封面.jpg")
    desc_src = ROOT / "overall-copy-optimized.md"
    if desc_src.exists():
        shutil.copyfile(desc_src, EXPORT / "整体描述.md")


def make_overall_copy():
    old = Path("/Users/xieyahao/Desktop/我自己/小红/视频/推特专用-AI信息差视频/导出-2026年06月28日-推特版AI信息差快报/整体描述.md")
    text = old.read_text(encoding="utf-8")
    header = "# 2026年06月28日 推特版 AI 信息差快报整体描述（背后公司逻辑版）\n\n本批一共 5 个项目。每个项目目录只保留 `视频.mp4` 和 `封面.jpg`；全部标题、文案和标签集中在本文件。\n\n"
    sections = text.split("## 01 ", 1)[1]
    sections = "## 01 " + sections
    sections = sections.replace("项目文件：\n- 视频：`01-视频/01-GPT-56-Sol限量预览/视频-01-GPT-56-Sol限量预览.mp4`\n- 封面：`02-封面/01-GPT-56-Sol限量预览/封面-01-GPT-56-Sol限量预览.jpg`\n\n", "项目文件：`01-GPT-56-Sol限量预览/视频.mp4`、`01-GPT-56-Sol限量预览/封面.jpg`\n\n")
    sections = sections.replace("项目文件：\n- 视频：`01-视频/02-Google-Finance-AI研究工具/视频-02-Google-Finance-AI研究工具.mp4`\n- 封面：`02-封面/02-Google-Finance-AI研究工具/封面-02-Google-Finance-AI研究工具.jpg`\n\n", "项目文件：`02-Google-Finance-AI研究工具/视频.mp4`、`02-Google-Finance-AI研究工具/封面.jpg`\n\n")
    sections = sections.replace("项目文件：\n- 视频：`01-视频/03-BytePlus-Seedance-20-4K/视频-03-BytePlus-Seedance-20-4K.mp4`\n- 封面：`02-封面/03-BytePlus-Seedance-20-4K/封面-03-BytePlus-Seedance-20-4K.jpg`\n\n", "项目文件：`03-BytePlus-Seedance-20-4K/视频.mp4`、`03-BytePlus-Seedance-20-4K/封面.jpg`\n\n")
    sections = sections.replace("项目文件：\n- 视频：`01-视频/04-Claude-Tag进入Slack/视频-04-Claude-Tag进入Slack.mp4`\n- 封面：`02-封面/04-Claude-Tag进入Slack/封面-04-Claude-Tag进入Slack.jpg`\n\n", "项目文件：`04-Claude-Tag进入Slack/视频.mp4`、`04-Claude-Tag进入Slack/封面.jpg`\n\n")
    sections = sections.replace("项目文件：\n- 视频：`01-视频/05-A24回应Google-AI合作/视频-05-A24回应Google-AI合作.mp4`\n- 封面：`02-封面/05-A24回应Google-AI合作/封面-05-A24回应Google-AI合作.jpg`\n\n", "项目文件：`05-A24回应Google-AI合作/视频.mp4`、`05-A24回应Google-AI合作/封面.jpg`\n\n")
    out = ROOT / "overall-copy-optimized.md"
    out.write_text(header + sections, encoding="utf-8")
    RECORDS.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(out, RECORDS / "整体描述-背后公司逻辑版.md")


def make_overviews(covers):
    def sheet(paths, out_path, tile_size=(216, 384)):
        cols = len(paths)
        canvas = Image.new("RGB", (cols * tile_size[0], tile_size[1]), (245, 247, 250))
        for i, path in enumerate(paths):
            im = Image.open(path).convert("RGB")
            im.thumbnail(tile_size, Image.Resampling.LANCZOS)
            x = i * tile_size[0] + (tile_size[0] - im.width) // 2
            y = (tile_size[1] - im.height) // 2
            canvas.paste(im, (x, y))
        out_path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(out_path, quality=92)

    sheet([covers[t["id"]] for t in TOPICS], ROOT / "renders/optimized-cover-overview.jpg")


def main():
    for topic in TOPICS:
        for filename, raw, label, caption, mode, crop in topic["visuals"]:
            make_panel(topic, filename, raw, label, caption, mode, crop)
        render_tweet_card(topic)
    update_video_configs()
    covers = {topic["id"]: make_cover(topic) for topic in TOPICS}
    render_videos()
    make_overall_copy()
    copy_exports(covers)
    make_overviews(covers)
    print(EXPORT)


if __name__ == "__main__":
    main()
