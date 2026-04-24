import glob
from bs4 import BeautifulSoup
import json

html_files = []
html_files.extend(glob.glob("*.html"))
html_files.extend(glob.glob("*/*.html"))

socials = {
    "LinkedIn": "https://www.linkedin.com/company/%C3%A7esan-makina-sanayi-ve-tic-a%C5%9F/",
    "Instagram": "https://www.instagram.com/cesan_makina?igsh=MTViOWZ1cGpnZWxheA%3D%3D",
    "Youtube": "https://www.youtube.com/@cesanmakina4196"
}

for filepath in html_files:
    if "vr/viewer.html" not in filepath and "vr/" in filepath:
        # Ignore old vr files if they still exist somehow
        continue

    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
        
        changed = False

        # Update Social Links in footer
        social_div = soup.find('div', class_='social-links')
        if social_div:
            links = social_div.find_all('a')
            for link in links:
                text = link.get_text(strip=True)
                if text in socials:
                    link['href'] = socials[text]
                    # Also suggest opening in new tab
                    link['target'] = '_blank'
                    link['rel'] = 'noopener noreferrer'
                    changed = True

        # Update Schema in index.html to include sameAs
        if filepath == "index.html":
            script_tag = soup.find('script', type='application/ld+json')
            if script_tag and script_tag.string:
                try:
                    data = json.loads(script_tag.string)
                    # Add social links to schema
                    data["sameAs"] = [
                        socials["LinkedIn"],
                        socials["Instagram"],
                        socials["Youtube"]
                    ]
                    # Also let's set address to full address based on map location
                    data["address"] = {
                        "@type": "PostalAddress",
                        "streetAddress": "İkitelli OSB",
                        "addressLocality": "Başakşehir / İstanbul",
                        "addressCountry": "TR"
                    }
                    
                    script_tag.string = json.dumps(data, ensure_ascii=False, indent=2)
                    changed = True
                except Exception as e:
                    print(f"Error parsing schema in index.html: {e}")

        if changed:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"Updated {filepath}")

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("Social links update complete!")
