import os
import re

def process_html(filepath, outpath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract fonts links
    fonts = re.findall(r'<link[^>]+fonts\.googleapis\.com[^>]+>', content)
    fonts += re.findall(r'<link[^>]+fonts\.gstatic\.com[^>]+>', content)
    
    # Extract style block
    style_match = re.search(r'(<style>.*?</style>)', content, re.DOTALL)
    style = style_match.group(1) if style_match else ''

    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', content, re.DOTALL)
    body = body_match.group(1) if body_match else ''

    output = []
    output.extend(fonts)
    output.append(style)
    output.append('<div class="tavci-wrap">')
    output.append(body)
    output.append('</div>')
    
    final_html = "\n".join(output)
    
    # Replace image paths with placeholder
    final_html = final_html.replace('assets/img/', 'WORDPRESS_BASE_URL_PLACEHOLDER/')
    
    with open(outpath, 'w', encoding='utf-8') as f:
        f.write(final_html)
    print(f"Generated {outpath}")

public_dir = 'c:/Users/Nejc/Desktop/Antigravity/Websites/Tavci Kuhna/tavci-kuhna-website/public'
process_html(os.path.join(public_dir, 'index.html'), os.path.join(public_dir, 'index_elementor.txt'))
process_html(os.path.join(public_dir, 'menu.html'), os.path.join(public_dir, 'menu_elementor.txt'))
