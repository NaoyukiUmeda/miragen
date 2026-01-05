from playwright.sync_api import sync_playwright
import json
import time

def scrape_website():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("Navigating to https://miragen.jp/...")
        page.goto("https://miragen.jp/", wait_until="networkidle", timeout=60000)
        
        # Wait for content to load
        time.sleep(3)
        
        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="miragen_screenshot.png", full_page=True)
        
        # Get HTML
        print("Getting HTML...")
        html = page.content()
        with open("miragen_source.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        # Get all CSS links
        print("Getting CSS files...")
        css_links = page.eval_on_selector_all("link[rel='stylesheet']", 
            "elements => elements.map(e => e.href)")
        
        # Get all image sources
        print("Getting image sources...")
        images = page.eval_on_selector_all("img", 
            "elements => elements.map(e => ({src: e.src, alt: e.alt, width: e.width, height: e.height}))")
        
        # Get computed styles for body
        print("Getting page info...")
        page_info = page.evaluate("""
            () => {
                const body = document.body;
                const style = window.getComputedStyle(body);
                return {
                    backgroundColor: style.backgroundColor,
                    fontFamily: style.fontFamily,
                    width: window.innerWidth,
                    height: document.body.scrollHeight
                };
            }
        """)
        
        # Save metadata
        metadata = {
            "css_links": css_links,
            "images": images,
            "page_info": page_info,
            "url": "https://miragen.jp/"
        }
        
        with open("miragen_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print("Done! Files saved:")
        print("- miragen_screenshot.png")
        print("- miragen_source.html")
        print("- miragen_metadata.json")
        
        browser.close()

if __name__ == "__main__":
    scrape_website()
