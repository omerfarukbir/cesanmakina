import os
import glob
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import json
import urllib.parse

# 1. Convert Images to WebP
def convert_images_to_webp(img_dir="img"):
    for root, dirs, files in os.walk(img_dir):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                filepath = Path(root) / file
                webp_path = filepath.with_suffix('.webp')
                if not webp_path.exists():
                    try:
                        with Image.open(filepath) as img:
                            img.save(webp_path, 'WEBP')
                            print(f"Converted: {filepath} -> {webp_path}")
                    except Exception as e:
                        print(f"Error converting {filepath}: {e}")

# 2. Extract VR HTML -> GLB mapping
def get_vr_mapping(vr_dir="vr"):
    mapping = {}
    for html_file in glob.glob(f"{vr_dir}/*.html"):
        if "viewer.html" in html_file:
            continue
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')
                model_viewer = soup.find('model-viewer')
                if model_viewer and model_viewer.has_attr('src'):
                    src = model_viewer['src']
                    # src could be ../vr/Wax Dolum.glb or similar
                    # extract just the filename
                    glb_name = Path(src).name
                    mapping[Path(html_file).name] = glb_name
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
    return mapping

# 3. Update HTML files
def update_html_files(mapping):
    # Find all HTML files in current directory and 1 level deep (dolum-makinalari, vb)
    html_files = []
    html_files.extend(glob.glob("*.html"))
    html_files.extend(glob.glob("*/*.html"))
    
    schema_json = {
        "@context": "https://schema.org",
        "@type": "LocalBusiness",
        "name": "Çesan Makina",
        "image": "https://www.cesanmakina.com/logo-img/Logo-footer.png",
        "url": "https://www.cesanmakina.com/",
        "telephone": "+905438035649",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Istanbul",
            "addressCountry": "TR"
        }
    }
    
    for filepath in html_files:
        if "vr/viewer.html" in filepath or "vr/etiketleme-mak.html" in filepath:
            # We don't want to update the old VR files because we'll delete them anyway
            # but we will process them just in case, except viewer.html
            if "viewer.html" in filepath:
                continue

        print(f"Processing {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f, 'html.parser')

            changed = False
            head = soup.find('head')
            if head:
                # Add SEO Meta Tags
                seo_tags = [
                    {'property': 'og:title', 'content': 'Çesan Makina - Endüstriyel Çözümler'},
                    {'property': 'og:description', 'content': 'Geliştirdiğimiz yenilikçi makinelerle üretim süreçlerinizi daha hızlı, güvenilir ve verimli hale getiriyoruz.'},
                    {'property': 'og:image', 'content': 'https://www.cesanmakina.com/logo-img/Logo-footer.png'},
                    {'property': 'og:url', 'content': 'https://www.cesanmakina.com/'},
                    {'name': 'twitter:card', 'content': 'summary_large_image'}
                ]
                for tag_attrs in seo_tags:
                    # check if exists
                    if 'property' in tag_attrs:
                        exists = soup.find('meta', property=tag_attrs['property'])
                    else:
                        exists = soup.find('meta', attrs={'name': tag_attrs['name']})
                    
                    if not exists:
                        # Extract the tag name (meta) and pass the rest as attrs
                        new_meta = soup.new_tag('meta')
                        for k, v in tag_attrs.items():
                            new_meta[k] = v
                        head.append(new_meta)
                        changed = True

                # Add Schema.org to index.html
                if filepath == "index.html":
                    exists_schema = soup.find('script', type='application/ld+json')
                    if not exists_schema:
                        script_tag = soup.new_tag('script', type='application/ld+json')
                        script_tag.string = json.dumps(schema_json, ensure_ascii=False, indent=2)
                        head.append(script_tag)
                        changed = True

            # Update empty links
            for a_tag in soup.find_all('a', href=True):
                if a_tag['href'] == '#':
                    a_tag['href'] = 'javascript:void(0)'
                    changed = True

                # Update VR links
                # e.g. href="vr/wax-dolum.html" or href="../vr/wax-dolum.html"
                href = a_tag['href']
                if "vr/" in href and ".html" in href and "viewer.html" not in href:
                    # get the filename
                    vr_filename = href.split('/')[-1]
                    if vr_filename in mapping:
                        glb_file = mapping[vr_filename]
                        # Construct new href
                        # if original was "../vr/wax.html", new is "../vr/viewer.html?model=Wax.glb"
                        # urlencode the model name just in case
                        encoded_glb = urllib.parse.quote(glb_file)
                        new_href = href.replace(vr_filename, f"viewer.html?model={encoded_glb}")
                        a_tag['href'] = new_href
                        changed = True

            # Add lazy loading and webp
            for img_tag in soup.find_all('img'):
                # Add lazy loading if not logo
                classes = img_tag.get('class', [])
                if 'logo-img' not in classes and 'footer-logo' not in classes:
                    if not img_tag.has_attr('loading'):
                        img_tag['loading'] = 'lazy'
                        changed = True
                
                # change .jpg / .png to .webp
                if img_tag.has_attr('src'):
                    src = img_tag['src']
                    if 'img/' in src and (src.lower().endswith('.jpg') or src.lower().endswith('.jpeg') or src.lower().endswith('.png')):
                        new_src = src.rsplit('.', 1)[0] + '.webp'
                        img_tag['src'] = new_src
                        changed = True

            # Fix Alt tags in index.html specifically
            if filepath == "index.html":
                # Find the blog grid
                blog_grid = soup.find('div', class_='blog-grid')
                if blog_grid:
                    cards = blog_grid.find_all('a', class_='blog-card')
                    # Expected order based on current index.html:
                    # 1: Dolum Makinaları
                    # 2: Folyo Yapıştırma
                    # 3: Kapak Kapatma
                    # 4: Etiketleme
                    alts = [
                        "Otomatik Likit Dolum Makinesi",
                        "Otomatik Folyo Yapıştırma Makinesi",
                        "Otomatik Folyo Yapıştırma ve Kapak Kapatma Makinesi",
                        "Otomatik Etiketleme Makinesi"
                    ]
                    for i, card in enumerate(cards):
                        img = card.find('img')
                        if img and i < len(alts):
                            if img.get('alt') == "Manue Parfüm Dolum Makinesi" or not img.get('alt'):
                                img['alt'] = alts[i]
                                changed = True

            if changed:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"Updated {filepath}")
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    print("1. Converting images to WebP...")
    convert_images_to_webp()
    
    print("\n2. Extracting VR mappings...")
    mapping = get_vr_mapping()
    print(f"Found {len(mapping)} VR mappings.")
    
    print("\n3. Updating HTML files...")
    update_html_files(mapping)
    print("Done!")
