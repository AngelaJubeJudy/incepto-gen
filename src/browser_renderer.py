from playwright.sync_api import sync_playwright
import time

def render_and_screenshot(html_path: str, output_path: str, wait_time: int = 3):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state('networkidle')
        time.sleep(wait_time)
        page.screenshot(path=output_path, full_page=True)
        browser.close()
