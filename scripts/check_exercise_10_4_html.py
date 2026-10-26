"""Offline browser checks for the actual Quarto exports (requires Chromium)."""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('PLAYWRIGHT_BROWSERS_PATH', str(ROOT / '.tools/playwright'))
from playwright.sync_api import sync_playwright


def main():
    screenshots = ROOT / '.tools/qa10_4'
    screenshots.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        for stem, count in [('paper', 3), ('notebook_presentation', 10)]:
            for width in [1400, 900]:
                page = browser.new_page(viewport={'width': width, 'height': 1100})
                page.route('https://**/*', lambda route: route.abort())
                page.goto((ROOT / f'outputs/ch10/exercise_10_4/{stem}.html').as_uri(), wait_until='load')
                result = page.evaluate('''() => ({
                    count: document.images.length,
                    decoded: [...document.images].every(i => i.complete && i.naturalWidth > 0),
                    fits: document.documentElement.scrollWidth <= innerWidth,
                    imagesFit: [...document.images].every(i => i.getBoundingClientRect().right <= innerWidth),
                    tablesFit: [...document.querySelectorAll('table')].every(t => t.getBoundingClientRect().right <= innerWidth)
                })''')
                assert result['count'] == count and all(v for k, v in result.items() if k != 'count'), (stem, width, result)
                if stem == 'paper':
                    fold = page.locator('details.code-fold')
                    fold.locator('summary').click()
                    assert fold.get_attribute('open') is not None
                    assert page.locator('#refs .csl-entry').count() == 4
                    assert 100 <= len(page.locator('.abstract').inner_text().split()) <= 150
                page.screenshot(path=str(screenshots / f'{stem}-{width}-top.png'))
                page.locator('img').last.scroll_into_view_if_needed()
                page.screenshot(path=str(screenshots / f'{stem}-{width}-last-figure.png'))
                page.close()
                print(f'PASS offline {stem}, width {width}: {count} decoded figures, page/images/tables fit')
        browser.close()


if __name__ == '__main__':
    main()
