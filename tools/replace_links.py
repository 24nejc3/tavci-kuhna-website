import os

files = [
    'c:/Users/Nejc/Desktop/Antigravity/Websites/Tavci Kuhna/tavci-kuhna-website/public/index_elementor.txt',
    'c:/Users/Nejc/Desktop/Antigravity/Websites/Tavci Kuhna/tavci-kuhna-website/public/menu_elementor.txt'
]

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    content = content.replace('href="index.html"', 'href="WORDPRESS_LINK_TO_HOME"')
    content = content.replace('href="menu.html"', 'href="WORDPRESS_LINK_TO_MENU"')
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print("Links replaced.")
