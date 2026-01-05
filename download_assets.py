import requests
import os
from urllib.parse import urlparse
import time

# Create directories for assets
os.makedirs("assets/images", exist_ok=True)
os.makedirs("assets/css", exist_ok=True)
os.makedirs("assets/js", exist_ok=True)

# Read metadata
import json
with open("miragen_metadata.json", "r") as f:
    metadata = json.load(f)

# Download CSS files
print("Downloading CSS files...")
for i, css_url in enumerate(metadata["css_links"]):
    try:
        print(f"Downloading {css_url}...")
        response = requests.get(css_url, timeout=30)
        filename = f"assets/css/style_{i}.css"
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Saved {filename}")
        time.sleep(0.5)
    except Exception as e:
        print(f"Error downloading {css_url}: {e}")

# Background image URL from screenshot analysis
background_image_url = "https://storage.googleapis.com/studio-design-asset-files/projects/rROnK0KXqA/s-1920x1079_v-frms_webp_7bf12d5e-edd4-4ea7-a99a-dddb9b2a0ce9_small.webp"

print(f"\nDownloading background image from {background_image_url}...")
try:
    response = requests.get(background_image_url, timeout=30)
    with open("assets/images/hero_bg.webp", "wb") as f:
        f.write(response.content)
    print("Background image saved")
except Exception as e:
    print(f"Error: {e}")

# Logo image
logo_url = "https://storage.googleapis.com/studio-design-asset-files/projects/rROnK0KXqA/s-854x191_v-fs_webp_60db0bfe-70c6-4768-bd39-a9794b47618b_small.webp"
print(f"\nDownloading logo from {logo_url}...")
try:
    response = requests.get(logo_url, timeout=30)
    with open("assets/images/logo.webp", "wb") as f:
        f.write(response.content)
    print("Logo saved")
except Exception as e:
    print(f"Error: {e}")

print("\nAssets download complete!")
