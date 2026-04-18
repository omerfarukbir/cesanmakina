import glob
import os
import re

html_files = glob.glob('/Users/omerfarukbir/Desktop/Çesan/**/*.html', recursive=True)
count = 0

old_pattern = re.compile(r'<div class="service-grid-card button-card">\s*<a href="#" class="btn-action">Buton 1</a>\s*<a href="#" class="btn-action outline">Buton 2</a>\s*</div>', re.MULTILINE)

new_block = """<div class="service-grid-card button-card custom-btn-card">
                <a href="#" class="custom-action-btn">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    <span>Teknik Broşür İndir</span>
                </a>
                <a href="#" class="custom-action-btn">
                    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#111" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M4 14v4a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-4"></path>
                        <rect x="2" y="6" width="20" height="8" rx="2" ry="2"></rect>
                        <path d="M10 14v-2h4v2"></path>
                        <circle cx="6" cy="10" r="1" fill="#111"></circle>
                        <circle cx="18" cy="10" r="1" fill="#111"></circle>
                    </svg>
                    <span style="font-weight: 700;">Vr Görüntüle</span>
                </a>
            </div>"""

for filepath in html_files:
    with open(filepath, 'r+', encoding='utf-8') as f:
        content = f.read()
        new_content, num_subs = re.subn(old_pattern, new_block, content)
        if num_subs > 0:
            f.seek(0)
            f.write(new_content)
            f.truncate()
            count += num_subs

print(f"Updated {count} files.")
