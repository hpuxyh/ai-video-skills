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
    left, top, width, height = parse_bounds(bounds_text)
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
                "scroll_y": args.scroll_y,
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
