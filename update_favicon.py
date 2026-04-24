import glob
import os
from bs4 import BeautifulSoup

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

        # Remove existing icon links
        for link in head.find_all('link', rel='icon'):
            link.decompose()
            changed = True
        
        # Determine relative path prefix
        # If the file is in a subdirectory (e.g. dolum-makinalari/file.html), prefix is "../"
        # If it's in root (e.g. index.html), prefix is ""
        if '/' in filepath:
            prefix = "../"
        else:
            prefix = ""

        # Create new favicon link
        new_link = soup.new_tag('link', href=f"{prefix}logo-img/İcon2.webp", rel="icon", type="image/png")
        head.append(new_link)
        changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated favicon in {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Favicon update complete!")
