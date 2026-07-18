import os
import re

files = [
    'c:/Users/Nejc/Desktop/Antigravity/Websites/Tavci Kuhna/tavci-kuhna-website/public/index_elementor.txt',
    'c:/Users/Nejc/Desktop/Antigravity/Websites/Tavci Kuhna/tavci-kuhna-website/public/menu_elementor.txt'
]

base_url = "https://tavci-kuhna.si/wp-content/uploads/2026/05/"

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 1. Replace base URL
    content = content.replace('WORDPRESS_BASE_URL_PLACEHOLDER/', base_url)
    
    # 2. Remove dead CSS
    content = re.sub(r'background-image:\s*url\([^)]+tavci_g_\d+\.jpg\'\);', '', content)
    content = re.sub(r'background-image:\s*url\([^)]+tavci_g_\d+\.jpg"\);', '', content)
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)

print("Final fix applied.")
