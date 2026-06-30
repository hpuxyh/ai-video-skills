#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_osascript(script):
    result = subprocess.run(
        ["osascript", "-e", script],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def parse_bounds(value):
    parts = [int(float(p.strip())) for p in value.replace("{", "").replace("}", "").split(",") if p.strip()]
    if len(parts) != 4:
        raise ValueError(f"Cannot parse Chrome bounds: {value!r}")
    left, top, right, bottom = parts
    return left, top, max(1, right - left), max(1, bottom - top)


def applescript_string(value):
    return json.dumps(value)


def clamp_region(left, top, width, height, window):
    win_left, win_top, win_width, win_height = window
    right = min(win_left + win_width, left + width)
    bottom = min(win_top + win_height, top + height)
    left = max(win_left, left)
    top = max(win_top, top)
    return left, top, max(1, right - left), max(1, bottom - top)


def get_element_region(selector, index, padding, window):
    escaped_selector = json.dumps(selector)
    scroll_js = f"""
(() => {{
  const nodes = Array.from(document.querySelectorAll({escaped_selector}));
  const el = nodes[{index}] || nodes[0];
  if (!el) return JSON.stringify({{found: false, count: nodes.length}});
  el.scrollIntoView({{block: "center", inline: "nearest"}});
  return JSON.stringify({{found: true, count: nodes.length}});
}})();
""".strip()
    run_osascript(
        f'''
tell application "Google Chrome"
  execute active tab of front window javascript {applescript_string(scroll_js)}
end tell
delay 1
'''
    )

    info_js = f"""
(() => {{
  const nodes = Array.from(document.querySelectorAll({escaped_selector}));
  const el = nodes[{index}] || nodes[0];
  if (!el) return JSON.stringify({{found: false, count: nodes.length}});
  const r = el.getBoundingClientRect();
  return JSON.stringify({{
    found: true,
    count: nodes.length,
    rect: {{left: r.left, top: r.top, width: r.width, height: r.height}},
    viewport: {{innerWidth: window.innerWidth, innerHeight: window.innerHeight}},
    outer: {{outerWidth: window.outerWidth, outerHeight: window.outerHeight}},
    devicePixelRatio: window.devicePixelRatio
  }});
}})();
""".strip()
    info_text = run_osascript(
        f'tell application "Google Chrome" to execute active tab of front window javascript {applescript_string(info_js)}'
    )
    info = json.loads(info_text)
    if not info.get("found"):
        return None, info

    win_left, win_top, win_width, win_height = window
    outer = info["outer"]
    viewport = info["viewport"]
    rect = info["rect"]
    scale_x = win_width / max(float(outer.get("outerWidth") or win_width), 1.0)
    scale_y = win_height / max(float(outer.get("outerHeight") or win_height), 1.0)

    viewport_left = max(0.0, (float(outer["outerWidth"]) - float(viewport["innerWidth"])) / 2.0)
    viewport_top = max(0.0, float(outer["outerHeight"]) - float(viewport["innerHeight"]))

    left = int(win_left + (viewport_left + float(rect["left"])) * scale_x - padding)
    top = int(win_top + (viewport_top + float(rect["top"])) * scale_y - padding)
    width = int(float(rect["width"]) * scale_x + padding * 2)
    height = int(float(rect["height"]) * scale_y + padding * 2)
    return clamp_region(left, top, width, height, window), info


def main():
    parser = argparse.ArgumentParser(description="Capture a real source page from the user's local Google Chrome window.")
    parser.add_argument("--url", required=True, help="X/Twitter, official, product, or news URL to open in local Chrome.")
    parser.add_argument("--output", required=True, help="PNG output path, usually assets/raw/chrome/<topic>-tweet.png.")
    parser.add_argument("--wait", type=float, default=8.0, help="Seconds to wait after opening the URL.")
    parser.add_argument("--scroll-y", type=int, default=0, help="Optional page scroll offset in CSS pixels before capture.")
    parser.add_argument(
        "--bounds",
        default="80,60,1400,980",
        help="Chrome window bounds as left,top,right,bottom in screen points before capture.",
    )
    parser.add_argument(
        "--element-selector",
        help="Optional DOM selector to crop directly, e.g. 'article[data-testid=\"tweet\"]' for the core X/Twitter post.",
    )
    parser.add_argument("--element-index", type=int, default=0, help="DOM element index for --element-selector.")
    parser.add_argument("--element-padding", type=int, default=16, help="Screen-point padding around a cropped DOM element.")
    parser.add_argument(
        "--tweet-only",
        action="store_true",
        help="Shortcut for --element-selector 'article[data-testid=\"tweet\"]' so only the core tweet card is captured.",
    )
    parser.add_argument("--metadata", help="Optional JSON metadata output path. Defaults to <output>.json.")
    args = parser.parse_args()

    output = Path(args.output).expanduser().resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    metadata = Path(args.metadata).expanduser().resolve() if args.metadata else output.with_suffix(output.suffix + ".json")

    bounds_values = [int(float(p.strip())) for p in args.bounds.split(",")]
    if len(bounds_values) != 4:
        raise SystemExit("--bounds must be left,top,right,bottom")
    bounds_list = ", ".join(str(v) for v in bounds_values)

    # Use the visible local Chrome profile so X/Twitter login state, cookies, locale,
    # and extensions match what the user actually sees.
    script = f'''
tell application "Google Chrome"
  activate
  if (count of windows) = 0 then make new window
  set bounds of front window to {{{bounds_list}}}
set URL of active tab of front window to "{args.url}"
end tell
delay {args.wait}
tell application "Google Chrome"
  activate
  if {args.scroll_y} is not 0 then
    execute active tab of front window javascript "window.scrollTo(0, {args.scroll_y});"
    delay 2
  end if
  return bounds of front window
end tell
'''
    bounds_text = run_osascript(script)
    window = parse_bounds(bounds_text)
    left, top, width, height = window
    selector = args.element_selector
    if args.tweet_only and not selector:
        selector = 'article[data-testid="tweet"]'

    element_info = None
    if selector:
        element_region, element_info = get_element_region(selector, args.element_index, args.element_padding, window)
        if element_region:
            left, top, width, height = element_region

    region = f"{left},{top},{width},{height}"
    subprocess.run(["screencapture", "-x", "-R", region, str(output)], check=True)

    metadata.parent.mkdir(parents=True, exist_ok=True)
    metadata.write_text(
        json.dumps(
            {
                "url": args.url,
                "output": str(output),
                "captured_at": datetime.now().isoformat(timespec="seconds"),
                "chrome_bounds": {"left": left, "top": top, "width": width, "height": height},
                "full_chrome_bounds": {
                    "left": window[0],
                    "top": window[1],
                    "width": window[2],
                    "height": window[3],
                },
                "scroll_y": args.scroll_y,
                "element_selector": selector,
                "element_index": args.element_index if selector else None,
                "element_padding": args.element_padding if selector else None,
                "element_info": element_info,
                "capture_method": "local Google Chrome + screencapture",
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(output)


if __name__ == "__main__":
    main()
