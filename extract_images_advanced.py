from playwright.sync_api import sync_playwright
import requests
import os
import time
import base64

def extract_images():
    os.makedirs("assets/images/extracted", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("Navigating to https://miragen.jp/...")
        page.goto("https://miragen.jp/", wait_until="networkidle", timeout=60000)
        time.sleep(5)
        
        # Take full page screenshot
        print("\nTaking full page screenshot...")
        page.screenshot(path="assets/images/extracted/fullpage.png", full_page=True)
        print("✓ Saved: assets/images/extracted/fullpage.png")
        
        # Get all CSS background image URLs from stylesheets
        print("\n=== Extracting CSS background images ===")
        css_images = page.evaluate("""
            () => {
                const images = new Set();
                
                // Check all stylesheets
                for (const sheet of document.styleSheets) {
                    try {
                        for (const rule of sheet.cssRules || sheet.rules) {
                            if (rule.style && rule.style.backgroundImage) {
                                const bg = rule.style.backgroundImage;
                                const matches = bg.match(/url\\(['"]?([^'"()]+)['"]?\\)/g);
                                if (matches) {
                                    matches.forEach(m => {
                                        const url = m.replace(/url\\(['"]?/, '').replace(/['"]?\\)/, '');
                                        if (url.startsWith('http') || url.startsWith('//')) {
                                            images.add(url.startsWith('//') ? 'https:' + url : url);
                                        }
                                    });
                                }
                            }
                        }
                    } catch (e) {
                        // CORS or other error, skip
                    }
                }
                
                // Also check inline styles
                document.querySelectorAll('[style*="background"]').forEach(el => {
                    const style = el.getAttribute('style');
                    if (style) {
                        const matches = style.match(/url\\(['"]?([^'"()]+)['"]?\\)/g);
                        if (matches) {
                            matches.forEach(m => {
                                const url = m.replace(/url\\(['"]?/, '').replace(/['"]?\\)/, '');
                                if (url.startsWith('http') || url.startsWith('//')) {
                                    images.add(url.startsWith('//') ? 'https:' + url : url);
                                }
                            });
                        }
                    }
                });
                
                return Array.from(images);
            }
        """)
        
        print(f"Found {len(css_images)} CSS background images")
        
        # Download CSS images
        for i, url in enumerate(css_images):
            try:
                print(f"\n[{i+1}/{len(css_images)}] {url[:80]}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    # Get filename from URL
                    filename = url.split('/')[-1].split('?')[0]
                    if not filename or '.' not in filename:
                        filename = f"bg_image_{i}.webp"
                    
                    filepath = f"assets/images/extracted/{filename}"
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Saved: {filepath}")
                else:
                    print(f"  ✗ HTTP {response.status_code}")
            except Exception as e:
                print(f"  ✗ Error: {e}")
            time.sleep(0.3)
        
        # Take screenshots of specific sections
        print("\n=== Taking section screenshots ===")
        sections = [
            {"selector": "header, [class*='header']", "name": "header"},
            {"selector": "section:nth-of-type(1)", "name": "hero"},
            {"selector": "section:nth-of-type(2)", "name": "section_2"},
            {"selector": "section:nth-of-type(3)", "name": "section_3"},
            {"selector": "section:nth-of-type(4)", "name": "section_4"},
        ]
        
        for section in sections:
            try:
                element = page.query_selector(section['selector'])
                if element:
                    element.screenshot(path=f"assets/images/extracted/{section['name']}.png")
                    print(f"✓ Saved: {section['name']}.png")
            except Exception as e:
                print(f"✗ {section['name']}: {e}")
        
        print("\n=== Complete ===")
        browser.close()

if __name__ == "__main__":
    extract_images()
