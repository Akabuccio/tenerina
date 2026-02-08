import re
import base64
import os
import urllib.parse

def bundle_site():
    print("Reading index.html...")
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    print("Reading css/style.css...")
    with open('css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Inline CSS
    print("Inlining CSS...")
    html = html.replace('<link href="./css/style.css" rel="stylesheet">', f'<style>{css}</style>')

    # Find and inline images
    # Matches src="./Images/filename.ext"
    matches = re.findall(r'src="(\./Images/([^"]+))"', html)
    
    for full_match, filename in matches:
        # Decode URL (e.g. %20 -> space)
        real_filename = urllib.parse.unquote(filename)
        file_path = os.path.join('Images', real_filename)
        
        if os.path.exists(file_path):
            print(f"Inlining image: {real_filename}")
            with open(file_path, 'rb') as img_f:
                encoded = base64.b64encode(img_f.read()).decode('utf-8')
                
            # Determine mime type
            ext = os.path.splitext(real_filename)[1].lower()
            mime = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
            
            data_uri = f'data:{mime};base64,{encoded}'
            html = html.replace(full_match, data_uri)
        else:
            print(f"Warning: Image not found: {file_path}")

    output_filename = 'tenerina_standalone.html'
    print(f"Writing {output_filename}...")
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("Done!")

if __name__ == '__main__':
    bundle_site()
