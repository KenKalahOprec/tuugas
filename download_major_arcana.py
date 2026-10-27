"""
Download 22 Major Arcana Card Images from lsind18/tarot-json
"""
import os
import urllib.request

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "cards")
os.makedirs(output_dir, exist_ok=True)

base_url = "https://raw.githubusercontent.com/metabismuth/tarot-json/master/cards/"

print(f"Downloading 22 Major Arcana images into: {output_dir}")
for i in range(22):
    filename = f"m{i:02d}.jpg"
    target_path = os.path.join(output_dir, filename)
    url = f"{base_url}{filename}"
    if not os.path.exists(target_path) or os.path.getsize(target_path) == 0:
        try:
            print(f"Downloading {filename}...")
            urllib.request.urlretrieve(url, target_path)
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
    else:
        print(f"Already exists: {filename}")

print("Download complete!")

