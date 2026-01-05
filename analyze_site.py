from playwright.sync_api import sync_playwright
import json
import time

def analyze_site_deeply():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("Navigating to https://miragen.jp/...")
        page.goto("https://miragen.jp/", wait_until="networkidle", timeout=60000)
        time.sleep(5)
        
        # Get all background images
        print("\n=== Background Images ===")
        bg_images = page.evaluate("""
            () => {
                const elements = document.querySelectorAll('*');
                const bgImages = [];
                elements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    const bgImage = style.backgroundImage;
                    if (bgImage && bgImage !== 'none') {
                        bgImages.push({
                            selector: el.tagName + (el.className ? '.' + el.className.split(' ')[0] : ''),
                            backgroundImage: bgImage,
                            width: el.offsetWidth,
                            height: el.offsetHeight
                        });
                    }
                });
                return bgImages;
            }
        """)
        
        for img in bg_images[:10]:
            print(f"Element: {img['selector']}")
            print(f"  Background: {img['backgroundImage'][:100]}...")
            print(f"  Size: {img['width']}x{img['height']}")
            print()
        
        # Get text content from main sections
        print("\n=== Text Content ===")
        text_content = page.evaluate("""
            () => {
                const sections = [];
                
                // Hero section
                const heroTexts = document.querySelectorAll('[class*="hero"], [class*="title"], h1, h2');
                heroTexts.forEach(el => {
                    if (el.textContent.trim()) {
                        sections.push({
                            type: 'heading',
                            text: el.textContent.trim(),
                            tag: el.tagName
                        });
                    }
                });
                
                return sections.slice(0, 20);
            }
        """)
        
        for content in text_content:
            print(f"{content['tag']}: {content['text'][:100]}")
        
        # Get animation properties
        print("\n=== Animations and Transitions ===")
        animations = page.evaluate("""
            () => {
                const elements = document.querySelectorAll('[class*="appear"], [class*="sd"]');
                const anims = [];
                for (let i = 0; i < Math.min(elements.length, 10); i++) {
                    const el = elements[i];
                    const style = window.getComputedStyle(el);
                    anims.push({
                        transition: style.transition,
                        animation: style.animation,
                        transform: style.transform,
                        opacity: style.opacity
                    });
                }
                return anims;
            }
        """)
        
        for i, anim in enumerate(animations):
            print(f"\nElement {i+1}:")
            print(f"  Transition: {anim['transition'][:80] if anim['transition'] != 'all 0s ease 0s' else 'none'}")
            print(f"  Animation: {anim['animation'][:80] if anim['animation'] != 'none 0s ease 0s 1 normal none running' else 'none'}")
        
        # Get all unique image URLs
        print("\n=== All Image URLs ===")
        image_urls = page.evaluate("""
            () => {
                const images = new Set();
                
                // Get img tags
                document.querySelectorAll('img').forEach(img => {
                    if (img.src) images.add(img.src);
                });
                
                // Get background images
                document.querySelectorAll('*').forEach(el => {
                    const bg = window.getComputedStyle(el).backgroundImage;
                    if (bg && bg !== 'none') {
                        const match = bg.match(/url\(['"]?([^'"]+)['"]?\)/);
                        if (match) images.add(match[1]);
                    }
                });
                
                return Array.from(images);
            }
        """)
        
        print(f"\nFound {len(image_urls)} unique images:")
        for url in image_urls:
            print(f"  {url}")
        
        # Save to file
        with open("detailed_analysis.json", "w", encoding="utf-8") as f:
            json.dump({
                "background_images": bg_images,
                "text_content": text_content,
                "animations": animations,
                "image_urls": image_urls
            }, f, indent=2, ensure_ascii=False)
        
        print("\n\n=== Analysis saved to detailed_analysis.json ===")
        
        browser.close()

if __name__ == "__main__":
    analyze_site_deeply()
