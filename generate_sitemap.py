import glob
from datetime import datetime

# Domain for the sitemap
DOMAIN = "https://www.cesanmakina.com/"

html_files = []
html_files.extend(glob.glob("*.html"))
html_files.extend(glob.glob("*/*.html"))

# Exclude some files that shouldn't be indexed directly without parameters
exclude_files = ["vr/viewer.html"]

current_date = datetime.now().strftime("%Y-%m-%d")

xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

for filepath in html_files:
    # Normalize path (replace Windows backslashes if any, URL encode spaces etc.)
    normalized_path = filepath.replace("\\", "/")
    
    if normalized_path in exclude_files:
        continue
        
    # urlencode path for special chars
    import urllib.parse
    parts = normalized_path.split('/')
    encoded_parts = [urllib.parse.quote(p) for p in parts]
    url_path = '/'.join(encoded_parts)
    
    # Priority and frequency logic
    if normalized_path == "index.html":
        priority = "1.0"
        changefreq = "weekly"
        url_path = "" # root url
    elif "makinalari" in normalized_path or normalized_path in ["contact.html", "etiket-makinalari.html"]:
        priority = "0.8"
        changefreq = "monthly"
    else:
        priority = "0.6"
        changefreq = "monthly"
        
    full_url = DOMAIN + url_path
    
    xml_content += '  <url>\n'
    xml_content += f'    <loc>{full_url}</loc>\n'
    xml_content += f'    <lastmod>{current_date}</lastmod>\n'
    xml_content += f'    <changefreq>{changefreq}</changefreq>\n'
    xml_content += f'    <priority>{priority}</priority>\n'
    xml_content += '  </url>\n'

xml_content += '</urlset>'

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)

robots_txt = f"""User-agent: *
Allow: /

Sitemap: {DOMAIN}sitemap.xml
"""

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(robots_txt)

print("sitemap.xml and robots.txt created successfully!")
