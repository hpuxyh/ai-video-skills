#!/usr/bin/env python3
"""Select varied local BGM tracks for vertical AI news video batches.

This script is intentionally deterministic by default: the same batch topics
produce the same choices unless --seed changes. It updates each config's `bgm`
field and copies the selected local audio into the project assets folder.
"""

import argparse
import hashlib
import json
import math
import random
import shutil
from collections import Counter
from pathlib import Path


BGM_POOL = {
    "bba进行曲.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/bba进行曲.mp3",
        "project_name": "bgm-bba-march.mp3",
        "default_weight": 3,
        "best_fit": "major company moves, policy, infrastructure, safety, heavy/urgent topics",
    },
    "时尚动感.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/时尚动感.mp3",
        "project_name": "bgm-fashion-motion.mp3",
        "default_weight": 1,
        "best_fit": "product launches, consumer apps, creator tools, stylish tech topics",
    },
    "时尚热情绽放.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/时尚热情绽放.mp3",
        "project_name": "bgm-fashion-bloom.mp3",
        "default_weight": 1,
        "best_fit": "upbeat releases, creator economy, growth and opportunity angles",
    },
    "do it.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/do it.mp3",
        "project_name": "bgm-do-it.mp3",
        "default_weight": 1,
        "best_fit": "action-oriented tools, workflow tips, what-to-do-now topics",
    },
    "drink.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/drink.mp3",
        "project_name": "bgm-drink.mp3",
        "default_weight": 1,
        "best_fit": "lighter consumer stories, lifestyle/service AI, casual app updates",
    },
    "moment.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/moment.mp3",
        "project_name": "bgm-moment.mp3",
        "default_weight": 1,
        "best_fit": "reflective business shifts, slower strategic explainers",
    },
    "say no cry.mp3": {
        "local_path": "/Users/xieyahao/Desktop/我自己/小红/半奏/say no cry.mp3",
        "project_name": "bgm-say-no-cry.mp3",
        "default_weight": 1,
        "best_fit": "controversy, risk, tension, dispute, security and compliance topics",
    },
}


MOOD_RULES = [
    {
        "mood": "controversy_risk",
        "keywords": ["争议", "指控", "蒸馏", "攻击", "安全", "合规", "风控", "风险", "账号", "偷学", "盗", "封禁", "诉讼"],
        "candidates": [("say no cry.mp3", 3), ("bba进行曲.mp3", 2), ("moment.mp3", 1)],
        "reason": "争议、风险、安全、合规类新闻优先使用紧张或厚重音乐",
    },
    {
        "mood": "creator_product",
        "keywords": ["视频", "创作者", "AIGC", "影像", "分镜", "发布", "上线", "升级", "产品", "模型升级"],
        "candidates": [("时尚动感.mp3", 2), ("时尚热情绽放.mp3", 2), ("do it.mp3", 1)],
        "reason": "产品发布、AI 视频、创作者工具优先使用更轻快的科技感音乐",
    },
    {
        "mood": "consumer_lifestyle",
        "keywords": ["打车", "本地生活", "消费", "生活服务", "下单", "App", "豆包", "外卖", "出行", "聊天框"],
        "candidates": [("drink.mp3", 2), ("do it.mp3", 1), ("时尚动感.mp3", 1)],
        "reason": "消费应用和生活服务类新闻优先使用轻松、行动感音乐",
    },
    {
        "mood": "heavy_infrastructure",
        "keywords": ["算力", "GPU", "芯片", "机房", "数据中心", "基础设施", "NVIDIA", "SpaceX", "政策", "白宫", "审查"],
        "candidates": [("bba进行曲.mp3", 3), ("moment.mp3", 1), ("say no cry.mp3", 1)],
        "reason": "算力、芯片、政策、基础设施类新闻优先使用厚重音乐，bba 提高概率",
    },
    {
        "mood": "workflow_action",
        "keywords": ["工具", "工作流", "效率", "办公", "任务", "方法", "机会", "怎么做", "入口"],
        "candidates": [("do it.mp3", 2), ("时尚热情绽放.mp3", 1), ("moment.mp3", 1)],
        "reason": "工具、工作流、行动建议类新闻优先使用行动感音乐",
    },
    {
        "mood": "reflective_business",
        "keywords": ["商业", "战略", "平台", "合并", "入口", "生态", "百度", "文心", "价格", "订阅"],
        "candidates": [("moment.mp3", 2), ("do it.mp3", 1), ("bba进行曲.mp3", 1)],
        "reason": "商业变化和入口整合类新闻优先使用解释感或战略感音乐",
    },
]

DEFAULT_CANDIDATES = [("bba进行曲.mp3", 2), ("moment.mp3", 1), ("do it.mp3", 1)]


def parse_args():
    parser = argparse.ArgumentParser(description="Assign varied BGM to a batch of paper-card video configs.")
    parser.add_argument("--project-dir", required=True, help="Project directory used by render scripts.")
    parser.add_argument("--configs", nargs="+", required=True, help="Config JSON paths, usually configs/*-paper-card.json.")
    parser.add_argument("--seed", help="Optional deterministic seed. Defaults to a hash of the batch topic text.")
    parser.add_argument("--audio-dir", default="assets/audio", help="Project-relative audio output directory.")
    parser.add_argument("--write-plan", help="Optional path for a JSON BGM assignment report.")
    parser.add_argument("--dry-run", action="store_true", help="Print/write plan without changing configs or copying audio.")
    parser.add_argument("--allow-all-same", action="store_true", help="Allow every video in the batch to use the same BGM.")
    return parser.parse_args()


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_config(path, cfg):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
        f.write("\n")


def normalize_title_item(item):
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        return str(item.get("text", ""))
    return str(item)


def topic_text(cfg):
    parts = []
    title = cfg.get("title", [])
    if isinstance(title, list):
        parts.extend(normalize_title_item(item) for item in title)
    else:
        parts.append(str(title))
    for key in ["strap", "action_text", "badge", "date", "output"]:
        if cfg.get(key):
            parts.append(str(cfg[key]))
    header = cfg.get("header") or {}
    if isinstance(header, dict):
        parts.extend(str(v) for v in header.values())
    for row in cfg.get("body_rows", []) + cfg.get("info_rows", []):
        if isinstance(row, dict):
            parts.append(str(row.get("label", "")))
            parts.append(str(row.get("text", "")))
    return " ".join(parts)


def available_pool():
    pool = {}
    for name, meta in BGM_POOL.items():
        if Path(meta["local_path"]).exists():
            pool[name] = meta
    return pool


def classify(text):
    lower_text = text.lower()
    best = None
    best_score = 0
    for rule in MOOD_RULES:
        score = sum(1 for keyword in rule["keywords"] if keyword.lower() in lower_text)
        if score > best_score:
            best = rule
            best_score = score
    if best:
        return best
    return {
        "mood": "default",
        "candidates": DEFAULT_CANDIDATES,
        "reason": "未命中特定主题词，使用通用 AI 新闻候选音乐",
    }


def candidate_list(rule, pool):
    candidates = []
    for name, weight in rule["candidates"]:
        if name in pool:
            candidates.append({"name": name, "weight": int(weight), "reason": rule["reason"]})
    if candidates:
        return candidates
    return [
        {"name": name, "weight": int(meta.get("default_weight", 1)), "reason": "主题候选音乐不可用，回退到可用 BGM 池"}
        for name, meta in pool.items()
    ]


def stable_seed(items, explicit_seed=None):
    if explicit_seed is not None:
        return explicit_seed
    digest = hashlib.sha256("\n".join(items).encode("utf-8")).hexdigest()
    return str(int(digest[:16], 16))


def weighted_choice(candidates, rng):
    total = sum(item["weight"] for item in candidates)
    pick = rng.uniform(0, total)
    upto = 0
    for item in candidates:
        upto += item["weight"]
        if upto >= pick:
            return item
    return candidates[-1]


def choose_alternative(entry, used_name, rng):
    alternatives = [item for item in entry["candidates"] if item["name"] != used_name]
    if not alternatives:
        return None
    alternatives = sorted(alternatives, key=lambda item: item["weight"], reverse=True)
    top_weight = alternatives[0]["weight"]
    top = [item for item in alternatives if item["weight"] == top_weight]
    return rng.choice(top)


def enforce_variety(plan, rng, allow_all_same=False):
    if allow_all_same or len(plan) <= 1:
        return
    counts = Counter(item["track"] for item in plan)
    if len(counts) == 1:
        first_track = plan[0]["track"]
        for item in plan[1:]:
            alt = choose_alternative(item, first_track, rng)
            if alt:
                item["track"] = alt["name"]
                item["reason"] = item["reason"] + "；批量去重：避免 5 条全部同一首"
                break
    max_same = max(2, math.ceil(len(plan) * 0.6))
    counts = Counter(item["track"] for item in plan)
    for track, count in list(counts.items()):
        if count <= max_same:
            continue
        changed = 0
        for item in reversed(plan):
            if item["track"] != track or count - changed <= max_same:
                continue
            alt = choose_alternative(item, track, rng)
            if alt:
                item["track"] = alt["name"]
                item["reason"] = item["reason"] + f"；批量去重：单首最多 {max_same} 条"
                changed += 1


def main():
    args = parse_args()
    project_dir = Path(args.project_dir).resolve()
    config_paths = [Path(path).resolve() for path in args.configs]
    configs = [(path, load_config(path)) for path in sorted(config_paths)]
    texts = [topic_text(cfg) for _, cfg in configs]
    pool = available_pool()
    if not pool:
        raise SystemExit("No configured local BGM files are available.")

    rng = random.Random(stable_seed(texts, args.seed))
    plan = []
    for path, cfg in configs:
        text = topic_text(cfg)
        rule = classify(text)
        candidates = candidate_list(rule, pool)
        chosen = weighted_choice(candidates, rng)
        plan.append(
            {
                "config": str(path),
                "output": cfg.get("output"),
                "mood": rule["mood"],
                "track": chosen["name"],
                "reason": chosen["reason"],
                "candidates": candidates,
            }
        )

    enforce_variety(plan, rng, allow_all_same=args.allow_all_same)

    audio_dir = project_dir / args.audio_dir
    for item in plan:
        meta = pool[item["track"]]
        item["source_path"] = meta["local_path"]
        item["project_path"] = str(Path(args.audio_dir) / meta["project_name"])
        item["best_fit"] = meta["best_fit"]

    if not args.dry_run:
        audio_dir.mkdir(parents=True, exist_ok=True)
        for item, (path, cfg) in zip(plan, configs):
            src = Path(item["source_path"])
            dst = project_dir / item["project_path"]
            shutil.copy2(src, dst)
            cfg["bgm"] = {
                "path": item["project_path"],
                "start": 3,
                "volume": 0.55,
                "fade_in": 0.08,
                "fade_out": 0.35,
                "source_track": item["track"],
                "mood": item["mood"],
            }
            dump_config(path, cfg)

    report = {
        "schema": "vertical-ai-info-video.bgm-plan.v1",
        "project_dir": str(project_dir),
        "dry_run": args.dry_run,
        "tracks": plan,
        "summary": dict(Counter(item["track"] for item in plan)),
    }
    if args.write_plan:
        write_path = Path(args.write_plan)
        if not write_path.is_absolute():
            write_path = project_dir / write_path
        write_path.parent.mkdir(parents=True, exist_ok=True)
        with open(write_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            f.write("\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
