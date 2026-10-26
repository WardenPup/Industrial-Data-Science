"""Offline browser QA of the Exercise 11.2 export; screenshots remain local."""

import os
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
if (ROOT / ".tools/playwright").exists():
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(ROOT / ".tools/playwright"))


def main():
    output = ROOT / ".tools/11_2_html"
    output.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        for width in [900, 1400]:
            page = browser.new_page(viewport={"width": width, "height": 1000}, offline=True)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            page.goto((ROOT / "outputs/ch11/exercise_11_2/production_imputation.html").as_uri())
            page.wait_for_load_state("load")
            assert page.locator("img").count() == 7
            assert page.locator("img").evaluate_all("images => images.every(i => i.complete && i.naturalWidth > 0)")
            assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
            assert not errors, errors
            page.screenshot(path=str(output / f"{width}.png"), full_page=True)
            page.close()
            print(f"PASS offline HTML {width}px: seven loaded images, no page errors or horizontal overflow")
        browser.close()


if __name__ == "__main__":
    main()
