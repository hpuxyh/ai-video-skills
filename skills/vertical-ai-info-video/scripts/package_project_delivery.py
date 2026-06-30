#!/usr/bin/env python3
"""Create a clean project-level delivery folder for AI info-video batches.

The clean delivery structure mirrors the Twitter-version handoff: each topic
folder contains only the final video and cover, while root 整体描述.md carries
publishing copy and source notes for the whole batch.

  batch-project/
    01-topic-name/
      视频.mp4
      封面.jpg
    02-topic-name/
      视频.mp4
      封面.jpg
    整体描述.md
    _记录/

It can consume the earlier category-first layout used by older batches:

  01-视频/<topic>/视频-*.mp4
  02-封面/<topic>/封面-*.jpg
  03-发布文案/<topic>/*.md
  04-总览与记录/*
  05-素材与来源/*
"""

import argparse
import re
import shutil
from pathlib import Path


CORE_NAMES = {
    "video": "视频.mp4",
    "cover": "封面.jpg",
}


def parse_args():
    parser = argparse.ArgumentParser(description="Package video and cover into per-topic folders, with copy in root 整体描述.md.")
    parser.add_argument("--legacy-batch-dir", required=True, help="Existing batch folder with 01-视频/02-封面/03-发布文案 layout.")
    parser.add_argument("--output-dir", required=True, help="Clean project-level output folder to create/update.")
    parser.add_argument("--overwrite", action="store_true", help="Replace existing clean delivery files.")
    return parser.parse_args()


def copy_file(src, dst, overwrite=False):
    if dst.exists() and not overwrite:
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def topic_key(path):
    match = re.match(r"^(\d{2})-", path.name)
    if match:
        return match.group(1)
    return path.name


def display_topic_name(name):
    return re.sub(r"^\d{2}-", "", name)


def first_file(folder, patterns):
    for pattern in patterns:
        matches = sorted(folder.glob(pattern))
        if matches:
            return matches[0]
    return None


def read_optional(path):
    return path.read_text(encoding="utf-8") if path and path.exists() else ""


def merge_copy(topic_name, copy_folder):
    xhs = first_file(copy_folder, ["小红书-*.md", "*小红书*.md"])
    douyin = first_file(copy_folder, ["抖音-*.md", "*抖音*.md"])
    parts = [f"# {topic_name}", ""]
    if xhs:
        parts.extend(["## 小红书", "", read_optional(xhs).strip(), ""])
    if douyin:
        parts.extend(["## 抖音", "", read_optional(douyin).strip(), ""])
    if not xhs and not douyin:
        parts.extend(["## 发布文案", "", "待补充。", ""])
    return "\n".join(parts).rstrip() + "\n"


def package_topics(legacy_dir, output_dir, overwrite=False):
    video_root = legacy_dir / "01-视频"
    cover_root = legacy_dir / "02-封面"
    copy_root = legacy_dir / "03-发布文案"
    if not video_root.exists():
        raise SystemExit(f"Missing legacy video folder: {video_root}")

    video_dirs = sorted([path for path in video_root.iterdir() if path.is_dir()], key=topic_key)
    packaged = []
    for video_dir in video_dirs:
        key = topic_key(video_dir)
        topic_name = video_dir.name
        topic_dir = output_dir / topic_name
        video = first_file(video_dir, ["视频-*.mp4", "*.mp4"])
        cover_candidates = sorted((cover_root).glob(f"{key}-*/封面-*.jpg")) + sorted((cover_root).glob(f"{key}-*/*.jpg"))
        cover = cover_candidates[0] if cover_candidates else None
        copy_candidates = sorted((copy_root).glob(f"{key}-*"))
        copy_folder = copy_candidates[0] if copy_candidates else None

        if not video:
            raise SystemExit(f"Missing video file for {topic_name}")
        if not cover:
            raise SystemExit(f"Missing cover file for {topic_name}")

        copy_file(video, topic_dir / CORE_NAMES["video"], overwrite=overwrite)
        copy_file(cover, topic_dir / CORE_NAMES["cover"], overwrite=overwrite)

        copy_text = merge_copy(topic_name, copy_folder) if copy_folder else f"# {topic_name}\n\n待补充。\n"

        packaged.append({"key": key, "topic": topic_name, "folder": topic_dir, "copy": copy_text})
    return packaged


def package_records(legacy_dir, output_dir, packaged, overwrite=False):
    record_dir = output_dir / "_记录"
    record_dir.mkdir(parents=True, exist_ok=True)
    for source_name in ["03-发布文案", "04-总览与记录", "05-素材与来源"]:
        source = legacy_dir / source_name
        if source.exists():
            dest = record_dir / source_name
            if dest.exists() and overwrite:
                shutil.rmtree(dest)
            if not dest.exists():
                shutil.copytree(source, dest)

    lines = [
        "# 整体描述",
        "",
        "本目录是项目维度交付版：每条视频一个文件夹，每个文件夹只放两个发布核心文件。",
        "",
        "- `视频.mp4`：最终视频",
        "- `封面.jpg`：发布封面",
        "- 发布标题、视频下方内容、标签和来源摘要统一写在本文档中",
        "",
        "## 条目",
        "",
    ]
    for item in packaged:
        rel = item["folder"].name
        display_name = display_topic_name(item["topic"])
        lines.extend(
            [
                f"### {item['key']} {display_name}",
                f"- 文件夹：`{rel}/`",
                f"- 视频：`{rel}/视频.mp4`",
                f"- 封面：`{rel}/封面.jpg`",
                "",
                "#### 发布文案",
                "",
                item["copy"].strip(),
                "",
            ]
        )
    (output_dir / "整体描述.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main():
    args = parse_args()
    legacy_dir = Path(args.legacy_batch_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    packaged = package_topics(legacy_dir, output_dir, overwrite=args.overwrite)
    package_records(legacy_dir, output_dir, packaged, overwrite=args.overwrite)
    print(output_dir)


if __name__ == "__main__":
    main()
