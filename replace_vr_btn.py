import glob
import os
import re

base_dir = '/Users/omerfarukbir/Desktop/Çesan'
html_files = glob.glob(f'{base_dir}/**/*.html', recursive=True)
count = 0

# The pattern captures the second button.
pattern = re.compile(r'<a href="#" class="custom-action-btn">\s*<svg width="32"[\s\S]*?<span[^>]*>Vr Görüntüle</span>\s*</a>', re.MULTILINE)

for filepath in html_files:
    if "contact.html" in filepath: continue
    
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        
        # calculate relative path to img/vr.png
        img_target = os.path.join(base_dir, 'img', 'vr.png')
        rel_img_path = os.path.relpath(img_target, os.path.dirname(filepath))
        
        # New block
        new_btn = f"""<a href="#" class="custom-action-btn">
                    <img src="{rel_img_path}" alt="VR Görüntüle" style="width: 32px; height: 32px; object-fit: contain;">
                    <span>Vr Görüntüle</span>
                </a>"""

        new_content, num_subs = re.subn(pattern, new_btn, content)
        
        if num_subs > 0:
            f.seek(0)
            f.write(new_content)
            f.truncate()
            count += 1
            print(f"Updated: {filepath}")

print(f"Total Updated {count} files.")
