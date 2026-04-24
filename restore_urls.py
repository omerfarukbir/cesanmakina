import glob
from bs4 import BeautifulSoup
import os

html_files = []
html_files.extend(glob.glob("*.html"))
html_files.extend(glob.glob("*/*.html"))

for filepath in html_files:
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        changed = False

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Skip external links, javascript, or anchors
            if href.startswith('http') or href.startswith('javascript') or href.startswith('tel:') or href.startswith('mailto:') or href == '#':
                continue
                
            # If it doesn't have .html and isn't just a slash
            if not href.endswith('.html') and '.html?' not in href and href != "/":
                if '?' in href:
                    # e.g. vr/viewer?model=Wax
                    parts = href.split('?', 1)
                    if not parts[0].endswith('.html'):
                        new_href = parts[0] + '.html?' + parts[1]
                        a_tag['href'] = new_href
                        changed = True
                else:
                    # e.g. contact or dolum-makinalari/dolum-makinalari
                    if not href.endswith('.html'):
                        new_href = href + '.html'
                        a_tag['href'] = new_href
                        changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Restored .html URLs in {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("URL restoration complete!")
