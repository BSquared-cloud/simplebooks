"""
Automated screenshot tool for SimpleBooks.

Takes timestamped screenshots of each page so Claude can "see" how the UI
renders and compare changes over time. Saves to screenshots/ folder.

Usage:
    Make sure the app is running (python run.py), then:
    python screenshots.py              # screenshot all pages
    python screenshots.py <url>        # screenshot a single URL
    python screenshots.py --clean 5    # keep only the 5 most recent batches
"""
import sys
import os
import glob
from datetime import datetime
from playwright.sync_api import sync_playwright

# Where to save screenshots
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

# Pages to capture — add new routes here as the app grows
PAGES = {
    "dashboard": "/",
    "add_entry": "/entries/add",
    "pnl_report": "/reports/pnl",
    "balance_sheet": "/reports/balance",
}

BASE_URL = "http://localhost:5000"


def take_screenshots(target_url=None):
    """
    Capture timestamped screenshots of app pages.

    Files are named like: dashboard_20260324_153012.png
    This lets us compare before/after across UI changes.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        if target_url:
            page.goto(target_url)
            page.wait_for_load_state("networkidle")
            filepath = os.path.join(OUTPUT_DIR, f"custom_{timestamp}.png")
            page.screenshot(path=filepath, full_page=True)
            print(f"Saved: {filepath}")
        else:
            for name, route in PAGES.items():
                url = f"{BASE_URL}{route}"
                page.goto(url)
                page.wait_for_load_state("networkidle")
                filepath = os.path.join(OUTPUT_DIR, f"{name}_{timestamp}.png")
                page.screenshot(path=filepath, full_page=True)
                print(f"Saved: {filepath}")

        browser.close()
    print(f"Done. Batch timestamp: {timestamp}")
    return timestamp


def clean_old_screenshots(keep=5):
    """
    Remove old screenshot batches, keeping the most recent ones.

    Args:
        keep: Number of most recent batches to keep. Default 5.
    """
    if not os.path.exists(OUTPUT_DIR):
        return

    # Find all unique timestamps from filenames (format: name_YYYYMMDD_HHMMSS.png)
    files = glob.glob(os.path.join(OUTPUT_DIR, "*.png"))
    timestamps = set()
    for f in files:
        basename = os.path.basename(f)
        # Extract the timestamp portion (last two underscore-separated parts before .png)
        parts = basename.replace(".png", "").rsplit("_", 2)
        if len(parts) >= 3:
            ts = f"{parts[-2]}_{parts[-1]}"
            timestamps.add(ts)

    # Sort timestamps and find which ones to delete
    sorted_ts = sorted(timestamps, reverse=True)
    to_delete = sorted_ts[keep:]

    if not to_delete:
        print(f"Nothing to clean — only {len(sorted_ts)} batch(es) exist.")
        return

    deleted = 0
    for f in files:
        basename = os.path.basename(f)
        for ts in to_delete:
            if ts in basename:
                os.remove(f)
                deleted += 1
                break

    print(f"Cleaned {deleted} files from {len(to_delete)} old batch(es). Kept {keep} most recent.")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        keep = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        clean_old_screenshots(keep=keep)
    elif len(sys.argv) > 1:
        take_screenshots(target_url=sys.argv[1])
    else:
        take_screenshots()
