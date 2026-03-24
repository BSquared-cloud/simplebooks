"""
Automated screenshot tool for SimpleBooks.

Takes screenshots of each page so Claude can "see" how the UI renders.
Saves images to the screenshots/ folder.

Usage:
    Make sure the app is running (python run.py), then:
    python screenshots.py

    Optional: pass a specific URL to screenshot just one page:
    python screenshots.py http://localhost:5000/reports/pnl
"""
import sys
import os
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
    Capture screenshots of app pages.

    Args:
        target_url: If provided, only screenshot this single URL.
                    Otherwise, screenshot all pages in PAGES dict.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        if target_url:
            # Screenshot a single URL
            page.goto(target_url)
            page.wait_for_load_state("networkidle")
            filename = "custom_page.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            page.screenshot(path=filepath, full_page=True)
            print(f"Saved: {filepath}")
        else:
            # Screenshot all known pages
            for name, path in PAGES.items():
                url = f"{BASE_URL}{path}"
                page.goto(url)
                page.wait_for_load_state("networkidle")
                filepath = os.path.join(OUTPUT_DIR, f"{name}.png")
                page.screenshot(path=filepath, full_page=True)
                print(f"Saved: {filepath}")

        browser.close()
    print("Done.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        take_screenshots(target_url=sys.argv[1])
    else:
        take_screenshots()
