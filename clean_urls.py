import glob
from bs4 import BeautifulSoup

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
            # We only remove .html from internal links, not external links like https://...
            if href.endswith('.html') and not href.startswith('http'):
                new_href = href[:-5]  # remove .html
                a_tag['href'] = new_href
                changed = True
            elif '.html?' in href and not href.startswith('http'):
                # Handle vr/viewer.html?model=...
                new_href = href.replace('.html?', '?')
                a_tag['href'] = new_href
                changed = True

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Cleaned URLs in {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Clean URLs update complete!")
