import glob
import os
from bs4 import BeautifulSoup
import urllib.parse

DOMAIN = "https://www.cesanmakina.com/"

html_files = []
html_files.extend(glob.glob("*.html"))
html_files.extend(glob.glob("*/*.html"))

for filepath in html_files:
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        head = soup.find('head')
        if not head:
            continue

        changed = False

        # First remove any existing canonical link
        for link in head.find_all('link', rel='canonical'):
            link.decompose()
            changed = True

        # Calculate new canonical URL
        # e.g., dolum-makinalari/tam-oto-parfüm.html -> dolum-makinalari/tam-oto-parfüm
        normalized_path = filepath.replace("\\", "/")
        if normalized_path == "index.html":
            canonical_url = DOMAIN
        else:
            # remove .html
            if normalized_path.endswith('.html'):
                clean_path = normalized_path[:-5]
            else:
                clean_path = normalized_path
            
            # URL encode parts
            parts = clean_path.split('/')
            encoded_parts = [urllib.parse.quote(p) for p in parts]
            url_path = '/'.join(encoded_parts)
            
            canonical_url = DOMAIN + url_path

        # Create new canonical link
        new_canonical = soup.new_tag('link', href=canonical_url, rel="canonical")
        head.append(new_canonical)
        changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated canonical in {filepath} to {canonical_url}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Canonical tags update complete!")
