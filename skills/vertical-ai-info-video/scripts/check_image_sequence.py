#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROLE_PRIORITY = ["hero", "official", "product", "media", "auxiliary", "unknown"]

TOKEN_RULES = {
    "error": [
        "403",
        "404",
        "429",
        "blocked",
        "captcha",
        "cloudflare",
        "error",
        "forbidden",
        "loading",
        "too-many",
        "unavailable",
    ],
    "media": [
        "ap",
        "axios",
        "bbc",
        "bloomberg",
        "cnbc",
        "cnn",
        "forbes",
        "media",
        "pandaily",
        "reuters",
        "source",
        "techcrunch",
        "technode",
        "theverge",
        "verge",
        "wired",
        "yahoo",
    ],
    "hero": [
        "altman",
        "amodei",
        "ceo",
        "dario",
        "elon",
        "founder",
        "headshot",
        "hq",
        "liang",
        "logo",
        "musk",
        "office",
        "portrait",
        "sam",
        "starbase",
    ],
    "official": [
        "announcement",
        "blog",
        "docs",
        "help",
        "official",
        "release",
        "safety",
        "whitehouse",
    ],
    "product": [
        "api",
        "app",
        "chatgpt",
        "claude",
        "codex",
        "console",
        "entry",
        "model",
        "platform",
        "product",
        "selector",
        "ui",
    ],
    "auxiliary": [
        "chip",
        "compute",
        "datacenter",
        "developer",
        "flow",
        "gpu",
        "h100",
        "laptop",
        "local",
        "nvidia",
        "scene",
    ],
}


def resolve_path(project_dir, value):
    path = Path(value).expanduser()
    if path.is_absolute():
        return path
    return project_dir / path


def normalized_tokens(path):
    text = re.sub(r"[^a-z0-9]+", " ", str(path).lower())
    return set(text.split())


def role_from_tokens(path):
    tokens = normalized_tokens(path)
    if any(token in tokens for token in TOKEN_RULES["error"]):
        return "error"
    for role in ROLE_PRIORITY:
        if role == "unknown":
            continue
        if any(token in tokens for token in TOKEN_RULES[role]):
            return role
    return "unknown"


def explicit_role_for(cfg, image_path, index):
    roles = cfg.get("image_roles")
    if isinstance(roles, list) and index < len(roles):
        role = roles[index]
        if isinstance(role, str):
            return role
        if isinstance(role, dict):
            return role.get("role")
    if isinstance(roles, dict):
        return roles.get(image_path) or roles.get(Path(image_path).name)
    return None


def explicit_quality_for(cfg, image_path, index):
    qualities = cfg.get("image_quality")
    if isinstance(qualities, list) and index < len(qualities):
        quality = qualities[index]
        if isinstance(quality, str):
            return quality
        if isinstance(quality, dict):
            return quality.get("quality")
    if isinstance(qualities, dict):
        return qualities.get(image_path) or qualities.get(Path(image_path).name)
    return None


def card_like_signal(path):
    try:
        with Image.open(path).convert("L") as img:
            thumb = img.resize((160, 90))
            pixels = list(thumb.getdata())
    except Exception:
        return False
    if not pixels:
        return False
    mean = sum(pixels) / len(pixels)
    dark_ratio = sum(value < 80 for value in pixels) / len(pixels)
    bright_ratio = sum(value > 180 for value in pixels) / len(pixels)
    return mean < 95 and dark_ratio > 0.58 and bright_ratio < 0.18


def inspect_image(project_dir, image_path):
    path = resolve_path(project_dir, image_path)
    if not path.exists():
        return {"exists": False, "width": None, "height": None, "card_like": False}
    with Image.open(path) as img:
        width, height = img.size
    return {"exists": True, "width": width, "height": height, "card_like": card_like_signal(path)}


def check_sequence(cfg, project_dir):
    images = cfg.get("images") or ([cfg["image"]] if cfg.get("image") else [])
    items = []
    errors = []
    warnings = []

    for index, image_path in enumerate(images):
        explicit_role = explicit_role_for(cfg, image_path, index)
        explicit_quality = explicit_quality_for(cfg, image_path, index)
        role = explicit_role or role_from_tokens(image_path)
        meta = inspect_image(project_dir, image_path)
        item = {
            "index": index + 1,
            "path": image_path,
            "role": role,
            "role_source": "explicit" if explicit_role else "filename",
            "quality": explicit_quality or "unchecked",
            **meta,
        }
        items.append(item)

        if not meta["exists"]:
            errors.append(f"image {index + 1} missing: {image_path}")
        elif not meta["width"] or not meta["height"]:
            errors.append(f"image {index + 1} has invalid dimensions: {image_path}")
        if role == "error":
            errors.append(f"image {index + 1} looks like an error/fallback asset: {image_path}")
        if explicit_quality in {"bad", "blocked", "error", "fallback"}:
            errors.append(f"image {index + 1} is marked as bad quality: {image_path}")
        if meta["card_like"] and role in {"hero", "auxiliary"}:
            warnings.append(
                f"image {index + 1} looks like a generated/source card but is marked {role}; "
                "replace it with a real visual or move it to media/product evidence"
            )

    if len(items) < 3:
        warnings.append("image carousel should usually include at least 3 images")
    if len(items) and len(items) != 5:
        warnings.append("7-second AI info videos should usually use exactly 5 images")

    roles = [item["role"] for item in items]
    if roles:
        if roles[0] not in {"hero", "official", "product"}:
            errors.append(
                "first image should identify the protagonist/company/product, "
                f"but detected {roles[0]}: {items[0]['path']}"
            )
        if "hero" not in roles[:2]:
            warnings.append("put a real person/company/product recognition image in the first two slots")
        if roles[0] in {"media", "auxiliary", "unknown"}:
            warnings.append("media/source/auxiliary images should not lead the carousel")

    for index, role in enumerate(roles[:2], start=1):
        if role == "media":
            warnings.append(f"media screenshot appears too early at slot {index}; move it after hero/official/product")

    media_count = sum(role == "media" for role in roles)
    auxiliary_count = sum(role == "auxiliary" for role in roles)
    unknown_count = sum(role == "unknown" for role in roles)
    if media_count > 2:
        warnings.append("too many media/source screenshots; keep them as evidence, not the main carousel")
    if auxiliary_count > 1:
        warnings.append("too many auxiliary/context images; prefer real protagonist, official, or product visuals")
    if unknown_count:
        warnings.append("some image roles are unknown; add image_roles to the config or rename assets descriptively")

    return {"ok": not errors, "items": items, "errors": errors, "warnings": warnings}


def print_text_report(report):
    for item in report["items"]:
        dims = "missing" if not item["exists"] else f"{item['width']}x{item['height']}"
        card = " card-like" if item["card_like"] else ""
        print(f"{item['index']:02d} {item['role']:<9} {dims:<10} {item['quality']:<10} {item['path']}{card}")
    if report["errors"]:
        print("\nErrors:")
        for error in report["errors"]:
            print(f"- {error}")
    if report["warnings"]:
        print("\nWarnings:")
        for warning in report["warnings"]:
            print(f"- {warning}")
    if not report["errors"] and not report["warnings"]:
        print("\nImage sequence check passed.")


def make_contact_sheet(report, project_dir, output):
    items = report["items"]
    thumb_w, thumb_h = 320, 180
    label_h = 52
    cols = 2
    rows = max(1, (len(items) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb_w, rows * (thumb_h + label_h)), (245, 245, 245))
    draw = ImageDraw.Draw(sheet)
    try:
        label_font = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc", 16)
    except Exception:
        label_font = None

    for i, item in enumerate(items):
        cell_x = (i % cols) * thumb_w
        cell_y = (i // cols) * (thumb_h + label_h)
        path = resolve_path(project_dir, item["path"])
        if path.exists():
            img = Image.open(path).convert("RGB")
            img.thumbnail((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            x = cell_x + (thumb_w - img.width) // 2
            y = cell_y + (thumb_h - img.height) // 2
            sheet.paste(img, (x, y))
        label = f"{item['index']:02d} {item['role']} {Path(item['path']).name}"
        if item["card_like"]:
            label += " [card-like]"
        draw.text((cell_x + 8, cell_y + thumb_h + 6), label[:58], fill=(0, 0, 0), font=label_font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=92)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True)
    parser.add_argument("--project-dir", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on warnings as well as errors")
    parser.add_argument("--contact-sheet", help="write an image contact sheet for visual inspection")
    args = parser.parse_args()

    project_dir = Path(args.project_dir).expanduser().resolve()
    config_path = resolve_path(project_dir, args.config)
    cfg = json.loads(config_path.read_text(encoding="utf-8"))
    report = check_sequence(cfg, project_dir)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_text_report(report)

    if args.contact_sheet:
        make_contact_sheet(report, project_dir, resolve_path(project_dir, args.contact_sheet))

    if report["errors"] or (args.strict and report["warnings"]):
        sys.exit(1)


if __name__ == "__main__":
    main()
