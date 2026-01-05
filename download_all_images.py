from playwright.sync_api import sync_playwright
import requests
import os
import time
from urllib.parse import urlparse, urljoin

def download_all_images():
    os.makedirs("assets/images/original", exist_ok=True)
    
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        print("Navigating to https://miragen.jp/...")
        page.goto("https://miragen.jp/", wait_until="networkidle", timeout=60000)
        time.sleep(5)
        
        # Get all image URLs
        print("\n=== Extracting all image URLs ===")
        image_data = page.evaluate("""
            () => {
                const images = [];
                
                // Get all img tags
                document.querySelectorAll('img').forEach(img => {
                    if (img.src) {
                        images.push({
                            url: img.src,
                            alt: img.alt || '',
                            width: img.naturalWidth,
                            height: img.naturalHeight,
                            type: 'img'
                        });
                    }
                });
                
                // Get all background images from computed styles
                const elements = document.querySelectorAll('*');
                elements.forEach(el => {
                    const style = window.getComputedStyle(el);
                    const bgImage = style.backgroundImage;
                    
                    if (bgImage && bgImage !== 'none' && bgImage.includes('url')) {
                        const matches = bgImage.match(/url\(['"]?([^'"]+)['"]?\)/g);
                        if (matches) {
                            matches.forEach(match => {
                                const url = match.replace(/url\(['"]?/, '').replace(/['"]?\)/, '');
                                if (url.startsWith('http') || url.startsWith('//')) {
                                    images.push({
                                        url: url.startsWith('//') ? 'https:' + url : url,
                                        alt: el.className || el.tagName,
                                        width: el.offsetWidth,
                                        height: el.offsetHeight,
                                        type: 'background'
                                    });
                                }
                            });
                        }
                    }
                });
                
                // Remove duplicates
                const uniqueImages = [];
                const seenUrls = new Set();
                images.forEach(img => {
                    if (!seenUrls.has(img.url)) {
                        seenUrls.add(img.url);
                        uniqueImages.push(img);
                    }
                });
                
                return uniqueImages;
            }
        """)
        
        print(f"\nFound {len(image_data)} unique images")
        
        # Download each image
        downloaded = 0
        for i, img_info in enumerate(image_data):
            url = img_info['url']
            img_type = img_info['type']
            
            try:
                print(f"\n[{i+1}/{len(image_data)}] Downloading from {url[:80]}...")
                print(f"  Type: {img_type}, Size: {img_info['width']}x{img_info['height']}")
                
                # Determine filename from URL
                parsed = urlparse(url)
                path_parts = parsed.path.split('/')
                filename = path_parts[-1] if path_parts[-1] else f"image_{i}"
                
                # Add extension if missing
                if '.' not in filename:
                    filename += '.webp'
                
                # Clean filename
                filename = filename.replace('?', '_').replace('&', '_').replace('=', '_')
                filename = f"{img_type}_{i:03d}_{filename}"
                
                filepath = f"assets/images/original/{filename}"
                
                # Download
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Saved: {filepath} ({len(response.content)} bytes)")
                    downloaded += 1
                else:
                    print(f"  ✗ Failed: HTTP {response.status_code}")
                
                time.sleep(0.3)
                
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print(f"\n\n=== Download Complete ===")
        print(f"Successfully downloaded {downloaded}/{len(image_data)} images")
        print(f"Images saved to: assets/images/original/")
        
        browser.close()

if __name__ == "__main__":
    download_all_images()
